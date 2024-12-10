from typing import TypedDict, Optional

from filum_utils.enums import EngagementMessageStatus


class EngagementMessageUser(TypedDict, total=False):
    phone: Optional[str]
    email: Optional[str]
    name: Optional[str]
    user_id: Optional[str]
    anonymous_id: Optional[str]


class CreateEngagementMessage(TypedDict, total=False):
    id: str
    status: EngagementMessageStatus
    distribution_id: int
    user: EngagementMessageUser
    send_timestamp: str
    send_cost: Optional[float]
    sending_failed_reason: Optional[str]
    zns_template_id: Optional[int]
    sms_template_id: Optional[int]
    purpose_id: Optional[str]
