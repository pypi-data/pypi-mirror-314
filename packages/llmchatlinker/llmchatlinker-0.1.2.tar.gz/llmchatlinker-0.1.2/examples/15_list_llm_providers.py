# examples/15_list_llm_providers.py

from llmchatlinker.client import LLMChatLinkerClient

def main():
    client = LLMChatLinkerClient()
    response = client.list_llm_providers()
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()