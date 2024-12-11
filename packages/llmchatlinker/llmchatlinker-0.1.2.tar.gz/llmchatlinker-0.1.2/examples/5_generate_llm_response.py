# examples/5_generate_llm_response.py

import json
from llmchatlinker.client import LLMChatLinkerClient

def main():
    client = LLMChatLinkerClient()

    # Load necessary IDs from config.json
    with open('config.json', 'r') as f:
        config = json.load(f)
        user_id = config['user_id']
        chat_id = config['chat_id']
        provider_id = config['provider_id']
        llm_id = config['llm_id']

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
    with open('config.json', 'r+') as f:
        config = json.load(f)
        config['message_id'] = message_id
        f.seek(0)
        json.dump(config, f, indent=4)
        f.truncate()

if __name__ == "__main__":
    main()