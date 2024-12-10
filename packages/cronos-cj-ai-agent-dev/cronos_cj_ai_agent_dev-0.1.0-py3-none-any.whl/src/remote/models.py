from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Any
from datetime import datetime
from pydantic import BaseModel


@dataclass
class ServerInfo:
    """Information about a processing server"""

    url: str
    capabilities: Set[str]
    priority: int = 0


class Function(BaseModel):
    name: str
    arguments: str


class FunctionCall(BaseModel):
    id: str
    type: str
    function: Dict[str, str]  # Changed from Function to Dict

    class Config:
        extra = "allow"


class FunctionResult(BaseModel):
    """Result of function execution"""

    tool_call_id: str
    output: str


class ExecuteRequest(BaseModel):
    """Request format for function execution"""

    function_calls: List[FunctionCall]
    context: Dict[str, Any]


class ExecuteResponse(BaseModel):
    """Response format for function execution"""

    outputs: List[FunctionResult]
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class MessageContext:
    """Context for message processing"""

    chat_id: str
    sender_id: str
    message: str
    is_group: bool = False
    bot_name: Optional[str] = None
    history: Optional[List[Dict]] = None
    metadata: Optional[Dict] = None


@dataclass
class ProcessedMessage:
    """Result of message processing"""

    response: str
    updated_history: List[Dict]
    error: Optional[str] = None
    metadata: Optional[Dict] = None
    timestamp: datetime = datetime.utcnow()


class MessageRequestAPI(BaseModel):
    """API request format"""

    chat_id: str
    sender_id: str
    message: str
    is_group: bool = False
    bot_name: Optional[str] = None
    metadata: Optional[Dict] = None


class MessageResponseAPI(BaseModel):
    """API response format"""

    response: str
    history: List[Dict]
    error: Optional[str] = None
    metadata: Optional[Dict] = None
    timestamp: str
