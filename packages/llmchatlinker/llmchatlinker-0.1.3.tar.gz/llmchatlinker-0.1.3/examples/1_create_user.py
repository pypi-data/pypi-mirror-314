# examples/1_create_user.py

from llmchatlinker.client import LLMChatLinkerClient
from config_utils import read_config, write_config

def main():
    client = LLMChatLinkerClient()
    response = client.create_user(username="john_doe", profile="Sample profile")
    print(f" [x] Received {response}")
    user_id = response['data']['user']['user_id']
    print(f" [x] User ID: {user_id}")

    # Save user_id to config.json
    config = read_config()
    config['user_id'] = user_id
    write_config(config)

if __name__ == "__main__":
    main()