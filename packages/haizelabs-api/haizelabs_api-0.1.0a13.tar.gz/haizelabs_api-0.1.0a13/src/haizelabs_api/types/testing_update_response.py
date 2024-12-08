# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel

__all__ = [
    "TestingUpdateResponse",
    "Content",
    "ContentBehavior",
    "ContentInputDetection",
    "ContentInputDetectionDetectorData",
    "ContentInputDetectionDetectorDataTextMatchingDetector",
    "ContentInputDetectionDetectorDataCategoryDetector",
    "ContentInputDetectionDetectorDataNaturalLanguageDetector",
    "ContentInputDetectionDetectorDataComparatorDetector",
    "ContentInputDetectionDetectorDataCustomDetector",
    "ContentInputMessage",
    "ContentInputMessageChatCompletionSystemMessageParam",
    "ContentInputMessageChatCompletionSystemMessageParamContentUnionMember1",
    "ContentInputMessageChatCompletionUserMessageParamOutput",
    "ContentInputMessageChatCompletionUserMessageParamOutputContentUnionMember1",
    "ContentInputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartTextParam",
    "ContentInputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartImageParam",
    "ContentInputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartImageParamImageURL",
    "ContentInputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartInputAudioParam",
    "ContentInputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio",
    "ContentInputMessageChatCompletionAssistantMessageParamOutput",
    "ContentInputMessageChatCompletionAssistantMessageParamOutputAudio",
    "ContentInputMessageChatCompletionAssistantMessageParamOutputContentUnionMember1",
    "ContentInputMessageChatCompletionAssistantMessageParamOutputContentUnionMember1ChatCompletionContentPartTextParam",
    "ContentInputMessageChatCompletionAssistantMessageParamOutputContentUnionMember1ChatCompletionContentPartRefusalParam",
    "ContentInputMessageChatCompletionAssistantMessageParamOutputFunctionCall",
    "ContentInputMessageChatCompletionAssistantMessageParamOutputToolCall",
    "ContentInputMessageChatCompletionAssistantMessageParamOutputToolCallFunction",
    "ContentInputMessageChatCompletionToolMessageParam",
    "ContentInputMessageChatCompletionToolMessageParamContentUnionMember1",
    "ContentInputMessageChatCompletionFunctionMessageParam",
    "ContentOutputDetection",
    "ContentOutputDetectionDetectorData",
    "ContentOutputDetectionDetectorDataTextMatchingDetector",
    "ContentOutputDetectionDetectorDataCategoryDetector",
    "ContentOutputDetectionDetectorDataNaturalLanguageDetector",
    "ContentOutputDetectionDetectorDataComparatorDetector",
    "ContentOutputDetectionDetectorDataCustomDetector",
    "ContentOutputMessage",
    "ContentOutputMessageChatCompletionSystemMessageParam",
    "ContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1",
    "ContentOutputMessageChatCompletionUserMessageParamOutput",
    "ContentOutputMessageChatCompletionUserMessageParamOutputContentUnionMember1",
    "ContentOutputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartTextParam",
    "ContentOutputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartImageParam",
    "ContentOutputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartImageParamImageURL",
    "ContentOutputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartInputAudioParam",
    "ContentOutputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio",
    "ContentOutputMessageChatCompletionAssistantMessageParamOutput",
    "ContentOutputMessageChatCompletionAssistantMessageParamOutputAudio",
    "ContentOutputMessageChatCompletionAssistantMessageParamOutputContentUnionMember1",
    "ContentOutputMessageChatCompletionAssistantMessageParamOutputContentUnionMember1ChatCompletionContentPartTextParam",
    "ContentOutputMessageChatCompletionAssistantMessageParamOutputContentUnionMember1ChatCompletionContentPartRefusalParam",
    "ContentOutputMessageChatCompletionAssistantMessageParamOutputFunctionCall",
    "ContentOutputMessageChatCompletionAssistantMessageParamOutputToolCall",
    "ContentOutputMessageChatCompletionAssistantMessageParamOutputToolCallFunction",
    "ContentOutputMessageChatCompletionToolMessageParam",
    "ContentOutputMessageChatCompletionToolMessageParamContentUnionMember1",
    "ContentOutputMessageChatCompletionFunctionMessageParam",
]


class ContentBehavior(BaseModel):
    description: str


class ContentInputDetectionDetectorDataTextMatchingDetector(BaseModel):
    name: str

    regex: str

    user_id: str

    id: Optional[str] = None

    created: Optional[datetime] = None

    detector_type: Optional[Literal["TEXT_MATCHING"]] = None

    last_updated: Optional[datetime] = None


class ContentInputDetectionDetectorDataCategoryDetector(BaseModel):
    category: str

    name: str

    user_id: str

    id: Optional[str] = None

    created: Optional[datetime] = None

    detector_type: Optional[Literal["CATEGORY"]] = None

    last_updated: Optional[datetime] = None


class ContentInputDetectionDetectorDataNaturalLanguageDetector(BaseModel):
    name: str

    natural_language_content: str

    user_id: str

    id: Optional[str] = None

    created: Optional[datetime] = None

    detector_type: Optional[Literal["NATURAL_LANGUAGE"]] = None

    last_updated: Optional[datetime] = None


class ContentInputDetectionDetectorDataComparatorDetector(BaseModel):
    name: str

    type: Literal["EXACT_MATCH", "LANGUAGE_MODEL_SIMILARITY"]

    user_id: str

    id: Optional[str] = None

    created: Optional[datetime] = None

    detector_type: Optional[Literal["COMPARATOR"]] = None

    last_updated: Optional[datetime] = None


class ContentInputDetectionDetectorDataCustomDetector(BaseModel):
    name: str

    type: Literal["TIERED_DETECTOR"]

    user_id: str

    id: Optional[str] = None

    created: Optional[datetime] = None

    detector_type: Optional[Literal["CUSTOM"]] = None

    last_updated: Optional[datetime] = None


ContentInputDetectionDetectorData: TypeAlias = Annotated[
    Union[
        ContentInputDetectionDetectorDataTextMatchingDetector,
        ContentInputDetectionDetectorDataCategoryDetector,
        ContentInputDetectionDetectorDataNaturalLanguageDetector,
        ContentInputDetectionDetectorDataComparatorDetector,
        ContentInputDetectionDetectorDataCustomDetector,
        None,
    ],
    PropertyInfo(discriminator="detector_type"),
]


class ContentInputDetection(BaseModel):
    content_id: str

    detected: bool

    detector_id: str

    end_time: datetime

    score: float

    start_time: datetime

    detector_data: Optional[ContentInputDetectionDetectorData] = None


class ContentInputMessageChatCompletionSystemMessageParamContentUnionMember1(BaseModel):
    text: str

    type: Literal["text"]


class ContentInputMessageChatCompletionSystemMessageParam(BaseModel):
    content: Union[str, List[ContentInputMessageChatCompletionSystemMessageParamContentUnionMember1]]

    role: Literal["system"]

    name: Optional[str] = None


class ContentInputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartTextParam(
    BaseModel
):
    text: str

    type: Literal["text"]


class ContentInputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartImageParamImageURL(
    BaseModel
):
    url: str

    detail: Optional[Literal["auto", "low", "high"]] = None


class ContentInputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartImageParam(
    BaseModel
):
    image_url: ContentInputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartImageParamImageURL

    type: Literal["image_url"]


class ContentInputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio(
    BaseModel
):
    data: str

    format: Literal["wav", "mp3"]


class ContentInputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartInputAudioParam(
    BaseModel
):
    input_audio: ContentInputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio

    type: Literal["input_audio"]


ContentInputMessageChatCompletionUserMessageParamOutputContentUnionMember1: TypeAlias = Union[
    ContentInputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartTextParam,
    ContentInputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartImageParam,
    ContentInputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartInputAudioParam,
]


class ContentInputMessageChatCompletionUserMessageParamOutput(BaseModel):
    content: Union[str, List[ContentInputMessageChatCompletionUserMessageParamOutputContentUnionMember1]]

    role: Literal["user"]

    name: Optional[str] = None


class ContentInputMessageChatCompletionAssistantMessageParamOutputAudio(BaseModel):
    id: str


class ContentInputMessageChatCompletionAssistantMessageParamOutputContentUnionMember1ChatCompletionContentPartTextParam(
    BaseModel
):
    text: str

    type: Literal["text"]


class ContentInputMessageChatCompletionAssistantMessageParamOutputContentUnionMember1ChatCompletionContentPartRefusalParam(
    BaseModel
):
    refusal: str

    type: Literal["refusal"]


ContentInputMessageChatCompletionAssistantMessageParamOutputContentUnionMember1: TypeAlias = Union[
    ContentInputMessageChatCompletionAssistantMessageParamOutputContentUnionMember1ChatCompletionContentPartTextParam,
    ContentInputMessageChatCompletionAssistantMessageParamOutputContentUnionMember1ChatCompletionContentPartRefusalParam,
]


class ContentInputMessageChatCompletionAssistantMessageParamOutputFunctionCall(BaseModel):
    arguments: str

    name: str


class ContentInputMessageChatCompletionAssistantMessageParamOutputToolCallFunction(BaseModel):
    arguments: str

    name: str


class ContentInputMessageChatCompletionAssistantMessageParamOutputToolCall(BaseModel):
    id: str

    function: ContentInputMessageChatCompletionAssistantMessageParamOutputToolCallFunction

    type: Literal["function"]


class ContentInputMessageChatCompletionAssistantMessageParamOutput(BaseModel):
    role: Literal["assistant"]

    audio: Optional[ContentInputMessageChatCompletionAssistantMessageParamOutputAudio] = None

    content: Union[str, List[ContentInputMessageChatCompletionAssistantMessageParamOutputContentUnionMember1], None] = (
        None
    )

    function_call: Optional[ContentInputMessageChatCompletionAssistantMessageParamOutputFunctionCall] = None

    name: Optional[str] = None

    refusal: Optional[str] = None

    tool_calls: Optional[List[ContentInputMessageChatCompletionAssistantMessageParamOutputToolCall]] = None


class ContentInputMessageChatCompletionToolMessageParamContentUnionMember1(BaseModel):
    text: str

    type: Literal["text"]


class ContentInputMessageChatCompletionToolMessageParam(BaseModel):
    content: Union[str, List[ContentInputMessageChatCompletionToolMessageParamContentUnionMember1]]

    role: Literal["tool"]

    tool_call_id: str


class ContentInputMessageChatCompletionFunctionMessageParam(BaseModel):
    content: Optional[str] = None

    name: str

    role: Literal["function"]


ContentInputMessage: TypeAlias = Union[
    ContentInputMessageChatCompletionSystemMessageParam,
    ContentInputMessageChatCompletionUserMessageParamOutput,
    ContentInputMessageChatCompletionAssistantMessageParamOutput,
    ContentInputMessageChatCompletionToolMessageParam,
    ContentInputMessageChatCompletionFunctionMessageParam,
]


class ContentOutputDetectionDetectorDataTextMatchingDetector(BaseModel):
    name: str

    regex: str

    user_id: str

    id: Optional[str] = None

    created: Optional[datetime] = None

    detector_type: Optional[Literal["TEXT_MATCHING"]] = None

    last_updated: Optional[datetime] = None


class ContentOutputDetectionDetectorDataCategoryDetector(BaseModel):
    category: str

    name: str

    user_id: str

    id: Optional[str] = None

    created: Optional[datetime] = None

    detector_type: Optional[Literal["CATEGORY"]] = None

    last_updated: Optional[datetime] = None


class ContentOutputDetectionDetectorDataNaturalLanguageDetector(BaseModel):
    name: str

    natural_language_content: str

    user_id: str

    id: Optional[str] = None

    created: Optional[datetime] = None

    detector_type: Optional[Literal["NATURAL_LANGUAGE"]] = None

    last_updated: Optional[datetime] = None


class ContentOutputDetectionDetectorDataComparatorDetector(BaseModel):
    name: str

    type: Literal["EXACT_MATCH", "LANGUAGE_MODEL_SIMILARITY"]

    user_id: str

    id: Optional[str] = None

    created: Optional[datetime] = None

    detector_type: Optional[Literal["COMPARATOR"]] = None

    last_updated: Optional[datetime] = None


class ContentOutputDetectionDetectorDataCustomDetector(BaseModel):
    name: str

    type: Literal["TIERED_DETECTOR"]

    user_id: str

    id: Optional[str] = None

    created: Optional[datetime] = None

    detector_type: Optional[Literal["CUSTOM"]] = None

    last_updated: Optional[datetime] = None


ContentOutputDetectionDetectorData: TypeAlias = Annotated[
    Union[
        ContentOutputDetectionDetectorDataTextMatchingDetector,
        ContentOutputDetectionDetectorDataCategoryDetector,
        ContentOutputDetectionDetectorDataNaturalLanguageDetector,
        ContentOutputDetectionDetectorDataComparatorDetector,
        ContentOutputDetectionDetectorDataCustomDetector,
        None,
    ],
    PropertyInfo(discriminator="detector_type"),
]


class ContentOutputDetection(BaseModel):
    content_id: str

    detected: bool

    detector_id: str

    end_time: datetime

    score: float

    start_time: datetime

    detector_data: Optional[ContentOutputDetectionDetectorData] = None


class ContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1(BaseModel):
    text: str

    type: Literal["text"]


class ContentOutputMessageChatCompletionSystemMessageParam(BaseModel):
    content: Union[str, List[ContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1]]

    role: Literal["system"]

    name: Optional[str] = None


class ContentOutputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartTextParam(
    BaseModel
):
    text: str

    type: Literal["text"]


class ContentOutputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartImageParamImageURL(
    BaseModel
):
    url: str

    detail: Optional[Literal["auto", "low", "high"]] = None


class ContentOutputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartImageParam(
    BaseModel
):
    image_url: ContentOutputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartImageParamImageURL

    type: Literal["image_url"]


class ContentOutputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio(
    BaseModel
):
    data: str

    format: Literal["wav", "mp3"]


class ContentOutputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartInputAudioParam(
    BaseModel
):
    input_audio: ContentOutputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio

    type: Literal["input_audio"]


ContentOutputMessageChatCompletionUserMessageParamOutputContentUnionMember1: TypeAlias = Union[
    ContentOutputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartTextParam,
    ContentOutputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartImageParam,
    ContentOutputMessageChatCompletionUserMessageParamOutputContentUnionMember1ChatCompletionContentPartInputAudioParam,
]


class ContentOutputMessageChatCompletionUserMessageParamOutput(BaseModel):
    content: Union[str, List[ContentOutputMessageChatCompletionUserMessageParamOutputContentUnionMember1]]

    role: Literal["user"]

    name: Optional[str] = None


class ContentOutputMessageChatCompletionAssistantMessageParamOutputAudio(BaseModel):
    id: str


class ContentOutputMessageChatCompletionAssistantMessageParamOutputContentUnionMember1ChatCompletionContentPartTextParam(
    BaseModel
):
    text: str

    type: Literal["text"]


class ContentOutputMessageChatCompletionAssistantMessageParamOutputContentUnionMember1ChatCompletionContentPartRefusalParam(
    BaseModel
):
    refusal: str

    type: Literal["refusal"]


ContentOutputMessageChatCompletionAssistantMessageParamOutputContentUnionMember1: TypeAlias = Union[
    ContentOutputMessageChatCompletionAssistantMessageParamOutputContentUnionMember1ChatCompletionContentPartTextParam,
    ContentOutputMessageChatCompletionAssistantMessageParamOutputContentUnionMember1ChatCompletionContentPartRefusalParam,
]


class ContentOutputMessageChatCompletionAssistantMessageParamOutputFunctionCall(BaseModel):
    arguments: str

    name: str


class ContentOutputMessageChatCompletionAssistantMessageParamOutputToolCallFunction(BaseModel):
    arguments: str

    name: str


class ContentOutputMessageChatCompletionAssistantMessageParamOutputToolCall(BaseModel):
    id: str

    function: ContentOutputMessageChatCompletionAssistantMessageParamOutputToolCallFunction

    type: Literal["function"]


class ContentOutputMessageChatCompletionAssistantMessageParamOutput(BaseModel):
    role: Literal["assistant"]

    audio: Optional[ContentOutputMessageChatCompletionAssistantMessageParamOutputAudio] = None

    content: Union[
        str, List[ContentOutputMessageChatCompletionAssistantMessageParamOutputContentUnionMember1], None
    ] = None

    function_call: Optional[ContentOutputMessageChatCompletionAssistantMessageParamOutputFunctionCall] = None

    name: Optional[str] = None

    refusal: Optional[str] = None

    tool_calls: Optional[List[ContentOutputMessageChatCompletionAssistantMessageParamOutputToolCall]] = None


class ContentOutputMessageChatCompletionToolMessageParamContentUnionMember1(BaseModel):
    text: str

    type: Literal["text"]


class ContentOutputMessageChatCompletionToolMessageParam(BaseModel):
    content: Union[str, List[ContentOutputMessageChatCompletionToolMessageParamContentUnionMember1]]

    role: Literal["tool"]

    tool_call_id: str


class ContentOutputMessageChatCompletionFunctionMessageParam(BaseModel):
    content: Optional[str] = None

    name: str

    role: Literal["function"]


ContentOutputMessage: TypeAlias = Union[
    ContentOutputMessageChatCompletionSystemMessageParam,
    ContentOutputMessageChatCompletionUserMessageParamOutput,
    ContentOutputMessageChatCompletionAssistantMessageParamOutput,
    ContentOutputMessageChatCompletionToolMessageParam,
    ContentOutputMessageChatCompletionFunctionMessageParam,
]


class Content(BaseModel):
    id: Optional[str] = None

    algorithm: Optional[str] = None

    behavior: Optional[ContentBehavior] = None

    content_group_ids: Optional[List[str]] = None

    content_type: Optional[Literal["BASE", "TEST", "EXPERIMENT"]] = None

    end: Optional[datetime] = None

    generate_end_time: Optional[datetime] = None

    generate_start_time: Optional[datetime] = None

    input_detections: Optional[List[ContentInputDetection]] = None

    input_messages: Optional[List[ContentInputMessage]] = None

    metadata: Optional[object] = None

    output_detections: Optional[List[ContentOutputDetection]] = None

    output_messages: Optional[List[ContentOutputMessage]] = None

    start: Optional[datetime] = None

    status: Optional[
        Literal["GENERATING_CONTENT", "AWAITING_RESPONSE", "ANALYZING_RESPONSE", "COMPLETE", "DISCARDED"]
    ] = None
    """Status for a single content object in a test."""

    test_id: Optional[str] = None

    time: Optional[datetime] = None

    user_id: Optional[str] = None


class TestingUpdateResponse(BaseModel):
    __test__ = False
    status: Literal["COMPLETE", "ERROR", "RUNNING", "STEP_COMPLETE", "STOPPED"]
    """Status for the overall test."""

    id: Optional[str] = None

    contents: Optional[List[Content]] = None

    test_id: Optional[str] = None

    time: Optional[datetime] = None
