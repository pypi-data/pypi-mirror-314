# examples/3_add_llm_provider.py

import json
from llmchatlinker.client import LLMChatLinkerClient

def main():
    client = LLMChatLinkerClient()
    response = client.add_llm_provider(name="MLModelScope", api_endpoint="http://localhost:15555/api/chat")
    print(f" [x] Received {response}")
    provider_id = response['data']['provider']['provider_id']
    print(f" [x] LLM Provider ID: {provider_id}")

    # Save provider_id to config.json
    with open('config.json', 'r+') as f:
        config = json.load(f)
        config['provider_id'] = provider_id
        f.seek(0)
        json.dump(config, f, indent=4)
        f.truncate()

if __name__ == "__main__":
    main()