# examples/11_list_chats.py

from llmchatlinker.client import LLMChatLinkerClient

def main():
    client = LLMChatLinkerClient()
    response = client.list_chats()
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()