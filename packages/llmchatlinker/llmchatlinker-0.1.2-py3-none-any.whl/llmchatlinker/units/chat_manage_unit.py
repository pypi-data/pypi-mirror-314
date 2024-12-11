# llmchatlinker/units/chat_manage_unit.py

import logging
from typing import Dict, Any, List, Optional
from .database_manage_unit import DatabaseManageUnit, NotFoundError, ValidationError

logger = logging.getLogger(__name__)

class ChatManageUnit:
    """Handles chat-related operations and instructions"""

    def __init__(self, database_manage_unit: DatabaseManageUnit):
        self.db = database_manage_unit
        self.handlers = {
            'CHAT_CREATE': self.create_chat,
            'CHAT_UPDATE': self.update_chat,
            'CHAT_DELETE': self.delete_chat,
            'CHAT_LOAD': self.get_chat,
            'CHAT_LIST': self.list_chats,
            'CHAT_LIST_BY_USER': self.list_chats_by_user
        }

    def handle_instruction(self, instruction_type: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Route instruction to appropriate handler"""
        handler = self.handlers.get(instruction_type)
        if not handler:
            return self._error_response("Invalid instruction type")

        try:
            return handler(data or {})
        except (NotFoundError, ValidationError) as e:
            return self._error_response(str(e))
        except Exception as e:
            return self._error_response(f"Operation failed: {str(e)}")
    
    def create_chat(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new chat"""
        if not self._validate_data(data, ['title', 'user_ids']):
            return self._error_response("Missing required fields: title and user_ids")

        try:
            user_public_ids = [
                user.get('user_id') for user_id in data['user_ids']
                if (user := self.db.get_user_by_public_id(user_id))
            ]
            
            if len(user_public_ids) != len(data['user_ids']):
                return self._error_response("Invalid user IDs provided")
            
            chat_data = self.db.create_chat(title=data['title'], user_public_ids=user_public_ids)
            return self._success_response("Chat created successfully", {"chat": chat_data})
        except Exception as e:
            return self._error_response(f"Failed to create chat: {str(e)}")

    def update_chat(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update existing chat"""
        if not self._validate_data(data, ['chat_id', 'title']):
            return self._error_response("Chat ID is required")

        try:
            public_id = data['chat_id']
            chat_data = self.db.update_chat(public_id, title=data['title'])
            return self._success_response("Chat updated successfully", {"chat": chat_data})
        except NotFoundError as e:
            return self._error_response(str(e))
        except Exception as e:
            return self._error_response(f"Failed to update chat: {str(e)}")
    
    def delete_chat(self, data: Dict[str, Any]) -> None:
        """Delete chat"""
        if not self._validate_data(data, ['chat_id']):
            return self._error_response("Chat ID is required")

        try:
            public_id = data['chat_id']
            self.db.delete_chat(public_id)
            return self._success_response("Chat deleted successfully")
        except NotFoundError as e:
            return self._error_response(str(e))
        except Exception as e:
            return self._error_response(f"Failed to delete chat: {str(e)}")
    
    def list_chats(self, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List all chats"""
        try:
            chat_data = self.db.get_all_chats()
            return self._success_response("Chats retrieved successfully", {"chats": chat_data})
        except Exception as e:
            return self._error_response(f"Failed to list chats: {str(e)}")

    def list_chats_by_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """List chats for specific user"""
        if not self._validate_data(data, ['user_id']):
            return self._error_response("User ID is required")

        try:
            chat_data = self.db.get_chats_by_user(data['user_id'])
            return self._success_response(f"Chats retrieved for user {data['user_id']}", {"chats": chat_data})
        except Exception as e:
            return self._error_response(f"Failed to list user chats: {str(e)}")

    def get_chat(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get chat details"""
        if not self._validate_data(data, ['chat_id']):
            return self._error_response("Chat ID is required")

        try:
            public_id = data['chat_id']
            chat_data = self.db.get_chat_by_public_id(public_id)
            return self._success_response("Chat loaded successfully", {"chat": chat_data})
        except NotFoundError as e:
            return self._error_response(str(e))
        except Exception as e:
            return self._error_response(f"Failed to load chat: {str(e)}")

    @staticmethod
    def _validate_data(data: Dict[str, Any], required_keys: List[str]) -> bool:
        """Validate presence of required keys in data"""
        return data is not None and all(key in data for key in required_keys)

    @staticmethod
    def _success_response(message: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Format success response."""
        response = {"status": "success", "message": message, "data": data or {}}
        return response

    @staticmethod
    def _error_response(message: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Format error response."""
        return {"status": "error", "message": message, "data": data or {}}