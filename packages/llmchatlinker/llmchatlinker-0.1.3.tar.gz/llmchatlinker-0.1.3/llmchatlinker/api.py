# llmchatlinker/api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from .client import LLMChatLinkerClient

app = FastAPI(
    title="LLMChatLinker API",
    description="API for managing chat interactions with LLMs",
    version="1.0.0"
)

client = LLMChatLinkerClient()

class BaseResponse(BaseModel):
    status: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)

class DataResponse(BaseResponse):
    data: Dict[str, Any]

# User Management Models
class UserCreateRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=30, pattern=r'^[a-zA-Z][a-zA-Z0-9_]{2,29}$')
    display_name: Optional[str] = Field(None, max_length=50)
    profile: Optional[str] = None

class UserUpdateRequest(BaseModel):
    user_id: str
    username: Optional[str] = Field(None, min_length=3, max_length=30, pattern=r'^[a-zA-Z][a-zA-Z0-9_]{2,29}$')
    display_name: Optional[str] = Field(None, max_length=50)
    profile: Optional[str] = None

class UserResponse(DataResponse):
    data: Dict[str, Any]

# Chat Management Models
class ChatCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    user_ids: List[str] = Field(..., min_items=1)

class ChatUpdateRequest(BaseModel):
    chat_id: str
    title: str = Field(..., min_length=1, max_length=100)

class ChatResponse(DataResponse):
    data: Dict[str, Any]

# LLM Provider Management Models
class LLMProviderAddRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    api_endpoint: str = Field(..., max_length=255)
    api_key: Optional[str] = Field(None, max_length=255)

class LLMProviderUpdateRequest(BaseModel):
    provider_id: str
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    api_endpoint: Optional[str] = Field(None, max_length=255)

# LLM Management Models
class LLMAddRequest(BaseModel):
    provider_id: str
    llm_name: str = Field(..., min_length=1, max_length=100)

class LLMUpdateRequest(BaseModel):
    llm_id: str
    llm_name: str = Field(..., min_length=1, max_length=100)

class LLMResponseGenerateRequest(BaseModel):
    user_id: str
    chat_id: str
    provider_id: str
    llm_id: str
    user_input: str = Field(..., min_length=1)

class LLMResponseRegenerateRequest(BaseModel):
    message_id: str

# User Management Endpoints
@app.post("/user/create", response_model=UserResponse, tags=["User Management"])
async def create_user(request: UserCreateRequest):
    """Create a new user with a username and profile."""
    return client.create_user(request.username, request.display_name, request.profile)

@app.put("/user/update", response_model=UserResponse, tags=["User Management"])
async def update_user(request: UserUpdateRequest):
    """Update an existing user's username and profile."""
    return client.update_user(request.user_id, request.username, request.display_name, request.profile)

@app.delete("/user/delete", response_model=BaseResponse, tags=["User Management"])
async def delete_user(request: UserUpdateRequest):
    """Delete a user by user ID."""
    return client.delete_user(request.user_id)

@app.get("/user/list", response_model=DataResponse, tags=["User Management"])
async def list_users():
    """List all users."""
    return client.list_users()

@app.get("/user/{username}", response_model=UserResponse, tags=["User Management"])
async def get_user(username: str):
    """Get user details by username."""
    return client.get_user(username=username)

@app.get("/user/id/{user_id}", response_model=UserResponse, tags=["User Management"])
async def get_user_by_id(user_id: str):
    """Get user details by user ID."""
    return client.get_user(user_id=user_id)

@app.post("/user/{user_id}/instruction-recording/enable", response_model=BaseResponse, tags=["User Management"])
async def enable_instruction_recording(user_id: str):
    """Enable instruction recording for a user."""
    return client.enable_instruction_recording(user_id)

@app.post("/user/{user_id}/instruction-recording/disable", response_model=BaseResponse, tags=["User Management"])
async def disable_instruction_recording(user_id: str):
    """Disable instruction recording for a user."""
    return client.disable_instruction_recording(user_id)

@app.get("/user/{user_id}/instructions", response_model=DataResponse, tags=["User Management"])
async def list_user_instructions(user_id: str):
    """List instruction records for a user."""
    return client.list_user_instructions(user_id)

@app.delete("/user/{user_id}/instructions", response_model=BaseResponse, tags=["User Management"])
async def delete_user_instructions(user_id: str):
    """Delete all instruction records for a user."""
    return client.delete_user_instructions(user_id)

# Chat Management Endpoints
@app.post("/chat/create", response_model=ChatResponse, tags=["Chat Management"])
async def create_chat(request: ChatCreateRequest):
    """Create a new chat with a title and list of user_ids."""
    return client.create_chat(request.title, request.user_ids)

@app.put("/chat/update", response_model=ChatResponse, tags=["Chat Management"])
async def update_chat(request: ChatUpdateRequest):
    """Update an existing chat's title."""
    return client.update_chat(request.chat_id, request.title)

@app.delete("/chat/delete", response_model=BaseResponse, tags=["Chat Management"])
async def delete_chat(request: ChatUpdateRequest):
    """Delete a chat by chat ID."""
    return client.delete_chat(request.chat_id)

@app.get("/chat/list", response_model=DataResponse, tags=["Chat Management"])
async def list_chats():
    """List all chats."""
    return client.list_chats()

@app.get("/chat/id/{chat_id}", response_model=DataResponse, tags=["Chat Management"])
async def get_chat(chat_id: str):
    """Get chat details by chat ID."""
    return client.get_chat(chat_id)

@app.get("/chat/user/{user_id}", response_model=DataResponse, tags=["Chat Management"])
async def list_user_chats(user_id: str):
    """List all chats for a user by user ID."""
    return client.list_user_chats(user_id)

# LLM Provider Management Endpoints
@app.post("/llm_provider/add", response_model=DataResponse, tags=["LLM Provider Management"])
async def add_llm_provider(request: LLMProviderAddRequest):
    """Add a new LLM provider with a name and API endpoint."""
    return client.add_llm_provider(request.name, request.api_endpoint, request.api_key)

@app.put("/llm_provider/update", response_model=DataResponse, tags=["LLM Provider Management"])
async def update_llm_provider(request: LLMProviderUpdateRequest):
    """Update an existing LLM provider's name and API endpoint."""
    return client.update_llm_provider(request.provider_id, request.name, request.api_endpoint)

@app.delete("/llm_provider/delete", response_model=BaseResponse, tags=["LLM Provider Management"])
async def delete_llm_provider(request: LLMProviderUpdateRequest):
    """Delete an LLM provider by provider ID."""
    return client.delete_llm_provider(request.provider_id)

@app.get("/llm_provider/list", response_model=DataResponse, tags=["LLM Provider Management"])
async def list_llm_providers():
    """List all LLM providers."""
    return client.list_llm_providers()

# LLM Management Endpoints
@app.post("/llm/add", response_model=DataResponse, tags=["LLM Management"])
async def add_llm(request: LLMAddRequest):
    """Add a new LLM with a provider name and LLM name."""
    return client.add_llm(request.provider_id, request.llm_name)

@app.put("/llm/update", response_model=DataResponse, tags=["LLM Management"])
async def update_llm(request: LLMUpdateRequest):
    """Update an existing LLM's name."""
    return client.update_llm(request.llm_id, request.llm_name)

@app.delete("/llm/delete", response_model=BaseResponse, tags=["LLM Management"])
async def delete_llm(request: LLMUpdateRequest):
    """Delete an LLM by LLM ID."""
    return client.delete_llm(request.llm_id)

@app.get("/llm/list", response_model=DataResponse, tags=["LLM Management"])
async def list_llms():
    """List all LLMs."""
    return client.list_llms()

@app.get("/llm/llm_provider/{provider_id}", response_model=DataResponse, tags=["LLM Management"])
async def list_llms_by_provider(provider_id: str):
    """List all LLMs for a provider by provider ID."""
    return client.list_llms_by_provider(provider_id)

# LLM Response Management Endpoints
@app.post("/llm/response_generate", response_model=DataResponse, tags=["LLM Response Management"])
async def generate_llm_response(request: LLMResponseGenerateRequest):
    """Generate a response from an LLM based on user input."""
    return client.generate_llm_response(request.user_id, request.chat_id, request.provider_id, request.llm_id, request.user_input)

@app.post("/llm/response_regenerate", response_model=DataResponse, tags=["LLM Response Management"])
async def regenerate_llm_response(request: LLMResponseRegenerateRequest):
    """Regenerate a response from an LLM based on a previous message."""
    return client.regenerate_llm_response(request.message_id)