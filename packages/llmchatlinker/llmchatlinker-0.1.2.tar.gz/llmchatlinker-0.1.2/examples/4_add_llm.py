# examples/4_add_llm.py

import json
from llmchatlinker.client import LLMChatLinkerClient

def main():
    client = LLMChatLinkerClient()

    # Load provider_id from config.json
    with open('config.json', 'r') as f:
        config = json.load(f)
        provider_id = config['provider_id']

    response = client.add_llm(provider_id=provider_id, llm_name="llama_3_2_1b_instruct")
    print(f" [x] Received {response}")
    llm_id = response['data']['llm']['llm_id']
    print(f" [x] LLM ID: {llm_id}")

    # Save llm_id to config.json
    with open('config.json', 'r+') as f:
        config = json.load(f)
        config['llm_id'] = llm_id
        f.seek(0)
        json.dump(config, f, indent=4)
        f.truncate()

if __name__ == "__main__":
    main()