# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["TestingStartResponse"]


class TestingStartResponse(BaseModel):
    __test__ = False
    status: Literal["COMPLETE", "ERROR", "RUNNING", "STEP_COMPLETE", "STOPPED"]
    """Status for the overall test."""

    test_id: str
