"""
Chat router with JWT dependency for the AI chatbot integration.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional, Union
from pydantic import BaseModel
from dependencies.auth import get_current_user, security
from fastapi.security import HTTPAuthorizationCredentials


router = APIRouter(
    prefix="/api/{user_id}",
    tags=["chat"],
    # Remove the global dependency and handle auth per endpoint
)


class ChatRequest(BaseModel):
    """
    Request model for chat endpoint.
    """
    conversation_id: Optional[Union[str, int]] = None
    message: str

    def __init__(self, **data):
        # Convert conversation_id to string if it's an integer
        if 'conversation_id' in data and data['conversation_id'] is not None:
            data['conversation_id'] = str(data['conversation_id'])
        super().__init__(**data)


class ChatResponse(BaseModel):
    """
    Response model for chat endpoint.
    """
    conversation_id: str  # Keep as string to match frontend expectations
    response: str
    tool_calls: list = []


import traceback

@router.post("/chat", response_model=ChatResponse)
async def process_chat_message(
    user_id: str,
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Process a chat message from the user and return AI response.

    Args:
        user_id: The ID of the user making the request (from URL path)
        request: The chat request containing the message and optional conversation_id
        current_user: The authenticated user from the JWT token

    Returns:
        ChatResponse with conversation_id, AI response, and any tool calls executed
    """

    print(f"DEBUG: Chat endpoint called - user_id: {user_id}, current_user: {current_user}")
    
    # Verify user ID match - convert both to string for comparison to handle different formats
    token_user_id_str = str(current_user["user_id"])
    url_user_id_str = str(user_id)
    
    if token_user_id_str != url_user_id_str:
        print(f"DEBUG: User ID mismatch - token: {token_user_id_str}, URL: {url_user_id_str}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied: user ID mismatch. Token user_id: {token_user_id_str}, URL user_id: {url_user_id_str}"
        )
    
    print(f"DEBUG: User ID match confirmed - both: {url_user_id_str}")
    
    try:
        # Import and process
        from agents.todo_agent import process_chat_request
        response = await process_chat_request(user_id, request)
        return ChatResponse(**response)
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        # Log full traceback
        error_details = traceback.format_exc()
        print(f"DEBUG: Chat endpoint error: {error_details}")
        
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


# Temporary debug endpoints to test Gemini API and database
@router.get("/debug-gemini-test")
async def debug_gemini_test():
    """Test Gemini API connection directly"""
    try:
        import google.generativeai as genai
        import os
        
        api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
        if not api_key:
            return {"status": "Error", "message": "No API key found"}
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        # Test a simple generation
        response = model.generate_content("Say hello")
        return {"status": "Gemini OK", "response_preview": str(response.text)[:50]}
    except Exception as e:
        return {"status": "Gemini Error", "error": str(e)}


@router.get("/debug-db-test")
async def debug_db_test(user_id: str, current_user: dict = Depends(get_current_user)):
    """Test basic database operations"""
    try:
        from dependencies.database import get_session_context
        from models.conversation import Conversation
        from sqlmodel import select

        user_id_int = int(user_id)
        print(f"DEBUG: Testing DB with user_id: {user_id_int}")

        # Use the same approach as the main code
        with get_session_context() as session:
            # Try to count conversations for this user
            statement = select(Conversation).where(Conversation.user_id == user_id_int)
            results = session.exec(statement).all()
            count = len(results)
            return {"status": "DB OK", "user_id": user_id_int, "conversation_count": count}
    except Exception as e:
        return {"status": "DB Error", "error": str(e)}


@router.get("/debug-token-test")
async def debug_token_test(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Test token decoding with current configuration"""
    token = credentials.credentials
    from dependencies.auth import SECRET_KEY
    from jose import jwt
    
    try:
        # Try to decode with HS256
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"status": "Token decoded successfully", "payload": payload}
    except Exception as e:
        return {"status": "Token decode failed", "error": str(e)}