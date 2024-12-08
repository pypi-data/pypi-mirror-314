# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable, Optional
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "MonitoringLogParams",
    "Span",
    "SpanContent",
    "SpanContentInputDetection",
    "SpanContentInputDetectionDetectorData",
    "SpanContentInputDetectionDetectorDataTextMatchingDetector",
    "SpanContentInputDetectionDetectorDataCategoryDetector",
    "SpanContentInputDetectionDetectorDataNaturalLanguageDetector",
    "SpanContentInputDetectionDetectorDataComparatorDetector",
    "SpanContentInputDetectionDetectorDataCustomDetector",
    "SpanContentInputMessage",
    "SpanContentInputMessageChatCompletionSystemMessageParam",
    "SpanContentInputMessageChatCompletionSystemMessageParamContentUnionMember1",
    "SpanContentInputMessageChatCompletionUserMessageParamInput",
    "SpanContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1",
    "SpanContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "SpanContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam",
    "SpanContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL",
    "SpanContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam",
    "SpanContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio",
    "SpanContentInputMessageChatCompletionAssistantMessageParamInput",
    "SpanContentInputMessageChatCompletionAssistantMessageParamInputAudio",
    "SpanContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1",
    "SpanContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "SpanContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam",
    "SpanContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall",
    "SpanContentInputMessageChatCompletionAssistantMessageParamInputToolCall",
    "SpanContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction",
    "SpanContentInputMessageChatCompletionToolMessageParam",
    "SpanContentInputMessageChatCompletionToolMessageParamContentUnionMember1",
    "SpanContentInputMessageChatCompletionFunctionMessageParam",
    "SpanContentOutputDetection",
    "SpanContentOutputDetectionDetectorData",
    "SpanContentOutputDetectionDetectorDataTextMatchingDetector",
    "SpanContentOutputDetectionDetectorDataCategoryDetector",
    "SpanContentOutputDetectionDetectorDataNaturalLanguageDetector",
    "SpanContentOutputDetectionDetectorDataComparatorDetector",
    "SpanContentOutputDetectionDetectorDataCustomDetector",
    "SpanContentOutputMessage",
    "SpanContentOutputMessageChatCompletionSystemMessageParam",
    "SpanContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1",
    "SpanContentOutputMessageChatCompletionUserMessageParamInput",
    "SpanContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1",
    "SpanContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "SpanContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam",
    "SpanContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL",
    "SpanContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam",
    "SpanContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio",
    "SpanContentOutputMessageChatCompletionAssistantMessageParamInput",
    "SpanContentOutputMessageChatCompletionAssistantMessageParamInputAudio",
    "SpanContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1",
    "SpanContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "SpanContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam",
    "SpanContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall",
    "SpanContentOutputMessageChatCompletionAssistantMessageParamInputToolCall",
    "SpanContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction",
    "SpanContentOutputMessageChatCompletionToolMessageParam",
    "SpanContentOutputMessageChatCompletionToolMessageParamContentUnionMember1",
    "SpanContentOutputMessageChatCompletionFunctionMessageParam",
    "Trace",
    "TraceRootContent",
    "TraceRootContentInputDetection",
    "TraceRootContentInputDetectionDetectorData",
    "TraceRootContentInputDetectionDetectorDataTextMatchingDetector",
    "TraceRootContentInputDetectionDetectorDataCategoryDetector",
    "TraceRootContentInputDetectionDetectorDataNaturalLanguageDetector",
    "TraceRootContentInputDetectionDetectorDataComparatorDetector",
    "TraceRootContentInputDetectionDetectorDataCustomDetector",
    "TraceRootContentInputMessage",
    "TraceRootContentInputMessageChatCompletionSystemMessageParam",
    "TraceRootContentInputMessageChatCompletionSystemMessageParamContentUnionMember1",
    "TraceRootContentInputMessageChatCompletionUserMessageParamInput",
    "TraceRootContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1",
    "TraceRootContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "TraceRootContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam",
    "TraceRootContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL",
    "TraceRootContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam",
    "TraceRootContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio",
    "TraceRootContentInputMessageChatCompletionAssistantMessageParamInput",
    "TraceRootContentInputMessageChatCompletionAssistantMessageParamInputAudio",
    "TraceRootContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1",
    "TraceRootContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "TraceRootContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam",
    "TraceRootContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall",
    "TraceRootContentInputMessageChatCompletionAssistantMessageParamInputToolCall",
    "TraceRootContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction",
    "TraceRootContentInputMessageChatCompletionToolMessageParam",
    "TraceRootContentInputMessageChatCompletionToolMessageParamContentUnionMember1",
    "TraceRootContentInputMessageChatCompletionFunctionMessageParam",
    "TraceRootContentOutputDetection",
    "TraceRootContentOutputDetectionDetectorData",
    "TraceRootContentOutputDetectionDetectorDataTextMatchingDetector",
    "TraceRootContentOutputDetectionDetectorDataCategoryDetector",
    "TraceRootContentOutputDetectionDetectorDataNaturalLanguageDetector",
    "TraceRootContentOutputDetectionDetectorDataComparatorDetector",
    "TraceRootContentOutputDetectionDetectorDataCustomDetector",
    "TraceRootContentOutputMessage",
    "TraceRootContentOutputMessageChatCompletionSystemMessageParam",
    "TraceRootContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1",
    "TraceRootContentOutputMessageChatCompletionUserMessageParamInput",
    "TraceRootContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1",
    "TraceRootContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "TraceRootContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam",
    "TraceRootContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL",
    "TraceRootContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam",
    "TraceRootContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio",
    "TraceRootContentOutputMessageChatCompletionAssistantMessageParamInput",
    "TraceRootContentOutputMessageChatCompletionAssistantMessageParamInputAudio",
    "TraceRootContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1",
    "TraceRootContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "TraceRootContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam",
    "TraceRootContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall",
    "TraceRootContentOutputMessageChatCompletionAssistantMessageParamInputToolCall",
    "TraceRootContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction",
    "TraceRootContentOutputMessageChatCompletionToolMessageParam",
    "TraceRootContentOutputMessageChatCompletionToolMessageParamContentUnionMember1",
    "TraceRootContentOutputMessageChatCompletionFunctionMessageParam",
    "Content",
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


class Span(TypedDict, total=False):
    id: str

    caller_id: Optional[str]

    content: Optional[SpanContent]

    end: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    metadata: Optional[object]

    name: str

    parent_id: Optional[str]

    span_type: Optional[Literal["DETECTOR", "JUDGE", "APP", "MODEL", "FUNCTION", "SCORER"]]

    start: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    tags: Optional[object]

    trace_id: str

    user_id: Optional[str]


class SpanContentInputDetectionDetectorDataTextMatchingDetector(TypedDict, total=False):
    name: Required[str]

    regex: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["TEXT_MATCHING"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class SpanContentInputDetectionDetectorDataCategoryDetector(TypedDict, total=False):
    category: Required[str]

    name: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CATEGORY"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class SpanContentInputDetectionDetectorDataNaturalLanguageDetector(TypedDict, total=False):
    name: Required[str]

    natural_language_content: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["NATURAL_LANGUAGE"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class SpanContentInputDetectionDetectorDataComparatorDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["EXACT_MATCH", "LANGUAGE_MODEL_SIMILARITY"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["COMPARATOR"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class SpanContentInputDetectionDetectorDataCustomDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["TIERED_DETECTOR"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CUSTOM"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


SpanContentInputDetectionDetectorData: TypeAlias = Union[
    SpanContentInputDetectionDetectorDataTextMatchingDetector,
    SpanContentInputDetectionDetectorDataCategoryDetector,
    SpanContentInputDetectionDetectorDataNaturalLanguageDetector,
    SpanContentInputDetectionDetectorDataComparatorDetector,
    SpanContentInputDetectionDetectorDataCustomDetector,
]


class SpanContentInputDetection(TypedDict, total=False):
    content_id: Required[str]

    detected: Required[bool]

    detector_id: Required[str]

    end_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    score: Required[float]

    start_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    detector_data: Optional[SpanContentInputDetectionDetectorData]


class SpanContentInputMessageChatCompletionSystemMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class SpanContentInputMessageChatCompletionSystemMessageParam(TypedDict, total=False):
    content: Required[Union[str, Iterable[SpanContentInputMessageChatCompletionSystemMessageParamContentUnionMember1]]]

    role: Required[Literal["system"]]

    name: str


class SpanContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class SpanContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["auto", "low", "high"]


class SpanContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam(
    TypedDict, total=False
):
    image_url: Required[
        SpanContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL
    ]

    type: Required[Literal["image_url"]]


class SpanContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio(
    TypedDict, total=False
):
    data: Required[str]

    format: Required[Literal["wav", "mp3"]]


class SpanContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam(
    TypedDict, total=False
):
    input_audio: Required[
        SpanContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio
    ]

    type: Required[Literal["input_audio"]]


SpanContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1: TypeAlias = Union[
    SpanContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    SpanContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam,
    SpanContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam,
]


class SpanContentInputMessageChatCompletionUserMessageParamInput(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[SpanContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1]]
    ]

    role: Required[Literal["user"]]

    name: str


class SpanContentInputMessageChatCompletionAssistantMessageParamInputAudio(TypedDict, total=False):
    id: Required[str]


class SpanContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class SpanContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam(
    TypedDict, total=False
):
    refusal: Required[str]

    type: Required[Literal["refusal"]]


SpanContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1: TypeAlias = Union[
    SpanContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    SpanContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam,
]


class SpanContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall(TypedDict, total=False):
    arguments: Required[str]

    name: Required[str]


class SpanContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction(TypedDict, total=False):
    arguments: Required[str]

    name: Required[str]


class SpanContentInputMessageChatCompletionAssistantMessageParamInputToolCall(TypedDict, total=False):
    id: Required[str]

    function: Required[SpanContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction]

    type: Required[Literal["function"]]


class SpanContentInputMessageChatCompletionAssistantMessageParamInput(TypedDict, total=False):
    role: Required[Literal["assistant"]]

    audio: Optional[SpanContentInputMessageChatCompletionAssistantMessageParamInputAudio]

    content: Union[
        str, Iterable[SpanContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1], None
    ]

    function_call: Optional[SpanContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall]

    name: str

    refusal: Optional[str]

    tool_calls: Iterable[SpanContentInputMessageChatCompletionAssistantMessageParamInputToolCall]


class SpanContentInputMessageChatCompletionToolMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class SpanContentInputMessageChatCompletionToolMessageParam(TypedDict, total=False):
    content: Required[Union[str, Iterable[SpanContentInputMessageChatCompletionToolMessageParamContentUnionMember1]]]

    role: Required[Literal["tool"]]

    tool_call_id: Required[str]


class SpanContentInputMessageChatCompletionFunctionMessageParam(TypedDict, total=False):
    content: Required[Optional[str]]

    name: Required[str]

    role: Required[Literal["function"]]


SpanContentInputMessage: TypeAlias = Union[
    SpanContentInputMessageChatCompletionSystemMessageParam,
    SpanContentInputMessageChatCompletionUserMessageParamInput,
    SpanContentInputMessageChatCompletionAssistantMessageParamInput,
    SpanContentInputMessageChatCompletionToolMessageParam,
    SpanContentInputMessageChatCompletionFunctionMessageParam,
]


class SpanContentOutputDetectionDetectorDataTextMatchingDetector(TypedDict, total=False):
    name: Required[str]

    regex: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["TEXT_MATCHING"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class SpanContentOutputDetectionDetectorDataCategoryDetector(TypedDict, total=False):
    category: Required[str]

    name: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CATEGORY"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class SpanContentOutputDetectionDetectorDataNaturalLanguageDetector(TypedDict, total=False):
    name: Required[str]

    natural_language_content: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["NATURAL_LANGUAGE"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class SpanContentOutputDetectionDetectorDataComparatorDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["EXACT_MATCH", "LANGUAGE_MODEL_SIMILARITY"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["COMPARATOR"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class SpanContentOutputDetectionDetectorDataCustomDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["TIERED_DETECTOR"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CUSTOM"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


SpanContentOutputDetectionDetectorData: TypeAlias = Union[
    SpanContentOutputDetectionDetectorDataTextMatchingDetector,
    SpanContentOutputDetectionDetectorDataCategoryDetector,
    SpanContentOutputDetectionDetectorDataNaturalLanguageDetector,
    SpanContentOutputDetectionDetectorDataComparatorDetector,
    SpanContentOutputDetectionDetectorDataCustomDetector,
]


class SpanContentOutputDetection(TypedDict, total=False):
    content_id: Required[str]

    detected: Required[bool]

    detector_id: Required[str]

    end_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    score: Required[float]

    start_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    detector_data: Optional[SpanContentOutputDetectionDetectorData]


class SpanContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class SpanContentOutputMessageChatCompletionSystemMessageParam(TypedDict, total=False):
    content: Required[Union[str, Iterable[SpanContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1]]]

    role: Required[Literal["system"]]

    name: str


class SpanContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class SpanContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["auto", "low", "high"]


class SpanContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam(
    TypedDict, total=False
):
    image_url: Required[
        SpanContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL
    ]

    type: Required[Literal["image_url"]]


class SpanContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio(
    TypedDict, total=False
):
    data: Required[str]

    format: Required[Literal["wav", "mp3"]]


class SpanContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam(
    TypedDict, total=False
):
    input_audio: Required[
        SpanContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio
    ]

    type: Required[Literal["input_audio"]]


SpanContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1: TypeAlias = Union[
    SpanContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    SpanContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam,
    SpanContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam,
]


class SpanContentOutputMessageChatCompletionUserMessageParamInput(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[SpanContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1]]
    ]

    role: Required[Literal["user"]]

    name: str


class SpanContentOutputMessageChatCompletionAssistantMessageParamInputAudio(TypedDict, total=False):
    id: Required[str]


class SpanContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class SpanContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam(
    TypedDict, total=False
):
    refusal: Required[str]

    type: Required[Literal["refusal"]]


SpanContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1: TypeAlias = Union[
    SpanContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    SpanContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam,
]


class SpanContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall(TypedDict, total=False):
    arguments: Required[str]

    name: Required[str]


class SpanContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction(TypedDict, total=False):
    arguments: Required[str]

    name: Required[str]


class SpanContentOutputMessageChatCompletionAssistantMessageParamInputToolCall(TypedDict, total=False):
    id: Required[str]

    function: Required[SpanContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction]

    type: Required[Literal["function"]]


class SpanContentOutputMessageChatCompletionAssistantMessageParamInput(TypedDict, total=False):
    role: Required[Literal["assistant"]]

    audio: Optional[SpanContentOutputMessageChatCompletionAssistantMessageParamInputAudio]

    content: Union[
        str, Iterable[SpanContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1], None
    ]

    function_call: Optional[SpanContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall]

    name: str

    refusal: Optional[str]

    tool_calls: Iterable[SpanContentOutputMessageChatCompletionAssistantMessageParamInputToolCall]


class SpanContentOutputMessageChatCompletionToolMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class SpanContentOutputMessageChatCompletionToolMessageParam(TypedDict, total=False):
    content: Required[Union[str, Iterable[SpanContentOutputMessageChatCompletionToolMessageParamContentUnionMember1]]]

    role: Required[Literal["tool"]]

    tool_call_id: Required[str]


class SpanContentOutputMessageChatCompletionFunctionMessageParam(TypedDict, total=False):
    content: Required[Optional[str]]

    name: Required[str]

    role: Required[Literal["function"]]


SpanContentOutputMessage: TypeAlias = Union[
    SpanContentOutputMessageChatCompletionSystemMessageParam,
    SpanContentOutputMessageChatCompletionUserMessageParamInput,
    SpanContentOutputMessageChatCompletionAssistantMessageParamInput,
    SpanContentOutputMessageChatCompletionToolMessageParam,
    SpanContentOutputMessageChatCompletionFunctionMessageParam,
]


class SpanContent(TypedDict, total=False):
    id: str

    content_group_ids: Optional[List[str]]

    content_type: Optional[Literal["BASE", "TEST", "EXPERIMENT"]]

    end: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    input_detections: Optional[Iterable[SpanContentInputDetection]]

    input_messages: Optional[Iterable[SpanContentInputMessage]]

    metadata: Optional[object]

    output_detections: Optional[Iterable[SpanContentOutputDetection]]

    output_messages: Optional[Iterable[SpanContentOutputMessage]]

    start: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    time: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    user_id: Optional[str]


class Trace(TypedDict, total=False):
    id: str

    end: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    name: Optional[str]

    root_content: Optional[TraceRootContent]

    start: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    user_id: Optional[str]


class TraceRootContentInputDetectionDetectorDataTextMatchingDetector(TypedDict, total=False):
    name: Required[str]

    regex: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["TEXT_MATCHING"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TraceRootContentInputDetectionDetectorDataCategoryDetector(TypedDict, total=False):
    category: Required[str]

    name: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CATEGORY"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TraceRootContentInputDetectionDetectorDataNaturalLanguageDetector(TypedDict, total=False):
    name: Required[str]

    natural_language_content: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["NATURAL_LANGUAGE"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TraceRootContentInputDetectionDetectorDataComparatorDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["EXACT_MATCH", "LANGUAGE_MODEL_SIMILARITY"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["COMPARATOR"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TraceRootContentInputDetectionDetectorDataCustomDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["TIERED_DETECTOR"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CUSTOM"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


TraceRootContentInputDetectionDetectorData: TypeAlias = Union[
    TraceRootContentInputDetectionDetectorDataTextMatchingDetector,
    TraceRootContentInputDetectionDetectorDataCategoryDetector,
    TraceRootContentInputDetectionDetectorDataNaturalLanguageDetector,
    TraceRootContentInputDetectionDetectorDataComparatorDetector,
    TraceRootContentInputDetectionDetectorDataCustomDetector,
]


class TraceRootContentInputDetection(TypedDict, total=False):
    content_id: Required[str]

    detected: Required[bool]

    detector_id: Required[str]

    end_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    score: Required[float]

    start_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    detector_data: Optional[TraceRootContentInputDetectionDetectorData]


class TraceRootContentInputMessageChatCompletionSystemMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class TraceRootContentInputMessageChatCompletionSystemMessageParam(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[TraceRootContentInputMessageChatCompletionSystemMessageParamContentUnionMember1]]
    ]

    role: Required[Literal["system"]]

    name: str


class TraceRootContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TraceRootContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["auto", "low", "high"]


class TraceRootContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam(
    TypedDict, total=False
):
    image_url: Required[
        TraceRootContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL
    ]

    type: Required[Literal["image_url"]]


class TraceRootContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio(
    TypedDict, total=False
):
    data: Required[str]

    format: Required[Literal["wav", "mp3"]]


class TraceRootContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam(
    TypedDict, total=False
):
    input_audio: Required[
        TraceRootContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio
    ]

    type: Required[Literal["input_audio"]]


TraceRootContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1: TypeAlias = Union[
    TraceRootContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    TraceRootContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam,
    TraceRootContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam,
]


class TraceRootContentInputMessageChatCompletionUserMessageParamInput(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[TraceRootContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1]]
    ]

    role: Required[Literal["user"]]

    name: str


class TraceRootContentInputMessageChatCompletionAssistantMessageParamInputAudio(TypedDict, total=False):
    id: Required[str]


class TraceRootContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TraceRootContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam(
    TypedDict, total=False
):
    refusal: Required[str]

    type: Required[Literal["refusal"]]


TraceRootContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1: TypeAlias = Union[
    TraceRootContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    TraceRootContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam,
]


class TraceRootContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall(TypedDict, total=False):
    arguments: Required[str]

    name: Required[str]


class TraceRootContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction(TypedDict, total=False):
    arguments: Required[str]

    name: Required[str]


class TraceRootContentInputMessageChatCompletionAssistantMessageParamInputToolCall(TypedDict, total=False):
    id: Required[str]

    function: Required[TraceRootContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction]

    type: Required[Literal["function"]]


class TraceRootContentInputMessageChatCompletionAssistantMessageParamInput(TypedDict, total=False):
    role: Required[Literal["assistant"]]

    audio: Optional[TraceRootContentInputMessageChatCompletionAssistantMessageParamInputAudio]

    content: Union[
        str, Iterable[TraceRootContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1], None
    ]

    function_call: Optional[TraceRootContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall]

    name: str

    refusal: Optional[str]

    tool_calls: Iterable[TraceRootContentInputMessageChatCompletionAssistantMessageParamInputToolCall]


class TraceRootContentInputMessageChatCompletionToolMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class TraceRootContentInputMessageChatCompletionToolMessageParam(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[TraceRootContentInputMessageChatCompletionToolMessageParamContentUnionMember1]]
    ]

    role: Required[Literal["tool"]]

    tool_call_id: Required[str]


class TraceRootContentInputMessageChatCompletionFunctionMessageParam(TypedDict, total=False):
    content: Required[Optional[str]]

    name: Required[str]

    role: Required[Literal["function"]]


TraceRootContentInputMessage: TypeAlias = Union[
    TraceRootContentInputMessageChatCompletionSystemMessageParam,
    TraceRootContentInputMessageChatCompletionUserMessageParamInput,
    TraceRootContentInputMessageChatCompletionAssistantMessageParamInput,
    TraceRootContentInputMessageChatCompletionToolMessageParam,
    TraceRootContentInputMessageChatCompletionFunctionMessageParam,
]


class TraceRootContentOutputDetectionDetectorDataTextMatchingDetector(TypedDict, total=False):
    name: Required[str]

    regex: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["TEXT_MATCHING"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TraceRootContentOutputDetectionDetectorDataCategoryDetector(TypedDict, total=False):
    category: Required[str]

    name: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CATEGORY"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TraceRootContentOutputDetectionDetectorDataNaturalLanguageDetector(TypedDict, total=False):
    name: Required[str]

    natural_language_content: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["NATURAL_LANGUAGE"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TraceRootContentOutputDetectionDetectorDataComparatorDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["EXACT_MATCH", "LANGUAGE_MODEL_SIMILARITY"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["COMPARATOR"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TraceRootContentOutputDetectionDetectorDataCustomDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["TIERED_DETECTOR"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CUSTOM"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


TraceRootContentOutputDetectionDetectorData: TypeAlias = Union[
    TraceRootContentOutputDetectionDetectorDataTextMatchingDetector,
    TraceRootContentOutputDetectionDetectorDataCategoryDetector,
    TraceRootContentOutputDetectionDetectorDataNaturalLanguageDetector,
    TraceRootContentOutputDetectionDetectorDataComparatorDetector,
    TraceRootContentOutputDetectionDetectorDataCustomDetector,
]


class TraceRootContentOutputDetection(TypedDict, total=False):
    content_id: Required[str]

    detected: Required[bool]

    detector_id: Required[str]

    end_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    score: Required[float]

    start_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    detector_data: Optional[TraceRootContentOutputDetectionDetectorData]


class TraceRootContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class TraceRootContentOutputMessageChatCompletionSystemMessageParam(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[TraceRootContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1]]
    ]

    role: Required[Literal["system"]]

    name: str


class TraceRootContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TraceRootContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["auto", "low", "high"]


class TraceRootContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam(
    TypedDict, total=False
):
    image_url: Required[
        TraceRootContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL
    ]

    type: Required[Literal["image_url"]]


class TraceRootContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio(
    TypedDict, total=False
):
    data: Required[str]

    format: Required[Literal["wav", "mp3"]]


class TraceRootContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam(
    TypedDict, total=False
):
    input_audio: Required[
        TraceRootContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio
    ]

    type: Required[Literal["input_audio"]]


TraceRootContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1: TypeAlias = Union[
    TraceRootContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    TraceRootContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam,
    TraceRootContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam,
]


class TraceRootContentOutputMessageChatCompletionUserMessageParamInput(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[TraceRootContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1]]
    ]

    role: Required[Literal["user"]]

    name: str


class TraceRootContentOutputMessageChatCompletionAssistantMessageParamInputAudio(TypedDict, total=False):
    id: Required[str]


class TraceRootContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TraceRootContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam(
    TypedDict, total=False
):
    refusal: Required[str]

    type: Required[Literal["refusal"]]


TraceRootContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1: TypeAlias = Union[
    TraceRootContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    TraceRootContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam,
]


class TraceRootContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall(TypedDict, total=False):
    arguments: Required[str]

    name: Required[str]


class TraceRootContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction(TypedDict, total=False):
    arguments: Required[str]

    name: Required[str]


class TraceRootContentOutputMessageChatCompletionAssistantMessageParamInputToolCall(TypedDict, total=False):
    id: Required[str]

    function: Required[TraceRootContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction]

    type: Required[Literal["function"]]


class TraceRootContentOutputMessageChatCompletionAssistantMessageParamInput(TypedDict, total=False):
    role: Required[Literal["assistant"]]

    audio: Optional[TraceRootContentOutputMessageChatCompletionAssistantMessageParamInputAudio]

    content: Union[
        str, Iterable[TraceRootContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1], None
    ]

    function_call: Optional[TraceRootContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall]

    name: str

    refusal: Optional[str]

    tool_calls: Iterable[TraceRootContentOutputMessageChatCompletionAssistantMessageParamInputToolCall]


class TraceRootContentOutputMessageChatCompletionToolMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class TraceRootContentOutputMessageChatCompletionToolMessageParam(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[TraceRootContentOutputMessageChatCompletionToolMessageParamContentUnionMember1]]
    ]

    role: Required[Literal["tool"]]

    tool_call_id: Required[str]


class TraceRootContentOutputMessageChatCompletionFunctionMessageParam(TypedDict, total=False):
    content: Required[Optional[str]]

    name: Required[str]

    role: Required[Literal["function"]]


TraceRootContentOutputMessage: TypeAlias = Union[
    TraceRootContentOutputMessageChatCompletionSystemMessageParam,
    TraceRootContentOutputMessageChatCompletionUserMessageParamInput,
    TraceRootContentOutputMessageChatCompletionAssistantMessageParamInput,
    TraceRootContentOutputMessageChatCompletionToolMessageParam,
    TraceRootContentOutputMessageChatCompletionFunctionMessageParam,
]


class TraceRootContent(TypedDict, total=False):
    id: str

    content_group_ids: Optional[List[str]]

    content_type: Optional[Literal["BASE", "TEST", "EXPERIMENT"]]

    end: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    input_detections: Optional[Iterable[TraceRootContentInputDetection]]

    input_messages: Optional[Iterable[TraceRootContentInputMessage]]

    metadata: Optional[object]

    output_detections: Optional[Iterable[TraceRootContentOutputDetection]]

    output_messages: Optional[Iterable[TraceRootContentOutputMessage]]

    start: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    time: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    user_id: Optional[str]


class Content(TypedDict, total=False):
    id: str

    content_group_ids: Optional[List[str]]

    content_type: Optional[Literal["BASE", "TEST", "EXPERIMENT"]]

    end: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    input_detections: Optional[Iterable[ContentInputDetection]]

    input_messages: Optional[Iterable[ContentInputMessage]]

    metadata: Optional[object]

    output_detections: Optional[Iterable[ContentOutputDetection]]

    output_messages: Optional[Iterable[ContentOutputMessage]]

    start: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    time: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    user_id: Optional[str]


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

MonitoringLogParams: TypeAlias = Union[Span, Trace, Content]
