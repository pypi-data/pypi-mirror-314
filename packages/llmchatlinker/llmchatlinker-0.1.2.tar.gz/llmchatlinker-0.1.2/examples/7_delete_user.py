# examples/7_delete_user.py

import json
from llmchatlinker.client import LLMChatLinkerClient

def main():
    client = LLMChatLinkerClient()

    # Load user_id from config.json
    with open('config.json', 'r') as f:
        config = json.load(f)
        user_id = config['user_id']

    response = client.delete_user(user_id=user_id)
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()