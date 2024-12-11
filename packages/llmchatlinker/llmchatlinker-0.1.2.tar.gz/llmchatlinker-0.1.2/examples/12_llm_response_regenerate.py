# examples/12_llm_response_regenerate.py

import json
from llmchatlinker.client import LLMChatLinkerClient

def main():
    client = LLMChatLinkerClient()

    # Load message_id from config.json
    with open('config.json', 'r') as f:
        config = json.load(f)
        message_id = config['message_id']

    response = client.regenerate_llm_response(message_id=message_id)
    print(f" [x] Received {response}")
    new_message_id = response['data']['llm_response']['message_id']
    print(f" [x] New Message ID: {new_message_id}")

    # Save new_message_id to config.json
    with open('config.json', 'r+') as f:
        config = json.load(f)
        config['message_id'] = new_message_id
        f.seek(0)
        json.dump(config, f, indent=4)
        f.truncate()

if __name__ == "__main__":
    main()