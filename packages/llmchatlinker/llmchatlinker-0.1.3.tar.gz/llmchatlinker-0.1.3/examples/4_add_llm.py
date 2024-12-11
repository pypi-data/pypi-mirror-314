# examples/4_add_llm.py

from llmchatlinker.client import LLMChatLinkerClient
from config_utils import read_config, write_config

def main():
    client = LLMChatLinkerClient()

    # Load provider_id from config.json
    config = read_config()
    provider_id = config.get('provider_id')

    response = client.add_llm(provider_id=provider_id, llm_name="llama_3_2_1b_instruct")
    print(f" [x] Received {response}")
    llm_id = response['data']['llm']['llm_id']
    print(f" [x] LLM ID: {llm_id}")

    # Save llm_id to config.json
    config['llm_id'] = llm_id
    write_config(config)

if __name__ == "__main__":
    main()