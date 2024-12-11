# examples/2_create_chat.py

from llmchatlinker.client import LLMChatLinkerClient
from config_utils import read_config, write_config

def main():
    client = LLMChatLinkerClient()

    # Load user_id from config.json
    config = read_config()
    user_id = config.get('user_id')

    response = client.create_chat(title="Sample Chat", user_ids=[user_id])
    print(f" [x] Received {response}")
    chat_id = response['data']['chat']['chat_id']
    print(f" [x] Chat ID: {chat_id}")

    # Save chat_id to config.json
    config['chat_id'] = chat_id
    write_config(config)

if __name__ == "__main__":
    main()