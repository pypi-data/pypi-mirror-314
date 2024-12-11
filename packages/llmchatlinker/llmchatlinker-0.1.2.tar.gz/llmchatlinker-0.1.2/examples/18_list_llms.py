# examples/18_list_llms.py

from llmchatlinker.client import LLMChatLinkerClient

def main():
    client = LLMChatLinkerClient()
    response = client.list_llms()
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()