from abc import abstractmethod
from typing import Dict, Any, Optional, Callable, List, Union

from filum_utils.clients.notification import PublisherType
from filum_utils.config import config
from filum_utils.enums import BaseStatus, ObjectType
from filum_utils.errors import BaseError, ErrorMessage
from filum_utils.services.file import FileService
from filum_utils.services.subscription import SubscriptionService
from filum_utils.types.action import Action
from filum_utils.types.campaign import Campaign
from filum_utils.types.common import CallableResponse, TriggerFunctionResponse
from filum_utils.types.engagement_campaign import EngagementCampaign
from filum_utils.types.organization import Organization
from filum_utils.types.subscription import Subscription, SubscriptionData

Event = Optional[Dict[str, Any]]
User = Optional[Dict[str, Any]]


class BaseCampaignSubscriptionService(SubscriptionService):
    def __init__(
        self,
        subscription: Subscription,
        action: Action,
        organization: Organization
    ):
        super().__init__(subscription, organization)
        self.action = action

    @property
    def _object_type(self) -> str:
        return ObjectType.ACTION

    @property
    def _object_id(self) -> int:
        return self.action["id"]

    @property
    def _notification_publisher_type(self) -> str:
        return PublisherType.VoC

    @property
    def _user_limit(self) -> int:
        return self.trigger_data.get("user_limit_per_trigger") or 0

    @abstractmethod
    def update_status(self, updated_status: str):
        ...

    @abstractmethod
    def _get_trigger_completed_notification_subtitle(self, channel_name: str, success_count: int) -> str:
        ...

    def handle_real_time_trigger(
        self,
        process_real_time_fn: Callable[
            [Action, Union[Campaign, EngagementCampaign], Organization, Event, SubscriptionData, Any],
            CallableResponse
        ],
        event: [Dict[str, Any]],
        **kwargs,
    ) -> TriggerFunctionResponse:
        result = self._handle_trigger(
            process_real_time_fn,
            event,
            **kwargs
        )

        return {
            "is_finished": True,
            "success_count": result.get("success_count"),
            "error_message": None,
        }

    def handle_segment_manual_trigger(
        self,
        process_segment_manual_fn: Callable[
            [Action, Union[Campaign, EngagementCampaign], Organization, List[User], SubscriptionData, Any],
            CallableResponse
        ],
        properties: List[str],
        last_current_index: int = 0,
        last_success_count: int = 0,
        channel_name: str = None,
        **kwargs,
    ) -> TriggerFunctionResponse:
        self._validate_last_current_index(last_current_index)

        segment_id = self.trigger_data.get("segment_id")
        if not segment_id:
            raise BaseError(
                message=ErrorMessage.MISSING_SEGMENT_ID,
                data={
                    "Campaign ID": self._parent_id,
                }
            )

        users = self.filum_client.get_user_csv_reader(
            properties=properties,
            object_ids=[segment_id],
            object_type="segment",
            organization=self.organization,
            offset=last_current_index,
            limit=config.SEGMENT_RECORD_LIMIT
        )

        return self._handle_manual_trigger(
            process_fn=process_segment_manual_fn,
            users=users,
            object_record_limit=config.SEGMENT_RECORD_LIMIT,
            last_current_index=last_current_index,
            last_success_count=last_success_count,
            channel_name=channel_name,
            **kwargs,
        )

    def handle_file_manual_trigger(
        self,
        process_file_manual_fn: Callable,
        last_current_index: int = 0,
        last_success_count: int = 0,
        channel_name: str = None,
        **kwargs,
    ):
        self._validate_last_current_index(last_current_index)

        file_name = self.trigger_data.get("file_name")
        if not file_name:
            raise BaseError(
                message=ErrorMessage.MISSING_FILE,
                data={
                    "Campaign ID": self._parent_id,
                }
            )

        file_content_bytes = self.filum_client.get_uploaded_file(file_name)
        users = FileService.get_rows(
            file_name,
            file_content_bytes,
            current_index=last_current_index,
            limit=config.FILE_RECORD_LIMIT,
        )

        return self._handle_manual_trigger(
            process_fn=process_file_manual_fn,
            users=users,
            object_record_limit=config.FILE_RECORD_LIMIT,
            last_current_index=last_current_index,
            last_success_count=last_success_count,
            channel_name=channel_name,
            **kwargs,
        )

    def handle_object_manual_trigger(
        self,
        process_object_manual_fn: Callable,
        **kwargs,
    ):
        ...

    def _exceeded_user_limit(self, current_total_users: int) -> bool:
        return current_total_users >= self._user_limit if self._user_limit else False

    def _validate_last_current_index(self, last_current_index: int):
        current_index = self.subscription_data.get("last_current_index") or 0
        if not current_index or current_index == last_current_index:
            return

        raise BaseError(
            message=ErrorMessage.MISMATCH_LAST_CURRENT_INDEX,
            data={
                "Campaign ID": self._parent_id,
                "Current Index": current_index,
                "Last Current Index": last_current_index
            }
        )

    def _handle_manual_trigger(
        self,
        process_fn: Callable,
        users: List[Dict[str, Any]],
        object_record_limit: int,
        last_current_index: int = 0,
        last_success_count: int = 0,
        channel_name: str = None,
        **kwargs
    ):
        result = self._handle_trigger(
            process_fn=process_fn,
            data=users,
            **kwargs,
        )

        success_count = result.get("success_count") or 0
        total_success_count = last_success_count + success_count

        total_users_in_page = len(users) if users else 0
        has_more_users = total_users_in_page >= object_record_limit

        current_index = total_users_in_page + last_current_index
        user_limit_exceeded = self._exceeded_user_limit(current_index)

        stop_running = user_limit_exceeded or not has_more_users
        if stop_running:
            # set campaign completed and stop running
            error_message = self._handle_trigger_function_with_try_except(
                "Update Campaign Status to Completed",
                self._handle_trigger_completed,
                fn_params={
                    "channel_name": channel_name,
                    "success_count": total_success_count
                }
            )
        else:
            # handle running next page
            error_message = self._handle_publish_subscription(
                last_current_index=current_index,
                last_success_count=total_success_count,
            )

        return {
            "is_finished": stop_running,
            "success_count": success_count,
            "error_message": error_message,
        }

    def _handle_trigger(
        self,
        process_fn: Callable,
        data: Any,
        **kwargs,
    ):
        params = {
            "action": self.action,
            "campaign": self.parent,
            "data": data,
            "subscription_data": self.subscription_data,
            "organization": self.organization,
            **kwargs
        }

        return process_fn(**params)

    def _handle_trigger_completed(
        self,
        channel_name: Optional[str],
        success_count: int
    ) -> str:
        update_status_error_message = self._handle_trigger_function_with_try_except(
            "Update Subscription Status",
            self.update_status,
            fn_params={
                "updated_status": BaseStatus.COMPLETED
            }
        )

        update_subscription_data_error_message = self._update_subscription_data_with_try_except({
            "last_current_index": 0
        })

        notify_error_message = ""
        if channel_name:
            subtitle = self._get_trigger_completed_notification_subtitle(
                channel_name, success_count
            )
            notify_error_message = self._handle_trigger_function_with_try_except(
                "Create Notification",
                self._notify,
                fn_params={
                    "publisher_type": f"{self._notification_publisher_type}",
                    "title": f"{self._parent_name} has been distributed successfully to your recipients",
                    "subtitle": subtitle,
                }
            )

        error_messages = {
            update_subscription_data_error_message,
            update_status_error_message,
            notify_error_message,
        }
        return " ".join([error_message for error_message in error_messages if error_message])

    def _handle_publish_subscription(
        self,
        last_current_index: int,
        last_success_count: int
    ):
        update_subscription_data_error_message = self._update_subscription_data_with_try_except({
            "last_current_index": last_current_index
        })
        publish_subscription_error_message = self._handle_trigger_function_with_try_except(
            "Publish Subscription",
            self.subscription_client.publish,
            fn_params={
                "request_data": {
                    "last_current_index": last_current_index,
                    "last_success_count": last_success_count,
                }
            }
        )
        error_message = None
        if update_subscription_data_error_message or publish_subscription_error_message:
            error_message = (
                f"{update_subscription_data_error_message} {publish_subscription_error_message}"
            )

        return error_message

    def _update_subscription_data_with_try_except(self, updated_data: Dict[str, Any]) -> str:
        return self._handle_trigger_function_with_try_except(
            "Update Subscription Data",
            self.update_subscription_data,
            fn_params={
                "updated_data": updated_data
            }
        )

    @staticmethod
    def _handle_trigger_function_with_try_except(
        fn_name: str,
        fn: Callable,
        fn_params: Dict[str, Any] = None
    ) -> str:
        error_message = None
        try:
            fn_params = fn_params if fn_params else {}
            fn(**fn_params)
        except BaseError as e:
            error_message = e.message
        except Exception:
            error_message = ErrorMessage.IMPLEMENTATION_ERROR

        return f"{fn_name}: {error_message}" if error_message else ""
