import os
from pathlib import Path
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        # Load environment variables
        load_dotenv(dotenv_path=Path(__file__).parent.parent.parent.parent.parent / '.env')
        
        # Cosmos DB Configuration
        self.cosmos_db_uri = os.getenv('COSMOS_DB_URI')
        self.cosmos_db_key = os.getenv('COSMOS_DB_KEY')
        self.cosmos_db_database = os.getenv('COSMOS_DB_DATABASE')
        self.cosmos_db_container = os.getenv('COSMOS_DB_CONTAINER')
        
        # OpenAI Configuration
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.openai_endpoint = os.getenv('OPENAI_ENDPOINT')
        self.openai_deployment = os.getenv('OPENAI_DEPLOYMENT', 'gpt-4.1')
        self.openai_api_version = os.getenv('OPENAI_API_VERSION', '2024-12-01-preview')
        
        # Log Analytics Configuration
        self.log_analytics_workspace_id = os.getenv('LOG_ANALYTICS_WORKSPACE_ID')
        self.log_analytics_shared_key = os.getenv('LOG_ANALYTICS_SHARED_KEY')
        self.log_analytics_log_type = os.getenv('LOG_ANALYTICS_LOG_TYPE', 'PlayerExtractionLog')
        
        # Bing Search Configuration
        self.foundry_agent_endpoint = os.getenv('PROJECT_ENDPOINT')
        self.bing_connection_id = os.environ["BING_CONNECTION_ID"]
        
        # Validation Configuration
        self.validation_threshold = 8
        self.max_retries = 3
        
        # File Paths
        self.base_dir = Path(__file__).parent.parent
        self.players_dir = self.base_dir / 'players-round1'
        self.prompts_dir = self.base_dir / 'prompts'
        self.schemas_dir = self.base_dir / 'schemas'
    
    def validate_config(self):
        """Validate that all required configuration is present"""
        required_fields = [
            'cosmos_db_uri', 'cosmos_db_key', 'cosmos_db_database', 'cosmos_db_container',
            'openai_api_key', 'openai_endpoint'
        ]
        
        missing_fields = []
        for field in required_fields:
            if not getattr(self, field):
                missing_fields.append(field.upper())
        
        if missing_fields:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_fields)}")

# Global settings instance
settings = Settings()
