# examples/1_create_user.py

import json
from llmchatlinker.client import LLMChatLinkerClient

def main():
    client = LLMChatLinkerClient()
    response = client.create_user(username="john_doe", profile="Sample profile")
    print(f" [x] Received {response}")
    user_id = response['data']['user']['user_id']
    print(f" [x] User ID: {user_id}")

    # Save user_id to config.json
    with open('config.json', 'r+') as f:
        config = json.load(f)
        config['user_id'] = user_id
        f.seek(0)
        json.dump(config, f, indent=4)
        f.truncate()

if __name__ == "__main__":
    main()