# LLMChatLinker

LLMChatLinker is a Middleware SDK designed to facilitate interaction between clients and Large Language Models (LLMs). The SDK acts as an intermediary between the client and the LLM(s), allowing multiple users to communicate with the LLM(s) simultaneously through the client's front-end.

## Architecture

The interaction flow follows the fetch-decode-execute-store cycle, similar to the architecture of a CPU (CISC/RISC):

1. **Fetch**: The Orchestrator (acting as the CPU) fetches the instructions from the instruction queue.
2. **Decode**: The Control Unit decodes the fetched instructions. Depending on the instruction type, it decodes the instruction to be directly executed later.
3. **Execute**: The decoded instruction is executed by the relevant manage unit (User, Chat, LLM, or Database Manage Unit).
4. **Store**: The result from the execution is stored back in the result queue, ensuring each user request is immediately linked to its corresponding result.

## Components

- **Client**: The front-end that interacts with users.
- **Middleware SDK (LLMChatLinker)**: Facilitates communication between the client and LLM(s). Composed of various units that mimic the functionality of CPU components:
  - **Orchestrator**: Acts as the CPU, fetching, decoding, executing, and storing instructions.
  - **Control Unit**: Decodes instructions fetched by the Orchestrator.
  - **User Manage Unit**: Manages user-related instructions.
  - **Chat Manage Unit**: Manages chat-related instructions.
  - **LLM Manage Unit**: Manages LLM-related instructions.
  - **Database Manage Unit**: Manages database interactions.
- **LLM(s)**: Large Language Models providing responses to user queries.

## Features

- **Fetch-Decode-Execute-Store Cycle**: Adopts the CPU-like mechanism to process instructions efficiently.
- **User Management**: Create, update, delete, and list users.
- **Chat Management**: Create, update, delete, load, and list chats.
- **LLM Management**: Add, update, delete, list LLM providers and LLMs.
- **Instruction Management**: Enable/disable instruction recording, delete and list instruction records.

## Quick Start Guide

### Prerequisites

- Docker

### Installation

You can install LLMChatLinker via PyPI:

```bash
pip install llmchatlinker
```

### Setting Up the Environment

1. **Clone the repository:**
    ```bash
    git clone https://github.com/cjlee7128/LLMChatLinker.git
    cd LLMChatLinker
    ```

2. **Environment Configuration:**

    The repository includes a `.env.example` file which contains example environment variables. You need to create a `.env` file for Docker Compose to use these settings:

    ```bash
    cp .env.example .env
    ```

    Repeat the same process for the `llmchatlinker-frontend`:

    ```bash
    cd llmchatlinker-frontend
    cp .env.example .env
    cd ..
    ```

3. **Run services using Docker Compose:**

   Ensure that you have a properly configured `docker-compose.yml` file. This file should specify all necessary services like PostgreSQL, RabbitMQ, and any additional dependencies.

   Start all services defined in `docker-compose.yml`:

    ```bash
    docker compose up --build -d
    ```

4. **Pull and run MLModelScope API agent individually:**

    Execute the following command to start the MLModelScope API agent:

    ```bash
    docker run -d -p 15555:15555 xlabub/pytorch-agent-api:latest
    ```

    If you want MLModelScope API agent not to download huggingface models every time, you can use the following command:

    ```bash
    docker run -d -e HF_HOME=/root/.cache/huggingface \
      -p 15555:15555 -v ~/.cache/huggingface:/root/.cache/huggingface xlabub/pytorch-agent-api:latest
    ```

    (Recommended) After running the MLModelScope API agent, you can query the API to download the models if not existing and to reduce the next response time even if the model is already downloaded. For example:

    ```bash
    curl http://localhost:15555/api/chat \
      -H "Content-Type: application/json" \
      -d '{
          "model": "llama_3_2_1b_instruct",
          "messages": [
              {"role": "user", "content": "What is the longest river in the world?"}
          ]
      }'
    ```

    The above command will download the `llama_3_2_1b_instruct` model if it does not exist and generate a response for the given user message.

### Accessing the Front-end

After successfully running the `docker compose` command, you can access the front-end application via your web browser. Open the following URL:
    
```bash
http://localhost:<FRONTEND_PORT>
```

Replace `<FRONTEND_PORT>` with the actual port number specified in the `.env` file within the `LLMChatLinker` directory. This value should correspond to the port binding for your front-end application.

### Important Notes

- **Environment Variables:** Both backend and frontend parts of the application rely on certain environment variables. Ensure your `.env` files have correct values for seamless deployment.
  
- **Docker Compose:** It's crucial that your `docker-compose.yml` is configured correctly with all the required services. If you need additional environment-specific settings, update your `.env` files before running `docker compose up --build -d`.

## Deployment without Front-end (Optional)

The LLMChatLinker can be deployed without the front-end application in a [Python](https://www.python.org/) environment.

If you want to deploy the LLMChatLinker without the front-end, you can follow the steps below:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/cjlee7128/LLMChatLinker.git
    cd LLMChatLinker
    ```

2. **Run PostgreSQL service using Docker:**

    ```bash
    docker run --name my_postgres -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydatabase -p 5433:5432 -d postgres:16
    ```

3. **Run RabbitMQ service using Docker:**

    ```bash
    docker run -d -e RABBITMQ_DEFAULT_USER=myuser -e RABBITMQ_DEFAULT_PASS=mypassword --name rabbitmq -p 5673:5672 -p 15673:15672 rabbitmq:3-management
    ```

4. **Run MLModelScope API agent using Docker:**

    Execute the following command to start the MLModelScope API agent:

    ```bash
    docker run -d -p 15555:15555 xlabub/pytorch-agent-api:latest
    ```

    If you want MLModelScope API agent not to download huggingface models every time, you can use the following command:

    ```bash
    docker run -d -e HF_HOME=/root/.cache/huggingface \
      -p 15555:15555 -v ~/.cache/huggingface:/root/.cache/huggingface xlabub/pytorch-agent-api:latest
    ```

    (Recommended) After running the MLModelScope API agent, you can query the API to download the models if not existing and to reduce the next response time even if the model is already downloaded. For example:

    ```bash
    curl http://localhost:15555/api/chat \
      -H "Content-Type: application/json" \
      -d '{
          "model": "llama_3_2_1b_instruct",
          "messages": [
              {"role": "user", "content": "What is the longest river in the world?"}
          ]
      }'
    ```

    The above command will download the `llama_3_2_1b_instruct` model if it does not exist and generate a response for the given user message.

5. **Run the LLMChatLinker service without using api:**

    ```bash
    python -m llmchatlinker.main_without_api 
    ```

6. **(Optional) Run Example Scripts:**

    You can run the example scripts provided in the `examples` directory to interact with the LLMChatLinker service.

    ```bash
    python -m examples.1_create_user
    python -m examples.2_create_chat
    python -m examples.3_add_llm_provider
    python -m examples.4_add_llm
    python -m examples.5_generate_llm_response
    python -m examples.12_llm_response_regenerate
    ```

    Make sure to replace the placeholders with the actual IDs generated during the execution of the previous scripts.

## Usage

### Instructions

#### User-related Instructions

- **USER_CREATE**: Create a new user.
- **USER_UPDATE**: Update an existing user.
- **USER_DELETE**: Delete an existing user.
- **USER_LIST**: List all users.
- **USER_GET**: Get a user by username or ID.
- **USER_INSTRUCTION_RECORDING_ENABLE**: Enable instruction recording for a user.
- **USER_INSTRUCTION_RECORDING_DISABLE**: Disable instruction recording for a user.
- **USER_INSTRUCTION_RECORDS_DELETE**: Delete all instruction records for a user.
- **USER_INSTRUCTION_RECORDS_LIST**: List all instruction records for a user.

#### Chat-related Instructions

- **CHAT_CREATE**: Create a new chat.
- **CHAT_UPDATE**: Update an existing chat.
- **CHAT_DELETE**: Delete an existing chat.
- **CHAT_LOAD**: Load an existing chat.
- **CHAT_LIST**: List all chats.
- **CHAT_LIST_BY_USER**: List all chats for a user.

#### LLM-related Instructions

- **LLM_RESPONSE_GENERATE**: Generate a response from the LLM.
- **LLM_RESPONSE_REGENERATE**: Regenerate a response from the LLM.
- **LLM_PROVIDER_ADD**: Add a new LLM provider.
- **LLM_PROVIDER_UPDATE**: Update an existing LLM provider.
- **LLM_PROVIDER_DELETE**: Delete an LLM provider.
- **LLM_PROVIDER_LIST**: List all LLM providers.
- **LLM_ADD**: Add a new LLM.
- **LLM_UPDATE**: Update an existing LLM.
- **LLM_DELETE**: Delete an LLM.
- **LLM_LIST**: List all LLMs.
- **LLM_LIST_BY_PROVIDER**: List all LLMs for a provider.

### Examples

Below are some example usage scripts to interact with LLMChatLinker.

#### 1. Create a User

User creation requires a username and a profile. The response will contain the user ID. The user ID is required for subsequent instructions.

```python
from llmchatlinker.client import LLMChatLinkerClient
from config_utils import read_config, write_config

def main():
    client = LLMChatLinkerClient()
    response = client.create_user(username="john_doe", profile="Sample profile")
    print(f" [x] Received {response}")
    user_id = response['data']['user']['user_id']
    print(f" [x] User ID: {user_id}")

    # Save user_id to config.json
    config = read_config()
    config['user_id'] = user_id
    write_config(config)

if __name__ == "__main__":
    main()
```

#### 2. Create a Chat

Chat creation requires a title and a list of user_ids. The response will contain the chat ID. The chat ID is required for subsequent instructions.

You can get the User ID from the response of the previous instruction.

```python
from llmchatlinker.client import LLMChatLinkerClient
from config_utils import read_config, write_config

def main():
    client = LLMChatLinkerClient()

    # Load user_id from config.json
    config = read_config()
    user_id = config.get('user_id')

    response = client.create_chat(title="Sample Chat", user_ids=[user_id])
    print(f" [x] Received {response}")
    chat_id = response['data']['chat']['chat_id']
    print(f" [x] Chat ID: {chat_id}")

    # Save chat_id to config.json
    config['chat_id'] = chat_id
    write_config(config)

if __name__ == "__main__":
    main()
```

#### 3. Add an LLM Provider

LLM Provider addition requires a name and an API endpoint. The response will contain the LLM Provider ID. The LLM Provider ID is required for subsequent instructions.

```python
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
```

#### 4. Add an LLM

LLM addition requires an LLM Provider ID and an LLM name. The response will contain the LLM ID. The LLM ID is required for subsequent instructions.

You can get the LLM Provider ID from the response of the previous instruction.

```python
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
```

#### 5. Generate an LLM Response

LLM response generation requires a User ID, Chat ID, LLM Provider ID, LLM ID, and user input. The response will contain the message ID. The message ID is required for subsequent instructions.

You can get the User ID, Chat ID, LLM Provider ID, and LLM ID from the responses of the previous instructions.

```python
from llmchatlinker.client import LLMChatLinkerClient
from config_utils import read_config, write_config

def main():
    client = LLMChatLinkerClient()

    # Load necessary IDs from config.json
    config = read_config()
    user_id = config.get('user_id')
    chat_id = config.get('chat_id')
    provider_id = config.get('provider_id')
    llm_id = config.get('llm_id')

    response = client.generate_llm_response(
        user_id=user_id,
        chat_id=chat_id,
        provider_id=provider_id,
        llm_id=llm_id,
        user_input="What is the longest river in the world?"
    )
    print(f" [x] Received {response}")
    message_id = response['data']['llm_response']['message_id']
    print(f" [x] Message ID: {message_id}")

    # Save message_id to config.json
    config['message_id'] = message_id
    write_config(config)

if __name__ == "__main__":
    main()
```

#### 6. Regenerate an LLM Response

LLM response reg-eneration requires a Message ID. The response will contain the re-generated response.

You can get the Message ID from the response of the previous instruction.

```python
from llmchatlinker.client import LLMChatLinkerClient
from config_utils import read_config, write_config

def main():
    client = LLMChatLinkerClient()

    # Load message_id from config.json
    config = read_config()
    message_id = config.get('message_id')

    response = client.regenerate_llm_response(message_id=message_id)
    print(f" [x] Received {response}")
    new_message_id = response['data']['llm_response']['message_id']
    print(f" [x] New Message ID: {new_message_id}")

    # Save new_message_id to config.json
    config['message_id'] = new_message_id
    write_config(config)

if __name__ == "__main__":
    main()
```
