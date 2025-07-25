from typing import List, Optional, Dict, Any
from azure.cosmos import CosmosClient
from models.player_models import Player
from utils.logging_utils import LogAnalyticsLogger

class CosmosService:
    """Service for Cosmos DB operations"""
    
    def __init__(self, uri: str, key: str, database: str, container: str, logger: LogAnalyticsLogger):
        self.uri = uri
        self.key = key
        self.database_name = database
        self.container_name = container
        self.logger = logger
        self._client = None
        self._database = None
        self._container = None
    
    @property
    def client(self) -> CosmosClient:
        """Lazy-loaded Cosmos client"""
        if self._client is None:
            self._client = CosmosClient(self.uri, credential=self.key)
        return self._client
    
    @property
    def database(self):
        """Lazy-loaded database client"""
        if self._database is None:
            self._database = self.client.get_database_client(self.database_name)
        return self._database
    
    @property
    def container(self):
        """Lazy-loaded container client"""
        if self._container is None:
            self._container = self.database.get_container_client(self.container_name)
        return self._container
    
    def store_player(self, player: Player) -> bool:
        """
        Store a single player in Cosmos DB
        
        Args:
            player: Player object to store
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert player to dictionary
            player_dict = self._player_to_dict(player)
            
            self.container.upsert_item(player_dict)
            self.logger.log_info("Player stored in CosmosDB", player_name=player.name, player_id=player.id)
            return True
            
        except Exception as e:
            self.logger.log_error(f"Failed to store player in CosmosDB: {e}", 
                                player_name=player.name, player_id=player.id)
            return False
    
    def store_players_batch(self, players: List[Player]) -> int:
        """
        Store multiple players in Cosmos DB
        
        Args:
            players: List of Player objects to store
            
        Returns:
            Number of players successfully stored
        """
        stored_count = 0
        
        for player in players:
            if self.store_player(player):
                stored_count += 1
        
        self.logger.log_info(f"Stored {stored_count}/{len(players)} players in CosmosDB")
        return stored_count
    
    def _player_to_dict(self, player: Player) -> Dict[str, Any]:
        """
        Convert Player object to dictionary for Cosmos DB storage
        
        Args:
            player: Player object
            
        Returns:
            Dictionary representation of the player
        """
        return {
            "id": player.id,
            "name": player.name,
            "team": player.team,
            "points": player.points,
            "worth": player.worth,
            "jersey": player.jersey,
            "position": player.position
        }
    
    def _generate_player_id(self, player: Player, index: int) -> str:
        """
        Generate a unique ID for a player
        
        Args:
            player: Player object
            index: Index in the list
            
        Returns:
            Generated player ID
        """
        position = player.position if player.position else 'unknown'
        return f"{position}{index}"
