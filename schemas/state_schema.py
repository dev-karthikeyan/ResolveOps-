from typing import TypedDict , List , Optional

class ResolveOpsState(TypedDict) :

    # Ticket information
    ticket_id : str 
    tickt_title : str 
    tickt_discription : str

    # Classification
    category: Optional[str]
    priority: Optional[str]

    # RAG
    retrieved_docs: List[str]

    # Investigation
    investigation_notes: List[str]

    # Root Cause
    root_cause: Optional[str]

    # Reflection
    reflection_feedback: Optional[str]

    # Solution
    solution: Optional[str]

    # Approval
    approved: Optional[bool]

    # Jira Update
    jira_comment: Optional[str]

    # Workflow Status
    status: Optional[str]