# examples/6_update_user.py

import json
from llmchatlinker.client import LLMChatLinkerClient

def main():
    client = LLMChatLinkerClient()

    # Load user_id from config.json
    with open('config.json', 'r') as f:
        config = json.load(f)
        user_id = config['user_id']

    response = client.update_user(user_id=user_id, username="john_doe_updated", profile="Updated profile")
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()