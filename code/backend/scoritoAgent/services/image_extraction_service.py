import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from openai import AzureOpenAI

from models.player_models import Player
from utils.logging_utils import LogAnalyticsLogger
from utils.image_utils import encode_image_to_base64

class ImageExtractionService:
    """Service for extracting player information from images using OpenAI"""
    
    def __init__(self, openai_client: AzureOpenAI, deployment: str, logger: LogAnalyticsLogger):
        self.client = openai_client
        self.deployment = deployment
        self.logger = logger
    
    def extract_info_from_image(self, image_path: Path, prompt: str, schema: Dict[str, Any]) -> Optional[List[Player]]:
        """
        Extract player information from an image
        
        Args:
            image_path: Path to the image file
            prompt: System prompt for extraction
            schema: Response schema for structured output
            
        Returns:
            List of Player objects or None if extraction fails
        """
        try:
            image_b64 = encode_image_to_base64(image_path)
            self.logger.log_info(f"Extracting info from image: {str(image_path)}")
            
            messages = self._create_messages(image_b64, prompt)
            response_format = self._format_response_schema(schema)
            
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                response_format=response_format
            )
            
            result = response.choices[0].message.content
            self.logger.log_info(f"OpenAI extraction completed for image: {str(image_path)}")
            
            return self._parse_extraction_result(result)
            
        except Exception as e:
            self.logger.log_error(f"Azure OpenAI extraction failed: {e}", image_path=str(image_path))
            return None
    
    def _create_messages(self, image_b64: str, prompt: str) -> List[Dict[str, Any]]:
        """
        Create messages for OpenAI API call
        
        Args:
            image_b64: Base64 encoded image
            prompt: System prompt
            
        Returns:
            List of message dictionaries
        """
        return [
            {"role": "system", "content": prompt},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
            ]}
        ]
    
    def _format_response_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format schema for OpenAI structured output
        
        Args:
            schema: Raw schema dictionary
            
        Returns:
            Formatted response format dictionary
        """
        return {
            "type": "json_schema",
            "json_schema": {
                "name": "player_extraction",
                "strict": True,
                "schema": schema
            }
        }
    
    def _parse_extraction_result(self, result: str) -> List[Player]:
        """
        Parse the JSON result and convert to Player objects
        
        Args:
            result: JSON string from OpenAI response
            
        Returns:
            List of Player objects
        """
        try:
            parsed_result = json.loads(result)
            players_data = parsed_result.get("players", [])
            
            players = []
            for player_data in players_data:
                player = Player(
                    name=player_data.get("name", ""),
                    team=player_data.get("team", ""),
                    points=player_data.get("points", ""),
                    worth=player_data.get("worth", ""),
                    jersey=player_data.get("jersey", ""),
                    position=player_data.get("position", "")
                )
                players.append(player)
            
            return players
            
        except json.JSONDecodeError as e:
            self.logger.log_error(f"Failed to parse extraction result JSON: {e}")
            return []
        except Exception as e:
            self.logger.log_error(f"Error parsing extraction result: {e}")
            return []
