# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable, Optional
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "TestingStartParams",
    "TestData",
    "TestDataRedTeamingTest",
    "TestDataRedTeamingTestAlgorithmStatus",
    "TestDataRedTeamingTestBehavior",
    "TestDataRedTeamingTestContent",
    "TestDataRedTeamingTestContentBehavior",
    "TestDataRedTeamingTestContentInputDetection",
    "TestDataRedTeamingTestContentInputDetectionDetectorData",
    "TestDataRedTeamingTestContentInputDetectionDetectorDataTextMatchingDetector",
    "TestDataRedTeamingTestContentInputDetectionDetectorDataCategoryDetector",
    "TestDataRedTeamingTestContentInputDetectionDetectorDataNaturalLanguageDetector",
    "TestDataRedTeamingTestContentInputDetectionDetectorDataComparatorDetector",
    "TestDataRedTeamingTestContentInputDetectionDetectorDataCustomDetector",
    "TestDataRedTeamingTestContentInputMessage",
    "TestDataRedTeamingTestContentInputMessageChatCompletionSystemMessageParam",
    "TestDataRedTeamingTestContentInputMessageChatCompletionSystemMessageParamContentUnionMember1",
    "TestDataRedTeamingTestContentInputMessageChatCompletionUserMessageParamInput",
    "TestDataRedTeamingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1",
    "TestDataRedTeamingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "TestDataRedTeamingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam",
    "TestDataRedTeamingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL",
    "TestDataRedTeamingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam",
    "TestDataRedTeamingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio",
    "TestDataRedTeamingTestContentInputMessageChatCompletionAssistantMessageParamInput",
    "TestDataRedTeamingTestContentInputMessageChatCompletionAssistantMessageParamInputAudio",
    "TestDataRedTeamingTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1",
    "TestDataRedTeamingTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "TestDataRedTeamingTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam",
    "TestDataRedTeamingTestContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall",
    "TestDataRedTeamingTestContentInputMessageChatCompletionAssistantMessageParamInputToolCall",
    "TestDataRedTeamingTestContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction",
    "TestDataRedTeamingTestContentInputMessageChatCompletionToolMessageParam",
    "TestDataRedTeamingTestContentInputMessageChatCompletionToolMessageParamContentUnionMember1",
    "TestDataRedTeamingTestContentInputMessageChatCompletionFunctionMessageParam",
    "TestDataRedTeamingTestContentOutputDetection",
    "TestDataRedTeamingTestContentOutputDetectionDetectorData",
    "TestDataRedTeamingTestContentOutputDetectionDetectorDataTextMatchingDetector",
    "TestDataRedTeamingTestContentOutputDetectionDetectorDataCategoryDetector",
    "TestDataRedTeamingTestContentOutputDetectionDetectorDataNaturalLanguageDetector",
    "TestDataRedTeamingTestContentOutputDetectionDetectorDataComparatorDetector",
    "TestDataRedTeamingTestContentOutputDetectionDetectorDataCustomDetector",
    "TestDataRedTeamingTestContentOutputMessage",
    "TestDataRedTeamingTestContentOutputMessageChatCompletionSystemMessageParam",
    "TestDataRedTeamingTestContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1",
    "TestDataRedTeamingTestContentOutputMessageChatCompletionUserMessageParamInput",
    "TestDataRedTeamingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1",
    "TestDataRedTeamingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "TestDataRedTeamingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam",
    "TestDataRedTeamingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL",
    "TestDataRedTeamingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam",
    "TestDataRedTeamingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio",
    "TestDataRedTeamingTestContentOutputMessageChatCompletionAssistantMessageParamInput",
    "TestDataRedTeamingTestContentOutputMessageChatCompletionAssistantMessageParamInputAudio",
    "TestDataRedTeamingTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1",
    "TestDataRedTeamingTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "TestDataRedTeamingTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam",
    "TestDataRedTeamingTestContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall",
    "TestDataRedTeamingTestContentOutputMessageChatCompletionAssistantMessageParamInputToolCall",
    "TestDataRedTeamingTestContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction",
    "TestDataRedTeamingTestContentOutputMessageChatCompletionToolMessageParam",
    "TestDataRedTeamingTestContentOutputMessageChatCompletionToolMessageParamContentUnionMember1",
    "TestDataRedTeamingTestContentOutputMessageChatCompletionFunctionMessageParam",
    "TestDataRedTeamingTestTargetModel",
    "TestDataRedTeamingTestTargetModelGenerationParams",
    "TestDataFuzzingTest",
    "TestDataFuzzingTestAlgorithmStatus",
    "TestDataFuzzingTestBehavior",
    "TestDataFuzzingTestContent",
    "TestDataFuzzingTestContentBehavior",
    "TestDataFuzzingTestContentInputDetection",
    "TestDataFuzzingTestContentInputDetectionDetectorData",
    "TestDataFuzzingTestContentInputDetectionDetectorDataTextMatchingDetector",
    "TestDataFuzzingTestContentInputDetectionDetectorDataCategoryDetector",
    "TestDataFuzzingTestContentInputDetectionDetectorDataNaturalLanguageDetector",
    "TestDataFuzzingTestContentInputDetectionDetectorDataComparatorDetector",
    "TestDataFuzzingTestContentInputDetectionDetectorDataCustomDetector",
    "TestDataFuzzingTestContentInputMessage",
    "TestDataFuzzingTestContentInputMessageChatCompletionSystemMessageParam",
    "TestDataFuzzingTestContentInputMessageChatCompletionSystemMessageParamContentUnionMember1",
    "TestDataFuzzingTestContentInputMessageChatCompletionUserMessageParamInput",
    "TestDataFuzzingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1",
    "TestDataFuzzingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "TestDataFuzzingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam",
    "TestDataFuzzingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL",
    "TestDataFuzzingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam",
    "TestDataFuzzingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio",
    "TestDataFuzzingTestContentInputMessageChatCompletionAssistantMessageParamInput",
    "TestDataFuzzingTestContentInputMessageChatCompletionAssistantMessageParamInputAudio",
    "TestDataFuzzingTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1",
    "TestDataFuzzingTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "TestDataFuzzingTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam",
    "TestDataFuzzingTestContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall",
    "TestDataFuzzingTestContentInputMessageChatCompletionAssistantMessageParamInputToolCall",
    "TestDataFuzzingTestContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction",
    "TestDataFuzzingTestContentInputMessageChatCompletionToolMessageParam",
    "TestDataFuzzingTestContentInputMessageChatCompletionToolMessageParamContentUnionMember1",
    "TestDataFuzzingTestContentInputMessageChatCompletionFunctionMessageParam",
    "TestDataFuzzingTestContentOutputDetection",
    "TestDataFuzzingTestContentOutputDetectionDetectorData",
    "TestDataFuzzingTestContentOutputDetectionDetectorDataTextMatchingDetector",
    "TestDataFuzzingTestContentOutputDetectionDetectorDataCategoryDetector",
    "TestDataFuzzingTestContentOutputDetectionDetectorDataNaturalLanguageDetector",
    "TestDataFuzzingTestContentOutputDetectionDetectorDataComparatorDetector",
    "TestDataFuzzingTestContentOutputDetectionDetectorDataCustomDetector",
    "TestDataFuzzingTestContentOutputMessage",
    "TestDataFuzzingTestContentOutputMessageChatCompletionSystemMessageParam",
    "TestDataFuzzingTestContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1",
    "TestDataFuzzingTestContentOutputMessageChatCompletionUserMessageParamInput",
    "TestDataFuzzingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1",
    "TestDataFuzzingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "TestDataFuzzingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam",
    "TestDataFuzzingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL",
    "TestDataFuzzingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam",
    "TestDataFuzzingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio",
    "TestDataFuzzingTestContentOutputMessageChatCompletionAssistantMessageParamInput",
    "TestDataFuzzingTestContentOutputMessageChatCompletionAssistantMessageParamInputAudio",
    "TestDataFuzzingTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1",
    "TestDataFuzzingTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "TestDataFuzzingTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam",
    "TestDataFuzzingTestContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall",
    "TestDataFuzzingTestContentOutputMessageChatCompletionAssistantMessageParamInputToolCall",
    "TestDataFuzzingTestContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction",
    "TestDataFuzzingTestContentOutputMessageChatCompletionToolMessageParam",
    "TestDataFuzzingTestContentOutputMessageChatCompletionToolMessageParamContentUnionMember1",
    "TestDataFuzzingTestContentOutputMessageChatCompletionFunctionMessageParam",
    "TestDataFuzzingTestTargetModel",
    "TestDataFuzzingTestTargetModelGenerationParams",
    "TestDataDataReplayTest",
    "TestDataDataReplayTestAlgorithmStatus",
    "TestDataDataReplayTestContent",
    "TestDataDataReplayTestContentBehavior",
    "TestDataDataReplayTestContentInputDetection",
    "TestDataDataReplayTestContentInputDetectionDetectorData",
    "TestDataDataReplayTestContentInputDetectionDetectorDataTextMatchingDetector",
    "TestDataDataReplayTestContentInputDetectionDetectorDataCategoryDetector",
    "TestDataDataReplayTestContentInputDetectionDetectorDataNaturalLanguageDetector",
    "TestDataDataReplayTestContentInputDetectionDetectorDataComparatorDetector",
    "TestDataDataReplayTestContentInputDetectionDetectorDataCustomDetector",
    "TestDataDataReplayTestContentInputMessage",
    "TestDataDataReplayTestContentInputMessageChatCompletionSystemMessageParam",
    "TestDataDataReplayTestContentInputMessageChatCompletionSystemMessageParamContentUnionMember1",
    "TestDataDataReplayTestContentInputMessageChatCompletionUserMessageParamInput",
    "TestDataDataReplayTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1",
    "TestDataDataReplayTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "TestDataDataReplayTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam",
    "TestDataDataReplayTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL",
    "TestDataDataReplayTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam",
    "TestDataDataReplayTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio",
    "TestDataDataReplayTestContentInputMessageChatCompletionAssistantMessageParamInput",
    "TestDataDataReplayTestContentInputMessageChatCompletionAssistantMessageParamInputAudio",
    "TestDataDataReplayTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1",
    "TestDataDataReplayTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "TestDataDataReplayTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam",
    "TestDataDataReplayTestContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall",
    "TestDataDataReplayTestContentInputMessageChatCompletionAssistantMessageParamInputToolCall",
    "TestDataDataReplayTestContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction",
    "TestDataDataReplayTestContentInputMessageChatCompletionToolMessageParam",
    "TestDataDataReplayTestContentInputMessageChatCompletionToolMessageParamContentUnionMember1",
    "TestDataDataReplayTestContentInputMessageChatCompletionFunctionMessageParam",
    "TestDataDataReplayTestContentOutputDetection",
    "TestDataDataReplayTestContentOutputDetectionDetectorData",
    "TestDataDataReplayTestContentOutputDetectionDetectorDataTextMatchingDetector",
    "TestDataDataReplayTestContentOutputDetectionDetectorDataCategoryDetector",
    "TestDataDataReplayTestContentOutputDetectionDetectorDataNaturalLanguageDetector",
    "TestDataDataReplayTestContentOutputDetectionDetectorDataComparatorDetector",
    "TestDataDataReplayTestContentOutputDetectionDetectorDataCustomDetector",
    "TestDataDataReplayTestContentOutputMessage",
    "TestDataDataReplayTestContentOutputMessageChatCompletionSystemMessageParam",
    "TestDataDataReplayTestContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1",
    "TestDataDataReplayTestContentOutputMessageChatCompletionUserMessageParamInput",
    "TestDataDataReplayTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1",
    "TestDataDataReplayTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "TestDataDataReplayTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam",
    "TestDataDataReplayTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL",
    "TestDataDataReplayTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam",
    "TestDataDataReplayTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio",
    "TestDataDataReplayTestContentOutputMessageChatCompletionAssistantMessageParamInput",
    "TestDataDataReplayTestContentOutputMessageChatCompletionAssistantMessageParamInputAudio",
    "TestDataDataReplayTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1",
    "TestDataDataReplayTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "TestDataDataReplayTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam",
    "TestDataDataReplayTestContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall",
    "TestDataDataReplayTestContentOutputMessageChatCompletionAssistantMessageParamInputToolCall",
    "TestDataDataReplayTestContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction",
    "TestDataDataReplayTestContentOutputMessageChatCompletionToolMessageParam",
    "TestDataDataReplayTestContentOutputMessageChatCompletionToolMessageParamContentUnionMember1",
    "TestDataDataReplayTestContentOutputMessageChatCompletionFunctionMessageParam",
    "TestDataDataReplayTestTargetModel",
    "TestDataDataReplayTestTargetModelGenerationParams",
    "TestDataExperimentTest",
    "TestDataExperimentTestAlgorithmStatus",
    "TestDataExperimentTestContent",
    "TestDataExperimentTestContentBehavior",
    "TestDataExperimentTestContentExpectedMessage",
    "TestDataExperimentTestContentExpectedMessageChatCompletionSystemMessageParam",
    "TestDataExperimentTestContentExpectedMessageChatCompletionSystemMessageParamContentUnionMember1",
    "TestDataExperimentTestContentExpectedMessageChatCompletionUserMessageParamInput",
    "TestDataExperimentTestContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1",
    "TestDataExperimentTestContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "TestDataExperimentTestContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam",
    "TestDataExperimentTestContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL",
    "TestDataExperimentTestContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam",
    "TestDataExperimentTestContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio",
    "TestDataExperimentTestContentExpectedMessageChatCompletionAssistantMessageParamInput",
    "TestDataExperimentTestContentExpectedMessageChatCompletionAssistantMessageParamInputAudio",
    "TestDataExperimentTestContentExpectedMessageChatCompletionAssistantMessageParamInputContentUnionMember1",
    "TestDataExperimentTestContentExpectedMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "TestDataExperimentTestContentExpectedMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam",
    "TestDataExperimentTestContentExpectedMessageChatCompletionAssistantMessageParamInputFunctionCall",
    "TestDataExperimentTestContentExpectedMessageChatCompletionAssistantMessageParamInputToolCall",
    "TestDataExperimentTestContentExpectedMessageChatCompletionAssistantMessageParamInputToolCallFunction",
    "TestDataExperimentTestContentExpectedMessageChatCompletionToolMessageParam",
    "TestDataExperimentTestContentExpectedMessageChatCompletionToolMessageParamContentUnionMember1",
    "TestDataExperimentTestContentExpectedMessageChatCompletionFunctionMessageParam",
    "TestDataExperimentTestContentInputDetection",
    "TestDataExperimentTestContentInputDetectionDetectorData",
    "TestDataExperimentTestContentInputDetectionDetectorDataTextMatchingDetector",
    "TestDataExperimentTestContentInputDetectionDetectorDataCategoryDetector",
    "TestDataExperimentTestContentInputDetectionDetectorDataNaturalLanguageDetector",
    "TestDataExperimentTestContentInputDetectionDetectorDataComparatorDetector",
    "TestDataExperimentTestContentInputDetectionDetectorDataCustomDetector",
    "TestDataExperimentTestContentInputMessage",
    "TestDataExperimentTestContentInputMessageChatCompletionSystemMessageParam",
    "TestDataExperimentTestContentInputMessageChatCompletionSystemMessageParamContentUnionMember1",
    "TestDataExperimentTestContentInputMessageChatCompletionUserMessageParamInput",
    "TestDataExperimentTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1",
    "TestDataExperimentTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "TestDataExperimentTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam",
    "TestDataExperimentTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL",
    "TestDataExperimentTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam",
    "TestDataExperimentTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio",
    "TestDataExperimentTestContentInputMessageChatCompletionAssistantMessageParamInput",
    "TestDataExperimentTestContentInputMessageChatCompletionAssistantMessageParamInputAudio",
    "TestDataExperimentTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1",
    "TestDataExperimentTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "TestDataExperimentTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam",
    "TestDataExperimentTestContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall",
    "TestDataExperimentTestContentInputMessageChatCompletionAssistantMessageParamInputToolCall",
    "TestDataExperimentTestContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction",
    "TestDataExperimentTestContentInputMessageChatCompletionToolMessageParam",
    "TestDataExperimentTestContentInputMessageChatCompletionToolMessageParamContentUnionMember1",
    "TestDataExperimentTestContentInputMessageChatCompletionFunctionMessageParam",
    "TestDataExperimentTestContentOutputDetection",
    "TestDataExperimentTestContentOutputDetectionDetectorData",
    "TestDataExperimentTestContentOutputDetectionDetectorDataTextMatchingDetector",
    "TestDataExperimentTestContentOutputDetectionDetectorDataCategoryDetector",
    "TestDataExperimentTestContentOutputDetectionDetectorDataNaturalLanguageDetector",
    "TestDataExperimentTestContentOutputDetectionDetectorDataComparatorDetector",
    "TestDataExperimentTestContentOutputDetectionDetectorDataCustomDetector",
    "TestDataExperimentTestContentOutputMessage",
    "TestDataExperimentTestContentOutputMessageChatCompletionSystemMessageParam",
    "TestDataExperimentTestContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1",
    "TestDataExperimentTestContentOutputMessageChatCompletionUserMessageParamInput",
    "TestDataExperimentTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1",
    "TestDataExperimentTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "TestDataExperimentTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam",
    "TestDataExperimentTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL",
    "TestDataExperimentTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam",
    "TestDataExperimentTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio",
    "TestDataExperimentTestContentOutputMessageChatCompletionAssistantMessageParamInput",
    "TestDataExperimentTestContentOutputMessageChatCompletionAssistantMessageParamInputAudio",
    "TestDataExperimentTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1",
    "TestDataExperimentTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam",
    "TestDataExperimentTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam",
    "TestDataExperimentTestContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall",
    "TestDataExperimentTestContentOutputMessageChatCompletionAssistantMessageParamInputToolCall",
    "TestDataExperimentTestContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction",
    "TestDataExperimentTestContentOutputMessageChatCompletionToolMessageParam",
    "TestDataExperimentTestContentOutputMessageChatCompletionToolMessageParamContentUnionMember1",
    "TestDataExperimentTestContentOutputMessageChatCompletionFunctionMessageParam",
    "TestDataExperimentTestTargetModel",
    "TestDataExperimentTestTargetModelGenerationParams",
]


class TestingStartParams(TypedDict, total=False):
    test_data: Required[TestData]

    id: str

    user_id: Optional[str]


class TestDataRedTeamingTestAlgorithmStatus(TypedDict, total=False):
    name: Required[str]

    status: Required[Literal["COMPLETE", "ERROR", "RUNNING", "STEP_COMPLETE", "STOPPED"]]
    """Status for the overall test."""


class TestDataRedTeamingTestBehavior(TypedDict, total=False):
    description: Required[str]


class TestDataRedTeamingTestContentBehavior(TypedDict, total=False):
    description: Required[str]


class TestDataRedTeamingTestContentInputDetectionDetectorDataTextMatchingDetector(TypedDict, total=False):
    name: Required[str]

    regex: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["TEXT_MATCHING"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataRedTeamingTestContentInputDetectionDetectorDataCategoryDetector(TypedDict, total=False):
    category: Required[str]

    name: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CATEGORY"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataRedTeamingTestContentInputDetectionDetectorDataNaturalLanguageDetector(TypedDict, total=False):
    name: Required[str]

    natural_language_content: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["NATURAL_LANGUAGE"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataRedTeamingTestContentInputDetectionDetectorDataComparatorDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["EXACT_MATCH", "LANGUAGE_MODEL_SIMILARITY"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["COMPARATOR"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataRedTeamingTestContentInputDetectionDetectorDataCustomDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["TIERED_DETECTOR"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CUSTOM"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


TestDataRedTeamingTestContentInputDetectionDetectorData: TypeAlias = Union[
    TestDataRedTeamingTestContentInputDetectionDetectorDataTextMatchingDetector,
    TestDataRedTeamingTestContentInputDetectionDetectorDataCategoryDetector,
    TestDataRedTeamingTestContentInputDetectionDetectorDataNaturalLanguageDetector,
    TestDataRedTeamingTestContentInputDetectionDetectorDataComparatorDetector,
    TestDataRedTeamingTestContentInputDetectionDetectorDataCustomDetector,
]


class TestDataRedTeamingTestContentInputDetection(TypedDict, total=False):
    content_id: Required[str]

    detected: Required[bool]

    detector_id: Required[str]

    end_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    score: Required[float]

    start_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    detector_data: Optional[TestDataRedTeamingTestContentInputDetectionDetectorData]


class TestDataRedTeamingTestContentInputMessageChatCompletionSystemMessageParamContentUnionMember1(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataRedTeamingTestContentInputMessageChatCompletionSystemMessageParam(TypedDict, total=False):
    content: Required[
        Union[
            str, Iterable[TestDataRedTeamingTestContentInputMessageChatCompletionSystemMessageParamContentUnionMember1]
        ]
    ]

    role: Required[Literal["system"]]

    name: str


class TestDataRedTeamingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataRedTeamingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["auto", "low", "high"]


class TestDataRedTeamingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam(
    TypedDict, total=False
):
    image_url: Required[
        TestDataRedTeamingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL
    ]

    type: Required[Literal["image_url"]]


class TestDataRedTeamingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio(
    TypedDict, total=False
):
    data: Required[str]

    format: Required[Literal["wav", "mp3"]]


class TestDataRedTeamingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam(
    TypedDict, total=False
):
    input_audio: Required[
        TestDataRedTeamingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio
    ]

    type: Required[Literal["input_audio"]]


TestDataRedTeamingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1: TypeAlias = Union[
    TestDataRedTeamingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    TestDataRedTeamingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam,
    TestDataRedTeamingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam,
]


class TestDataRedTeamingTestContentInputMessageChatCompletionUserMessageParamInput(TypedDict, total=False):
    content: Required[
        Union[
            str,
            Iterable[TestDataRedTeamingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1],
        ]
    ]

    role: Required[Literal["user"]]

    name: str


class TestDataRedTeamingTestContentInputMessageChatCompletionAssistantMessageParamInputAudio(TypedDict, total=False):
    id: Required[str]


class TestDataRedTeamingTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataRedTeamingTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam(
    TypedDict, total=False
):
    refusal: Required[str]

    type: Required[Literal["refusal"]]


TestDataRedTeamingTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1: TypeAlias = Union[
    TestDataRedTeamingTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    TestDataRedTeamingTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam,
]


class TestDataRedTeamingTestContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall(
    TypedDict, total=False
):
    arguments: Required[str]

    name: Required[str]


class TestDataRedTeamingTestContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction(
    TypedDict, total=False
):
    arguments: Required[str]

    name: Required[str]


class TestDataRedTeamingTestContentInputMessageChatCompletionAssistantMessageParamInputToolCall(TypedDict, total=False):
    id: Required[str]

    function: Required[
        TestDataRedTeamingTestContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction
    ]

    type: Required[Literal["function"]]


class TestDataRedTeamingTestContentInputMessageChatCompletionAssistantMessageParamInput(TypedDict, total=False):
    role: Required[Literal["assistant"]]

    audio: Optional[TestDataRedTeamingTestContentInputMessageChatCompletionAssistantMessageParamInputAudio]

    content: Union[
        str,
        Iterable[TestDataRedTeamingTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1],
        None,
    ]

    function_call: Optional[
        TestDataRedTeamingTestContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall
    ]

    name: str

    refusal: Optional[str]

    tool_calls: Iterable[TestDataRedTeamingTestContentInputMessageChatCompletionAssistantMessageParamInputToolCall]


class TestDataRedTeamingTestContentInputMessageChatCompletionToolMessageParamContentUnionMember1(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataRedTeamingTestContentInputMessageChatCompletionToolMessageParam(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[TestDataRedTeamingTestContentInputMessageChatCompletionToolMessageParamContentUnionMember1]]
    ]

    role: Required[Literal["tool"]]

    tool_call_id: Required[str]


class TestDataRedTeamingTestContentInputMessageChatCompletionFunctionMessageParam(TypedDict, total=False):
    content: Required[Optional[str]]

    name: Required[str]

    role: Required[Literal["function"]]


TestDataRedTeamingTestContentInputMessage: TypeAlias = Union[
    TestDataRedTeamingTestContentInputMessageChatCompletionSystemMessageParam,
    TestDataRedTeamingTestContentInputMessageChatCompletionUserMessageParamInput,
    TestDataRedTeamingTestContentInputMessageChatCompletionAssistantMessageParamInput,
    TestDataRedTeamingTestContentInputMessageChatCompletionToolMessageParam,
    TestDataRedTeamingTestContentInputMessageChatCompletionFunctionMessageParam,
]


class TestDataRedTeamingTestContentOutputDetectionDetectorDataTextMatchingDetector(TypedDict, total=False):
    name: Required[str]

    regex: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["TEXT_MATCHING"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataRedTeamingTestContentOutputDetectionDetectorDataCategoryDetector(TypedDict, total=False):
    category: Required[str]

    name: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CATEGORY"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataRedTeamingTestContentOutputDetectionDetectorDataNaturalLanguageDetector(TypedDict, total=False):
    name: Required[str]

    natural_language_content: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["NATURAL_LANGUAGE"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataRedTeamingTestContentOutputDetectionDetectorDataComparatorDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["EXACT_MATCH", "LANGUAGE_MODEL_SIMILARITY"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["COMPARATOR"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataRedTeamingTestContentOutputDetectionDetectorDataCustomDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["TIERED_DETECTOR"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CUSTOM"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


TestDataRedTeamingTestContentOutputDetectionDetectorData: TypeAlias = Union[
    TestDataRedTeamingTestContentOutputDetectionDetectorDataTextMatchingDetector,
    TestDataRedTeamingTestContentOutputDetectionDetectorDataCategoryDetector,
    TestDataRedTeamingTestContentOutputDetectionDetectorDataNaturalLanguageDetector,
    TestDataRedTeamingTestContentOutputDetectionDetectorDataComparatorDetector,
    TestDataRedTeamingTestContentOutputDetectionDetectorDataCustomDetector,
]


class TestDataRedTeamingTestContentOutputDetection(TypedDict, total=False):
    content_id: Required[str]

    detected: Required[bool]

    detector_id: Required[str]

    end_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    score: Required[float]

    start_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    detector_data: Optional[TestDataRedTeamingTestContentOutputDetectionDetectorData]


class TestDataRedTeamingTestContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataRedTeamingTestContentOutputMessageChatCompletionSystemMessageParam(TypedDict, total=False):
    content: Required[
        Union[
            str, Iterable[TestDataRedTeamingTestContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1]
        ]
    ]

    role: Required[Literal["system"]]

    name: str


class TestDataRedTeamingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataRedTeamingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["auto", "low", "high"]


class TestDataRedTeamingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam(
    TypedDict, total=False
):
    image_url: Required[
        TestDataRedTeamingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL
    ]

    type: Required[Literal["image_url"]]


class TestDataRedTeamingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio(
    TypedDict, total=False
):
    data: Required[str]

    format: Required[Literal["wav", "mp3"]]


class TestDataRedTeamingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam(
    TypedDict, total=False
):
    input_audio: Required[
        TestDataRedTeamingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio
    ]

    type: Required[Literal["input_audio"]]


TestDataRedTeamingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1: TypeAlias = Union[
    TestDataRedTeamingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    TestDataRedTeamingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam,
    TestDataRedTeamingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam,
]


class TestDataRedTeamingTestContentOutputMessageChatCompletionUserMessageParamInput(TypedDict, total=False):
    content: Required[
        Union[
            str,
            Iterable[TestDataRedTeamingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1],
        ]
    ]

    role: Required[Literal["user"]]

    name: str


class TestDataRedTeamingTestContentOutputMessageChatCompletionAssistantMessageParamInputAudio(TypedDict, total=False):
    id: Required[str]


class TestDataRedTeamingTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataRedTeamingTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam(
    TypedDict, total=False
):
    refusal: Required[str]

    type: Required[Literal["refusal"]]


TestDataRedTeamingTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1: TypeAlias = Union[
    TestDataRedTeamingTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    TestDataRedTeamingTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam,
]


class TestDataRedTeamingTestContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall(
    TypedDict, total=False
):
    arguments: Required[str]

    name: Required[str]


class TestDataRedTeamingTestContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction(
    TypedDict, total=False
):
    arguments: Required[str]

    name: Required[str]


class TestDataRedTeamingTestContentOutputMessageChatCompletionAssistantMessageParamInputToolCall(
    TypedDict, total=False
):
    id: Required[str]

    function: Required[
        TestDataRedTeamingTestContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction
    ]

    type: Required[Literal["function"]]


class TestDataRedTeamingTestContentOutputMessageChatCompletionAssistantMessageParamInput(TypedDict, total=False):
    role: Required[Literal["assistant"]]

    audio: Optional[TestDataRedTeamingTestContentOutputMessageChatCompletionAssistantMessageParamInputAudio]

    content: Union[
        str,
        Iterable[TestDataRedTeamingTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1],
        None,
    ]

    function_call: Optional[
        TestDataRedTeamingTestContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall
    ]

    name: str

    refusal: Optional[str]

    tool_calls: Iterable[TestDataRedTeamingTestContentOutputMessageChatCompletionAssistantMessageParamInputToolCall]


class TestDataRedTeamingTestContentOutputMessageChatCompletionToolMessageParamContentUnionMember1(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataRedTeamingTestContentOutputMessageChatCompletionToolMessageParam(TypedDict, total=False):
    content: Required[
        Union[
            str, Iterable[TestDataRedTeamingTestContentOutputMessageChatCompletionToolMessageParamContentUnionMember1]
        ]
    ]

    role: Required[Literal["tool"]]

    tool_call_id: Required[str]


class TestDataRedTeamingTestContentOutputMessageChatCompletionFunctionMessageParam(TypedDict, total=False):
    content: Required[Optional[str]]

    name: Required[str]

    role: Required[Literal["function"]]


TestDataRedTeamingTestContentOutputMessage: TypeAlias = Union[
    TestDataRedTeamingTestContentOutputMessageChatCompletionSystemMessageParam,
    TestDataRedTeamingTestContentOutputMessageChatCompletionUserMessageParamInput,
    TestDataRedTeamingTestContentOutputMessageChatCompletionAssistantMessageParamInput,
    TestDataRedTeamingTestContentOutputMessageChatCompletionToolMessageParam,
    TestDataRedTeamingTestContentOutputMessageChatCompletionFunctionMessageParam,
]


class TestDataRedTeamingTestContent(TypedDict, total=False):
    id: str

    algorithm: Optional[str]

    behavior: Optional[TestDataRedTeamingTestContentBehavior]

    content_group_ids: Optional[List[str]]

    content_type: Optional[Literal["BASE", "TEST", "EXPERIMENT"]]

    end: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    generate_end_time: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    generate_start_time: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    input_detections: Optional[Iterable[TestDataRedTeamingTestContentInputDetection]]

    input_messages: Optional[Iterable[TestDataRedTeamingTestContentInputMessage]]

    metadata: Optional[object]

    output_detections: Optional[Iterable[TestDataRedTeamingTestContentOutputDetection]]

    output_messages: Optional[Iterable[TestDataRedTeamingTestContentOutputMessage]]

    start: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    status: Optional[Literal["GENERATING_CONTENT", "AWAITING_RESPONSE", "ANALYZING_RESPONSE", "COMPLETE", "DISCARDED"]]
    """Status for a single content object in a test."""

    test_id: Optional[str]

    time: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    user_id: Optional[str]


class TestDataRedTeamingTestTargetModelGenerationParams(TypedDict, total=False):
    id: str

    max_tokens: Optional[int]

    system_message: Optional[str]

    temperature: Optional[float]

    user_id: Optional[str]


class TestDataRedTeamingTestTargetModel(TypedDict, total=False):
    model_id: Required[str]

    id: str

    api_key: Optional[str]

    base_url: Optional[str]

    generation_params: Optional[TestDataRedTeamingTestTargetModelGenerationParams]

    model_provider: Optional[str]

    model_type: Optional[Literal["STANDARD", "CUSTOM"]]

    name: Optional[str]

    time: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    user_id: Optional[str]


class TestDataRedTeamingTest(TypedDict, total=False):
    name: Required[str]

    user_id: Required[Optional[str]]

    id: str

    algorithm_status: Optional[Iterable[TestDataRedTeamingTestAlgorithmStatus]]

    behaviors: Iterable[TestDataRedTeamingTestBehavior]

    content: Optional[Iterable[TestDataRedTeamingTestContent]]

    content_group_ids: Optional[List[str]]

    detector_ids: Optional[List[str]]

    end_date: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    start_date: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    status: Optional[Literal["COMPLETE", "ERROR", "RUNNING", "STEP_COMPLETE", "STOPPED"]]
    """Status for the overall test."""

    target_model: Optional[TestDataRedTeamingTestTargetModel]

    test_type: Literal["RED_TEAMING"]


class TestDataFuzzingTestAlgorithmStatus(TypedDict, total=False):
    name: Required[str]

    status: Required[Literal["COMPLETE", "ERROR", "RUNNING", "STEP_COMPLETE", "STOPPED"]]
    """Status for the overall test."""


class TestDataFuzzingTestBehavior(TypedDict, total=False):
    description: Required[str]


class TestDataFuzzingTestContentBehavior(TypedDict, total=False):
    description: Required[str]


class TestDataFuzzingTestContentInputDetectionDetectorDataTextMatchingDetector(TypedDict, total=False):
    name: Required[str]

    regex: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["TEXT_MATCHING"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataFuzzingTestContentInputDetectionDetectorDataCategoryDetector(TypedDict, total=False):
    category: Required[str]

    name: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CATEGORY"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataFuzzingTestContentInputDetectionDetectorDataNaturalLanguageDetector(TypedDict, total=False):
    name: Required[str]

    natural_language_content: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["NATURAL_LANGUAGE"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataFuzzingTestContentInputDetectionDetectorDataComparatorDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["EXACT_MATCH", "LANGUAGE_MODEL_SIMILARITY"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["COMPARATOR"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataFuzzingTestContentInputDetectionDetectorDataCustomDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["TIERED_DETECTOR"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CUSTOM"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


TestDataFuzzingTestContentInputDetectionDetectorData: TypeAlias = Union[
    TestDataFuzzingTestContentInputDetectionDetectorDataTextMatchingDetector,
    TestDataFuzzingTestContentInputDetectionDetectorDataCategoryDetector,
    TestDataFuzzingTestContentInputDetectionDetectorDataNaturalLanguageDetector,
    TestDataFuzzingTestContentInputDetectionDetectorDataComparatorDetector,
    TestDataFuzzingTestContentInputDetectionDetectorDataCustomDetector,
]


class TestDataFuzzingTestContentInputDetection(TypedDict, total=False):
    content_id: Required[str]

    detected: Required[bool]

    detector_id: Required[str]

    end_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    score: Required[float]

    start_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    detector_data: Optional[TestDataFuzzingTestContentInputDetectionDetectorData]


class TestDataFuzzingTestContentInputMessageChatCompletionSystemMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataFuzzingTestContentInputMessageChatCompletionSystemMessageParam(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[TestDataFuzzingTestContentInputMessageChatCompletionSystemMessageParamContentUnionMember1]]
    ]

    role: Required[Literal["system"]]

    name: str


class TestDataFuzzingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataFuzzingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["auto", "low", "high"]


class TestDataFuzzingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam(
    TypedDict, total=False
):
    image_url: Required[
        TestDataFuzzingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL
    ]

    type: Required[Literal["image_url"]]


class TestDataFuzzingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio(
    TypedDict, total=False
):
    data: Required[str]

    format: Required[Literal["wav", "mp3"]]


class TestDataFuzzingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam(
    TypedDict, total=False
):
    input_audio: Required[
        TestDataFuzzingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio
    ]

    type: Required[Literal["input_audio"]]


TestDataFuzzingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1: TypeAlias = Union[
    TestDataFuzzingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    TestDataFuzzingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam,
    TestDataFuzzingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam,
]


class TestDataFuzzingTestContentInputMessageChatCompletionUserMessageParamInput(TypedDict, total=False):
    content: Required[
        Union[
            str, Iterable[TestDataFuzzingTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1]
        ]
    ]

    role: Required[Literal["user"]]

    name: str


class TestDataFuzzingTestContentInputMessageChatCompletionAssistantMessageParamInputAudio(TypedDict, total=False):
    id: Required[str]


class TestDataFuzzingTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataFuzzingTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam(
    TypedDict, total=False
):
    refusal: Required[str]

    type: Required[Literal["refusal"]]


TestDataFuzzingTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1: TypeAlias = Union[
    TestDataFuzzingTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    TestDataFuzzingTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam,
]


class TestDataFuzzingTestContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall(
    TypedDict, total=False
):
    arguments: Required[str]

    name: Required[str]


class TestDataFuzzingTestContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction(
    TypedDict, total=False
):
    arguments: Required[str]

    name: Required[str]


class TestDataFuzzingTestContentInputMessageChatCompletionAssistantMessageParamInputToolCall(TypedDict, total=False):
    id: Required[str]

    function: Required[TestDataFuzzingTestContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction]

    type: Required[Literal["function"]]


class TestDataFuzzingTestContentInputMessageChatCompletionAssistantMessageParamInput(TypedDict, total=False):
    role: Required[Literal["assistant"]]

    audio: Optional[TestDataFuzzingTestContentInputMessageChatCompletionAssistantMessageParamInputAudio]

    content: Union[
        str,
        Iterable[TestDataFuzzingTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1],
        None,
    ]

    function_call: Optional[TestDataFuzzingTestContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall]

    name: str

    refusal: Optional[str]

    tool_calls: Iterable[TestDataFuzzingTestContentInputMessageChatCompletionAssistantMessageParamInputToolCall]


class TestDataFuzzingTestContentInputMessageChatCompletionToolMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataFuzzingTestContentInputMessageChatCompletionToolMessageParam(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[TestDataFuzzingTestContentInputMessageChatCompletionToolMessageParamContentUnionMember1]]
    ]

    role: Required[Literal["tool"]]

    tool_call_id: Required[str]


class TestDataFuzzingTestContentInputMessageChatCompletionFunctionMessageParam(TypedDict, total=False):
    content: Required[Optional[str]]

    name: Required[str]

    role: Required[Literal["function"]]


TestDataFuzzingTestContentInputMessage: TypeAlias = Union[
    TestDataFuzzingTestContentInputMessageChatCompletionSystemMessageParam,
    TestDataFuzzingTestContentInputMessageChatCompletionUserMessageParamInput,
    TestDataFuzzingTestContentInputMessageChatCompletionAssistantMessageParamInput,
    TestDataFuzzingTestContentInputMessageChatCompletionToolMessageParam,
    TestDataFuzzingTestContentInputMessageChatCompletionFunctionMessageParam,
]


class TestDataFuzzingTestContentOutputDetectionDetectorDataTextMatchingDetector(TypedDict, total=False):
    name: Required[str]

    regex: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["TEXT_MATCHING"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataFuzzingTestContentOutputDetectionDetectorDataCategoryDetector(TypedDict, total=False):
    category: Required[str]

    name: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CATEGORY"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataFuzzingTestContentOutputDetectionDetectorDataNaturalLanguageDetector(TypedDict, total=False):
    name: Required[str]

    natural_language_content: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["NATURAL_LANGUAGE"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataFuzzingTestContentOutputDetectionDetectorDataComparatorDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["EXACT_MATCH", "LANGUAGE_MODEL_SIMILARITY"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["COMPARATOR"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataFuzzingTestContentOutputDetectionDetectorDataCustomDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["TIERED_DETECTOR"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CUSTOM"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


TestDataFuzzingTestContentOutputDetectionDetectorData: TypeAlias = Union[
    TestDataFuzzingTestContentOutputDetectionDetectorDataTextMatchingDetector,
    TestDataFuzzingTestContentOutputDetectionDetectorDataCategoryDetector,
    TestDataFuzzingTestContentOutputDetectionDetectorDataNaturalLanguageDetector,
    TestDataFuzzingTestContentOutputDetectionDetectorDataComparatorDetector,
    TestDataFuzzingTestContentOutputDetectionDetectorDataCustomDetector,
]


class TestDataFuzzingTestContentOutputDetection(TypedDict, total=False):
    content_id: Required[str]

    detected: Required[bool]

    detector_id: Required[str]

    end_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    score: Required[float]

    start_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    detector_data: Optional[TestDataFuzzingTestContentOutputDetectionDetectorData]


class TestDataFuzzingTestContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataFuzzingTestContentOutputMessageChatCompletionSystemMessageParam(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[TestDataFuzzingTestContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1]]
    ]

    role: Required[Literal["system"]]

    name: str


class TestDataFuzzingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataFuzzingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["auto", "low", "high"]


class TestDataFuzzingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam(
    TypedDict, total=False
):
    image_url: Required[
        TestDataFuzzingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL
    ]

    type: Required[Literal["image_url"]]


class TestDataFuzzingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio(
    TypedDict, total=False
):
    data: Required[str]

    format: Required[Literal["wav", "mp3"]]


class TestDataFuzzingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam(
    TypedDict, total=False
):
    input_audio: Required[
        TestDataFuzzingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio
    ]

    type: Required[Literal["input_audio"]]


TestDataFuzzingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1: TypeAlias = Union[
    TestDataFuzzingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    TestDataFuzzingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam,
    TestDataFuzzingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam,
]


class TestDataFuzzingTestContentOutputMessageChatCompletionUserMessageParamInput(TypedDict, total=False):
    content: Required[
        Union[
            str, Iterable[TestDataFuzzingTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1]
        ]
    ]

    role: Required[Literal["user"]]

    name: str


class TestDataFuzzingTestContentOutputMessageChatCompletionAssistantMessageParamInputAudio(TypedDict, total=False):
    id: Required[str]


class TestDataFuzzingTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataFuzzingTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam(
    TypedDict, total=False
):
    refusal: Required[str]

    type: Required[Literal["refusal"]]


TestDataFuzzingTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1: TypeAlias = Union[
    TestDataFuzzingTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    TestDataFuzzingTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam,
]


class TestDataFuzzingTestContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall(
    TypedDict, total=False
):
    arguments: Required[str]

    name: Required[str]


class TestDataFuzzingTestContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction(
    TypedDict, total=False
):
    arguments: Required[str]

    name: Required[str]


class TestDataFuzzingTestContentOutputMessageChatCompletionAssistantMessageParamInputToolCall(TypedDict, total=False):
    id: Required[str]

    function: Required[TestDataFuzzingTestContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction]

    type: Required[Literal["function"]]


class TestDataFuzzingTestContentOutputMessageChatCompletionAssistantMessageParamInput(TypedDict, total=False):
    role: Required[Literal["assistant"]]

    audio: Optional[TestDataFuzzingTestContentOutputMessageChatCompletionAssistantMessageParamInputAudio]

    content: Union[
        str,
        Iterable[TestDataFuzzingTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1],
        None,
    ]

    function_call: Optional[TestDataFuzzingTestContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall]

    name: str

    refusal: Optional[str]

    tool_calls: Iterable[TestDataFuzzingTestContentOutputMessageChatCompletionAssistantMessageParamInputToolCall]


class TestDataFuzzingTestContentOutputMessageChatCompletionToolMessageParamContentUnionMember1(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataFuzzingTestContentOutputMessageChatCompletionToolMessageParam(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[TestDataFuzzingTestContentOutputMessageChatCompletionToolMessageParamContentUnionMember1]]
    ]

    role: Required[Literal["tool"]]

    tool_call_id: Required[str]


class TestDataFuzzingTestContentOutputMessageChatCompletionFunctionMessageParam(TypedDict, total=False):
    content: Required[Optional[str]]

    name: Required[str]

    role: Required[Literal["function"]]


TestDataFuzzingTestContentOutputMessage: TypeAlias = Union[
    TestDataFuzzingTestContentOutputMessageChatCompletionSystemMessageParam,
    TestDataFuzzingTestContentOutputMessageChatCompletionUserMessageParamInput,
    TestDataFuzzingTestContentOutputMessageChatCompletionAssistantMessageParamInput,
    TestDataFuzzingTestContentOutputMessageChatCompletionToolMessageParam,
    TestDataFuzzingTestContentOutputMessageChatCompletionFunctionMessageParam,
]


class TestDataFuzzingTestContent(TypedDict, total=False):
    id: str

    algorithm: Optional[str]

    behavior: Optional[TestDataFuzzingTestContentBehavior]

    content_group_ids: Optional[List[str]]

    content_type: Optional[Literal["BASE", "TEST", "EXPERIMENT"]]

    end: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    generate_end_time: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    generate_start_time: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    input_detections: Optional[Iterable[TestDataFuzzingTestContentInputDetection]]

    input_messages: Optional[Iterable[TestDataFuzzingTestContentInputMessage]]

    metadata: Optional[object]

    output_detections: Optional[Iterable[TestDataFuzzingTestContentOutputDetection]]

    output_messages: Optional[Iterable[TestDataFuzzingTestContentOutputMessage]]

    start: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    status: Optional[Literal["GENERATING_CONTENT", "AWAITING_RESPONSE", "ANALYZING_RESPONSE", "COMPLETE", "DISCARDED"]]
    """Status for a single content object in a test."""

    test_id: Optional[str]

    time: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    user_id: Optional[str]


class TestDataFuzzingTestTargetModelGenerationParams(TypedDict, total=False):
    id: str

    max_tokens: Optional[int]

    system_message: Optional[str]

    temperature: Optional[float]

    user_id: Optional[str]


class TestDataFuzzingTestTargetModel(TypedDict, total=False):
    model_id: Required[str]

    id: str

    api_key: Optional[str]

    base_url: Optional[str]

    generation_params: Optional[TestDataFuzzingTestTargetModelGenerationParams]

    model_provider: Optional[str]

    model_type: Optional[Literal["STANDARD", "CUSTOM"]]

    name: Optional[str]

    time: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    user_id: Optional[str]


class TestDataFuzzingTest(TypedDict, total=False):
    name: Required[str]

    user_id: Required[Optional[str]]

    id: str

    algorithm_status: Optional[Iterable[TestDataFuzzingTestAlgorithmStatus]]

    behaviors: Iterable[TestDataFuzzingTestBehavior]

    content: Optional[Iterable[TestDataFuzzingTestContent]]

    content_group_ids: Optional[List[str]]

    detector_ids: Optional[List[str]]

    end_date: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    start_date: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    status: Optional[Literal["COMPLETE", "ERROR", "RUNNING", "STEP_COMPLETE", "STOPPED"]]
    """Status for the overall test."""

    target_model: Optional[TestDataFuzzingTestTargetModel]

    test_type: Literal["FUZZING"]


class TestDataDataReplayTestAlgorithmStatus(TypedDict, total=False):
    name: Required[str]

    status: Required[Literal["COMPLETE", "ERROR", "RUNNING", "STEP_COMPLETE", "STOPPED"]]
    """Status for the overall test."""


class TestDataDataReplayTestContentBehavior(TypedDict, total=False):
    description: Required[str]


class TestDataDataReplayTestContentInputDetectionDetectorDataTextMatchingDetector(TypedDict, total=False):
    name: Required[str]

    regex: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["TEXT_MATCHING"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataDataReplayTestContentInputDetectionDetectorDataCategoryDetector(TypedDict, total=False):
    category: Required[str]

    name: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CATEGORY"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataDataReplayTestContentInputDetectionDetectorDataNaturalLanguageDetector(TypedDict, total=False):
    name: Required[str]

    natural_language_content: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["NATURAL_LANGUAGE"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataDataReplayTestContentInputDetectionDetectorDataComparatorDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["EXACT_MATCH", "LANGUAGE_MODEL_SIMILARITY"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["COMPARATOR"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataDataReplayTestContentInputDetectionDetectorDataCustomDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["TIERED_DETECTOR"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CUSTOM"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


TestDataDataReplayTestContentInputDetectionDetectorData: TypeAlias = Union[
    TestDataDataReplayTestContentInputDetectionDetectorDataTextMatchingDetector,
    TestDataDataReplayTestContentInputDetectionDetectorDataCategoryDetector,
    TestDataDataReplayTestContentInputDetectionDetectorDataNaturalLanguageDetector,
    TestDataDataReplayTestContentInputDetectionDetectorDataComparatorDetector,
    TestDataDataReplayTestContentInputDetectionDetectorDataCustomDetector,
]


class TestDataDataReplayTestContentInputDetection(TypedDict, total=False):
    content_id: Required[str]

    detected: Required[bool]

    detector_id: Required[str]

    end_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    score: Required[float]

    start_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    detector_data: Optional[TestDataDataReplayTestContentInputDetectionDetectorData]


class TestDataDataReplayTestContentInputMessageChatCompletionSystemMessageParamContentUnionMember1(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataDataReplayTestContentInputMessageChatCompletionSystemMessageParam(TypedDict, total=False):
    content: Required[
        Union[
            str, Iterable[TestDataDataReplayTestContentInputMessageChatCompletionSystemMessageParamContentUnionMember1]
        ]
    ]

    role: Required[Literal["system"]]

    name: str


class TestDataDataReplayTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataDataReplayTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["auto", "low", "high"]


class TestDataDataReplayTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam(
    TypedDict, total=False
):
    image_url: Required[
        TestDataDataReplayTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL
    ]

    type: Required[Literal["image_url"]]


class TestDataDataReplayTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio(
    TypedDict, total=False
):
    data: Required[str]

    format: Required[Literal["wav", "mp3"]]


class TestDataDataReplayTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam(
    TypedDict, total=False
):
    input_audio: Required[
        TestDataDataReplayTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio
    ]

    type: Required[Literal["input_audio"]]


TestDataDataReplayTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1: TypeAlias = Union[
    TestDataDataReplayTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    TestDataDataReplayTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam,
    TestDataDataReplayTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam,
]


class TestDataDataReplayTestContentInputMessageChatCompletionUserMessageParamInput(TypedDict, total=False):
    content: Required[
        Union[
            str,
            Iterable[TestDataDataReplayTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1],
        ]
    ]

    role: Required[Literal["user"]]

    name: str


class TestDataDataReplayTestContentInputMessageChatCompletionAssistantMessageParamInputAudio(TypedDict, total=False):
    id: Required[str]


class TestDataDataReplayTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataDataReplayTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam(
    TypedDict, total=False
):
    refusal: Required[str]

    type: Required[Literal["refusal"]]


TestDataDataReplayTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1: TypeAlias = Union[
    TestDataDataReplayTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    TestDataDataReplayTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam,
]


class TestDataDataReplayTestContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall(
    TypedDict, total=False
):
    arguments: Required[str]

    name: Required[str]


class TestDataDataReplayTestContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction(
    TypedDict, total=False
):
    arguments: Required[str]

    name: Required[str]


class TestDataDataReplayTestContentInputMessageChatCompletionAssistantMessageParamInputToolCall(TypedDict, total=False):
    id: Required[str]

    function: Required[
        TestDataDataReplayTestContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction
    ]

    type: Required[Literal["function"]]


class TestDataDataReplayTestContentInputMessageChatCompletionAssistantMessageParamInput(TypedDict, total=False):
    role: Required[Literal["assistant"]]

    audio: Optional[TestDataDataReplayTestContentInputMessageChatCompletionAssistantMessageParamInputAudio]

    content: Union[
        str,
        Iterable[TestDataDataReplayTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1],
        None,
    ]

    function_call: Optional[
        TestDataDataReplayTestContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall
    ]

    name: str

    refusal: Optional[str]

    tool_calls: Iterable[TestDataDataReplayTestContentInputMessageChatCompletionAssistantMessageParamInputToolCall]


class TestDataDataReplayTestContentInputMessageChatCompletionToolMessageParamContentUnionMember1(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataDataReplayTestContentInputMessageChatCompletionToolMessageParam(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[TestDataDataReplayTestContentInputMessageChatCompletionToolMessageParamContentUnionMember1]]
    ]

    role: Required[Literal["tool"]]

    tool_call_id: Required[str]


class TestDataDataReplayTestContentInputMessageChatCompletionFunctionMessageParam(TypedDict, total=False):
    content: Required[Optional[str]]

    name: Required[str]

    role: Required[Literal["function"]]


TestDataDataReplayTestContentInputMessage: TypeAlias = Union[
    TestDataDataReplayTestContentInputMessageChatCompletionSystemMessageParam,
    TestDataDataReplayTestContentInputMessageChatCompletionUserMessageParamInput,
    TestDataDataReplayTestContentInputMessageChatCompletionAssistantMessageParamInput,
    TestDataDataReplayTestContentInputMessageChatCompletionToolMessageParam,
    TestDataDataReplayTestContentInputMessageChatCompletionFunctionMessageParam,
]


class TestDataDataReplayTestContentOutputDetectionDetectorDataTextMatchingDetector(TypedDict, total=False):
    name: Required[str]

    regex: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["TEXT_MATCHING"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataDataReplayTestContentOutputDetectionDetectorDataCategoryDetector(TypedDict, total=False):
    category: Required[str]

    name: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CATEGORY"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataDataReplayTestContentOutputDetectionDetectorDataNaturalLanguageDetector(TypedDict, total=False):
    name: Required[str]

    natural_language_content: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["NATURAL_LANGUAGE"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataDataReplayTestContentOutputDetectionDetectorDataComparatorDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["EXACT_MATCH", "LANGUAGE_MODEL_SIMILARITY"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["COMPARATOR"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataDataReplayTestContentOutputDetectionDetectorDataCustomDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["TIERED_DETECTOR"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CUSTOM"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


TestDataDataReplayTestContentOutputDetectionDetectorData: TypeAlias = Union[
    TestDataDataReplayTestContentOutputDetectionDetectorDataTextMatchingDetector,
    TestDataDataReplayTestContentOutputDetectionDetectorDataCategoryDetector,
    TestDataDataReplayTestContentOutputDetectionDetectorDataNaturalLanguageDetector,
    TestDataDataReplayTestContentOutputDetectionDetectorDataComparatorDetector,
    TestDataDataReplayTestContentOutputDetectionDetectorDataCustomDetector,
]


class TestDataDataReplayTestContentOutputDetection(TypedDict, total=False):
    content_id: Required[str]

    detected: Required[bool]

    detector_id: Required[str]

    end_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    score: Required[float]

    start_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    detector_data: Optional[TestDataDataReplayTestContentOutputDetectionDetectorData]


class TestDataDataReplayTestContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataDataReplayTestContentOutputMessageChatCompletionSystemMessageParam(TypedDict, total=False):
    content: Required[
        Union[
            str, Iterable[TestDataDataReplayTestContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1]
        ]
    ]

    role: Required[Literal["system"]]

    name: str


class TestDataDataReplayTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataDataReplayTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["auto", "low", "high"]


class TestDataDataReplayTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam(
    TypedDict, total=False
):
    image_url: Required[
        TestDataDataReplayTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL
    ]

    type: Required[Literal["image_url"]]


class TestDataDataReplayTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio(
    TypedDict, total=False
):
    data: Required[str]

    format: Required[Literal["wav", "mp3"]]


class TestDataDataReplayTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam(
    TypedDict, total=False
):
    input_audio: Required[
        TestDataDataReplayTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio
    ]

    type: Required[Literal["input_audio"]]


TestDataDataReplayTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1: TypeAlias = Union[
    TestDataDataReplayTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    TestDataDataReplayTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam,
    TestDataDataReplayTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam,
]


class TestDataDataReplayTestContentOutputMessageChatCompletionUserMessageParamInput(TypedDict, total=False):
    content: Required[
        Union[
            str,
            Iterable[TestDataDataReplayTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1],
        ]
    ]

    role: Required[Literal["user"]]

    name: str


class TestDataDataReplayTestContentOutputMessageChatCompletionAssistantMessageParamInputAudio(TypedDict, total=False):
    id: Required[str]


class TestDataDataReplayTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataDataReplayTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam(
    TypedDict, total=False
):
    refusal: Required[str]

    type: Required[Literal["refusal"]]


TestDataDataReplayTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1: TypeAlias = Union[
    TestDataDataReplayTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    TestDataDataReplayTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam,
]


class TestDataDataReplayTestContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall(
    TypedDict, total=False
):
    arguments: Required[str]

    name: Required[str]


class TestDataDataReplayTestContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction(
    TypedDict, total=False
):
    arguments: Required[str]

    name: Required[str]


class TestDataDataReplayTestContentOutputMessageChatCompletionAssistantMessageParamInputToolCall(
    TypedDict, total=False
):
    id: Required[str]

    function: Required[
        TestDataDataReplayTestContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction
    ]

    type: Required[Literal["function"]]


class TestDataDataReplayTestContentOutputMessageChatCompletionAssistantMessageParamInput(TypedDict, total=False):
    role: Required[Literal["assistant"]]

    audio: Optional[TestDataDataReplayTestContentOutputMessageChatCompletionAssistantMessageParamInputAudio]

    content: Union[
        str,
        Iterable[TestDataDataReplayTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1],
        None,
    ]

    function_call: Optional[
        TestDataDataReplayTestContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall
    ]

    name: str

    refusal: Optional[str]

    tool_calls: Iterable[TestDataDataReplayTestContentOutputMessageChatCompletionAssistantMessageParamInputToolCall]


class TestDataDataReplayTestContentOutputMessageChatCompletionToolMessageParamContentUnionMember1(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataDataReplayTestContentOutputMessageChatCompletionToolMessageParam(TypedDict, total=False):
    content: Required[
        Union[
            str, Iterable[TestDataDataReplayTestContentOutputMessageChatCompletionToolMessageParamContentUnionMember1]
        ]
    ]

    role: Required[Literal["tool"]]

    tool_call_id: Required[str]


class TestDataDataReplayTestContentOutputMessageChatCompletionFunctionMessageParam(TypedDict, total=False):
    content: Required[Optional[str]]

    name: Required[str]

    role: Required[Literal["function"]]


TestDataDataReplayTestContentOutputMessage: TypeAlias = Union[
    TestDataDataReplayTestContentOutputMessageChatCompletionSystemMessageParam,
    TestDataDataReplayTestContentOutputMessageChatCompletionUserMessageParamInput,
    TestDataDataReplayTestContentOutputMessageChatCompletionAssistantMessageParamInput,
    TestDataDataReplayTestContentOutputMessageChatCompletionToolMessageParam,
    TestDataDataReplayTestContentOutputMessageChatCompletionFunctionMessageParam,
]


class TestDataDataReplayTestContent(TypedDict, total=False):
    id: str

    algorithm: Optional[str]

    behavior: Optional[TestDataDataReplayTestContentBehavior]

    content_group_ids: Optional[List[str]]

    content_type: Optional[Literal["BASE", "TEST", "EXPERIMENT"]]

    end: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    generate_end_time: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    generate_start_time: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    input_detections: Optional[Iterable[TestDataDataReplayTestContentInputDetection]]

    input_messages: Optional[Iterable[TestDataDataReplayTestContentInputMessage]]

    metadata: Optional[object]

    output_detections: Optional[Iterable[TestDataDataReplayTestContentOutputDetection]]

    output_messages: Optional[Iterable[TestDataDataReplayTestContentOutputMessage]]

    start: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    status: Optional[Literal["GENERATING_CONTENT", "AWAITING_RESPONSE", "ANALYZING_RESPONSE", "COMPLETE", "DISCARDED"]]
    """Status for a single content object in a test."""

    test_id: Optional[str]

    time: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    user_id: Optional[str]


class TestDataDataReplayTestTargetModelGenerationParams(TypedDict, total=False):
    id: str

    max_tokens: Optional[int]

    system_message: Optional[str]

    temperature: Optional[float]

    user_id: Optional[str]


class TestDataDataReplayTestTargetModel(TypedDict, total=False):
    model_id: Required[str]

    id: str

    api_key: Optional[str]

    base_url: Optional[str]

    generation_params: Optional[TestDataDataReplayTestTargetModelGenerationParams]

    model_provider: Optional[str]

    model_type: Optional[Literal["STANDARD", "CUSTOM"]]

    name: Optional[str]

    time: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    user_id: Optional[str]


class TestDataDataReplayTest(TypedDict, total=False):
    name: Required[str]

    user_id: Required[Optional[str]]

    id: str

    algorithm_status: Optional[Iterable[TestDataDataReplayTestAlgorithmStatus]]

    content: Optional[Iterable[TestDataDataReplayTestContent]]

    content_group_ids: Optional[List[str]]

    detector_ids: Optional[List[str]]

    end_date: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    start_date: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    status: Optional[Literal["COMPLETE", "ERROR", "RUNNING", "STEP_COMPLETE", "STOPPED"]]
    """Status for the overall test."""

    target_model: Optional[TestDataDataReplayTestTargetModel]

    test_type: Literal["DATA_REPLAY"]


class TestDataExperimentTestAlgorithmStatus(TypedDict, total=False):
    name: Required[str]

    status: Required[Literal["COMPLETE", "ERROR", "RUNNING", "STEP_COMPLETE", "STOPPED"]]
    """Status for the overall test."""


class TestDataExperimentTestContentBehavior(TypedDict, total=False):
    description: Required[str]


class TestDataExperimentTestContentExpectedMessageChatCompletionSystemMessageParamContentUnionMember1(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataExperimentTestContentExpectedMessageChatCompletionSystemMessageParam(TypedDict, total=False):
    content: Required[
        Union[
            str,
            Iterable[TestDataExperimentTestContentExpectedMessageChatCompletionSystemMessageParamContentUnionMember1],
        ]
    ]

    role: Required[Literal["system"]]

    name: str


class TestDataExperimentTestContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataExperimentTestContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["auto", "low", "high"]


class TestDataExperimentTestContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam(
    TypedDict, total=False
):
    image_url: Required[
        TestDataExperimentTestContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL
    ]

    type: Required[Literal["image_url"]]


class TestDataExperimentTestContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio(
    TypedDict, total=False
):
    data: Required[str]

    format: Required[Literal["wav", "mp3"]]


class TestDataExperimentTestContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam(
    TypedDict, total=False
):
    input_audio: Required[
        TestDataExperimentTestContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio
    ]

    type: Required[Literal["input_audio"]]


TestDataExperimentTestContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1: TypeAlias = Union[
    TestDataExperimentTestContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    TestDataExperimentTestContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam,
    TestDataExperimentTestContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam,
]


class TestDataExperimentTestContentExpectedMessageChatCompletionUserMessageParamInput(TypedDict, total=False):
    content: Required[
        Union[
            str,
            Iterable[
                TestDataExperimentTestContentExpectedMessageChatCompletionUserMessageParamInputContentUnionMember1
            ],
        ]
    ]

    role: Required[Literal["user"]]

    name: str


class TestDataExperimentTestContentExpectedMessageChatCompletionAssistantMessageParamInputAudio(TypedDict, total=False):
    id: Required[str]


class TestDataExperimentTestContentExpectedMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataExperimentTestContentExpectedMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam(
    TypedDict, total=False
):
    refusal: Required[str]

    type: Required[Literal["refusal"]]


TestDataExperimentTestContentExpectedMessageChatCompletionAssistantMessageParamInputContentUnionMember1: TypeAlias = Union[
    TestDataExperimentTestContentExpectedMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    TestDataExperimentTestContentExpectedMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam,
]


class TestDataExperimentTestContentExpectedMessageChatCompletionAssistantMessageParamInputFunctionCall(
    TypedDict, total=False
):
    arguments: Required[str]

    name: Required[str]


class TestDataExperimentTestContentExpectedMessageChatCompletionAssistantMessageParamInputToolCallFunction(
    TypedDict, total=False
):
    arguments: Required[str]

    name: Required[str]


class TestDataExperimentTestContentExpectedMessageChatCompletionAssistantMessageParamInputToolCall(
    TypedDict, total=False
):
    id: Required[str]

    function: Required[
        TestDataExperimentTestContentExpectedMessageChatCompletionAssistantMessageParamInputToolCallFunction
    ]

    type: Required[Literal["function"]]


class TestDataExperimentTestContentExpectedMessageChatCompletionAssistantMessageParamInput(TypedDict, total=False):
    role: Required[Literal["assistant"]]

    audio: Optional[TestDataExperimentTestContentExpectedMessageChatCompletionAssistantMessageParamInputAudio]

    content: Union[
        str,
        Iterable[
            TestDataExperimentTestContentExpectedMessageChatCompletionAssistantMessageParamInputContentUnionMember1
        ],
        None,
    ]

    function_call: Optional[
        TestDataExperimentTestContentExpectedMessageChatCompletionAssistantMessageParamInputFunctionCall
    ]

    name: str

    refusal: Optional[str]

    tool_calls: Iterable[TestDataExperimentTestContentExpectedMessageChatCompletionAssistantMessageParamInputToolCall]


class TestDataExperimentTestContentExpectedMessageChatCompletionToolMessageParamContentUnionMember1(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataExperimentTestContentExpectedMessageChatCompletionToolMessageParam(TypedDict, total=False):
    content: Required[
        Union[
            str, Iterable[TestDataExperimentTestContentExpectedMessageChatCompletionToolMessageParamContentUnionMember1]
        ]
    ]

    role: Required[Literal["tool"]]

    tool_call_id: Required[str]


class TestDataExperimentTestContentExpectedMessageChatCompletionFunctionMessageParam(TypedDict, total=False):
    content: Required[Optional[str]]

    name: Required[str]

    role: Required[Literal["function"]]


TestDataExperimentTestContentExpectedMessage: TypeAlias = Union[
    TestDataExperimentTestContentExpectedMessageChatCompletionSystemMessageParam,
    TestDataExperimentTestContentExpectedMessageChatCompletionUserMessageParamInput,
    TestDataExperimentTestContentExpectedMessageChatCompletionAssistantMessageParamInput,
    TestDataExperimentTestContentExpectedMessageChatCompletionToolMessageParam,
    TestDataExperimentTestContentExpectedMessageChatCompletionFunctionMessageParam,
]


class TestDataExperimentTestContentInputDetectionDetectorDataTextMatchingDetector(TypedDict, total=False):
    name: Required[str]

    regex: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["TEXT_MATCHING"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataExperimentTestContentInputDetectionDetectorDataCategoryDetector(TypedDict, total=False):
    category: Required[str]

    name: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CATEGORY"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataExperimentTestContentInputDetectionDetectorDataNaturalLanguageDetector(TypedDict, total=False):
    name: Required[str]

    natural_language_content: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["NATURAL_LANGUAGE"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataExperimentTestContentInputDetectionDetectorDataComparatorDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["EXACT_MATCH", "LANGUAGE_MODEL_SIMILARITY"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["COMPARATOR"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataExperimentTestContentInputDetectionDetectorDataCustomDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["TIERED_DETECTOR"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CUSTOM"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


TestDataExperimentTestContentInputDetectionDetectorData: TypeAlias = Union[
    TestDataExperimentTestContentInputDetectionDetectorDataTextMatchingDetector,
    TestDataExperimentTestContentInputDetectionDetectorDataCategoryDetector,
    TestDataExperimentTestContentInputDetectionDetectorDataNaturalLanguageDetector,
    TestDataExperimentTestContentInputDetectionDetectorDataComparatorDetector,
    TestDataExperimentTestContentInputDetectionDetectorDataCustomDetector,
]


class TestDataExperimentTestContentInputDetection(TypedDict, total=False):
    content_id: Required[str]

    detected: Required[bool]

    detector_id: Required[str]

    end_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    score: Required[float]

    start_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    detector_data: Optional[TestDataExperimentTestContentInputDetectionDetectorData]


class TestDataExperimentTestContentInputMessageChatCompletionSystemMessageParamContentUnionMember1(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataExperimentTestContentInputMessageChatCompletionSystemMessageParam(TypedDict, total=False):
    content: Required[
        Union[
            str, Iterable[TestDataExperimentTestContentInputMessageChatCompletionSystemMessageParamContentUnionMember1]
        ]
    ]

    role: Required[Literal["system"]]

    name: str


class TestDataExperimentTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataExperimentTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["auto", "low", "high"]


class TestDataExperimentTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam(
    TypedDict, total=False
):
    image_url: Required[
        TestDataExperimentTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL
    ]

    type: Required[Literal["image_url"]]


class TestDataExperimentTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio(
    TypedDict, total=False
):
    data: Required[str]

    format: Required[Literal["wav", "mp3"]]


class TestDataExperimentTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam(
    TypedDict, total=False
):
    input_audio: Required[
        TestDataExperimentTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio
    ]

    type: Required[Literal["input_audio"]]


TestDataExperimentTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1: TypeAlias = Union[
    TestDataExperimentTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    TestDataExperimentTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam,
    TestDataExperimentTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam,
]


class TestDataExperimentTestContentInputMessageChatCompletionUserMessageParamInput(TypedDict, total=False):
    content: Required[
        Union[
            str,
            Iterable[TestDataExperimentTestContentInputMessageChatCompletionUserMessageParamInputContentUnionMember1],
        ]
    ]

    role: Required[Literal["user"]]

    name: str


class TestDataExperimentTestContentInputMessageChatCompletionAssistantMessageParamInputAudio(TypedDict, total=False):
    id: Required[str]


class TestDataExperimentTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataExperimentTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam(
    TypedDict, total=False
):
    refusal: Required[str]

    type: Required[Literal["refusal"]]


TestDataExperimentTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1: TypeAlias = Union[
    TestDataExperimentTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    TestDataExperimentTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam,
]


class TestDataExperimentTestContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall(
    TypedDict, total=False
):
    arguments: Required[str]

    name: Required[str]


class TestDataExperimentTestContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction(
    TypedDict, total=False
):
    arguments: Required[str]

    name: Required[str]


class TestDataExperimentTestContentInputMessageChatCompletionAssistantMessageParamInputToolCall(TypedDict, total=False):
    id: Required[str]

    function: Required[
        TestDataExperimentTestContentInputMessageChatCompletionAssistantMessageParamInputToolCallFunction
    ]

    type: Required[Literal["function"]]


class TestDataExperimentTestContentInputMessageChatCompletionAssistantMessageParamInput(TypedDict, total=False):
    role: Required[Literal["assistant"]]

    audio: Optional[TestDataExperimentTestContentInputMessageChatCompletionAssistantMessageParamInputAudio]

    content: Union[
        str,
        Iterable[TestDataExperimentTestContentInputMessageChatCompletionAssistantMessageParamInputContentUnionMember1],
        None,
    ]

    function_call: Optional[
        TestDataExperimentTestContentInputMessageChatCompletionAssistantMessageParamInputFunctionCall
    ]

    name: str

    refusal: Optional[str]

    tool_calls: Iterable[TestDataExperimentTestContentInputMessageChatCompletionAssistantMessageParamInputToolCall]


class TestDataExperimentTestContentInputMessageChatCompletionToolMessageParamContentUnionMember1(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataExperimentTestContentInputMessageChatCompletionToolMessageParam(TypedDict, total=False):
    content: Required[
        Union[str, Iterable[TestDataExperimentTestContentInputMessageChatCompletionToolMessageParamContentUnionMember1]]
    ]

    role: Required[Literal["tool"]]

    tool_call_id: Required[str]


class TestDataExperimentTestContentInputMessageChatCompletionFunctionMessageParam(TypedDict, total=False):
    content: Required[Optional[str]]

    name: Required[str]

    role: Required[Literal["function"]]


TestDataExperimentTestContentInputMessage: TypeAlias = Union[
    TestDataExperimentTestContentInputMessageChatCompletionSystemMessageParam,
    TestDataExperimentTestContentInputMessageChatCompletionUserMessageParamInput,
    TestDataExperimentTestContentInputMessageChatCompletionAssistantMessageParamInput,
    TestDataExperimentTestContentInputMessageChatCompletionToolMessageParam,
    TestDataExperimentTestContentInputMessageChatCompletionFunctionMessageParam,
]


class TestDataExperimentTestContentOutputDetectionDetectorDataTextMatchingDetector(TypedDict, total=False):
    name: Required[str]

    regex: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["TEXT_MATCHING"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataExperimentTestContentOutputDetectionDetectorDataCategoryDetector(TypedDict, total=False):
    category: Required[str]

    name: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CATEGORY"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataExperimentTestContentOutputDetectionDetectorDataNaturalLanguageDetector(TypedDict, total=False):
    name: Required[str]

    natural_language_content: Required[str]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["NATURAL_LANGUAGE"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataExperimentTestContentOutputDetectionDetectorDataComparatorDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["EXACT_MATCH", "LANGUAGE_MODEL_SIMILARITY"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["COMPARATOR"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


class TestDataExperimentTestContentOutputDetectionDetectorDataCustomDetector(TypedDict, total=False):
    name: Required[str]

    type: Required[Literal["TIERED_DETECTOR"]]

    user_id: Required[str]

    id: str

    created: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    detector_type: Literal["CUSTOM"]

    last_updated: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]


TestDataExperimentTestContentOutputDetectionDetectorData: TypeAlias = Union[
    TestDataExperimentTestContentOutputDetectionDetectorDataTextMatchingDetector,
    TestDataExperimentTestContentOutputDetectionDetectorDataCategoryDetector,
    TestDataExperimentTestContentOutputDetectionDetectorDataNaturalLanguageDetector,
    TestDataExperimentTestContentOutputDetectionDetectorDataComparatorDetector,
    TestDataExperimentTestContentOutputDetectionDetectorDataCustomDetector,
]


class TestDataExperimentTestContentOutputDetection(TypedDict, total=False):
    content_id: Required[str]

    detected: Required[bool]

    detector_id: Required[str]

    end_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    score: Required[float]

    start_time: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    detector_data: Optional[TestDataExperimentTestContentOutputDetectionDetectorData]


class TestDataExperimentTestContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataExperimentTestContentOutputMessageChatCompletionSystemMessageParam(TypedDict, total=False):
    content: Required[
        Union[
            str, Iterable[TestDataExperimentTestContentOutputMessageChatCompletionSystemMessageParamContentUnionMember1]
        ]
    ]

    role: Required[Literal["system"]]

    name: str


class TestDataExperimentTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataExperimentTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["auto", "low", "high"]


class TestDataExperimentTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam(
    TypedDict, total=False
):
    image_url: Required[
        TestDataExperimentTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParamImageURL
    ]

    type: Required[Literal["image_url"]]


class TestDataExperimentTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio(
    TypedDict, total=False
):
    data: Required[str]

    format: Required[Literal["wav", "mp3"]]


class TestDataExperimentTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam(
    TypedDict, total=False
):
    input_audio: Required[
        TestDataExperimentTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParamInputAudio
    ]

    type: Required[Literal["input_audio"]]


TestDataExperimentTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1: TypeAlias = Union[
    TestDataExperimentTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    TestDataExperimentTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartImageParam,
    TestDataExperimentTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1ChatCompletionContentPartInputAudioParam,
]


class TestDataExperimentTestContentOutputMessageChatCompletionUserMessageParamInput(TypedDict, total=False):
    content: Required[
        Union[
            str,
            Iterable[TestDataExperimentTestContentOutputMessageChatCompletionUserMessageParamInputContentUnionMember1],
        ]
    ]

    role: Required[Literal["user"]]

    name: str


class TestDataExperimentTestContentOutputMessageChatCompletionAssistantMessageParamInputAudio(TypedDict, total=False):
    id: Required[str]


class TestDataExperimentTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataExperimentTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam(
    TypedDict, total=False
):
    refusal: Required[str]

    type: Required[Literal["refusal"]]


TestDataExperimentTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1: TypeAlias = Union[
    TestDataExperimentTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartTextParam,
    TestDataExperimentTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1ChatCompletionContentPartRefusalParam,
]


class TestDataExperimentTestContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall(
    TypedDict, total=False
):
    arguments: Required[str]

    name: Required[str]


class TestDataExperimentTestContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction(
    TypedDict, total=False
):
    arguments: Required[str]

    name: Required[str]


class TestDataExperimentTestContentOutputMessageChatCompletionAssistantMessageParamInputToolCall(
    TypedDict, total=False
):
    id: Required[str]

    function: Required[
        TestDataExperimentTestContentOutputMessageChatCompletionAssistantMessageParamInputToolCallFunction
    ]

    type: Required[Literal["function"]]


class TestDataExperimentTestContentOutputMessageChatCompletionAssistantMessageParamInput(TypedDict, total=False):
    role: Required[Literal["assistant"]]

    audio: Optional[TestDataExperimentTestContentOutputMessageChatCompletionAssistantMessageParamInputAudio]

    content: Union[
        str,
        Iterable[TestDataExperimentTestContentOutputMessageChatCompletionAssistantMessageParamInputContentUnionMember1],
        None,
    ]

    function_call: Optional[
        TestDataExperimentTestContentOutputMessageChatCompletionAssistantMessageParamInputFunctionCall
    ]

    name: str

    refusal: Optional[str]

    tool_calls: Iterable[TestDataExperimentTestContentOutputMessageChatCompletionAssistantMessageParamInputToolCall]


class TestDataExperimentTestContentOutputMessageChatCompletionToolMessageParamContentUnionMember1(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["text"]]


class TestDataExperimentTestContentOutputMessageChatCompletionToolMessageParam(TypedDict, total=False):
    content: Required[
        Union[
            str, Iterable[TestDataExperimentTestContentOutputMessageChatCompletionToolMessageParamContentUnionMember1]
        ]
    ]

    role: Required[Literal["tool"]]

    tool_call_id: Required[str]


class TestDataExperimentTestContentOutputMessageChatCompletionFunctionMessageParam(TypedDict, total=False):
    content: Required[Optional[str]]

    name: Required[str]

    role: Required[Literal["function"]]


TestDataExperimentTestContentOutputMessage: TypeAlias = Union[
    TestDataExperimentTestContentOutputMessageChatCompletionSystemMessageParam,
    TestDataExperimentTestContentOutputMessageChatCompletionUserMessageParamInput,
    TestDataExperimentTestContentOutputMessageChatCompletionAssistantMessageParamInput,
    TestDataExperimentTestContentOutputMessageChatCompletionToolMessageParam,
    TestDataExperimentTestContentOutputMessageChatCompletionFunctionMessageParam,
]


class TestDataExperimentTestContent(TypedDict, total=False):
    id: str

    algorithm: Optional[str]

    behavior: Optional[TestDataExperimentTestContentBehavior]

    content_group_ids: Optional[List[str]]

    content_type: Optional[Literal["BASE", "TEST", "EXPERIMENT"]]

    end: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    expected_messages: Optional[Iterable[TestDataExperimentTestContentExpectedMessage]]

    generate_end_time: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    generate_start_time: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    input_detections: Optional[Iterable[TestDataExperimentTestContentInputDetection]]

    input_messages: Optional[Iterable[TestDataExperimentTestContentInputMessage]]

    metadata: Optional[object]

    output_detections: Optional[Iterable[TestDataExperimentTestContentOutputDetection]]

    output_messages: Optional[Iterable[TestDataExperimentTestContentOutputMessage]]

    start: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    status: Optional[Literal["GENERATING_CONTENT", "AWAITING_RESPONSE", "ANALYZING_RESPONSE", "COMPLETE", "DISCARDED"]]
    """Status for a single content object in a test."""

    test_id: Optional[str]

    time: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    user_id: Optional[str]


class TestDataExperimentTestTargetModelGenerationParams(TypedDict, total=False):
    id: str

    max_tokens: Optional[int]

    system_message: Optional[str]

    temperature: Optional[float]

    user_id: Optional[str]


class TestDataExperimentTestTargetModel(TypedDict, total=False):
    model_id: Required[str]

    id: str

    api_key: Optional[str]

    base_url: Optional[str]

    generation_params: Optional[TestDataExperimentTestTargetModelGenerationParams]

    model_provider: Optional[str]

    model_type: Optional[Literal["STANDARD", "CUSTOM"]]

    name: Optional[str]

    time: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    user_id: Optional[str]


class TestDataExperimentTest(TypedDict, total=False):
    name: Required[str]

    user_id: Required[Optional[str]]

    id: str

    algorithm_status: Optional[Iterable[TestDataExperimentTestAlgorithmStatus]]

    content: Optional[Iterable[TestDataExperimentTestContent]]

    content_group_ids: Optional[List[str]]

    dataset_id: Optional[str]

    detector_ids: Optional[List[str]]

    end_date: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    start_date: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    status: Optional[Literal["COMPLETE", "ERROR", "RUNNING", "STEP_COMPLETE", "STOPPED"]]
    """Status for the overall test."""

    target_model: Optional[TestDataExperimentTestTargetModel]

    test_type: Literal["EXPERIMENT"]


TestData: TypeAlias = Union[TestDataRedTeamingTest, TestDataFuzzingTest, TestDataDataReplayTest, TestDataExperimentTest]
