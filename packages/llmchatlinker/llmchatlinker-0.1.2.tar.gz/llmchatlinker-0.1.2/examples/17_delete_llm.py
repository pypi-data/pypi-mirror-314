# examples/17_delete_llm.py

import json
from llmchatlinker.client import LLMChatLinkerClient

def main():
    client = LLMChatLinkerClient()

    # Load llm_id from config.json
    with open('config.json', 'r') as f:
        config = json.load(f)
        llm_id = config['llm_id']

    response = client.delete_llm(llm_id=llm_id)
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()