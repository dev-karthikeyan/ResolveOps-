from typing import TypedDict, Optional

class ResolveOpsState(TypedDict):

    ticket: dict

    classification: Optional[dict]

    retrieved_evidence: Optional[dict]

    investigation: Optional[dict]

    root_cause: Optional[dict]

    reflection: Optional[dict]

    solution: Optional[dict]

    approved: Optional[bool]

    status: Optional[str]