# llmchatlinker/units/llm_manage_unit.py

import logging
from typing import Dict, Any, Optional, List
import requests
import json
from datetime import datetime
from .database_manage_unit import DatabaseManageUnit, NotFoundError, ValidationError

logger = logging.getLogger(__name__)

class LLMManageUnit:
    """Handles LLM-related operations and instructions"""

    def __init__(self, database_manage_unit: DatabaseManageUnit):
        self.db = database_manage_unit
        self.handlers = {
            'LLM_PROVIDER_ADD': self.add_llm_provider,
            'LLM_PROVIDER_UPDATE': self.update_llm_provider,
            'LLM_PROVIDER_DELETE': self.delete_llm_provider,
            'LLM_PROVIDER_LIST': self.list_llm_providers,
            'LLM_ADD': self.add_llm,
            'LLM_UPDATE': self.update_llm,
            'LLM_DELETE': self.delete_llm,
            'LLM_LIST': self.list_llms,
            'LLM_LIST_BY_PROVIDER': self.list_llms_by_provider,
            'LLM_RESPONSE_GENERATE': self.generate_llm_response,
            'LLM_RESPONSE_REGENERATE': self.regenerate_llm_response
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
    
    def add_llm_provider(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new LLM provider"""
        if not self._validate_data(data, ['name', 'api_endpoint']):
            return self._error_response("Missing required fields: name and api_endpoint")

        try:
            provider_data = self.db.add_provider(
                name=data['name'], 
                api_endpoint=data['api_endpoint'],
                api_key=data.get('api_key')
            )
            return self._success_response("Provider added successfully", {"provider": provider_data})
        except Exception as e:
            return self._error_response(f"Failed to add provider: {str(e)}")
    
    def update_llm_provider(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update existing LLM provider"""
        if not self._validate_data(data, ['provider_id']):
            return self._error_response("Provider ID is required")
        
        try:
            provider_id = data.pop('provider_id')
            provider_data = self.db.update_provider(provider_id, **data)
            return self._success_response("Provider updated successfully", {"provider": provider_data})
        except Exception as e:
            return self._error_response(f"Failed to update provider: {str(e)}")
    
    def delete_llm_provider(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Delete LLM provider"""
        if not self._validate_data(data, ['provider_id']):
            return self._error_response("Provider ID is required")

        try:
            self.db.delete_provider(data['provider_id'])
            return self._success_response("Provider deleted successfully")
        except NotFoundError:
            return self._error_response(f"Provider with ID {data['provider_id']} not found")
        except Exception as e:
            return self._error_response(f"Failed to delete provider: {str(e)}")
    
    def list_llm_providers(self, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List all LLM providers"""
        try:
            providers = self.db.get_all_providers()
            return self._success_response("Providers retrieved successfully", {"providers": providers})
        except Exception as e:
            return self._error_response(f"Failed to list providers: {str(e)}")
    
    def add_llm(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new LLM"""
        if not self._validate_data(data, ['provider_id', 'llm_name']):
            return self._error_response("Missing required fields: provider_id and llm_name")

        logger.info(f"Adding LLM: {data['llm_name']} for provider: {data['provider_id']}")
        try:
            llm_data = self.db.add_llm(name=data['llm_name'], provider_public_id=data['provider_id'])
            logger.info(f"LLM added: {llm_data}")
            return self._success_response("LLM added successfully", {"llm": llm_data})
        except Exception as e:
            return self._error_response(f"Failed to add LLM: {str(e)}")
    
    def update_llm(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update existing LLM"""
        if not self._validate_data(data, ['llm_id', 'llm_name']):
            return self._error_response("LLM ID and name are required")

        try:
            llm_data = self.db.update_llm(data['llm_id'], name=data['llm_name'])
            return self._success_response("LLM updated successfully", {"llm": llm_data})
        except Exception as e:
            return self._error_response(f"Failed to update LLM: {str(e)}")
    
    def delete_llm(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Delete LLM"""
        if not self._validate_data(data, ['llm_id']):
            return self._error_response("LLM ID is required")

        try:
            self.db.delete_llm(data['llm_id'])
            return self._success_response("LLM deleted successfully")
        except NotFoundError:
            return self._error_response(f"LLM with ID {data['llm_id']} not found")
        except Exception as e:
            return self._error_response(f"Failed to delete LLM: {str(e)}")
    
    def list_llms(self, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List all LLMs"""
        try:
            llms = self.db.get_all_llms()
            return self._success_response("LLMs retrieved successfully", {"llms": llms})
        except Exception as e:
            return self._error_response(f"Failed to list LLMs: {str(e)}")
    
    def list_llms_by_provider(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """List LLMs for specific provider"""
        if not self._validate_data(data, ['provider_id']):
            return self._error_response("Provider ID is required")

        try:
            llms = self.db.get_llms_by_provider(data['provider_id'])
            return self._success_response(f"LLMs retrieved for provider {data['provider_id']}", {"llms": llms})
        except Exception as e:
            return self._error_response(f"Failed to list provider LLMs: {str(e)}")
        
    def generate_llm_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate response from LLM"""
        required_fields = ['chat_id', 'user_id', 'provider_id', 'llm_id', 'user_input']
        if not self._validate_data(data, required_fields):
            return self._error_response(f"Missing required fields: {', '.join(required_fields)}")

        try:
            provider_data = self.db.get_provider_by_public_id(data['provider_id'])
            endpoint = provider_data.get('api_endpoint')
            api_key = provider_data.get('api_key')
            model = self.db.get_llm_by_public_id(data['llm_id']).get('name')

            # already ordered by created_at
            chat_messages = self.db.get_messages_by_chat(data['chat_id'])

            message_history = [
                {"role": message.get('role'), "content": message.get('content')} 
                for message in chat_messages
            ]

            message_history.append({"role": "user", "content": data['user_input']})

            response_content = self._call_llm_api(endpoint, model, message_history, api_key)

            message_data = self.db.create_message(
                chat_public_id=data['chat_id'],
                user_public_id=data['user_id'],
                content=data['user_input'],
                role='user',
                llm_public_id=data['llm_id']
            )

            if not message_data:
                raise ValidationError("Failed to create user message")

            llm_message_data = self.db.create_message(
                chat_public_id=data['chat_id'],
                user_public_id=data['user_id'],
                content=response_content,
                role='assistant',
                llm_public_id=data['llm_id']
            )
            return self._success_response("Response generated successfully", {"llm_response": llm_message_data})
        except Exception as e:
            return self._error_response(f"Failed to generate response: {str(e)}")
    
    def regenerate_llm_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Regenerate response from LLM"""
        if not self._validate_data(data, ['message_id']):
            return self._error_response("Message ID is required")

        try:
            message_data = self.db.get_message_by_public_id(data['message_id'])
            if not message_data:
                return self._error_response("Message not found")

            if not message_data.get('llm_id'):
                return self._error_response("Original message has no associated LLM")

            llm_data = self.db.get_llm_by_public_id(message_data.get('llm_id'))
            if not llm_data:
                return self._error_response("LLM not found")
            
            provider_data = self.db.get_provider_by_public_id(llm_data.get('provider_id'))
            endpoint = provider_data.get('api_endpoint')
            api_key = provider_data.get('api_key')
            model = llm_data.get('name')

            # already ordered by created_at
            chat_messages = self.db.get_messages_by_chat(message_data.get('chat_id'))

            def parse_datetime(date_string: str) -> datetime:
                """Parse a datetime string into a datetime object."""
                return datetime.fromisoformat(date_string)

            # exclude the message which has the given message_id and the subsequent messages
            message_history = [
                {"role": message.get('role'), "content": message.get('content')} 
                for message in chat_messages
                if parse_datetime(message.get('created_at')) < parse_datetime(message_data.get('created_at'))
            ]
            # message_history = [
            #     {"role": message.get('role'), "content": message.get('content')}
            #     for message in chat_messages[:-1]
            # ]

            response_content = self._call_llm_api(endpoint, model, message_history, api_key)

            llm_message_data = self.db.create_message(
                chat_public_id=message_data.get('chat_id'),
                user_public_id=message_data.get('user_id'),
                content=response_content,
                role='assistant',
                llm_public_id=message_data.get('llm_id')
            )
            return self._success_response("Response regenerated successfully", {"llm_response": llm_message_data})
        except Exception as e:
            return self._error_response(f"Failed to regenerate response: {str(e)}")

    @staticmethod
    def _call_llm_api(endpoint: str, model: str, messages: List[Dict[str, str]], api_key: str = None) -> str:
        """Call LLM API with error handling"""
        try:
            headers = {"Content-Type": "application/json"}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            payload = {
                "model": model,
                "messages": messages
            }

            # logger.info(f"Calling LLM API at {endpoint} with payload: {json.dumps(payload)}")

            response = requests.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except requests.RequestException as e:
            raise Exception(f"API call failed: {str(e)}")

    @staticmethod
    def _validate_data(data: Dict[str, Any], required_keys: List[str]) -> bool:
        """Validate presence of required keys in data"""
        return data is not None and all(key in data for key in required_keys)

    @staticmethod
    def _success_response(message: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Format success response"""
        response = {"status": "success", "message": message, "data": data or {}}
        return response

    @staticmethod
    def _error_response(message: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Format error response"""
        return {"status": "error", "message": message, "data": data or {}}