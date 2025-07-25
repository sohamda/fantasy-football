# BingService Migration to Azure AI Agents

## Overview
Successfully migrated the BingService from direct OpenAI API calls to Azure AI Agents with Bing grounding tool integration.

## Key Changes Made

### 1. BingService Updates (`services/bing_service.py`)

#### Imports and Dependencies
- Added Azure AI Agents imports:
  - `AgentsClient`
  - `Agent`, `AgentThread`, `BingGroundingTool`
  - `DefaultAzureCredential`
- Removed direct `AzureOpenAI` dependency
- Added `asyncio` support

#### Constructor Changes
- **Before**: Required `AzureOpenAI` client parameter
- **After**: Removed OpenAI client dependency, now uses `AgentsClient`
- Added async context manager support (`__aenter__`, `__aexit__`)

#### Agent Initialization
- Creates Azure AI Agents client using `PROJECT_ENDPOINT` and `DefaultAzureCredential`
- Creates agent with Bing grounding tool using `BING_CONNECTION_ID`
- Agent name: "PlayerValidationAgent"
- Includes proper cleanup on exit

#### Method Updates

**`finalize_extraction_with_bing()`**
- **Before**: Direct OpenAI API call with structured output
- **After**: Uses Azure AI Agents pattern:
  1. Creates thread
  2. Creates message with validation request
  3. Runs agent with `create_and_process`
  4. Retrieves response from message list

**`validate_individual_player()`**
- **Before**: Used direct Bing search + OpenAI analysis
- **After**: Uses agents pattern with Bing grounding tool for search and analysis
- Returns enhanced player information based on search results

#### Removed Methods
- `search()` - No longer needed as Bing search is handled by the grounding tool
- `_format_response_schema()` - Not needed with agents
- `_extract_snippets()` - Handled by Bing grounding tool

### 2. ImageProcessor Updates (`processors/image_processor.py`)

#### Async Support
- Made `process_single_image()` async
- Made `process_all_images_in_directory()` async
- Made `_validate_players_with_bing()` async
- All Bing validation calls now use `await`

### 3. Main Application Updates (`main.py`)

#### Service Initialization
- Removed BingService from `initialize_services()`
- BingService now created with async context manager in processing functions

#### Async Function Updates
- `process_goalkeepers()` is now async
- `test_bing_search()` is now async
- Main execution uses `asyncio.run()`

#### Context Manager Usage
```python
async with BingService(...) as bing_service:
    # Use bing_service for validation
    image_processor = ImageProcessor(...)
    await image_processor.process_all_images_in_directory(...)
```

### 4. Environment Variables Required

The following environment variables must be set:
- `PROJECT_ENDPOINT` - Azure AI Project endpoint
- `BING_CONNECTION_ID` - Bing search connection ID
- `OPENAI_DEPLOYMENT` - Model deployment name

### 5. New Test Script (`test_bing_agents.py`)

Created comprehensive test script that:
- Tests BingService initialization with Azure AI Agents
- Tests batch player validation
- Tests individual player validation
- Includes proper error handling and reporting

## Benefits of Migration

1. **Integrated Bing Search**: Direct access to Bing search through grounding tool
2. **Better Error Handling**: Azure AI Agents provides robust error handling
3. **Scalability**: Azure AI Agents handles rate limiting and optimization
4. **Consistency**: Uses the same pattern as the original `extractionAgent.py`
5. **Authentication**: Uses Azure identity for secure access

## Usage Pattern

```python
# Initialize with async context manager
async with BingService(
    subscription_key=settings.bing_subscription_key,
    resource_id=settings.bing_resource_id,
    endpoint=settings.bing_endpoint,
    logger=logger,
    deployment=settings.openai_deployment
) as bing_service:
    
    # Batch validation
    validated_players = await bing_service.finalize_extraction_with_bing(players)
    
    # Individual validation
    validated_player = await bing_service.validate_individual_player(player)
```

## Testing

Run the test script to verify functionality:
```bash
cd code/backend/scoritoAgent
python test_bing_agents.py
```

## Integration with Existing Workflow

The updated BingService integrates seamlessly with the existing image processing pipeline:
1. Images are processed and players extracted
2. Players are validated using OpenAI Vision
3. **NEW**: Players are enhanced and validated using Bing search through Azure AI Agents
4. Results can be stored in Cosmos DB

This maintains the existing workflow while adding powerful Bing search validation capabilities.
