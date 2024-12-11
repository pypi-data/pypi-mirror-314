import pytest
import json
from llmchatlinker.client import LLMChatLinkerClient
from dotenv import load_dotenv
import os

# Load environment variables from the .env file in the parent directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')

@pytest.fixture(scope="module")
def client():
    return LLMChatLinkerClient()

@pytest.fixture(scope="module")
def config():
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'w') as f:
            json.dump({
                "user_id": "",
                "chat_id": "",
                "provider_id": "",
                "llm_id": "",
                "message_id": ""
            }, f)
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)

def test_create_user(client, config):
    response = client.create_user(username="john_doe", profile="Sample profile")
    assert response["status"] == "success"
    user_id = response["data"]["user"]["user_id"]
    assert user_id

    # Save user_id to config.json
    config['user_id'] = user_id
    save_config(config)
    
    print(f" [x] User ID: {user_id}")

def test_create_chat(client, config):
    user_id = config['user_id']
    response = client.create_chat(title="Sample Chat", user_ids=[user_id])
    assert response["status"] == "success"
    chat_id = response["data"]["chat"]["chat_id"]
    assert chat_id

    # Save chat_id to config.json
    config['chat_id'] = chat_id
    save_config(config)
    
    print(f" [x] Chat ID: {chat_id}")

def test_add_llm_provider(client, config):
    response = client.add_llm_provider(name="MLModelScope", api_endpoint="http://localhost:15555/api/chat")
    assert response["status"] == "success"
    provider_id = response["data"]["provider"]["provider_id"]
    assert provider_id

    # Save provider_id to config.json
    config['provider_id'] = provider_id
    save_config(config)
    
    print(f" [x] LLM Provider ID: {provider_id}")

def test_add_llm(client, config):
    provider_id = config['provider_id']
    response = client.add_llm(provider_id=provider_id, llm_name="llama_3_2_1b_instruct")
    assert response["status"] == "success"
    llm_id = response["data"]["llm"]["llm_id"]
    assert llm_id

    # Save llm_id to config.json
    config['llm_id'] = llm_id
    save_config(config)
    
    print(f" [x] LLM ID: {llm_id}")

def test_generate_llm_response(client, config):
    user_id = config['user_id']
    chat_id = config['chat_id']
    provider_id = config['provider_id']
    llm_id = config['llm_id']
    response = client.generate_llm_response(
        user_id=user_id,
        chat_id=chat_id,
        provider_id=provider_id,
        llm_id=llm_id,
        user_input="What is the longest river in the world?"
    )
    assert response["status"] == "success"
    message_id = response["data"]["llm_response"]["message_id"]
    assert message_id

    # Save message_id to config.json
    config['message_id'] = message_id
    save_config(config)
    
    print(f" [x] Message ID: {message_id}")

def test_regenerate_llm_response(client, config):
    message_id = config['message_id']
    response = client.regenerate_llm_response(message_id=message_id)
    assert response["status"] == "success"
    new_message_id = response["data"]["llm_response"]["message_id"]
    assert new_message_id

    # Save new_message_id to config.json
    config['message_id'] = new_message_id
    save_config(config)
    
    print(f" [x] New Message ID: {new_message_id}")