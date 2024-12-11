# llmchatlinker/units/control_unit.py

from typing import Dict, Any, Optional, Callable
import logging
from .database_manage_unit import DatabaseManageUnit, NotFoundError, ValidationError
from .user_manage_unit import UserManageUnit
from .chat_manage_unit import ChatManageUnit
from .llm_manage_unit import LLMManageUnit

# Configure logging
logger = logging.getLogger(__name__)

class ControlUnit:
    """Central control unit for managing and routing instructions"""

    def __init__(
        self,
        user_manage_unit: UserManageUnit,
        chat_manage_unit: ChatManageUnit,
        llm_manage_unit: LLMManageUnit,
        database_manage_unit: DatabaseManageUnit
    ):
        """Initialize with all management units"""
        self.handlers: Dict[str, Callable] = {
            'USER_': user_manage_unit.handle_instruction,
            'CHAT_': chat_manage_unit.handle_instruction,
            'LLM_': llm_manage_unit.handle_instruction,
            # 'INSTRUCTION_': database_manage_unit.handle_instruction
        }

    def decode_and_execute_instruction(self, instruction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Decode and execute the given instruction by routing to appropriate handler
        
        Args:
            instruction: Dictionary containing instruction type and data
            
        Returns:
            Dict containing execution status and result
        """
        try:
            # Validate instruction format
            if not self._validate_instruction(instruction):
                return self._error_response("Invalid instruction format")

            instruction_type = instruction['type']
            data = instruction.get('data', {})

            # Get appropriate handler
            handler = self._get_handler(instruction_type)
            if not handler:
                return self._error_response(f"No handler found for instruction type: {instruction_type}")

            # Execute instruction
            return handler(instruction_type, data)

        except (NotFoundError, ValidationError) as e:
            logger.error(f"Validation error: {str(e)}")
            return self._error_response(str(e))
        except Exception as e:
            logger.error(f"Error processing instruction: {str(e)}", exc_info=True)
            return self._error_response(f"An error occurred while processing the instruction: {str(e)}")

    def _get_handler(self, instruction_type: str) -> Optional[Callable]:
        """
        Determine the appropriate handler based on instruction type prefix
        
        Args:
            instruction_type: Type of instruction to handle
            
        Returns:
            Handler function if found, None otherwise
        """
        for prefix, handler in self.handlers.items():
            if instruction_type.startswith(prefix):
                return handler
        return None

    @staticmethod
    def _validate_instruction(instruction: Dict[str, Any]) -> bool:
        """
        Validate instruction format
        
        Args:
            instruction: Instruction dictionary to validate
            
        Returns:
            bool indicating if instruction is valid
        """
        return (
            isinstance(instruction, dict) and
            'type' in instruction and
            isinstance(instruction['type'], str) and
            ('data' not in instruction or isinstance(instruction['data'], dict))
        )

    @staticmethod
    def _success_response(message: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Format success response."""
        response = {"status": "success", "message": message, "data": data or {}}
        return response

    @staticmethod
    def _error_response(message: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Format error response."""
        return {"status": "error", "message": message, "data": data or {}}