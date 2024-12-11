# examples/13_update_llm_provider.py

import json
from llmchatlinker.client import LLMChatLinkerClient

def main():
    client = LLMChatLinkerClient()

    # Load provider_id from config.json
    with open('config.json', 'r') as f:
        config = json.load(f)
        provider_id = config['provider_id']

    response = client.update_llm_provider(
        provider_id=provider_id,
        name="Updated Provider Name",
        api_endpoint="http://updated.endpoint/v1/chat/completions"
    )
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()