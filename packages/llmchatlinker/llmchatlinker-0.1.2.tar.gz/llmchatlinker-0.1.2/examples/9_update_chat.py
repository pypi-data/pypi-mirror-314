# examples/9_update_chat.py

import json
from llmchatlinker.client import LLMChatLinkerClient

def main():
    client = LLMChatLinkerClient()

    # Load chat_id from config.json
    with open('config.json', 'r') as f:
        config = json.load(f)
        chat_id = config['chat_id']

    response = client.update_chat(chat_id=chat_id, title="Updated Chat Title")
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()