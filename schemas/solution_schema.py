from pydantic import BaseModel , Field

class SolutionSchema(BaseModel) :
    root_cause : str = Field(
        ...,
        description= "idenfied the root cause of the problem"
    )

    solution: str = Field(
        ...,
        description="Recommended solution for the issue"
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1"
    )

    jira_comment: str = Field(
        ...,
        description="Comment to be posted on the Jira ticket"
    )