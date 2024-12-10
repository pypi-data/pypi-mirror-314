from datetime import date
from typing import List

from tenacity import retry, stop_after_attempt, wait_fixed

from filum_utils.clients.common import BaseClient
from filum_utils.config import config
from filum_utils.enums import Organization
from filum_utils.types.engagement_message import CreateEngagementMessage
from filum_utils.types.survey_response import CreateSurveyResponse

_RETRY_PARAMS = {
    "wait": wait_fixed(10),
    "stop": stop_after_attempt(3),
}


class FilumClient(BaseClient):
    def __init__(self):
        super().__init__(
            base_url=config.FILUM_BASE_URL,
            username=config.FILUM_USERNAME,
            password=config.FILUM_PASSWORD,
        )

    def get_automated_action(self, automated_action_id: int):
        return self._request(
            method="GET",
            endpoint=f"/internal/automated-actions/{automated_action_id}"
        )

    def get_campaign(self, campaign_id: str):
        return self._request(
            method="GET",
            endpoint=f"/internal/survey-campaigns/{campaign_id}"
        )

    def get_segment(self, segment_id: str, organization: Organization):
        return self._request(
            method="GET",
            endpoint=f"/internal/segments/{segment_id}",
            params={
                "organization_id": organization["id"],
                "organization_slug": organization["slug"]
            }
        )

    def update_campaign_subscription_status(
        self,
        campaign_id: str,
        subscription_id: str,
        updated_status: str
    ):
        return self._request(
            method="PUT",
            endpoint=f"/internal/survey-campaigns/{campaign_id}/subscription-webhooks",
            data={
                "subscription_id": subscription_id,
                "status": updated_status
            }
        )

    def update_engagement_campaign_subscription_status(
        self,
        organization_id: str,
        campaign_id: str,
        distribution_id: str,
        updated_status: str
    ):
        return self._request(
            method="PUT",
            endpoint=f"/internal/engagement-campaigns/{campaign_id}/distributions/{distribution_id}/status",
            params={
                "organization_id": organization_id
            },
            data={
                "status": updated_status
            }
        )

    def get_user_csv_reader(
        self,
        properties: List[str],
        object_ids: List[str],
        object_type: str,
        organization: Organization,
        limit: int = config.SEGMENT_RECORD_LIMIT,
        offset: int = 0
    ):
        return self._request(
            method="POST",
            endpoint="/internal/users/export",
            data={
                "object_ids": object_ids,
                "object_type": object_type,
                "organization_id": organization["id"],
                "properties": properties,
                "offset": offset,
                "limit": limit
            },
            timeout=120,
        )

    def get_uploaded_file(self, file_name):
        return self._request(
            method="POST",
            endpoint="/internal/download-file",
            data={
                "file_name": file_name,
            }
        )

    @retry(**_RETRY_PARAMS)
    def create_survey_responses(self, campaign_id: str, responses: List[CreateSurveyResponse]):
        return self._request(
            method="POST",
            endpoint=f"/internal/survey-campaigns/{campaign_id}/survey-responses/batch",
            data=responses,
        )

    @retry(**_RETRY_PARAMS)
    def create_engagement_messages(
        self,
        organization_id: str,
        campaign_id: str,
        messages: List[CreateEngagementMessage]
    ):
        return self._request(
            method="POST",
            endpoint=f"/internal/engagement-campaigns/{campaign_id}/messages/batch",
            params={
                "organization_id": organization_id
            },
            data=messages,
        )

    @retry(**_RETRY_PARAMS)
    def get_sent_engagement_message_count(self, organization_id: str, campaign_id: str, day: date):
        return self._request(
            method="GET",
            endpoint=f"/internal/engagement-campaigns/{campaign_id}/sent-message-count",
            params={
                "organization_id": organization_id,
                "day": day.isoformat(),
            }
        )
