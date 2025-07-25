
import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv
from azure.cosmos import CosmosClient
from openai import AzureOpenAI
import base64
import requests

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
    #logger.info(f"LogAnalytics: {message} | {custom_dimensions}")
    print(f"Info Log: {message}")

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

def get_image_extraction_prompt():
    prompt_path = Path(__file__).parent / 'prompts/imageExtraction.txt'
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_response_schema():
    schema_path = Path(__file__).parent / 'schemas/playerdata.json'
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_validation_schema():
    schema_path = Path(__file__).parent / 'schemas/validate.json'
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def get_validate_image_extraction_prompt():
    prompt_path = Path(__file__).parent / 'prompts/validateImageExtraction.txt'
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def encode_image_to_base64(image_path):
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')
    
# Function to perform Bing Search
def bing_search(query):
    try:
        headers = {"Ocp-Apim-Subscription-Key": "9383692ece2240689f673a4b30046764",
                "resource-id": "/subscriptions/3b250d66-c6d7-48ff-b78e-351fa7f7a8eb/resourceGroups/fantasy-football/providers/Microsoft.Bing/accounts/ff-bing"}
        
        params = {"q": query, "count": 3}  # Limit results for brevity
        response = requests.get("https://api.bing.microsoft.com/", headers=headers, params=params)
        response.raise_for_status()
        results = response.json()
        log_to_loganalytics(f"Bing results: {results}")
        return [item["snippet"] for item in results.get("webPages", {}).get("value", [])]
    except Exception as e:
        log_to_loganalytics(f"Bing failed: {e}")
        return None


def validate_image_extraction(extracted_players, image_file):
    
    prompt_template = get_validate_image_extraction_prompt()
    formatted_content = prompt_template.format(
        image_data=f"data:image/jpeg;base64,{encode_image_to_base64(image_file)}",
        json_extracted=extracted_players
    )

    log_to_loganalytics(f"Validating extracted players prompt: {formatted_content}")

    schema = get_validation_schema()

    try:
        messages = [
            {"role": "user", "content": formatted_content}
        ]

        # Format the schema for OpenAI structured output
        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "validate",
                "strict": True,
                "schema": schema
            }
        }
        
        response = openai_client.chat.completions.create(
            model=OPENAI_DEPLOYMENT,
            messages=messages,
            response_format=response_format
        )
        #log_to_loganalytics(f"OpenAI response: {response}")
        result = response.choices[0].message.content
        log_to_loganalytics(f"OpenAI extraction result: {result}")
        return json.loads(result)
    except Exception as e:
        log_to_loganalytics(f"Azure OpenAI validation failed: {e}")
        return None

def extract_info_from_image(image_path, prompt):
    image_b64 = encode_image_to_base64(image_path)
    schema = get_response_schema()
    log_to_loganalytics(f"Extracting info from image: {image_b64[:30]}... (truncated for logging)")
    try:
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
            ]}
        ]
        
        # Format the schema for OpenAI structured output
        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "player_extraction",
                "strict": True,
                "schema": schema
            }
        }
        
        response = openai_client.chat.completions.create(
            model=OPENAI_DEPLOYMENT,
            messages=messages,
            response_format=response_format
        )
        #log_to_loganalytics(f"OpenAI response: {response}")
        result = response.choices[0].message.content
        log_to_loganalytics(f"OpenAI extraction result: {result}")
        parsed_result = json.loads(result)
        # Extract the players array from the response object
        return parsed_result.get("players", [])
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
    prompt = get_image_extraction_prompt()
    #for folder in base_dir.iterdir():
        #if folder.is_dir():
            #print(f"Processing folder: {folder}")
    extracted_players = []
    for img_file in base_dir.glob('**/*.jpeg'):
        log_to_loganalytics(f"Processing {img_file}")
        print(f"Processing {img_file}")
        validate = 10
        while validate >= 8:
            info = extract_info_from_image(img_file, prompt)
            validation_results = validate_image_extraction(info, img_file)
            
            # Check if validation results are valid
            if validation_results is None or 'validate' not in validation_results:
                log_to_loganalytics("Validation failed - no results returned, skipping image")
                break
                
            log_to_loganalytics(f"Validation done for image with score: {validation_results['validate']['score']}")
            validate = validation_results['validate']['score']
            if validate < 8:
                log_to_loganalytics("Validation failed for image, retrying...")
                continue
            else:
                log_to_loganalytics("Adding extracted players to the list")
                if info:
                    if isinstance(info, list):
                        extracted_players.extend(info)
                    else:
                        extracted_players.append(info)

    # Now store all extracted players in CosmosDB
    #for idx, player in enumerate(extracted_players):
    #    pos = player.get('position', 'unknown')
    #    player['id'] = f"{pos}{idx}"
    #    store_in_cosmos(player)

if __name__ == "__main__":
    process_all_images()
    #bing_search("what is an ounce")
