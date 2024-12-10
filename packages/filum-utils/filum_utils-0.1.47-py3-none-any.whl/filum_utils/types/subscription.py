from typing import TypedDict, Optional, Dict, Any, List


class DataMapping(TypedDict, total=False):
    piped_text: str
    value: str
    value_type: Optional[str]


class TriggerData(TypedDict, total=False):
    segment_id: Optional[str]
    file_name: Optional[str]
    user_limit_per_trigger: Optional[int]
    data_mapping: Optional[List[DataMapping]]


class ZaloTemplateParam(TypedDict, total=False):
    name: str
    require: Optional[bool]  # based on ZNS template parameter name
    type: str
    maxLength: Optional[int]  # based on ZNS template parameter name
    minLength: Optional[int]  # based on ZNS template parameter name
    acceptNull: Optional[bool]  # based on ZNS template parameter name


class SubscriptionData(TypedDict, total=False):
    input_data: Optional[Dict[str, Any]]
    last_current_index: Optional[int]
    last_current_row: Optional[int]
    triggered_source: Optional[str]
    trigger_data: Optional[TriggerData]
    distribution_id: Optional[str]
    purpose_id: Optional[str]
    # for ZNS distribution
    zalo_template_id: Optional[str]
    zalo_template_params: Optional[List[ZaloTemplateParam]]
    zalo_template_param_mappings: Optional[Dict[str, str]]
    zns_template_id: Optional[int]
    # for SMS distribution
    sms_brand_name: Optional[str]
    sms_template_content: Optional[str]
    sms_template_without_accent: Optional[bool]
    sms_template_id: Optional[int]

class Subscription(TypedDict, total=False):
    id: str
    data: Optional[SubscriptionData]
