import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from openai import AzureOpenAI

from models.player_models import Player, ValidationResult
from utils.logging_utils import LogAnalyticsLogger
from utils.image_utils import encode_image_to_base64

class ValidationService:
    """Service for validating extracted player information"""
    
    def __init__(self, openai_client: AzureOpenAI, deployment: str, logger: LogAnalyticsLogger):
        self.client = openai_client
        self.deployment = deployment
        self.logger = logger
    
    def validate_image_extraction(
        self, 
        extracted_players: List[Player], 
        image_file: Path, 
        prompt_template: str,
        schema: Dict[str, Any]
    ) -> Optional[ValidationResult]:
        """
        Validate extracted player information against the original image
        
        Args:
            extracted_players: List of extracted Player objects
            image_file: Path to the original image file
            prompt_template: Validation prompt template
            schema: Response schema for validation
            
        Returns:
            ValidationResult object or None if validation fails
        """
        try:
            # Convert players to JSON for validation
            players_json = self._players_to_json(extracted_players)
            
            # Format the validation prompt
            formatted_content = prompt_template.format(
                image_data=f"data:image/jpeg;base64,{encode_image_to_base64(image_file)}",
                json_extracted=players_json
            )
            
            self.logger.log_info(f"Validating extraction for image: {str(image_file)}")
            
            messages = [{"role": "user", "content": formatted_content}]
            response_format = self._format_response_schema(schema)
            
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                response_format=response_format
            )
            
            result = response.choices[0].message.content
            return self._parse_validation_result(result)
            
        except Exception as e:
            self.logger.log_error(f"Azure OpenAI validation failed: {e}", image_path=str(image_file))
            return None
    
    def is_validation_score_acceptable(self, score: int, threshold: int = 8) -> bool:
        """
        Check if validation score meets the threshold
        
        Args:
            score: Validation score
            threshold: Minimum acceptable score
            
        Returns:
            True if score is acceptable, False otherwise
        """
        return score >= threshold
    
    def _players_to_json(self, players: List[Player]) -> str:
        """
        Convert list of Player objects to JSON string
        
        Args:
            players: List of Player objects
            
        Returns:
            JSON string representation
        """
        players_data = []
        for player in players:
            players_data.append({
                "name": player.name,
                "team": player.team,
                "points": player.points,
                "worth": player.worth,
                "jersey": player.jersey,
                "position": player.position
            })
        
        return json.dumps({"players": players_data}, indent=2)
    
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
                "name": "validate",
                "strict": True,
                "schema": schema
            }
        }
    
    def _parse_validation_result(self, result: str) -> Optional[ValidationResult]:
        """
        Parse validation result JSON and convert to ValidationResult object
        
        Args:
            result: JSON string from OpenAI response
            
        Returns:
            ValidationResult object or None if parsing fails
        """
        try:
            parsed_result = json.loads(result)
            validate_data = parsed_result.get("validate", {})
            
            return ValidationResult(
                score=validate_data.get("score", 0),
                justification=validate_data.get("justification", "")
            )
            
        except json.JSONDecodeError as e:
            self.logger.log_error(f"Failed to parse validation result JSON: {e}")
            return None
        except Exception as e:
            self.logger.log_error(f"Error parsing validation result: {e}")
            return None
