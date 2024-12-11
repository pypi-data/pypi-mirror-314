# llmchatlinker/client.py

import json
import logging
from .message_queue import publish_message

class LLMChatLinkerClient:
    def __init__(self):
        """
        Initialize the LLMChatLinkerClient.
        """
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def _process_instruction(self, instruction_type: str, data: dict) -> dict:
        """
        Process an instruction by sending it to the message queue.

        Args:
            instruction_type (str): The type of instruction.
            data (dict): The data for the instruction.

        Returns:
            dict: The response from the message queue.
        """
        try:
            instruction = {"type": instruction_type, "data": data}
            response = publish_message(json.dumps(instruction))
            return json.loads(response.decode('utf-8'))
        except Exception as e:
            self.logger.error(f"Failed to process instruction: {e}")
            raise

    # User Management Methods
    def create_user(self, username: str, display_name: str = None, profile: str = None) -> dict:
        """
        Create a new user.

        Args:
            username (str): The username of the user.
            display_name (str, optional): The display name of the user.
            profile (str, optional): The profile of the user.

        Returns:
            dict: The response from the message queue.
        """
        if display_name is None:
            display_name = username
        data = {"username": username, "display_name": display_name, "profile": profile}
        return self._process_instruction("USER_CREATE", data)

    def update_user(self, user_id: str, username: str = None, display_name: str = None, profile: str = None) -> dict:
        """
        Update an existing user.

        Args:
            user_id (str): The ID of the user.
            username (str, optional): The new username of the user.
            display_name (str, optional): The new display name of the user.
            profile (str, optional): The new profile of the user.

        Returns:
            dict: The response from the message queue.
        """
        data = {"user_id": user_id, "username": username, "display_name": display_name, "profile": profile}
        return self._process_instruction("USER_UPDATE", data)

    def delete_user(self, user_id: str) -> dict:
        """
        Delete a user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            dict: The response from the message queue.
        """
        return self._process_instruction("USER_DELETE", {"user_id": user_id})

    def list_users(self) -> dict:
        """
        List all users.

        Returns:
            dict: The response from the message queue.
        """
        return self._process_instruction("USER_LIST", {})

    def get_user(self, username: str = None, user_id: str = None) -> dict:
        """
        Get a user by username or user ID.

        Args:
            username (str, optional): The username of the user.
            user_id (str, optional): The ID of the user.

        Returns:
            dict: The response from the message queue.
        """
        if username:
            return self._process_instruction("USER_GET", {"username": username})
        elif user_id:
            return self._process_instruction("USER_GET", {"user_id": user_id})
        else:
            raise ValueError("Either username or user_id must be provided")

    def enable_instruction_recording(self, user_id: str) -> dict:
        """
        Enable instruction recording for a user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            dict: The response from the message queue.
        """
        return self._process_instruction("USER_INSTRUCTION_RECORDING_ENABLE", {"user_id": user_id})

    def disable_instruction_recording(self, user_id: str) -> dict:
        """
        Disable instruction recording for a user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            dict: The response from the message queue.
        """
        return self._process_instruction("USER_INSTRUCTION_RECORDING_DISABLE", {"user_id": user_id})

    def list_user_instructions(self, user_id: str) -> dict:
        """
        List all instructions for a user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            dict: The response from the message queue.
        """
        return self._process_instruction("USER_INSTRUCTION_RECORDS_LIST", {"user_id": user_id})

    def delete_user_instructions(self, user_id: str) -> dict:
        """
        Delete all instructions for a user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            dict: The response from the message queue.
        """
        return self._process_instruction("USER_INSTRUCTION_RECORDS_DELETE", {"user_id": user_id})

    # Chat Management Methods
    def create_chat(self, title: str, user_ids: list) -> dict:
        """
        Create a new chat.

        Args:
            title (str): The title of the chat.
            user_ids (list): The list of user IDs to be added to the chat.

        Returns:
            dict: The response from the message queue.
        """
        data = {"title": title, "user_ids": user_ids}
        return self._process_instruction("CHAT_CREATE", data)

    def update_chat(self, chat_id: str, title: str) -> dict:
        """
        Update an existing chat.

        Args:
            chat_id (str): The ID of the chat.
            title (str): The new title of the chat.

        Returns:
            dict: The response from the message queue.
        """
        data = {"chat_id": chat_id, "title": title}
        return self._process_instruction("CHAT_UPDATE", data)

    def delete_chat(self, chat_id: str) -> dict:
        """
        Delete a chat.

        Args:
            chat_id (str): The ID of the chat.

        Returns:
            dict: The response from the message queue.
        """
        return self._process_instruction("CHAT_DELETE", {"chat_id": chat_id})

    def list_chats(self) -> dict:
        """
        List all chats.

        Returns:
            dict: The response from the message queue.
        """
        return self._process_instruction("CHAT_LIST", {})

    def get_chat(self, chat_id: str) -> dict:
        """
        Get a chat by chat ID.

        Args:
            chat_id (str): The ID of the chat.

        Returns:
            dict: The response from the message queue.
        """
        return self._process_instruction("CHAT_LOAD", {"chat_id": chat_id})

    def list_user_chats(self, user_id: str) -> dict:
        """
        List all chats for a user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            dict: The response from the message queue.
        """
        return self._process_instruction("CHAT_LIST_BY_USER", {"user_id": user_id})

    # LLM Provider Management Methods
    def add_llm_provider(self, name: str, api_endpoint: str, api_key: str = None) -> dict:
        """
        Add a new LLM provider.

        Args:
            name (str): The name of the LLM provider.
            api_endpoint (str): The API endpoint of the LLM provider.
            api_key (str, optional): The API key of the LLM provider.

        Returns:
            dict: The response from the message queue.
        """
        data = {"name": name, "api_endpoint": api_endpoint, "api_key": api_key}
        return self._process_instruction("LLM_PROVIDER_ADD", data)

    def update_llm_provider(self, provider_id: str, name: str = None, api_endpoint: str = None, api_key: str = None) -> dict:
        """
        Update an existing LLM provider.

        Args:
            provider_id (str): The ID of the LLM provider.
            name (str, optional): The new name of the LLM provider.
            api_endpoint (str, optional): The new API endpoint of the LLM provider.

        Returns:
            dict: The response from the message queue.
        """
        data = {"provider_id": provider_id, "name": name, "api_endpoint": api_endpoint, "api_key": api_key}
        return self._process_instruction("LLM_PROVIDER_UPDATE", data)

    def delete_llm_provider(self, provider_id: str) -> dict:
        """
        Delete an LLM provider.

        Args:
            provider_id (str): The ID of the LLM provider.

        Returns:
            dict: The response from the message queue.
        """
        return self._process_instruction("LLM_PROVIDER_DELETE", {"provider_id": provider_id})

    def list_llm_providers(self) -> dict:
        """
        List all LLM providers.

        Returns:
            dict: The response from the message queue.
        """
        return self._process_instruction("LLM_PROVIDER_LIST", {})

    # LLM Management Methods
    def add_llm(self, provider_id: str, llm_name: str) -> dict:
        """
        Add a new LLM.

        Args:
            provider_id (str): The ID of the LLM provider.
            llm_name (str): The name of the LLM.

        Returns:
            dict: The response from the message queue.
        """
        data = {"provider_id": provider_id, "llm_name": llm_name}
        return self._process_instruction("LLM_ADD", data)

    def update_llm(self, llm_id: str, llm_name: str) -> dict:
        """
        Update an existing LLM.

        Args:
            llm_id (str): The ID of the LLM.
            llm_name (str): The new name of the LLM.

        Returns:
            dict: The response from the message queue.
        """
        data = {"llm_id": llm_id, "llm_name": llm_name}
        return self._process_instruction("LLM_UPDATE", data)

    def delete_llm(self, llm_id: str) -> dict:
        """
        Delete an LLM.

        Args:
            llm_id (str): The ID of the LLM.

        Returns:
            dict: The response from the message queue.
        """
        return self._process_instruction("LLM_DELETE", {"llm_id": llm_id})

    def list_llms(self) -> dict:
        """
        List all LLMs.

        Returns:
            dict: The response from the message queue.
        """
        return self._process_instruction("LLM_LIST", {})

    def list_llms_by_provider(self, provider_id: str) -> dict:
        """
        List all LLMs for a provider.

        Args:
            provider_id (str): The ID of the LLM provider.

        Returns:
            dict: The response from the message queue.
        """
        return self._process_instruction("LLM_LIST_BY_PROVIDER", {"provider_id": provider_id})

    # LLM Response Management Methods
    def generate_llm_response(self, user_id: str, chat_id: str, provider_id: str, llm_id: str, user_input: str) -> dict:
        """
        Generate a response from an LLM based on user input.

        Args:
            user_id (str): The ID of the user.
            chat_id (str): The ID of the chat.
            provider_id (str): The ID of the LLM provider.
            llm_id (str): The ID of the LLM.
            user_input (str): The user input.

        Returns:
            dict: The response from the message queue.
        """
        data = {"user_id": user_id, "chat_id": chat_id, "provider_id": provider_id, "llm_id": llm_id, "user_input": user_input}
        return self._process_instruction("LLM_RESPONSE_GENERATE", data)

    def regenerate_llm_response(self, message_id: str) -> dict:
        """
        Regenerate a response from an LLM based on a previous message.

        Args:
            message_id (str): The ID of the original message.

        Returns:
            dict: The response from the message queue.
        """
        return self._process_instruction("LLM_RESPONSE_REGENERATE", {"message_id": message_id})