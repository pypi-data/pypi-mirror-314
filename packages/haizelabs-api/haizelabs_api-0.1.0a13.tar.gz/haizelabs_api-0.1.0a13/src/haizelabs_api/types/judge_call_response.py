# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime

from .._models import BaseModel

__all__ = ["JudgeCallResponse"]


class JudgeCallResponse(BaseModel):
    content_id: str

    detected: bool

    end_time: datetime

    judge_id: str

    score: float

    start_time: datetime
