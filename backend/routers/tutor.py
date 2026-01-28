import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
import uuid

from chat_utils import get_bot_response

router = APIRouter()

CHAT_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "chat_history_tutor_api.json")


class ChatMessage(BaseModel):
    message: str
    chat_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    chat_id: str
    sources: List[str] = []


def load_chats():
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as f:
            return json.load(f)
    return {}


def save_chats(chats):
    with open(CHAT_FILE, "w") as f:
        json.dump(chats, f, indent=2)


@router.get("/history")
def get_all_chats():
    """Get all chat sessions"""
    chats = load_chats()
    return {
        "chats": [
            {"id": chat_id, "message_count": len(data.get("messages", []))}
            for chat_id, data in chats.items()
        ]
    }


@router.get("/history/{chat_id}")
def get_chat_history(chat_id: str):
    """Get messages for a specific chat"""
    chats = load_chats()
    if chat_id not in chats:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"chat_id": chat_id, "messages": chats[chat_id].get("messages", [])}


@router.post("/new")
def create_new_chat():
    """Create a new chat session"""
    chats = load_chats()
    chat_id = str(uuid.uuid4())[:8]
    chats[chat_id] = {"messages": []}
    save_chats(chats)
    return {"chat_id": chat_id, "message": "New chat created"}


@router.post("/chat")
def send_message(request: ChatMessage):
    """Send a message and get a response"""
    chats = load_chats()
    
    chat_id = request.chat_id
    if not chat_id or chat_id not in chats:
        chat_id = str(uuid.uuid4())[:8]
        chats[chat_id] = {"messages": []}
    
    current_chat = chats[chat_id]
    
    try:
        bot_response = get_bot_response(request.message, current_chat)
        
        current_chat["messages"].append({
            "user": request.message,
            "bot": bot_response
        })
        save_chats(chats)
        
        return ChatResponse(
            response=bot_response,
            chat_id=chat_id,
            sources=[]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/chat/{chat_id}")
def delete_chat(chat_id: str):
    """Delete a chat session"""
    chats = load_chats()
    if chat_id not in chats:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    del chats[chat_id]
    save_chats(chats)
    return {"message": f"Chat {chat_id} deleted"}
