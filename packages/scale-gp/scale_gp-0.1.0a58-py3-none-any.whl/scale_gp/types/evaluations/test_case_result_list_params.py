# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, TypedDict

__all__ = ["TestCaseResultListParams"]


class TestCaseResultListParams(TypedDict, total=False):
    account_id: Optional[str]

    include_archived: bool

    limit: int
    """Maximum number of artifacts to be returned by the given endpoint.

    Defaults to 100 and cannot be greater than 10k.
    """

    page: int
    """Page number for pagination to be returned by the given endpoint.

    Starts at page 1
    """

    view: Optional[List[Literal["AnnotationResults", "Metrics", "Task", "TestCaseVersion", "Trace"]]]
