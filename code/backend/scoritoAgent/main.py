#!/usr/bin/env python3
"""
Main entry point for the player extraction system.
"""

import asyncio
from pathlib import Path
from openai import AzureOpenAI

from config import settings
from utils import LogAnalyticsLogger, SchemaLoader
from services import ImageExtractionService, ValidationService, CosmosService, BingService
from processors import ImageProcessor

def initialize_services():
    """Initialize all services and dependencies"""
    
    # Validate configuration
    settings.validate_config()
    
    # Initialize logger
    logger = LogAnalyticsLogger(
        workspace_id=settings.log_analytics_workspace_id,
        shared_key=settings.log_analytics_shared_key,
        log_type=settings.log_analytics_log_type
    )
    
    # Initialize OpenAI client
    openai_client = AzureOpenAI(
        api_version=settings.openai_api_version,
        azure_endpoint=settings.openai_endpoint,
        api_key=settings.openai_api_key,
        azure_deployment=settings.openai_deployment
    )
    
    # Initialize schema loader
    schema_loader = SchemaLoader(settings.base_dir)
    
    # Initialize services
    extraction_service = ImageExtractionService(
        openai_client=openai_client,
        deployment=settings.openai_deployment,
        logger=logger
    )
    
    validation_service = ValidationService(
        openai_client=openai_client,
        deployment=settings.openai_deployment,
        logger=logger
    )
    
    cosmos_service = CosmosService(
        uri=settings.cosmos_db_uri,
        key=settings.cosmos_db_key,
        database=settings.cosmos_db_database,
        container=settings.cosmos_db_container,
        logger=logger
    )
    
    return {
        'logger': logger,
        'schema_loader': schema_loader,
        'extraction_service': extraction_service,
        'validation_service': validation_service,
        'cosmos_service': cosmos_service,
        'openai_client': openai_client
    }

async def process_goalkeepers():
    """Process goalkeeper images"""
    
    services = initialize_services()
    logger = services['logger']
    schema_loader = services['schema_loader']
    extraction_service = services['extraction_service']
    validation_service = services['validation_service']
    cosmos_service = services['cosmos_service']
    
    try:
        # Load prompts and schemas
        extraction_prompt = schema_loader.get_image_extraction_prompt()
        validation_prompt = schema_loader.get_validate_image_extraction_prompt()
        extraction_schema = schema_loader.get_response_schema()
        validation_schema = schema_loader.get_validation_schema()
        
        # Set up directories
        goalkeepers_dir = settings.players_dir / 'goalkeepers'
        
        logger.log_info("Starting goalkeeper processing")
        
        # Initialize BingService with async context manager
        async with BingService(
            foundry_agent_endpoint= settings.foundry_agent_endpoint,
            bing_connection_id=settings.bing_connection_id,
            logger=logger,
            openai_deployment=settings.openai_deployment
        ) as bing_service:
            
            # Initialize processor with BingService
            image_processor = ImageProcessor(
                extraction_service=extraction_service,
                validation_service=validation_service,
                cosmos_service=cosmos_service,
                bing_service=bing_service,
                logger=logger,
                validation_threshold=settings.validation_threshold,
                max_retries=settings.max_retries
            )
            
            # Process all images
            extracted_players = await image_processor.process_all_images_in_directory(
                base_dir=goalkeepers_dir,
                extraction_prompt=extraction_prompt,
                validation_prompt=validation_prompt,
                extraction_schema=extraction_schema,
                validation_schema=validation_schema,
                store_in_cosmos=False  # Disable Cosmos DB storage with Bing validation
            )
        
        logger.log_info(f"Processing completed. Total players extracted: {len(extracted_players)}")
        
        # Print summary
        for i, player in enumerate(extracted_players):
            print(f"Player {i+1}: {player.name} ({player.team}) - {player.position}")
        
        return extracted_players
        
    except Exception as e:
        logger.log_error(f"Error in main processing: {e}")
        raise

if __name__ == "__main__":
    # Process goalkeeper images
    asyncio.run(process_goalkeepers())
    
