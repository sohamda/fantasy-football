import logging
import os
import base64
import asyncio
import json
from pathlib import Path

from azure.ai.agents.aio import AgentsClient

from azure.ai.agents.models import (
    Agent,
    AgentThread,
    AsyncToolSet,
    BingGroundingTool,
)
from azure.identity.aio import DefaultAzureCredential
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).parent.parent.parent.parent / '.env')

# Set up logging
logger = logging.getLogger('extraction_agent')
logger.setLevel(logging.INFO)

def log_to_loganalytics(message, custom_dimensions=None):
    # Placeholder for Log Analytics logging
    # You may need to implement a custom sender for Log Analytics HTTP Data Collector API
    #logger.info(f"LogAnalytics: {message} | {custom_dimensions}")
    print(f"Info Log: {message}")

def get_prompt():
    prompt_path = Path(__file__).parent / 'player_extraction_prompt.txt'
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def encode_image_to_base64(image_path):
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def get_ai_agents_client():
    return AgentsClient(
        endpoint=os.getenv('PROJECT_ENDPOINT'),
        credential=DefaultAzureCredential()
    )

async def create_agent() -> tuple[Agent, AgentThread]:
    client = get_ai_agents_client()

    conn_id = os.environ["BING_CONNECTION_ID"]
    bing = BingGroundingTool(connection_id=conn_id)
    
    created_agent = await client.create_agent(
        model=os.environ["OPENAI_DEPLOYMENT"],
        name="PlayerExtractionAgent",
        description="An agent to extract player information from Scorito screenshots",
        tools=bing.definitions,
        instructions=get_prompt()
    )
    log_to_loganalytics(f"Agent created: {created_agent.id}")

    thread = await client.threads.create()
    log_to_loganalytics(f"Thread created: {thread.id}")

    return created_agent, thread

async def extract_info_from_image(agent, thread, image_path):
    image_b64 = encode_image_to_base64(image_path)

    client = get_ai_agents_client()

    message = await client.messages.create(
        thread_id=thread.id,
        role="user",
        content="{\"type\": \"image_url\", \"image_url\": {\"url\": f\"data:image/jpeg;base64,"+ image_b64 +"}}"
    )

    log_to_loganalytics(f"Message created: {message.id}")

    run = await client.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id,)
    
    log_to_loganalytics(f"Run finished with status: {run.status}")

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")
    else:
        messages = client.messages.list(thread_id=thread.id, order="asc")
        last_message = None
        async for message in messages:
            last_message = message
            
            #    print(f"Role: {message.role}, Content: {message.content}")
            #reply = list(client.messages.list(thread_id=thread.id, order="asc"))[-1].text_messages[-1].text.value
        log_to_loganalytics(f"Agent response: {last_message.text_messages[0].text.value}")
        return json.loads(last_message.text_messages[0].text.value)



async def process_all_images(agent, thread):
    base_dir = Path(__file__).parent / 'players-round1/goalkeepers'
    #print(f"Base directory: {base_dir}")
    #for folder in base_dir.iterdir():
        #if folder.is_dir():
            #print(f"Processing folder: {folder}")
    extracted_players = []
    for img_file in base_dir.glob('**/*.jpeg'):
        log_to_loganalytics(f"Processing {img_file}")
        print(f"Processing {img_file}")
        info = await extract_info_from_image(agent, thread, img_file)
        if info:
            if isinstance(info, list):
                extracted_players.extend(info)
            else:
                extracted_players.append(info)

    # Now store all extracted players in CosmosDB
    log_to_loganalytics(f"Extracted players: {extracted_players}")


async def main():
    agent, thread = await create_agent()

    if not agent or not thread:
            log_to_loganalytics("Initialization failed. Ensure you have uncommented the instructions file for the lab.")
            log_to_loganalytics("Exiting...")
            return
    await process_all_images(agent, thread)

if __name__ == "__main__":
    asyncio.run(main())