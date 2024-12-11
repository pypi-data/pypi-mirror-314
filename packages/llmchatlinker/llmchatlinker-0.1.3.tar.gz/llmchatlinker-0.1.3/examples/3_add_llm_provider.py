# examples/3_add_llm_provider.py

from llmchatlinker.client import LLMChatLinkerClient
from config_utils import read_config, write_config

def main():
    client = LLMChatLinkerClient()
    response = client.add_llm_provider(name="MLModelScope", api_endpoint="http://localhost:15555/api/chat")
    print(f" [x] Received {response}")
    provider_id = response['data']['provider']['provider_id']
    print(f" [x] LLM Provider ID: {provider_id}")

    # Save provider_id to config.json
    config = read_config()
    config['provider_id'] = provider_id
    write_config(config)

if __name__ == "__main__":
    main()