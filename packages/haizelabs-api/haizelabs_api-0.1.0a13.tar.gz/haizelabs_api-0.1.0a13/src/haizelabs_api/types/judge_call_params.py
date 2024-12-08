# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable, Optional
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "JudgeCallParams",
    "Content",
    "ContentContent",
    "ContentContentInputDetection",
    "ContentContentInputDetectionDetectorData",
    "ContentContentInputDetectionDetectorDataTextMatchingDetector",
    "ContentContentInputDetectionDetectorDataCategoryDetector",
    "ContentContentInputDetectionDetectorDataNaturalLanguageDetector",
    "ContentContentInputDetectionDetectorDataComparatorDetector",
    "ContentContentInputDetectionDetectorDataCustomDetector",
    "ContentContentInputMessage",
    "ContentContentInputMessageChatCompletionSystemMessageParam",
    "ContentContentInputMessageChatCompletionSystemMessageParamContentUnionMember1",
    "ContentContentInputMessageChatCompletionUserMessageParamInput",
    "ContentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1",
    "ContentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "ContentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam",
    "ContentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL",
    "ContentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam",
    "ContentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio",
    "ContentContentInputMessageChatCompletionAssistantMessageParamInput",
    "ContentContentInputMessageChatCompletionAssistantMessageParamInputAudio",
    "ContentContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1",
    "ContentContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "ContentContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam",
    "ContentContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall",
    "ContentContentInputMessageChatCompletionAssistantMessageParamInputToolCall",
    "ContentContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction",
    "ContentContentInputMessageChatCompletionToolMessageParam",
    "ContentContentInputMessageChatCompletionToolMessageParamContentUnionMember1",
    "ContentContentInputMessageChatCompletionFunctionMessageParam",
    "ContentContentOutputDetection",
    "ContentContentOutputDetectionDetectorData",
    "ContentContentOutputDetectionDetectorDataTextMatchingDetector",
    "ContentContentOutputDetectionDetectorDataCategoryDetector",
    "ContentContentOutputDetectionDetectorDataNaturalLanguageDetector",
    "ContentContentOutputDetectionDetectorDataComparatorDetector",
    "ContentContentOutputDetectionDetectorDataCustomDetector",
    "ContentContentOutputMessage",
    "ContentContentOutputMessageChatCompletionSystemMessageParam",
    "ContentContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1",
    "ContentContentOutputMessageChatCompletionUserMessageParamInput",
    "ContentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1",
    "ContentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "ContentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam",
    "ContentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL",
    "ContentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam",
    "ContentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio",
    "ContentContentOutputMessageChatCompletionAssistantMessageParamInput",
    "ContentContentOutputMessageChatCompletionAssistantMessageParamInputAudio",
    "ContentContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1",
    "ContentContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "ContentContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam",
    "ContentContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall",
    "ContentContentOutputMessageChatCompletionAssistantMessageParamInputToolCall",
    "ContentContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction",
    "ContentContentOutputMessageChatCompletionToolMessageParam",
    "ContentContentOutputMessageChatCompletionToolMessageParamContentUnionMember1",
    "ContentContentOutputMessageChatCompletionFunctionMessageParam",
    "ContentExperimentContent",
    "ContentExperimentContentBehavior",
    "ContentExperimentContentExpectedMessage",
    "ContentExperimentContentExpectedMessageChatCompletionSystemMessageParam",
    "ContentExperimentContentExpectedMessageChatCompletionSystemMessageParamContentUnionMember1",
    "ContentExperimentContentExpectedMessageChatCompletionUserMessageParamInput",
    "ContentExperimentContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1",
    "ContentExperimentContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "ContentExperimentContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam",
    "ContentExperimentContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL",
    "ContentExperimentContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam",
    "ContentExperimentContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio",
    "ContentExperimentContentExpectedMessageChatCompletionAssistantMessageParamInput",
    "ContentExperimentContentExpectedMessageChatCompletionAssistantMessageParamInputAudio",
    "ContentExperimentContentExpectedMessageChatCompletionAssistantMessageParamInputContentUnionMember1",
    "ContentExperimentContentExpectedMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "ContentExperimentContentExpectedMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam",
    "ContentExperimentContentExpectedMessageChatCompletionAssistantMessageParamInputFunctionCall",
    "ContentExperimentContentExpectedMessageChatCompletionAssistantMessageParamInputToolCall",
    "ContentExperimentContentExpectedMessageChatCompletionAssistantMessageParamInputToolCallFunction",
    "ContentExperimentContentExpectedMessageChatCompletionToolMessageParam",
    "ContentExperimentContentExpectedMessageChatCompletionToolMessageParamContentUnionMember1",
    "ContentExperimentContentExpectedMessageChatCompletionFunctionMessageParam",
    "ContentExperimentContentInputDetection",
    "ContentExperimentContentInputDetectionDetectorData",
    "ContentExperimentContentInputDetectionDetectorDataTextMatchingDetector",
    "ContentExperimentContentInputDetectionDetectorDataCategoryDetector",
    "ContentExperimentContentInputDetectionDetectorDataNaturalLanguageDetector",
    "ContentExperimentContentInputDetectionDetectorDataComparatorDetector",
    "ContentExperimentContentInputDetectionDetectorDataCustomDetector",
    "ContentExperimentContentInputMessage",
    "ContentExperimentContentInputMessageChatCompletionSystemMessageParam",
    "ContentExperimentContentInputMessageChatCompletionSystemMessageParamContentUnionMember1",
    "ContentExperimentContentInputMessageChatCompletionUserMessageParamInput",
    "ContentExperimentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1",
    "ContentExperimentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "ContentExperimentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam",
    "ContentExperimentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL",
    "ContentExperimentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam",
    "ContentExperimentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio",
    "ContentExperimentContentInputMessageChatCompletionAssistantMessageParamInput",
    "ContentExperimentContentInputMessageChatCompletionAssistantMessageParamInputAudio",
    "ContentExperimentContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1",
    "ContentExperimentContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "ContentExperimentContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam",
    "ContentExperimentContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall",
    "ContentExperimentContentInputMessageChatCompletionAssistantMessageParamInputToolCall",
    "ContentExperimentContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction",
    "ContentExperimentContentInputMessageChatCompletionToolMessageParam",
    "ContentExperimentContentInputMessageChatCompletionToolMessageParamContentUnionMember1",
    "ContentExperimentContentInputMessageChatCompletionFunctionMessageParam",
    "ContentExperimentContentOutputDetection",
    "ContentExperimentContentOutputDetectionDetectorData",
    "ContentExperimentContentOutputDetectionDetectorDataTextMatchingDetector",
    "ContentExperimentContentOutputDetectionDetectorDataCategoryDetector",
    "ContentExperimentContentOutputDetectionDetectorDataNaturalLanguageDetector",
    "ContentExperimentContentOutputDetectionDetectorDataComparatorDetector",
    "ContentExperimentContentOutputDetectionDetectorDataCustomDetector",
    "ContentExperimentContentOutputMessage",
    "ContentExperimentContentOutputMessageChatCompletionSystemMessageParam",
    "ContentExperimentContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1",
    "ContentExperimentContentOutputMessageChatCompletionUserMessageParamInput",
    "ContentExperimentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1",
    "ContentExperimentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "ContentExperimentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam",
    "ContentExperimentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL",
    "ContentExperimentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam",
    "ContentExperimentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio",
    "ContentExperimentContentOutputMessageChatCompletionAssistantMessageParamInput",
    "ContentExperimentContentOutputMessageChatCompletionAssistantMessageParamInputAudio",
    "ContentExperimentContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1",
    "ContentExperimentContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "ContentExperimentContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam",
    "ContentExperimentContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall",
    "ContentExperimentContentOutputMessageChatCompletionAssistantMessageParamInputToolCall",
    "ContentExperimentContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction",
    "ContentExperimentContentOutputMessageChatCompletionToolMessageParam",
    "ContentExperimentContentOutputMessageChatCompletionToolMessageParamContentUnionMember1",
    "ContentExperimentContentOutputMessageChatCompletionFunctionMessageParam",
    "ContentTestContentInput",
    "ContentTestContentInputBehavior",
    "ContentTestContentInputInputDetection",
    "ContentTestContentInputInputDetectionDetectorData",
    "ContentTestContentInputInputDetectionDetectorDataTextMatchingDetector",
    "ContentTestContentInputInputDetectionDetectorDataCategoryDetector",
    "ContentTestContentInputInputDetectionDetectorDataNaturalLanguageDetector",
    "ContentTestContentInputInputDetectionDetectorDataComparatorDetector",
    "ContentTestContentInputInputDetectionDetectorDataCustomDetector",
    "ContentTestContentInputInputMessage",
    "ContentTestContentInputInputMessageChatCompletionSystemMessageParam",
    "ContentTestContentInputInputMessageChatCompletionSystemMessageParamContentUnionMember1",
    "ContentTestContentInputInputMessageChatCompletionUserMessageParamInput",
    "ContentTestContentInputInputMessageChatCompletionUserMessageParamInputContentUnionMember1",
    "ContentTestContentInputInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "ContentTestContentInputInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam",
    "ContentTestContentInputInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL",
    "ContentTestContentInputInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam",
    "ContentTestContentInputInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio",
    "ContentTestContentInputInputMessageChatCompletionAssistantMessageParamInput",
    "ContentTestContentInputInputMessageChatCompletionAssistantMessageParamInputAudio",
    "ContentTestContentInputInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1",
    "ContentTestContentInputInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "ContentTestContentInputInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam",
    "ContentTestContentInputInputMessageChatCompletionAssistantMessageParamInputFunctionCall",
    "ContentTestContentInputInputMessageChatCompletionAssistantMessageParamInputToolCall",
    "ContentTestContentInputInputMessageChatCompletionAssistantMessageParamInputToolCallFunction",
    "ContentTestContentInputInputMessageChatCompletionToolMessageParam",
    "ContentTestContentInputInputMessageChatCompletionToolMessageParamContentUnionMember1",
    "ContentTestContentInputInputMessageChatCompletionFunctionMessageParam",
    "ContentTestContentInputOutputDetection",
    "ContentTestContentInputOutputDetectionDetectorData",
    "ContentTestContentInputOutputDetectionDetectorDataTextMatchingDetector",
    "ContentTestContentInputOutputDetectionDetectorDataCategoryDetector",
    "ContentTestContentInputOutputDetectionDetectorDataNaturalLanguageDetector",
    "ContentTestContentInputOutputDetectionDetectorDataComparatorDetector",
    "ContentTestContentInputOutputDetectionDetectorDataCustomDetector",
    "ContentTestContentInputOutputMessage",
    "ContentTestContentInputOutputMessageChatCompletionSystemMessageParam",
    "ContentTestContentInputOutputMessageChatCompletionSystemMessageParamContentUnionMember1",
    "ContentTestContentInputOutputMessageChatCompletionUserMessageParamInput",
    "ContentTestContentInputOutputMessageChatCompletionUserMessageParamInputContentUnionMember1",
    "ContentTestContentInputOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "ContentTestContentInputOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam",
    "ContentTestContentInputOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL",
    "ContentTestContentInputOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam",
    "ContentTestContentInputOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio",
    "ContentTestContentInputOutputMessageChatCompletionAssistantMessageParamInput",
    "ContentTestContentInputOutputMessageChatCompletionAssistantMessageParamInputAudio",
    "ContentTestContentInputOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1",
    "ContentTestContentInputOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "ContentTestContentInputOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam",
    "ContentTestContentInputOutputMessageChatCompletionAssistantMessageParamInputFunctionCall",
    "ContentTestContentInputOutputMessageChatCompletionAssistantMessageParamInputToolCall",
    "ContentTestContentInputOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction",
    "ContentTestContentInputOutputMessageChatCompletionToolMessageParam",
    "ContentTestContentInputOutputMessageChatCompletionToolMessageParamContentUnionMember1",
    "ContentTestContentInputOutputMessageChatCompletionFunctionMessageParam",
]


class JudgeCallParams(TypedDict, total=False):
    judge_ids: Required[List[str]]

    id: str

    behavior: Optional[str]

    content: Optional[Content]
    """A single piece of content in a test."""

    content_id: Optional[str]

    judge_input: bool

    user_id: Optional[str]


class ContentContentInputDetectionDetectorDataTextMatchingDetector(TypedDict, total=False):
    name: Required[str]

    regex: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["TEXT_MATCHING"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentContentInputDetectionDetectorDataCategoryDetector(TypedDict, total=False):
    category: Required[str]

    name: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CATEGORY"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentContentInputDetectionDetectorDataNaturalLanguageDetector(TypedDict, total=False):
    name: Required[str]

    natural_language_content: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["NATURAL_LANGUAGE"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentContentInputDetectionDetectorDataComparatorDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["EXACT_MATCH", "LANGUAGE_MODEL_SIMILARITY"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["COMPARATOR"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentContentInputDetectionDetectorDataCustomDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["TIERED_DETECTOR"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CUSTOM"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


ContentContentInputDetectionDetectorData: TypeAlias = Union[
    ContentContentInputDetectionDetectorDataTextMatchingDetector,
    ContentContentInputDetectionDetectorDataCategoryDetector,
    ContentContentInputDetectionDetectorDataNaturalLanguageDetector,
    ContentContentInputDetectionDetectorDataComparatorDetector,
    ContentContentInputDetectionDetectorDataCustomDetector,
]


class ContentContentInputDetection(TypedDict, total=False):
    content_id: Required[str]

    detected: Required[bool]

    detector_id: Required[str]

    end_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    score: Required[float]

    start_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    detector_data: Optional[ContentContentInputDetectionDetectorData]


class ContentContentInputMessageChatCompletionSystemMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentContentInputMessageChatCompletionSystemMessageParam(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[ContentContentInputMessageChatCompletionSystemMessageParamContentUnionMember1]]
    ]

    role: Required[Literal["system"]]

    name: str


class ContentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["auto", "low", "high"]


class ContentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam(
    TypedDict, total=False
):
    image_url: Required[
        ContentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL
    ]

    type: Required[Literal["image_url"]]


class ContentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio(
    TypedDict, total=False
):
    data: Required[str]

    format: Required[Literal["wav", "mp3"]]


class ContentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam(
    TypedDict, total=False
):
    input_audio: Required[
        ContentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio
    ]

    type: Required[Literal["input_audio"]]


ContentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1: TypeAlias = Union[
    ContentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    ContentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam,
    ContentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam,
]


class ContentContentInputMessageChatCompletionUserMessageParamInput(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[ContentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1]]
    ]

    role: Required[Literal["user"]]

    name: str


class ContentContentInputMessageChatCompletionAssistantMessageParamInputAudio(TypedDict, total=False):
    id: Required[str]


class ContentContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam(
    TypedDict, total=False
):
    refusal: Required[str]

    type: Required[Literal["refusal"]]


ContentContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1: TypeAlias = Union[
    ContentContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    ContentContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam,
]


class ContentContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall(TypedDict, total=False):
    arguments: Required[str]

    name: Required[str]


class ContentContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction(TypedDict, total=False):
    arguments: Required[str]

    name: Required[str]


class ContentContentInputMessageChatCompletionAssistantMessageParamInputToolCall(TypedDict, total=False):
    id: Required[str]

    function: Required[ContentContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction]

    type: Required[Literal["function"]]


class ContentContentInputMessageChatCompletionAssistantMessageParamInput(TypedDict, total=False):
    role: Required[Literal["assistant"]]

    audio: Optional[ContentContentInputMessageChatCompletionAssistantMessageParamInputAudio]

    content: Union[
        str, Iterable[ContentContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1], None
    ]

    function_call: Optional[ContentContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall]

    name: str

    refusal: Optional[str]

    tool_calls: Iterable[ContentContentInputMessageChatCompletionAssistantMessageParamInputToolCall]


class ContentContentInputMessageChatCompletionToolMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentContentInputMessageChatCompletionToolMessageParam(TypedDict, total=False):
    content: Required[Union[str, Iterable[ContentContentInputMessageChatCompletionToolMessageParamContentUnionMember1]]]

    role: Required[Literal["tool"]]

    tool_call_id: Required[str]


class ContentContentInputMessageChatCompletionFunctionMessageParam(TypedDict, total=False):
    content: Required[Optional[str]]

    name: Required[str]

    role: Required[Literal["function"]]


ContentContentInputMessage: TypeAlias = Union[
    ContentContentInputMessageChatCompletionSystemMessageParam,
    ContentContentInputMessageChatCompletionUserMessageParamInput,
    ContentContentInputMessageChatCompletionAssistantMessageParamInput,
    ContentContentInputMessageChatCompletionToolMessageParam,
    ContentContentInputMessageChatCompletionFunctionMessageParam,
]


class ContentContentOutputDetectionDetectorDataTextMatchingDetector(TypedDict, total=False):
    name: Required[str]

    regex: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["TEXT_MATCHING"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentContentOutputDetectionDetectorDataCategoryDetector(TypedDict, total=False):
    category: Required[str]

    name: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CATEGORY"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentContentOutputDetectionDetectorDataNaturalLanguageDetector(TypedDict, total=False):
    name: Required[str]

    natural_language_content: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["NATURAL_LANGUAGE"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentContentOutputDetectionDetectorDataComparatorDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["EXACT_MATCH", "LANGUAGE_MODEL_SIMILARITY"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["COMPARATOR"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentContentOutputDetectionDetectorDataCustomDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["TIERED_DETECTOR"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CUSTOM"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


ContentContentOutputDetectionDetectorData: TypeAlias = Union[
    ContentContentOutputDetectionDetectorDataTextMatchingDetector,
    ContentContentOutputDetectionDetectorDataCategoryDetector,
    ContentContentOutputDetectionDetectorDataNaturalLanguageDetector,
    ContentContentOutputDetectionDetectorDataComparatorDetector,
    ContentContentOutputDetectionDetectorDataCustomDetector,
]


class ContentContentOutputDetection(TypedDict, total=False):
    content_id: Required[str]

    detected: Required[bool]

    detector_id: Required[str]

    end_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    score: Required[float]

    start_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    detector_data: Optional[ContentContentOutputDetectionDetectorData]


class ContentContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentContentOutputMessageChatCompletionSystemMessageParam(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[ContentContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1]]
    ]

    role: Required[Literal["system"]]

    name: str


class ContentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["auto", "low", "high"]


class ContentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam(
    TypedDict, total=False
):
    image_url: Required[
        ContentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL
    ]

    type: Required[Literal["image_url"]]


class ContentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio(
    TypedDict, total=False
):
    data: Required[str]

    format: Required[Literal["wav", "mp3"]]


class ContentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam(
    TypedDict, total=False
):
    input_audio: Required[
        ContentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio
    ]

    type: Required[Literal["input_audio"]]


ContentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1: TypeAlias = Union[
    ContentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    ContentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam,
    ContentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam,
]


class ContentContentOutputMessageChatCompletionUserMessageParamInput(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[ContentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1]]
    ]

    role: Required[Literal["user"]]

    name: str


class ContentContentOutputMessageChatCompletionAssistantMessageParamInputAudio(TypedDict, total=False):
    id: Required[str]


class ContentContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam(
    TypedDict, total=False
):
    refusal: Required[str]

    type: Required[Literal["refusal"]]


ContentContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1: TypeAlias = Union[
    ContentContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    ContentContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam,
]


class ContentContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall(TypedDict, total=False):
    arguments: Required[str]

    name: Required[str]


class ContentContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction(TypedDict, total=False):
    arguments: Required[str]

    name: Required[str]


class ContentContentOutputMessageChatCompletionAssistantMessageParamInputToolCall(TypedDict, total=False):
    id: Required[str]

    function: Required[ContentContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction]

    type: Required[Literal["function"]]


class ContentContentOutputMessageChatCompletionAssistantMessageParamInput(TypedDict, total=False):
    role: Required[Literal["assistant"]]

    audio: Optional[ContentContentOutputMessageChatCompletionAssistantMessageParamInputAudio]

    content: Union[
        str, Iterable[ContentContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1], None
    ]

    function_call: Optional[ContentContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall]

    name: str

    refusal: Optional[str]

    tool_calls: Iterable[ContentContentOutputMessageChatCompletionAssistantMessageParamInputToolCall]


class ContentContentOutputMessageChatCompletionToolMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentContentOutputMessageChatCompletionToolMessageParam(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[ContentContentOutputMessageChatCompletionToolMessageParamContentUnionMember1]]
    ]

    role: Required[Literal["tool"]]

    tool_call_id: Required[str]


class ContentContentOutputMessageChatCompletionFunctionMessageParam(TypedDict, total=False):
    content: Required[Optional[str]]

    name: Required[str]

    role: Required[Literal["function"]]


ContentContentOutputMessage: TypeAlias = Union[
    ContentContentOutputMessageChatCompletionSystemMessageParam,
    ContentContentOutputMessageChatCompletionUserMessageParamInput,
    ContentContentOutputMessageChatCompletionAssistantMessageParamInput,
    ContentContentOutputMessageChatCompletionToolMessageParam,
    ContentContentOutputMessageChatCompletionFunctionMessageParam,
]


class ContentContent(TypedDict, total=False):
    id: str

    content_group_ids: Optional[List[str]]

    content_type: Optional[Literal["BASE", "TEST", "EXPERIMENT"]]

    end: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    input_detections: Optional[Iterable[ContentContentInputDetection]]

    input_messages: Optional[Iterable[ContentContentInputMessage]]

    metadata: Optional[object]

    output_detections: Optional[Iterable[ContentContentOutputDetection]]

    output_messages: Optional[Iterable[ContentContentOutputMessage]]

    start: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    time: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    user_id: Optional[str]


class ContentExperimentContentBehavior(TypedDict, total=False):
    description: Required[str]


class ContentExperimentContentExpectedMessageChatCompletionSystemMessageParamContentUnionMember1(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentExperimentContentExpectedMessageChatCompletionSystemMessageParam(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[ContentExperimentContentExpectedMessageChatCompletionSystemMessageParamContentUnionMember1]]
    ]

    role: Required[Literal["system"]]

    name: str


class ContentExperimentContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentExperimentContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["auto", "low", "high"]


class ContentExperimentContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam(
    TypedDict, total=False
):
    image_url: Required[
        ContentExperimentContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL
    ]

    type: Required[Literal["image_url"]]


class ContentExperimentContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio(
    TypedDict, total=False
):
    data: Required[str]

    format: Required[Literal["wav", "mp3"]]


class ContentExperimentContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam(
    TypedDict, total=False
):
    input_audio: Required[
        ContentExperimentContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio
    ]

    type: Required[Literal["input_audio"]]


ContentExperimentContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1: TypeAlias = Union[
    ContentExperimentContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    ContentExperimentContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam,
    ContentExperimentContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam,
]


class ContentExperimentContentExpectedMessageChatCompletionUserMessageParamInput(TypedDict, total=False):
    content: Required[
        Union[
            str, Iterable[ContentExperimentContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1]
        ]
    ]

    role: Required[Literal["user"]]

    name: str


class ContentExperimentContentExpectedMessageChatCompletionAssistantMessageParamInputAudio(TypedDict, total=False):
    id: Required[str]


class ContentExperimentContentExpectedMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentExperimentContentExpectedMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam(
    TypedDict, total=False
):
    refusal: Required[str]

    type: Required[Literal["refusal"]]


ContentExperimentContentExpectedMessageChatCompletionAssistantMessageParamInputContentUnionMember1: TypeAlias = Union[
    ContentExperimentContentExpectedMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    ContentExperimentContentExpectedMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam,
]


class ContentExperimentContentExpectedMessageChatCompletionAssistantMessageParamInputFunctionCall(
    TypedDict, total=False
):
    arguments: Required[str]

    name: Required[str]


class ContentExperimentContentExpectedMessageChatCompletionAssistantMessageParamInputToolCallFunction(
    TypedDict, total=False
):
    arguments: Required[str]

    name: Required[str]


class ContentExperimentContentExpectedMessageChatCompletionAssistantMessageParamInputToolCall(TypedDict, total=False):
    id: Required[str]

    function: Required[ContentExperimentContentExpectedMessageChatCompletionAssistantMessageParamInputToolCallFunction]

    type: Required[Literal["function"]]


class ContentExperimentContentExpectedMessageChatCompletionAssistantMessageParamInput(TypedDict, total=False):
    role: Required[Literal["assistant"]]

    audio: Optional[ContentExperimentContentExpectedMessageChatCompletionAssistantMessageParamInputAudio]

    content: Union[
        str,
        Iterable[ContentExperimentContentExpectedMessageChatCompletionAssistantMessageParamInputContentUnionMember1],
        None,
    ]

    function_call: Optional[ContentExperimentContentExpectedMessageChatCompletionAssistantMessageParamInputFunctionCall]

    name: str

    refusal: Optional[str]

    tool_calls: Iterable[ContentExperimentContentExpectedMessageChatCompletionAssistantMessageParamInputToolCall]


class ContentExperimentContentExpectedMessageChatCompletionToolMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentExperimentContentExpectedMessageChatCompletionToolMessageParam(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[ContentExperimentContentExpectedMessageChatCompletionToolMessageParamContentUnionMember1]]
    ]

    role: Required[Literal["tool"]]

    tool_call_id: Required[str]


class ContentExperimentContentExpectedMessageChatCompletionFunctionMessageParam(TypedDict, total=False):
    content: Required[Optional[str]]

    name: Required[str]

    role: Required[Literal["function"]]


ContentExperimentContentExpectedMessage: TypeAlias = Union[
    ContentExperimentContentExpectedMessageChatCompletionSystemMessageParam,
    ContentExperimentContentExpectedMessageChatCompletionUserMessageParamInput,
    ContentExperimentContentExpectedMessageChatCompletionAssistantMessageParamInput,
    ContentExperimentContentExpectedMessageChatCompletionToolMessageParam,
    ContentExperimentContentExpectedMessageChatCompletionFunctionMessageParam,
]


class ContentExperimentContentInputDetectionDetectorDataTextMatchingDetector(TypedDict, total=False):
    name: Required[str]

    regex: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["TEXT_MATCHING"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentExperimentContentInputDetectionDetectorDataCategoryDetector(TypedDict, total=False):
    category: Required[str]

    name: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CATEGORY"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentExperimentContentInputDetectionDetectorDataNaturalLanguageDetector(TypedDict, total=False):
    name: Required[str]

    natural_language_content: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["NATURAL_LANGUAGE"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentExperimentContentInputDetectionDetectorDataComparatorDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["EXACT_MATCH", "LANGUAGE_MODEL_SIMILARITY"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["COMPARATOR"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentExperimentContentInputDetectionDetectorDataCustomDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["TIERED_DETECTOR"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CUSTOM"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


ContentExperimentContentInputDetectionDetectorData: TypeAlias = Union[
    ContentExperimentContentInputDetectionDetectorDataTextMatchingDetector,
    ContentExperimentContentInputDetectionDetectorDataCategoryDetector,
    ContentExperimentContentInputDetectionDetectorDataNaturalLanguageDetector,
    ContentExperimentContentInputDetectionDetectorDataComparatorDetector,
    ContentExperimentContentInputDetectionDetectorDataCustomDetector,
]


class ContentExperimentContentInputDetection(TypedDict, total=False):
    content_id: Required[str]

    detected: Required[bool]

    detector_id: Required[str]

    end_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    score: Required[float]

    start_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    detector_data: Optional[ContentExperimentContentInputDetectionDetectorData]


class ContentExperimentContentInputMessageChatCompletionSystemMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentExperimentContentInputMessageChatCompletionSystemMessageParam(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[ContentExperimentContentInputMessageChatCompletionSystemMessageParamContentUnionMember1]]
    ]

    role: Required[Literal["system"]]

    name: str


class ContentExperimentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentExperimentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["auto", "low", "high"]


class ContentExperimentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam(
    TypedDict, total=False
):
    image_url: Required[
        ContentExperimentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL
    ]

    type: Required[Literal["image_url"]]


class ContentExperimentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio(
    TypedDict, total=False
):
    data: Required[str]

    format: Required[Literal["wav", "mp3"]]


class ContentExperimentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam(
    TypedDict, total=False
):
    input_audio: Required[
        ContentExperimentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio
    ]

    type: Required[Literal["input_audio"]]


ContentExperimentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1: TypeAlias = Union[
    ContentExperimentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    ContentExperimentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam,
    ContentExperimentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam,
]


class ContentExperimentContentInputMessageChatCompletionUserMessageParamInput(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[ContentExperimentContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1]]
    ]

    role: Required[Literal["user"]]

    name: str


class ContentExperimentContentInputMessageChatCompletionAssistantMessageParamInputAudio(TypedDict, total=False):
    id: Required[str]


class ContentExperimentContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentExperimentContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam(
    TypedDict, total=False
):
    refusal: Required[str]

    type: Required[Literal["refusal"]]


ContentExperimentContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1: TypeAlias = Union[
    ContentExperimentContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    ContentExperimentContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam,
]


class ContentExperimentContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall(TypedDict, total=False):
    arguments: Required[str]

    name: Required[str]


class ContentExperimentContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction(
    TypedDict, total=False
):
    arguments: Required[str]

    name: Required[str]


class ContentExperimentContentInputMessageChatCompletionAssistantMessageParamInputToolCall(TypedDict, total=False):
    id: Required[str]

    function: Required[ContentExperimentContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction]

    type: Required[Literal["function"]]


class ContentExperimentContentInputMessageChatCompletionAssistantMessageParamInput(TypedDict, total=False):
    role: Required[Literal["assistant"]]

    audio: Optional[ContentExperimentContentInputMessageChatCompletionAssistantMessageParamInputAudio]

    content: Union[
        str,
        Iterable[ContentExperimentContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1],
        None,
    ]

    function_call: Optional[ContentExperimentContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall]

    name: str

    refusal: Optional[str]

    tool_calls: Iterable[ContentExperimentContentInputMessageChatCompletionAssistantMessageParamInputToolCall]


class ContentExperimentContentInputMessageChatCompletionToolMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentExperimentContentInputMessageChatCompletionToolMessageParam(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[ContentExperimentContentInputMessageChatCompletionToolMessageParamContentUnionMember1]]
    ]

    role: Required[Literal["tool"]]

    tool_call_id: Required[str]


class ContentExperimentContentInputMessageChatCompletionFunctionMessageParam(TypedDict, total=False):
    content: Required[Optional[str]]

    name: Required[str]

    role: Required[Literal["function"]]


ContentExperimentContentInputMessage: TypeAlias = Union[
    ContentExperimentContentInputMessageChatCompletionSystemMessageParam,
    ContentExperimentContentInputMessageChatCompletionUserMessageParamInput,
    ContentExperimentContentInputMessageChatCompletionAssistantMessageParamInput,
    ContentExperimentContentInputMessageChatCompletionToolMessageParam,
    ContentExperimentContentInputMessageChatCompletionFunctionMessageParam,
]


class ContentExperimentContentOutputDetectionDetectorDataTextMatchingDetector(TypedDict, total=False):
    name: Required[str]

    regex: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["TEXT_MATCHING"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentExperimentContentOutputDetectionDetectorDataCategoryDetector(TypedDict, total=False):
    category: Required[str]

    name: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CATEGORY"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentExperimentContentOutputDetectionDetectorDataNaturalLanguageDetector(TypedDict, total=False):
    name: Required[str]

    natural_language_content: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["NATURAL_LANGUAGE"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentExperimentContentOutputDetectionDetectorDataComparatorDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["EXACT_MATCH", "LANGUAGE_MODEL_SIMILARITY"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["COMPARATOR"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentExperimentContentOutputDetectionDetectorDataCustomDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["TIERED_DETECTOR"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CUSTOM"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


ContentExperimentContentOutputDetectionDetectorData: TypeAlias = Union[
    ContentExperimentContentOutputDetectionDetectorDataTextMatchingDetector,
    ContentExperimentContentOutputDetectionDetectorDataCategoryDetector,
    ContentExperimentContentOutputDetectionDetectorDataNaturalLanguageDetector,
    ContentExperimentContentOutputDetectionDetectorDataComparatorDetector,
    ContentExperimentContentOutputDetectionDetectorDataCustomDetector,
]


class ContentExperimentContentOutputDetection(TypedDict, total=False):
    content_id: Required[str]

    detected: Required[bool]

    detector_id: Required[str]

    end_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    score: Required[float]

    start_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    detector_data: Optional[ContentExperimentContentOutputDetectionDetectorData]


class ContentExperimentContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentExperimentContentOutputMessageChatCompletionSystemMessageParam(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[ContentExperimentContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1]]
    ]

    role: Required[Literal["system"]]

    name: str


class ContentExperimentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentExperimentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["auto", "low", "high"]


class ContentExperimentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam(
    TypedDict, total=False
):
    image_url: Required[
        ContentExperimentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL
    ]

    type: Required[Literal["image_url"]]


class ContentExperimentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio(
    TypedDict, total=False
):
    data: Required[str]

    format: Required[Literal["wav", "mp3"]]


class ContentExperimentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam(
    TypedDict, total=False
):
    input_audio: Required[
        ContentExperimentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio
    ]

    type: Required[Literal["input_audio"]]


ContentExperimentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1: TypeAlias = Union[
    ContentExperimentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    ContentExperimentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam,
    ContentExperimentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam,
]


class ContentExperimentContentOutputMessageChatCompletionUserMessageParamInput(TypedDict, total=False):
    content: Required[
        Union[
            str, Iterable[ContentExperimentContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1]
        ]
    ]

    role: Required[Literal["user"]]

    name: str


class ContentExperimentContentOutputMessageChatCompletionAssistantMessageParamInputAudio(TypedDict, total=False):
    id: Required[str]


class ContentExperimentContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentExperimentContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam(
    TypedDict, total=False
):
    refusal: Required[str]

    type: Required[Literal["refusal"]]


ContentExperimentContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1: TypeAlias = Union[
    ContentExperimentContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    ContentExperimentContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam,
]


class ContentExperimentContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall(TypedDict, total=False):
    arguments: Required[str]

    name: Required[str]


class ContentExperimentContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction(
    TypedDict, total=False
):
    arguments: Required[str]

    name: Required[str]


class ContentExperimentContentOutputMessageChatCompletionAssistantMessageParamInputToolCall(TypedDict, total=False):
    id: Required[str]

    function: Required[ContentExperimentContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction]

    type: Required[Literal["function"]]


class ContentExperimentContentOutputMessageChatCompletionAssistantMessageParamInput(TypedDict, total=False):
    role: Required[Literal["assistant"]]

    audio: Optional[ContentExperimentContentOutputMessageChatCompletionAssistantMessageParamInputAudio]

    content: Union[
        str,
        Iterable[ContentExperimentContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1],
        None,
    ]

    function_call: Optional[ContentExperimentContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall]

    name: str

    refusal: Optional[str]

    tool_calls: Iterable[ContentExperimentContentOutputMessageChatCompletionAssistantMessageParamInputToolCall]


class ContentExperimentContentOutputMessageChatCompletionToolMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentExperimentContentOutputMessageChatCompletionToolMessageParam(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[ContentExperimentContentOutputMessageChatCompletionToolMessageParamContentUnionMember1]]
    ]

    role: Required[Literal["tool"]]

    tool_call_id: Required[str]


class ContentExperimentContentOutputMessageChatCompletionFunctionMessageParam(TypedDict, total=False):
    content: Required[Optional[str]]

    name: Required[str]

    role: Required[Literal["function"]]


ContentExperimentContentOutputMessage: TypeAlias = Union[
    ContentExperimentContentOutputMessageChatCompletionSystemMessageParam,
    ContentExperimentContentOutputMessageChatCompletionUserMessageParamInput,
    ContentExperimentContentOutputMessageChatCompletionAssistantMessageParamInput,
    ContentExperimentContentOutputMessageChatCompletionToolMessageParam,
    ContentExperimentContentOutputMessageChatCompletionFunctionMessageParam,
]


class ContentExperimentContent(TypedDict, total=False):
    id: str

    algorithm: Optional[str]

    behavior: Optional[ContentExperimentContentBehavior]

    content_group_ids: Optional[List[str]]

    content_type: Optional[Literal["BASE", "TEST", "EXPERIMENT"]]

    end: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    expected_messages: Optional[Iterable[ContentExperimentContentExpectedMessage]]

    generate_end_time: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    generate_start_time: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    input_detections: Optional[Iterable[ContentExperimentContentInputDetection]]

    input_messages: Optional[Iterable[ContentExperimentContentInputMessage]]

    metadata: Optional[object]

    output_detections: Optional[Iterable[ContentExperimentContentOutputDetection]]

    output_messages: Optional[Iterable[ContentExperimentContentOutputMessage]]

    start: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    status: Optional[Literal["GENERATING_CONTENT", "AWAITING_RESPONSE", "ANALYZING_RESPONSE", "COMPLETE", "DISCARDED"]]
    """Status for a single content object in a test."""

    test_id: Optional[str]

    time: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    user_id: Optional[str]


class ContentTestContentInputBehavior(TypedDict, total=False):
    description: Required[str]


class ContentTestContentInputInputDetectionDetectorDataTextMatchingDetector(TypedDict, total=False):
    name: Required[str]

    regex: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["TEXT_MATCHING"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentTestContentInputInputDetectionDetectorDataCategoryDetector(TypedDict, total=False):
    category: Required[str]

    name: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CATEGORY"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentTestContentInputInputDetectionDetectorDataNaturalLanguageDetector(TypedDict, total=False):
    name: Required[str]

    natural_language_content: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["NATURAL_LANGUAGE"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentTestContentInputInputDetectionDetectorDataComparatorDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["EXACT_MATCH", "LANGUAGE_MODEL_SIMILARITY"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["COMPARATOR"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentTestContentInputInputDetectionDetectorDataCustomDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["TIERED_DETECTOR"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CUSTOM"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


ContentTestContentInputInputDetectionDetectorData: TypeAlias = Union[
    ContentTestContentInputInputDetectionDetectorDataTextMatchingDetector,
    ContentTestContentInputInputDetectionDetectorDataCategoryDetector,
    ContentTestContentInputInputDetectionDetectorDataNaturalLanguageDetector,
    ContentTestContentInputInputDetectionDetectorDataComparatorDetector,
    ContentTestContentInputInputDetectionDetectorDataCustomDetector,
]


class ContentTestContentInputInputDetection(TypedDict, total=False):
    content_id: Required[str]

    detected: Required[bool]

    detector_id: Required[str]

    end_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    score: Required[float]

    start_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    detector_data: Optional[ContentTestContentInputInputDetectionDetectorData]


class ContentTestContentInputInputMessageChatCompletionSystemMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentTestContentInputInputMessageChatCompletionSystemMessageParam(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[ContentTestContentInputInputMessageChatCompletionSystemMessageParamContentUnionMember1]]
    ]

    role: Required[Literal["system"]]

    name: str


class ContentTestContentInputInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentTestContentInputInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["auto", "low", "high"]


class ContentTestContentInputInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam(
    TypedDict, total=False
):
    image_url: Required[
        ContentTestContentInputInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL
    ]

    type: Required[Literal["image_url"]]


class ContentTestContentInputInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio(
    TypedDict, total=False
):
    data: Required[str]

    format: Required[Literal["wav", "mp3"]]


class ContentTestContentInputInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam(
    TypedDict, total=False
):
    input_audio: Required[
        ContentTestContentInputInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio
    ]

    type: Required[Literal["input_audio"]]


ContentTestContentInputInputMessageChatCompletionUserMessageParamInputContentUnionMember1: TypeAlias = Union[
    ContentTestContentInputInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    ContentTestContentInputInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam,
    ContentTestContentInputInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam,
]


class ContentTestContentInputInputMessageChatCompletionUserMessageParamInput(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[ContentTestContentInputInputMessageChatCompletionUserMessageParamInputContentUnionMember1]]
    ]

    role: Required[Literal["user"]]

    name: str


class ContentTestContentInputInputMessageChatCompletionAssistantMessageParamInputAudio(TypedDict, total=False):
    id: Required[str]


class ContentTestContentInputInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentTestContentInputInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam(
    TypedDict, total=False
):
    refusal: Required[str]

    type: Required[Literal["refusal"]]


ContentTestContentInputInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1: TypeAlias = Union[
    ContentTestContentInputInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    ContentTestContentInputInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam,
]


class ContentTestContentInputInputMessageChatCompletionAssistantMessageParamInputFunctionCall(TypedDict, total=False):
    arguments: Required[str]

    name: Required[str]


class ContentTestContentInputInputMessageChatCompletionAssistantMessageParamInputToolCallFunction(
    TypedDict, total=False
):
    arguments: Required[str]

    name: Required[str]


class ContentTestContentInputInputMessageChatCompletionAssistantMessageParamInputToolCall(TypedDict, total=False):
    id: Required[str]

    function: Required[ContentTestContentInputInputMessageChatCompletionAssistantMessageParamInputToolCallFunction]

    type: Required[Literal["function"]]


class ContentTestContentInputInputMessageChatCompletionAssistantMessageParamInput(TypedDict, total=False):
    role: Required[Literal["assistant"]]

    audio: Optional[ContentTestContentInputInputMessageChatCompletionAssistantMessageParamInputAudio]

    content: Union[
        str,
        Iterable[ContentTestContentInputInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1],
        None,
    ]

    function_call: Optional[ContentTestContentInputInputMessageChatCompletionAssistantMessageParamInputFunctionCall]

    name: str

    refusal: Optional[str]

    tool_calls: Iterable[ContentTestContentInputInputMessageChatCompletionAssistantMessageParamInputToolCall]


class ContentTestContentInputInputMessageChatCompletionToolMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentTestContentInputInputMessageChatCompletionToolMessageParam(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[ContentTestContentInputInputMessageChatCompletionToolMessageParamContentUnionMember1]]
    ]

    role: Required[Literal["tool"]]

    tool_call_id: Required[str]


class ContentTestContentInputInputMessageChatCompletionFunctionMessageParam(TypedDict, total=False):
    content: Required[Optional[str]]

    name: Required[str]

    role: Required[Literal["function"]]


ContentTestContentInputInputMessage: TypeAlias = Union[
    ContentTestContentInputInputMessageChatCompletionSystemMessageParam,
    ContentTestContentInputInputMessageChatCompletionUserMessageParamInput,
    ContentTestContentInputInputMessageChatCompletionAssistantMessageParamInput,
    ContentTestContentInputInputMessageChatCompletionToolMessageParam,
    ContentTestContentInputInputMessageChatCompletionFunctionMessageParam,
]


class ContentTestContentInputOutputDetectionDetectorDataTextMatchingDetector(TypedDict, total=False):
    name: Required[str]

    regex: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["TEXT_MATCHING"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentTestContentInputOutputDetectionDetectorDataCategoryDetector(TypedDict, total=False):
    category: Required[str]

    name: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CATEGORY"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentTestContentInputOutputDetectionDetectorDataNaturalLanguageDetector(TypedDict, total=False):
    name: Required[str]

    natural_language_content: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["NATURAL_LANGUAGE"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentTestContentInputOutputDetectionDetectorDataComparatorDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["EXACT_MATCH", "LANGUAGE_MODEL_SIMILARITY"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["COMPARATOR"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class ContentTestContentInputOutputDetectionDetectorDataCustomDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["TIERED_DETECTOR"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CUSTOM"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


ContentTestContentInputOutputDetectionDetectorData: TypeAlias = Union[
    ContentTestContentInputOutputDetectionDetectorDataTextMatchingDetector,
    ContentTestContentInputOutputDetectionDetectorDataCategoryDetector,
    ContentTestContentInputOutputDetectionDetectorDataNaturalLanguageDetector,
    ContentTestContentInputOutputDetectionDetectorDataComparatorDetector,
    ContentTestContentInputOutputDetectionDetectorDataCustomDetector,
]


class ContentTestContentInputOutputDetection(TypedDict, total=False):
    content_id: Required[str]

    detected: Required[bool]

    detector_id: Required[str]

    end_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    score: Required[float]

    start_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    detector_data: Optional[ContentTestContentInputOutputDetectionDetectorData]


class ContentTestContentInputOutputMessageChatCompletionSystemMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentTestContentInputOutputMessageChatCompletionSystemMessageParam(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[ContentTestContentInputOutputMessageChatCompletionSystemMessageParamContentUnionMember1]]
    ]

    role: Required[Literal["system"]]

    name: str


class ContentTestContentInputOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentTestContentInputOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["auto", "low", "high"]


class ContentTestContentInputOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam(
    TypedDict, total=False
):
    image_url: Required[
        ContentTestContentInputOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL
    ]

    type: Required[Literal["image_url"]]


class ContentTestContentInputOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio(
    TypedDict, total=False
):
    data: Required[str]

    format: Required[Literal["wav", "mp3"]]


class ContentTestContentInputOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam(
    TypedDict, total=False
):
    input_audio: Required[
        ContentTestContentInputOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio
    ]

    type: Required[Literal["input_audio"]]


ContentTestContentInputOutputMessageChatCompletionUserMessageParamInputContentUnionMember1: TypeAlias = Union[
    ContentTestContentInputOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    ContentTestContentInputOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam,
    ContentTestContentInputOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam,
]


class ContentTestContentInputOutputMessageChatCompletionUserMessageParamInput(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[ContentTestContentInputOutputMessageChatCompletionUserMessageParamInputContentUnionMember1]]
    ]

    role: Required[Literal["user"]]

    name: str


class ContentTestContentInputOutputMessageChatCompletionAssistantMessageParamInputAudio(TypedDict, total=False):
    id: Required[str]


class ContentTestContentInputOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentTestContentInputOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam(
    TypedDict, total=False
):
    refusal: Required[str]

    type: Required[Literal["refusal"]]


ContentTestContentInputOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1: TypeAlias = Union[
    ContentTestContentInputOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    ContentTestContentInputOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam,
]


class ContentTestContentInputOutputMessageChatCompletionAssistantMessageParamInputFunctionCall(TypedDict, total=False):
    arguments: Required[str]

    name: Required[str]


class ContentTestContentInputOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction(
    TypedDict, total=False
):
    arguments: Required[str]

    name: Required[str]


class ContentTestContentInputOutputMessageChatCompletionAssistantMessageParamInputToolCall(TypedDict, total=False):
    id: Required[str]

    function: Required[ContentTestContentInputOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction]

    type: Required[Literal["function"]]


class ContentTestContentInputOutputMessageChatCompletionAssistantMessageParamInput(TypedDict, total=False):
    role: Required[Literal["assistant"]]

    audio: Optional[ContentTestContentInputOutputMessageChatCompletionAssistantMessageParamInputAudio]

    content: Union[
        str,
        Iterable[ContentTestContentInputOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1],
        None,
    ]

    function_call: Optional[ContentTestContentInputOutputMessageChatCompletionAssistantMessageParamInputFunctionCall]

    name: str

    refusal: Optional[str]

    tool_calls: Iterable[ContentTestContentInputOutputMessageChatCompletionAssistantMessageParamInputToolCall]


class ContentTestContentInputOutputMessageChatCompletionToolMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class ContentTestContentInputOutputMessageChatCompletionToolMessageParam(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[ContentTestContentInputOutputMessageChatCompletionToolMessageParamContentUnionMember1]]
    ]

    role: Required[Literal["tool"]]

    tool_call_id: Required[str]


class ContentTestContentInputOutputMessageChatCompletionFunctionMessageParam(TypedDict, total=False):
    content: Required[Optional[str]]

    name: Required[str]

    role: Required[Literal["function"]]


ContentTestContentInputOutputMessage: TypeAlias = Union[
    ContentTestContentInputOutputMessageChatCompletionSystemMessageParam,
    ContentTestContentInputOutputMessageChatCompletionUserMessageParamInput,
    ContentTestContentInputOutputMessageChatCompletionAssistantMessageParamInput,
    ContentTestContentInputOutputMessageChatCompletionToolMessageParam,
    ContentTestContentInputOutputMessageChatCompletionFunctionMessageParam,
]


class ContentTestContentInput(TypedDict, total=False):
    id: str

    algorithm: Optional[str]

    behavior: Optional[ContentTestContentInputBehavior]

    content_group_ids: Optional[List[str]]

    content_type: Optional[Literal["BASE", "TEST", "EXPERIMENT"]]

    end: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    generate_end_time: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    generate_start_time: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    input_detections: Optional[Iterable[ContentTestContentInputInputDetection]]

    input_messages: Optional[Iterable[ContentTestContentInputInputMessage]]

    metadata: Optional[object]

    output_detections: Optional[Iterable[ContentTestContentInputOutputDetection]]

    output_messages: Optional[Iterable[ContentTestContentInputOutputMessage]]

    start: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    status: Optional[Literal["GENERATING_CONTENT", "AWAITING_RESPONSE", "ANALYZING_RESPONSE", "COMPLETE", "DISCARDED"]]
    """Status for a single content object in a test."""

    test_id: Optional[str]

    time: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    user_id: Optional[str]


Content: TypeAlias = Union[ContentContent, ContentExperimentContent, ContentTestContentInput]
