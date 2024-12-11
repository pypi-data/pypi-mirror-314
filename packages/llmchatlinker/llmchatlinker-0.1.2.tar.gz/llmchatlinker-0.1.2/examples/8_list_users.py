# examples/8_list_users.py

from llmchatlinker.client import LLMChatLinkerClient

def main():
    client = LLMChatLinkerClient()
    response = client.list_users()
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()