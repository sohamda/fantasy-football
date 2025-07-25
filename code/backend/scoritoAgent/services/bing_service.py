import json
from typing import List, Optional, Dict, Any
from pathlib import Path
from azure.ai.agents.aio import AgentsClient
from azure.ai.agents.models import (
    BingGroundingTool,
)
from azure.identity.aio import DefaultAzureCredential
from utils.logging_utils import LogAnalyticsLogger
from utils.schema_loader import SchemaLoader
from models.player_models import Player

class BingService:
    """Service for Bing search functionality and player validation using Azure AI Agents"""
    
    def __init__(self, foundry_agent_endpoint: str, bing_connection_id: str,
                 logger: LogAnalyticsLogger, openai_deployment: str):
        
        self.foundry_agent_endpoint = foundry_agent_endpoint
        self.deployment = openai_deployment
        self.bing_connection_id = bing_connection_id    
        self.logger = logger
        self.agents_client = None
        self.agent = None
                
        # Initialize schema loader with base directory
        self.schema_loader = SchemaLoader(Path(__file__).parent.parent)
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self._initialize_agents_client()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self._cleanup()
    
    async def _initialize_agents_client(self):
        """Initialize the Azure AI Agents client and create agent"""
        try:
            self.agents_client = AgentsClient(
                endpoint=self.foundry_agent_endpoint,
                credential=DefaultAzureCredential()
            )
            
            # Create agent with Bing grounding tool
            bing = BingGroundingTool(connection_id=self.bing_connection_id)
            
            self.agent = await self.agents_client.create_agent(
                model=self.deployment,
                name="PlayerValidationAgentWithBing",
                description="An agent to validate and enhance player information using Bing search",
                tools=bing.definitions,
                instructions="An agent to validate and enhance player information using Bing search."
            )
            
            self.logger.log_info(f"Agent created: {self.agent.id}")
            
        except Exception as e:
            self.logger.log_error(f"Failed to initialize agents client: {e}")
            raise
    
    async def _cleanup(self):
        """Cleanup agent and client"""
        try:
            if self.agent and self.agents_client:
                await self.agents_client.delete_agent(self.agent.id)
                await self.agents_client.close()
                self.logger.log_info(f"Agent deleted: {self.agent.id}")
        except Exception as e:
            self.logger.log_error(f"Failed to cleanup agent: {e}")
    
    def _get_bing_search_prompt(self) -> str:
        """Load the Bing search prompt"""
        try:
            # Try to load from prompts directory
            prompt_path = Path(__file__).parent.parent / 'prompts/bingSearch.txt'
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            # Fallback prompt if file doesn't exist
            return """
            Please use Bing search to validate and enhance the following player information.
            For each player, search for their current team, position, and other details.
            Update any incorrect information based on the search results.
            
            Players to validate:
            {extracted_players}
            
            IMPORTANT: Return ONLY valid JSON in the exact format below, with no additional text or markdown:
            {{
                "players": [
                    {{
                        "name": "player name",
                        "team": "team name",
                        "points": "points value",
                        "worth": "worth value", 
                        "jersey": "jersey number",
                        "position": "position"
                    }}
                ]
            }}
            """
    
    async def finalize_extraction_with_bing(self, extracted_players: List[Player]) -> List[Player]:
        """
        Use Bing search to validate and enhance player information using Azure AI Agents
        
        Args:
            extracted_players: List of Player objects to validate and enhance
            
        Returns:
            List of validated and enhanced Player objects
        """
        self.logger.log_info("Using Bing search prompt for validation")
        try:
            if not self.agents_client or not self.agent:
                self.logger.log_error("Agents client or agent not initialized")
                return extracted_players
            
            # Get the Bing search prompt
            bing_search_prompt = self._get_bing_search_prompt()
            
            # Convert players to JSON format for the prompt
            players_json = self._players_to_json(extracted_players)
            
            # Format the prompt with extracted players
            formatted_content = bing_search_prompt.format(
                extracted_players=players_json
            )
                        
            # Create thread for this validation session
            thread = await self.agents_client.threads.create()
            self.logger.log_info(f"Thread created: {thread.id}")
            
            # Create message with the validation request
            message = await self.agents_client.messages.create(
                thread_id=thread.id,
                role="user",
                content=formatted_content
            )
            self.logger.log_info(f"Message created: {message.id}")
            
            # Run the agent to process the validation
            run = await self.agents_client.runs.create_and_process(
                thread_id=thread.id,
                agent_id=self.agent.id
            )
            
            self.logger.log_info(f"Run finished with status: {run.status}")
            
            if run.status == "failed":
                self.logger.log_error(f"Run failed: {run.last_error}")
                return extracted_players
            
            # Get the agent's response
            messages = self.agents_client.messages.list(thread_id=thread.id, order="asc")
            
            last_message = None
            async for msg in messages:
                last_message = msg
            
            if last_message and last_message.text_messages:
                response_content = last_message.text_messages[0].text.value
                self.logger.log_info(f"Agent response received")
                
                # Parse and return validated players
                return self._parse_validated_players(response_content)
            else:
                self.logger.log_warning("No response received from agent")
                return extracted_players
            
        except Exception as e:
            self.logger.log_error(f"Bing search validation failed: {e}")
            # Return original players if validation fails
            return extracted_players
    
    async def validate_individual_player(self, player: Player) -> Player:
        """
        Validate and enhance a single player using Bing search through Azure AI Agents
        
        Args:
            player: Player object to validate
            
        Returns:
            Validated Player object
        """
        try:
            if not self.agents_client or not self.agent:
                self.logger.log_error("Agents client or agent not initialized")
                return player
            
            # Create validation prompt for individual player
            analysis_prompt = f"""
            Please use Bing search to validate and update the following player information:
            
            Player Information:
            - Name: {player.name}
            - Team: {player.team}
            - Position: {player.position}
            - Points: {player.points}
            - Worth: {player.worth}
            - Jersey: {player.jersey}
            
            Search for this player and verify all information. Update any incorrect details based on the search results.
            Return the corrected player information in JSON format with the same structure.
            """
            
            # Create thread for this validation
            thread = await self.agents_client.threads.create()
            self.logger.log_info(f"Individual validation thread created: {thread.id}")
            
            # Create message with the validation request
            message = await self.agents_client.messages.create(
                thread_id=thread.id,
                role="user",
                content=analysis_prompt
            )
            
            # Run the agent to process the validation
            run = await self.agents_client.runs.create_and_process(
                thread_id=thread.id,
                agent_id=self.agent.id
            )
            
            self.logger.log_info(f"Individual validation run finished with status: {run.status}")
            
            if run.status == "failed":
                self.logger.log_error(f"Individual validation run failed: {run.last_error}")
                return player
            
            # Get the agent's response
            messages = self.agents_client.messages.list(thread_id=thread.id, order="asc")
            
            last_message = None
            async for msg in messages:
                last_message = msg
            
            if last_message and last_message.text_messages:
                response_content = last_message.text_messages[0].text.value
                
                try:
                    # Try to parse the JSON response
                    validated_data = json.loads(response_content)
                    
                    # Update player with validated information
                    if isinstance(validated_data, dict):
                        player.name = validated_data.get("name", player.name)
                        player.team = validated_data.get("team", player.team)
                        player.position = validated_data.get("position", player.position)
                        player.points = validated_data.get("points", player.points)
                        player.worth = validated_data.get("worth", player.worth)
                        player.jersey = validated_data.get("jersey", player.jersey)
                        
                        self.logger.log_info(f"Updated player: {player.name}")
                    
                except json.JSONDecodeError:
                    self.logger.log_warning(f"Could not parse validation response for {player.name}")
            
            return player
            
        except Exception as e:
            self.logger.log_error(f"Individual player validation failed for {player.name}: {e}")
            return player
    
    def _players_to_json(self, players: List[Player]) -> str:
        """Convert list of Player objects to JSON string"""
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
    
    def _parse_validated_players(self, result: str) -> List[Player]:
        """Parse validated player result JSON and convert to Player objects"""
        try:
            # Log the raw response for debugging
            self.logger.log_info(f"Raw agent response: {repr(result)}")
            
            # Clean up the response - remove markdown code blocks if present
            cleaned_result = result.strip()
            if cleaned_result.startswith('```json'):
                cleaned_result = cleaned_result[7:]  # Remove ```json
            if cleaned_result.endswith('```'):
                cleaned_result = cleaned_result[:-3]  # Remove trailing ```
            cleaned_result = cleaned_result.strip()
            
            # Try to find JSON content in the response
            if '{' in cleaned_result and '}' in cleaned_result:
                start_idx = cleaned_result.find('{')
                # Find the last closing brace
                end_idx = cleaned_result.rfind('}') + 1
                json_content = cleaned_result[start_idx:end_idx]
                
                self.logger.log_info(f"Extracted JSON content: {json_content}")
                
                parsed_result = json.loads(json_content)
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
            else:
                self.logger.log_error("No JSON content found in agent response")
                return []
            
        except json.JSONDecodeError as e:
            self.logger.log_error(f"Failed to parse validated players JSON: {e}")
            self.logger.log_error(f"Problematic content: {repr(result)}")
            return []
        except Exception as e:
            self.logger.log_error(f"Error parsing validated players: {e}")
            return []
