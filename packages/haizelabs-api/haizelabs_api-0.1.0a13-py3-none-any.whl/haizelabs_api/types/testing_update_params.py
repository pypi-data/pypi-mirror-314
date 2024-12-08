# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable, Optional
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "TestingUpdateParams",
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
    "ContentInputMessageChatCompletionUserMessageParamInput",
    "ContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1",
    "ContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "ContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam",
    "ContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL",
    "ContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam",
    "ContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio",
    "ContentInputMessageChatCompletionAssistantMessageParamInput",
    "ContentInputMessageChatCompletionAssistantMessageParamInputAudio",
    "ContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1",
    "ContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "ContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam",
    "ContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall",
    "ContentInputMessageChatCompletionAssistantMessageParamInputToolCall",
    "ContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction",
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
    "ContentOutputMessageChatCompletionUserMessageParamInput",
    "ContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1",
    "ContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "ContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam",
    "ContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL",
    "ContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam",
    "ContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio",
    "ContentOutputMessageChatCompletionAssistantMessageParamInput",
    "ContentOutputMessageChatCompletionAssistantMessageParamInputAudio",
    "ContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1",
    "ContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "ContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam",
    "ContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall",
    "ContentOutputMessageChatCompletionAssistantMessageParamInputToolCall",
    "ContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction",
    "ContentOutputMessageChatCompletionToolMessageParam",
    "ContentOutputMessageChatCompletionToolMessageParamContentUnionMember1",
    "ContentOutputMessageChatCompletionFunctionMessageParam",
]


class TestingUpdateParams(TypedDict, total=False):
    id: str

    contents: Iterable[Content]

    test_id: str

    time: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentBehavior(TypedDict, total=False):
    description: Required[str]


class ContentInputDetectionDetectorDataTextMatchingDetector(TypedDict, total=False):
    name: Required[str]

    regex: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["TEXT_MATCHING"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentInputDetectionDetectorDataCategoryDetector(TypedDict, total=False):
    category: Required[str]

    name: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CATEGORY"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentInputDetectionDetectorDataNaturalLanguageDetector(TypedDict, total=False):
    name: Required[str]

    natural_language_content: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["NATURAL_LANGUAGE"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentInputDetectionDetectorDataComparatorDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["EXACT_MATCH", "LANGUAGE_MODEL_SIMILARITY"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["COMPARATOR"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentInputDetectionDetectorDataCustomDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["TIERED_DETECTOR"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CUSTOM"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


ContentInputDetectionDetectorData: TypeAlias = Union[
    ContentInputDetectionDetectorDataTextMatchingDetector,
    ContentInputDetectionDetectorDataCategoryDetector,
    ContentInputDetectionDetectorDataNaturalLanguageDetector,
    ContentInputDetectionDetectorDataComparatorDetector,
    ContentInputDetectionDetectorDataCustomDetector,
]


class ContentInputDetection(TypedDict, total=False):
    content_id: Required[str]

    detected: Required[bool]

    detector_id: Required[str]

    end_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    score: Required[float]

    start_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    detector_data: Optional[ContentInputDetectionDetectorData]


class ContentInputMessageChatCompletionSystemMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentInputMessageChatCompletionSystemMessageParam(TypedDict, total=False):
    content: Required[Union[str, Iterable[ContentInputMessageChatCompletionSystemMessageParamContentUnionMember1]]]

    role: Required[Literal["system"]]

    name: str


class ContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["auto", "low", "high"]


class ContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam(
    TypedDict, total=False
):
    image_url: Required[
        ContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL
    ]

    type: Required[Literal["image_url"]]


class ContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio(
    TypedDict, total=False
):
    data: Required[str]

    format: Required[Literal["wav", "mp3"]]


class ContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam(
    TypedDict, total=False
):
    input_audio: Required[
        ContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio
    ]

    type: Required[Literal["input_audio"]]


ContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1: TypeAlias = Union[
    ContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    ContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam,
    ContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam,
]


class ContentInputMessageChatCompletionUserMessageParamInput(TypedDict, total=False):
    content: Required[Union[str, Iterable[ContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1]]]

    role: Required[Literal["user"]]

    name: str


class ContentInputMessageChatCompletionAssistantMessageParamInputAudio(TypedDict, total=False):
    id: Required[str]


class ContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam(
    TypedDict, total=False
):
    refusal: Required[str]

    type: Required[Literal["refusal"]]


ContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1: TypeAlias = Union[
    ContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    ContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam,
]


class ContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall(TypedDict, total=False):
    arguments: Required[str]

    name: Required[str]


class ContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction(TypedDict, total=False):
    arguments: Required[str]

    name: Required[str]


class ContentInputMessageChatCompletionAssistantMessageParamInputToolCall(TypedDict, total=False):
    id: Required[str]

    function: Required[ContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction]

    type: Required[Literal["function"]]


class ContentInputMessageChatCompletionAssistantMessageParamInput(TypedDict, total=False):
    role: Required[Literal["assistant"]]

    audio: Optional[ContentInputMessageChatCompletionAssistantMessageParamInputAudio]

    content: Union[str, Iterable[ContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1], None]

    function_call: Optional[ContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall]

    name: str

    refusal: Optional[str]

    tool_calls: Iterable[ContentInputMessageChatCompletionAssistantMessageParamInputToolCall]


class ContentInputMessageChatCompletionToolMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentInputMessageChatCompletionToolMessageParam(TypedDict, total=False):
    content: Required[Union[str, Iterable[ContentInputMessageChatCompletionToolMessageParamContentUnionMember1]]]

    role: Required[Literal["tool"]]

    tool_call_id: Required[str]


class ContentInputMessageChatCompletionFunctionMessageParam(TypedDict, total=False):
    content: Required[Optional[str]]

    name: Required[str]

    role: Required[Literal["function"]]


ContentInputMessage: TypeAlias = Union[
    ContentInputMessageChatCompletionSystemMessageParam,
    ContentInputMessageChatCompletionUserMessageParamInput,
    ContentInputMessageChatCompletionAssistantMessageParamInput,
    ContentInputMessageChatCompletionToolMessageParam,
    ContentInputMessageChatCompletionFunctionMessageParam,
]


class ContentOutputDetectionDetectorDataTextMatchingDetector(TypedDict, total=False):
    name: Required[str]

    regex: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["TEXT_MATCHING"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentOutputDetectionDetectorDataCategoryDetector(TypedDict, total=False):
    category: Required[str]

    name: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CATEGORY"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentOutputDetectionDetectorDataNaturalLanguageDetector(TypedDict, total=False):
    name: Required[str]

    natural_language_content: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["NATURAL_LANGUAGE"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentOutputDetectionDetectorDataComparatorDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["EXACT_MATCH", "LANGUAGE_MODEL_SIMILARITY"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["COMPARATOR"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentOutputDetectionDetectorDataCustomDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["TIERED_DETECTOR"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CUSTOM"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


ContentOutputDetectionDetectorData: TypeAlias = Union[
    ContentOutputDetectionDetectorDataTextMatchingDetector,
    ContentOutputDetectionDetectorDataCategoryDetector,
    ContentOutputDetectionDetectorDataNaturalLanguageDetector,
    ContentOutputDetectionDetectorDataComparatorDetector,
    ContentOutputDetectionDetectorDataCustomDetector,
]


class ContentOutputDetection(TypedDict, total=False):
    content_id: Required[str]

    detected: Required[bool]

    detector_id: Required[str]

    end_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    score: Required[float]

    start_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    detector_data: Optional[ContentOutputDetectionDetectorData]


class ContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentOutputMessageChatCompletionSystemMessageParam(TypedDict, total=False):
    content: Required[Union[str, Iterable[ContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1]]]

    role: Required[Literal["system"]]

    name: str


class ContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["auto", "low", "high"]


class ContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam(
    TypedDict, total=False
):
    image_url: Required[
        ContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL
    ]

    type: Required[Literal["image_url"]]


class ContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio(
    TypedDict, total=False
):
    data: Required[str]

    format: Required[Literal["wav", "mp3"]]


class ContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam(
    TypedDict, total=False
):
    input_audio: Required[
        ContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio
    ]

    type: Required[Literal["input_audio"]]


ContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1: TypeAlias = Union[
    ContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    ContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam,
    ContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam,
]


class ContentOutputMessageChatCompletionUserMessageParamInput(TypedDict, total=False):
    content: Required[Union[str, Iterable[ContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1]]]

    role: Required[Literal["user"]]

    name: str


class ContentOutputMessageChatCompletionAssistantMessageParamInputAudio(TypedDict, total=False):
    id: Required[str]


class ContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam(
    TypedDict, total=False
):
    refusal: Required[str]

    type: Required[Literal["refusal"]]


ContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1: TypeAlias = Union[
    ContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    ContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam,
]


class ContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall(TypedDict, total=False):
    arguments: Required[str]

    name: Required[str]


class ContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction(TypedDict, total=False):
    arguments: Required[str]

    name: Required[str]


class ContentOutputMessageChatCompletionAssistantMessageParamInputToolCall(TypedDict, total=False):
    id: Required[str]

    function: Required[ContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction]

    type: Required[Literal["function"]]


class ContentOutputMessageChatCompletionAssistantMessageParamInput(TypedDict, total=False):
    role: Required[Literal["assistant"]]

    audio: Optional[ContentOutputMessageChatCompletionAssistantMessageParamInputAudio]

    content: Union[str, Iterable[ContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1], None]

    function_call: Optional[ContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall]

    name: str

    refusal: Optional[str]

    tool_calls: Iterable[ContentOutputMessageChatCompletionAssistantMessageParamInputToolCall]


class ContentOutputMessageChatCompletionToolMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentOutputMessageChatCompletionToolMessageParam(TypedDict, total=False):
    content: Required[Union[str, Iterable[ContentOutputMessageChatCompletionToolMessageParamContentUnionMember1]]]

    role: Required[Literal["tool"]]

    tool_call_id: Required[str]


class ContentOutputMessageChatCompletionFunctionMessageParam(TypedDict, total=False):
    content: Required[Optional[str]]

    name: Required[str]

    role: Required[Literal["function"]]


ContentOutputMessage: TypeAlias = Union[
    ContentOutputMessageChatCompletionSystemMessageParam,
    ContentOutputMessageChatCompletionUserMessageParamInput,
    ContentOutputMessageChatCompletionAssistantMessageParamInput,
    ContentOutputMessageChatCompletionToolMessageParam,
    ContentOutputMessageChatCompletionFunctionMessageParam,
]


class Content(TypedDict, total=False):
    id: str

    algorithm: Optional[str]

    behavior: Optional[ContentBehavior]

    content_group_ids: Optional[List[str]]

    content_type: Optional[Literal["BASE", "TEST", "EXPERIMENT"]]

    end: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    generate_end_time: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    generate_start_time: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    input_detections: Optional[Iterable[ContentInputDetection]]

    input_messages: Optional[Iterable[ContentInputMessage]]

    metadata: Optional[object]

    output_detections: Optional[Iterable[ContentOutputDetection]]

    output_messages: Optional[Iterable[ContentOutputMessage]]

    start: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    status: Optional[Literal["GENERATING_CONTENT", "AWAITING_RESPONSE", "ANALYZING_RESPONSE", "COMPLETE", "DISCARDED"]]
    """Status for a single content object in a test."""

    test_id: Optional[str]

    time: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    user_id: Optional[str]
