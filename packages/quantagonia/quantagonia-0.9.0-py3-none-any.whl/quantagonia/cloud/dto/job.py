# ruff: noqa: N815 allow camelCase because this is the model for the job query that requires these fields

from dataclasses import dataclass, field
from typing import List


@dataclass(init=True, repr=True, eq=True)
class JobDto:
    context: str = ""
    jobId: str = ""
    specs: str = ""
    tag: str = ""
    origin: str = ""
    status: str = ""
    messages: List[str] = field(default_factory=list)
    error: str = ""
    problemType: str = ""
    processor: str = ""
    problemFiles: List[str] = field(default_factory=list)
    specFiles: List[str] = field(default_factory=list)
