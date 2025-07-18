
import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv
from azure.cosmos import CosmosClient
from azure.loganalytics import LogAnalyticsDataClient
from azure.loganalytics.models import QueryBody
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from PIL import Image
import base64
import uuid

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).parent.parent.parent.parent / '.env')

COSMOS_DB_URI = os.getenv('COSMOS_DB_URI')
COSMOS_DB_KEY = os.getenv('COSMOS_DB_KEY')
COSMOS_DB_DATABASE = os.getenv('COSMOS_DB_DATABASE')
COSMOS_DB_CONTAINER = os.getenv('COSMOS_DB_CONTAINER')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ENDPOINT = os.getenv('OPENAI_ENDPOINT')
OPENAI_DEPLOYMENT = os.getenv('OPENAI_DEPLOYMENT', 'gpt-4.1')
OPENAI_API_VERSION = os.getenv('OPENAI_API_VERSION', '2024-12-01-preview')
LOG_ANALYTICS_WORKSPACE_ID = os.getenv('LOG_ANALYTICS_WORKSPACE_ID')
LOG_ANALYTICS_SHARED_KEY = os.getenv('LOG_ANALYTICS_SHARED_KEY')
LOG_ANALYTICS_LOG_TYPE = os.getenv('LOG_ANALYTICS_LOG_TYPE', 'PlayerExtractionLog')

# Set up logging
logger = logging.getLogger('player_extraction')
logger.setLevel(logging.INFO)

def log_to_loganalytics(message, custom_dimensions=None):
    # Placeholder for Log Analytics logging
    # You may need to implement a custom sender for Log Analytics HTTP Data Collector API
    logger.info(f"LogAnalytics: {message} | {custom_dimensions}")
    #print(f"Info Log: {message}")

# Set up Azure OpenAI client
if OPENAI_API_KEY and OPENAI_ENDPOINT:
    openai_client = AzureOpenAI(
        api_version=OPENAI_API_VERSION,
        azure_endpoint=OPENAI_ENDPOINT,
        api_key=OPENAI_API_KEY,
        azure_deployment=OPENAI_DEPLOYMENT
)
else:
    raise ValueError("OPENAI_ENDPOINT must be set in the environment.")

def get_prompt():
    prompt_path = Path(__file__).parent / 'player_extraction_prompt.txt'
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def encode_image_to_base64(image_path):
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')


def extract_info_from_image(image_path, prompt):
    image_b64 = encode_image_to_base64(image_path)
    log_to_loganalytics(f"Extracting info from image: {image_b64[:30]}... (truncated for logging)")
    try:
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
            ]}
        ]
        response = openai_client.chat.completions.create(
            model=OPENAI_DEPLOYMENT,
            messages=messages
        )
        #log_to_loganalytics(f"OpenAI response: {response}")
        result = response.choices[0].message.content
        return json.loads(result)
    except Exception as e:
        log_to_loganalytics(f"Azure OpenAI extraction failed: {e}", {"image_path": str(image_path)})
        return None

def store_in_cosmos(info):
    log_to_loganalytics(f"Storing info in CosmosDB: {info}")
    try:
        client = CosmosClient(COSMOS_DB_URI, credential=COSMOS_DB_KEY)
        db = client.get_database_client(COSMOS_DB_DATABASE)
        container = db.get_container_client(COSMOS_DB_CONTAINER)

        container.upsert_item(info)
        log_to_loganalytics("Stored in CosmosDB", info)
    except Exception as e:
        log_to_loganalytics(f"CosmosDB store failed: {e}", info)

# The screenshots are not committed to the repo, to protect Scorito's intellectual property.
def process_all_images():
    base_dir = Path(__file__).parent / 'players-round1/goalkeepers'
    #print(f"Base directory: {base_dir}")
    prompt = get_prompt()
    #for folder in base_dir.iterdir():
        #if folder.is_dir():
            #print(f"Processing folder: {folder}")
    extracted_players = []
    for img_file in base_dir.glob('**/*.jpeg'):
        log_to_loganalytics(f"Processing {img_file}")
        print(f"Processing {img_file}")
        info = extract_info_from_image(img_file, prompt)
        if info:
            if isinstance(info, list):
                extracted_players.extend(info)
            else:
                extracted_players.append(info)

    # Now store all extracted players in CosmosDB
    for idx, player in enumerate(extracted_players):
        pos = player.get('position', 'unknown')
        player['id'] = f"{pos}{idx}"
        store_in_cosmos(player)

if __name__ == "__main__":
    process_all_images()
