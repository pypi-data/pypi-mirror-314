# examples/2_create_chat.py

import json
from llmchatlinker.client import LLMChatLinkerClient

def main():
    client = LLMChatLinkerClient()

    # Load user_id from config.json
    with open('config.json', 'r') as f:
        config = json.load(f)
        user_id = config['user_id']

    response = client.create_chat(title="Sample Chat", user_ids=[user_id])
    print(f" [x] Received {response}")
    chat_id = response['data']['chat']['chat_id']
    print(f" [x] Chat ID: {chat_id}")

    # Save chat_id to config.json
    with open('config.json', 'r+') as f:
        config = json.load(f)
        config['chat_id'] = chat_id
        f.seek(0)
        json.dump(config, f, indent=4)
        f.truncate()

if __name__ == "__main__":
    main()