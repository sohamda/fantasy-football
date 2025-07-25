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

# global AgentsClient object
client = None

# Set up logging
logger = logging.getLogger('extraction_agent')
logger.setLevel(logging.INFO)

def log_to_loganalytics(message, custom_dimensions=None):
    # Placeholder for Log Analytics logging
    # You may need to implement a custom sender for Log Analytics HTTP Data Collector API
    #logger.info(f"LogAnalytics: {message} | {custom_dimensions}")
    print(f"Info Log: {message}")

def get_system_prompt():
    prompt_path = Path(__file__).parent / 'prompts/systemPrompt.txt'
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_image_extraction_prompt():
    prompt_path = Path(__file__).parent / 'prompts/imageExtraction.txt'
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_validate_image_extraction_prompt():
    prompt_path = Path(__file__).parent / 'prompts/validateImageExtraction.txt'
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_bing_search_prompt():
    prompt_path = Path(__file__).parent / 'prompts/bingSearch.txt'
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def encode_image_to_base64(image_path):
    with open(image_path, 'rb') as img_file:
        #return base64.b64encode(img_file.read()).decode('utf-8')
        return base64.b64encode(img_file.read()).decode('ascii')

def get_ai_agents_client():
    return AgentsClient(
        endpoint=os.getenv('PROJECT_ENDPOINT'),
        credential=DefaultAzureCredential()
    )

async def create_agent(client) -> tuple[Agent]:

    conn_id = os.environ["BING_CONNECTION_ID"]
    bing = BingGroundingTool(connection_id=conn_id)
    
    created_agent = await client.create_agent(
        model=os.environ["OPENAI_DEPLOYMENT"],
        name="PlayerExtractionAgent",
        description="An agent to extract player information from Scorito screenshots",
        tools=bing.definitions,
        instructions=get_system_prompt()
    )
    log_to_loganalytics(f"Agent created: {created_agent.id}")

    return created_agent

async def extract_info_from_image(client, agent, image_b64):

    thread = await client.threads.create()
    log_to_loganalytics(f"Image Processing Thread created: {thread.id}")

    promptImage = [
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}}
    ]

    promptProcess = [
        {"type": "text", "text": get_image_extraction_prompt()},
    ]


    imageMessage = await client.messages.create(
        thread_id=thread.id,
        role="user",
        content=promptImage
    )

    imagePrompt = await client.messages.create(
        thread_id=thread.id,
        role="user",
        content=promptProcess
    )

    log_to_loganalytics(f"Messages created: {imageMessage.id}, {imagePrompt.id}")

    imageProcessingRun = await client.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id,)

    log_to_loganalytics(f"Run finished with status: {imageProcessingRun.status}")

    if imageProcessingRun.status == "failed":
        log_to_loganalytics(f"Run failed: {imageProcessingRun.last_error}")
        raise Exception(f"Run failed: {imageProcessingRun.last_error}")
    else:
        messages = client.messages.list(thread_id=thread.id, order="asc")
        
        last_message = None
        async for message in messages:
            last_message = message
                    
        log_to_loganalytics(f"Agent response: {last_message.text_messages[0].text.value}")
        return json.loads(last_message.text_messages[0].text.value)

async def validate_image_extraction(client, agent, extracted_players, image_b64):
    # Implement validation logic here
    # This is a placeholder implementation
    thread = await client.threads.create()
    log_to_loganalytics(f"Image Validation Thread created: {thread.id}")

    prompt_template = get_validate_image_extraction_prompt()
    formatted_content = prompt_template.format(
        image_data=f"data:image/jpeg;base64,{image_b64}",
        json_extracted=extracted_players
    )

    log_to_loganalytics(f"Validating extracted players prompt: {formatted_content}")

    validationPrompt = await client.messages.create(
        thread_id=thread.id,
        role="user",
        content=formatted_content
    )

    log_to_loganalytics(f"Messages created: {validationPrompt.id}")

    validationRun = await client.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id,)

    log_to_loganalytics(f"Run finished with status: {validationRun.status}")

    if validationRun.status == "failed":
        log_to_loganalytics(f"Run failed: {validationRun.last_error}")
        raise Exception(f"Run failed: {validationRun.last_error}")
    else:
        messages = client.messages.list(thread_id=thread.id, order="asc")
        
        last_message = None
        async for message in messages:
            last_message = message
                    
        log_to_loganalytics(f"Agent response: {last_message.text_messages[0].text.value}")
        return last_message.text_messages[0].text.value

async def finalize_extraction_with_bing(client, agent, extracted_players):

    bing_search_prompt = get_bing_search_prompt()
    formatted_content = bing_search_prompt.format(
        extracted_players=extracted_players
    )
    thread = await client.threads.create()
    log_to_loganalytics(f"Thread created: {thread.id}")

    bingPrompt = await client.messages.create(
        thread_id=thread.id,
        role="user",
        content=formatted_content
    )
    log_to_loganalytics(f"Messages created: {bingPrompt.id}")

    bingProcessingRun = await client.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id,)

    log_to_loganalytics(f"Run finished with status: {bingProcessingRun.status}")

    if bingProcessingRun.status == "failed":
        log_to_loganalytics(f"Run failed: {bingProcessingRun.last_error}")
        raise Exception(f"Run failed: {bingProcessingRun.last_error}")
    else:
        messages = client.messages.list(thread_id=thread.id, order="asc")
        
        last_message = None
        async for message in messages:
            last_message = message
                    
        log_to_loganalytics(f"Agent response: {last_message.text_messages[0].text.value}")
        return json.loads(last_message.text_messages[0].text.value)


async def process_all_images(client, agent):
    base_dir = Path(__file__).parent / 'players-round1/goalkeepers'
    #log_to_loganalytics(f"Base directory: {base_dir}")
    #for folder in base_dir.iterdir():
        #if folder.is_dir():
            #log_to_loganalytics(f"Processing folder: {folder}")
    extracted_players = []
    for img_file in base_dir.glob('**/*.jpeg'):
        log_to_loganalytics(f"Processing {img_file}")

        validate = 10
        while validate >= 9:
            log_to_loganalytics(f"Extracting info from image: {img_file}")
            image_b64 = encode_image_to_base64(img_file)
            extracted_players = await extract_info_from_image(client, agent, image_b64)
            if not extracted_players:
                log_to_loganalytics("Failed to extract info from image")
                continue
            # Validate the extracted info
            validate = int(await validate_image_extraction(client, agent, extracted_players, image_b64))
            log_to_loganalytics(f"Validation done for image with score: {validate}")
            if validate < 9:
                log_to_loganalytics("Validation failed for image, retrying...")
                continue
            
        info = await finalize_extraction_with_bing(client, agent, extracted_players)
        if info:
            if isinstance(info, list):
                extracted_players.extend(info)
            else:
                extracted_players.append(info)
        await asyncio.sleep(10) # To avoid rate limiting issues

    # Now store all extracted players in CosmosDB
    log_to_loganalytics(f"Extracted players: {extracted_players}")


async def main():
    global client
    async with get_ai_agents_client() as client:
        agent = await create_agent(client)
        try:
            if not agent:
                log_to_loganalytics("Initialization failed. Agent failed to get created.")
                log_to_loganalytics("Exiting...")
                return
            await process_all_images(client,agent)
        except Exception as e:
            log_to_loganalytics(f"Exception occurred: {e}")
            # Optionally re-raise if you want to propagate the error
            # raise
        finally:
            # Delete the agent after execution or exception
            try:
                await client.delete_agent(agent.id)
                log_to_loganalytics(f"Agent deleted: {agent.id}")
            except Exception as delete_exc:
                log_to_loganalytics(f"Failed to delete agent: {delete_exc}")

if __name__ == "__main__":
    asyncio.run(main())