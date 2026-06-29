from pydantic import BaseModel , Field
class TicketSchema(BaseModel):
    ticket_id: str = Field(
        ...,
        description="Unique ticket identifier")

    title: str = Field(
        ...,
        description="Short summary of the ticket"
    )

    description: str = Field(
        ...,
        description="Detailed description of the issue"
    )

    reporter: str = Field(
        ...,
        description="Person who created the ticket"
    )

    priority: str = Field(
        default="Medium",
        description="Ticket priority"
    )

    status: str = Field(
        default="OPEN",
        description="Current ticket status"
    )

    