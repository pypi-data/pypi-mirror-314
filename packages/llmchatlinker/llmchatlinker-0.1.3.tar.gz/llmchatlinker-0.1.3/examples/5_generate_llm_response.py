# examples/5_generate_llm_response.py

from llmchatlinker.client import LLMChatLinkerClient
from config_utils import read_config, write_config

def main():
    client = LLMChatLinkerClient()

    # Load necessary IDs from config.json
    config = read_config()
    user_id = config.get('user_id')
    chat_id = config.get('chat_id')
    provider_id = config.get('provider_id')
    llm_id = config.get('llm_id')

    response = client.generate_llm_response(
        user_id=user_id,
        chat_id=chat_id,
        provider_id=provider_id,
        llm_id=llm_id,
        user_input="What is the longest river in the world?"
    )
    print(f" [x] Received {response}")
    message_id = response['data']['llm_response']['message_id']
    print(f" [x] Message ID: {message_id}")

    # Save message_id to config.json
    config['message_id'] = message_id
    write_config(config)

if __name__ == "__main__":
    main()