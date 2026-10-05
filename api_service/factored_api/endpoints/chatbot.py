import json
import uuid

from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect
from pydantic import ValidationError
from starlette.websockets import WebSocketState

from factored_api.ai.chatbot import generate_reply
from factored_api.models.chat import ChatRequest, ChatResponse

import traceback
router = APIRouter(tags=["chatbot"])


@router.websocket("/ws/chat")
async def chatbot_websocket(
    websocket: WebSocket,
    customer_id: str | None = Query(default=None),
    conversation_id: str | None = Query(default=None),
) -> None:
    """Exchange user messages with the dispute agent over a persistent session."""
    await websocket.accept()
    session_conversation_id = conversation_id or str(uuid.uuid4())
    session_customer_id = customer_id

    await _send_payload(
        websocket,
        ChatResponse(
            reply=(
                "Session started. Send your document number so I can look up your profile, "
                "then describe the transaction you want to dispute."
            ),
            conversation_id=session_conversation_id,
        ),
    )

    try:
        while True:
            payload = await _receive_payload(websocket)
            request = _session_request(payload, session_conversation_id, session_customer_id)
            if isinstance(request, dict):
                await websocket.send_json(request)
                continue

            try:
                response = await generate_reply(request)
            except Exception:
                print(traceback.format_exc())
                await websocket.send_json(
                    {
                        "error": "agent_error",
                        "detail": "The assistant could not process that message.",
                        "conversation_id": session_conversation_id,
                    }
                )
                continue

            session_conversation_id = response.conversation_id or session_conversation_id
            session_customer_id = session_customer_id or request.customer_id
            await _send_payload(websocket, response)
    except WebSocketDisconnect:
        return


async def handle_chat_request(payload: dict) -> dict:
    """Validate an incoming chat payload and return a serializable reply."""
    try:
        request = ChatRequest.model_validate(payload)
    except ValidationError as exc:
        return {"error": "invalid_request", "detail": exc.errors(include_url=False)}

    response: ChatResponse = await generate_reply(request)
    return response.model_dump()


async def _receive_payload(websocket: WebSocket) -> dict:
    raw = await websocket.receive_text()
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return {"message": raw}
    if isinstance(payload, str):
        return {"message": payload}
    if isinstance(payload, dict):
        return payload
    return {"message": str(payload)}


def _session_request(
    payload: dict,
    conversation_id: str,
    customer_id: str | None,
) -> ChatRequest | dict:
    data = dict(payload)
    data.setdefault("conversation_id", conversation_id)
    if customer_id and not data.get("customer_id"):
        data["customer_id"] = customer_id
    try:
        return ChatRequest.model_validate(data)
    except ValidationError as exc:
        return {
            "error": "invalid_request",
            "detail": exc.errors(include_url=False),
            "conversation_id": conversation_id,
        }


async def _send_payload(websocket: WebSocket, response: ChatResponse) -> None:
    if websocket.client_state != WebSocketState.CONNECTED:
        raise WebSocketDisconnect()
    await websocket.send_json(response.model_dump())
