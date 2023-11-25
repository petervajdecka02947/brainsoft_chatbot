# FastAPI CLI Tool

This command-line interface (CLI) tool is designed to interact with a FastAPI backend, offering a series of commands for various API endpoints.

## Installation

To use this CLI tool, follow these simple steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/petervajdecka02947/brainsoft_chatbot.git

2. **Set backend endpoint in the .env:**
    - Use `localhost` if you are running locally.
    OR
    - Use the static or public IP address of your external server (for example, an EC2 instance in AWS) if running on a server.

3. **In root, first install docker and docker-compose and then build run your docker containers orchestrated by docker-compose.yaml file:**
   ```bash
   bash install_docker_compose.sh
   sudo docker-compose up -d
3. **API should be runnng, so you can call any request analogically to the following examples:**
   ```bash
   docker-compose run cli main.py health
   [{'status': '🤙'}]
   docker-compose run cli main.py chat_nostream "Where is maintainer SDK ?"
   [{'input': 'Where is maintainer SDK ?', 'chat_history': [], 'output': 'The maintainer SDK can be found in the IBM watsonx.ai documentation. You can explore the documentation [here](https://www.ibm.com/products/watsonx-ai).'}]
   docker-compose run cli main.py llm_chat_nostream "Query" "Context"
   [{'input': 'What is first words of the sentence?', 'context': 'I know the answer', 'text': 'I'}]
 