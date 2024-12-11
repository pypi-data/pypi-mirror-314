# llmchatlinker/units/user_manage_unit.py

from typing import Dict, Any, List, Optional
import re
from .database_manage_unit import DatabaseManageUnit, NotFoundError, ValidationError

class UserManageUnit:
    def __init__(self, database_manage_unit: DatabaseManageUnit):
        self.db = database_manage_unit
        self.handlers = {
            'USER_CREATE': self.create_user,
            'USER_UPDATE': self.update_user,
            'USER_DELETE': self.delete_user,
            'USER_LIST': self.list_users,
            'USER_GET': self.get_user,
            'USER_INSTRUCTION_RECORDING_ENABLE': self.enable_instruction_recording,
            'USER_INSTRUCTION_RECORDING_DISABLE': self.disable_instruction_recording,
            'USER_INSTRUCTION_RECORDS_DELETE': self.delete_instruction_records,
            'USER_INSTRUCTION_RECORDS_LIST': self.list_instruction_records,
        }

    def handle_instruction(self, instruction_type, data):
        handler = self.handlers.get(instruction_type)
        if not handler:
            return self._error_response("Invalid instruction type")

        try:
            # Special handling for instruction recording and records management
            if instruction_type.startswith(('USER_INSTRUCTION_RECORDING_', 'USER_INSTRUCTION_RECORDS_')):
                return handler(data, instruction_type)
                
            # For other handlers, just pass the data
            return handler(data)
        except (NotFoundError, ValidationError) as e:
            return self._error_response(str(e))
        except Exception as e:
            return self._error_response(f"Operation failed: {str(e)}")

    def create_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user."""
        if not self._validate_data(data, ['username']):
            return self._error_response("Username is required")

        username = data.get('username', '').lower()
        if not self._is_valid_username(username):
            return self._error_response("Invalid username format")
        display_name = data.get('display_name', username)
        profile = data.get('profile')

        try:
            user_data = self.db.create_user(username=username, display_name=display_name, profile=profile)
            return self._success_response("User created successfully", {"user": user_data})
        except ValidationError as e:
            return self._error_response(str(e))
        except Exception as e:
            return self._error_response(f"Failed to create user: {str(e)}")

    def update_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update existing user."""
        if not self._validate_data(data, ['user_id']):
            return self._error_response("User ID is required")
        
        if 'username' in data:
            username = data['username'].lower()
            if not self._is_valid_username(username):
                return self._error_response("Invalid username format")
            data['username'] = username

        try:
            user_id = data.pop('user_id')
            user_data = self.db.update_user(user_id, **data)
            return self._success_response("User updated successfully", {"user": user_data})
        except NotFoundError as e:
            return self._error_response(str(e))
        except Exception as e:
            return self._error_response(f"Failed to update user: {str(e)}")
    
    def delete_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Delete user."""
        if not self._validate_data(data, ['user_id']):
            return self._error_response("User ID is required")
        
        try:
            self.db.delete_user(data['user_id'])
            return self._success_response("User deleted successfully")
        except NotFoundError as e:
            return self._error_response(str(e))
        except Exception as e:
            return self._error_response(f"Failed to delete user: {str(e)}")
    
    def list_users(self, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List all users."""
        try:
            users = self.db.get_all_users()
            return self._success_response("Users retrieved successfully", {"users": users})
        except Exception as e:
            return self._error_response(f"Failed to list users: {str(e)}")
    
    def get_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get user by username or ID."""
        try:
            user = None
            if 'username' in data:
                user = self.db.get_user_by_username(data['username'])
            elif 'user_id' in data:
                user = self.db.get_user_by_public_id(data['user_id'])
            else:
                return self._error_response("Username or user ID is required")

            if not user:
                return self._error_response("User not found")
            
            return self._success_response("User retrieved successfully", {"user": user})
        except Exception as e:
            return self._error_response(f"Failed to get user: {str(e)}")
    
    def enable_instruction_recording(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Enable instruction recording for user."""
        if not self._validate_data(data, ['user_id']):
            return self._error_response("Missing required field: user_id")
        
        public_id = data.get('user_id')
        if not public_id:
            return self._error_response("User ID is required")

        try:
            self.db.enable_instruction_recording(public_id)
            return self._success_response("Instruction recording enabled")
        except NotFoundError as e:
            return self._error_response(str(e))
        except Exception as e:
            return self._error_response(str(e))
    
    def disable_instruction_recording(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Disable instruction recording for user."""
        if not self._validate_data(data, ['user_id']):
            return self._error_response("User ID is required")
        
        try:
            self.db.disable_instruction_recording(data['user_id'])
            return self._success_response("Instruction recording disabled")
        except NotFoundError as e:
            return self._error_response(str(e))
        except Exception as e:
            return self._error_response(str(e))
    
    def delete_instruction_records(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Delete instruction records for user."""
        if not self._validate_data(data, ['user_id']):
            return self._error_response("User ID is required")
        
        try:
            self.db.delete_instruction_records(data['user_id'])
            return self._success_response("Instruction records deleted")
        except NotFoundError as e:
            return self._error_response(str(e))
        except Exception as e:
            return self._error_response(str(e))
    
    def list_instruction_records(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """List instruction records for user."""
        if not self._validate_data(data, ['user_id']):
            return self._error_response("User ID is required")
        
        try:
            records = self.db.get_instruction_records(data['user_id'])
            return self._success_response("Instruction records retrieved", {"records": records})
        except NotFoundError as e:
            return self._error_response(str(e))
        except Exception as e:
            return self._error_response(str(e))

    @staticmethod
    def _is_valid_username(username: str) -> bool:
        """Validate username format."""
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]{2,29}$'
        return bool(re.match(pattern, username))

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
