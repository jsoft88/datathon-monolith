from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Incoming chatbot payload from a connected client."""

    message: str = Field(..., min_length=1, description="User message for the chatbot")
    conversation_id: str | None = Field(
        default=None,
        description="Optional identifier used to keep conversation context",
    )
    customer_id: str | None = Field(
        default=None,
        max_length=20,
        description="Session customer ID; must match the customer found by document number",
    )


class ChatResponse(BaseModel):
    """Outgoing chatbot payload sent back to the client."""

    reply: str
    conversation_id: str | None = None
