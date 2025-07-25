# Fantasy Football Player Extraction System

A refactored Python application for extracting player information from images using Azure OpenAI, with validation and storage capabilities.

## Architecture

The application follows a clean architecture pattern with separation of concerns:

```
scoritoAgent/
├── config/
│   ├── __init__.py
│   └── settings.py                    # Environment variables and configuration
├── utils/
│   ├── __init__.py
│   ├── image_utils.py                 # Image encoding and file operations
│   ├── logging_utils.py               # Log Analytics integration
│   └── schema_loader.py               # Schema and prompt loading utilities
├── services/
│   ├── __init__.py
│   ├── image_extraction_service.py    # Core image extraction logic
│   ├── validation_service.py          # Validation logic
│   ├── cosmos_service.py              # Cosmos DB operations
│   └── bing_service.py                # Bing search functionality
├── models/
│   ├── __init__.py
│   └── player_models.py               # Data models/classes for players
├── processors/
│   ├── __init__.py
│   └── image_processor.py             # Main orchestration logic
├── main.py                            # Entry point
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

## Components

### Configuration (`config/`)
- **settings.py**: Centralized configuration management with environment variable loading

### Models (`models/`)
- **player_models.py**: Data classes for Player, ValidationResult, and other domain objects

### Utilities (`utils/`)
- **image_utils.py**: Image processing utilities (base64 encoding, file validation)
- **logging_utils.py**: Azure Log Analytics integration and logging utilities
- **schema_loader.py**: Utilities for loading prompts and JSON schemas

### Services (`services/`)
- **image_extraction_service.py**: OpenAI-based image analysis and player extraction
- **validation_service.py**: Validation of extracted data against original images
- **cosmos_service.py**: Cosmos DB operations for data persistence
- **bing_service.py**: Bing search integration for data enhancement

### Processors (`processors/`)
- **image_processor.py**: Main orchestration logic that coordinates all services

## Usage

### Basic Usage

```python
from main import process_goalkeepers

# Process all goalkeeper images
players = process_goalkeepers()
```

### Custom Processing

```python
from config.settings import settings
from main import initialize_services

# Initialize services
services = initialize_services()
image_processor = services['image_processor']
schema_loader = services['schema_loader']

# Load schemas and prompts
extraction_prompt = schema_loader.get_image_extraction_prompt()
validation_prompt = schema_loader.get_validate_image_extraction_prompt()
extraction_schema = schema_loader.get_response_schema()
validation_schema = schema_loader.get_validation_schema()

# Process a specific directory
players = image_processor.process_all_images_in_directory(
    base_dir=settings.players_dir / 'defenders',
    extraction_prompt=extraction_prompt,
    validation_prompt=validation_prompt,
    extraction_schema=extraction_schema,
    validation_schema=validation_schema,
    store_in_cosmos=True
)
```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
# Cosmos DB
COSMOS_DB_URI=your_cosmos_db_uri
COSMOS_DB_KEY=your_cosmos_db_key
COSMOS_DB_DATABASE=your_database_name
COSMOS_DB_CONTAINER=your_container_name

# Azure OpenAI
OPENAI_API_KEY=your_openai_api_key
OPENAI_ENDPOINT=your_openai_endpoint
OPENAI_DEPLOYMENT=gpt-4.1
OPENAI_API_VERSION=2024-12-01-preview

# Log Analytics (optional)
LOG_ANALYTICS_WORKSPACE_ID=your_workspace_id
LOG_ANALYTICS_SHARED_KEY=your_shared_key
LOG_ANALYTICS_LOG_TYPE=PlayerExtractionLog
```

## File Structure Requirements

The application expects the following file structure:

```
scoritoAgent/
├── prompts/
│   ├── imageExtraction.txt            # Main extraction prompt
│   └── validateImageExtraction.txt    # Validation prompt
├── schemas/
│   ├── playerdata.json               # Player data response schema
│   └── validate.json                 # Validation response schema
└── players-round1/
    ├── goalkeepers/
    ├── defenders/
    ├── midfielders/
    └── forwards/
```

## Benefits of Refactored Architecture

1. **Separation of Concerns**: Each component has a single responsibility
2. **Testability**: Services can be unit tested independently
3. **Maintainability**: Changes are isolated to specific modules
4. **Reusability**: Services can be reused across different workflows
5. **Error Handling**: Better error isolation and debugging
6. **Configuration Management**: Centralized configuration with validation

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the main application
python main.py
```

## Testing Individual Components

```python
# Test Bing search
from main import test_bing_search
results = test_bing_search()

# Test individual services
from main import initialize_services
services = initialize_services()

# Test extraction service
extraction_service = services['extraction_service']
# ... use service methods
```
