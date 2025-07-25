import json
from pathlib import Path
from typing import Dict, Any

class SchemaLoader:
    """Utility class for loading schemas and prompts"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.prompts_dir = base_dir / 'prompts'
        self.schemas_dir = base_dir / 'schemas'
    
    def get_image_extraction_prompt(self) -> str:
        """Load the image extraction prompt"""
        prompt_path = self.prompts_dir / 'imageExtraction.txt'
        return self._load_text_file(prompt_path)
    
    def get_validate_image_extraction_prompt(self) -> str:
        """Load the validation prompt"""
        prompt_path = self.prompts_dir / 'validateImageExtraction.txt'
        return self._load_text_file(prompt_path)
    
    def get_response_schema(self) -> Dict[str, Any]:
        """Load the player data response schema"""
        schema_path = self.schemas_dir / 'playerdata.json'
        return self._load_json_file(schema_path)
    
    def get_validation_schema(self) -> Dict[str, Any]:
        """Load the validation response schema"""
        schema_path = self.schemas_dir / 'validate.json'
        return self._load_json_file(schema_path)
    
    def _load_text_file(self, file_path: Path) -> str:
        """Load content from a text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file not found: {file_path}")
        except Exception as e:
            raise Exception(f"Error loading text file {file_path}: {e}")
    
    def _load_json_file(self, file_path: Path) -> Dict[str, Any]:
        """Load content from a JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Schema file not found: {file_path}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON in file {file_path}: {e}")
        except Exception as e:
            raise Exception(f"Error loading JSON file {file_path}: {e}")
