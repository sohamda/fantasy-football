from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Player:
    """Data model for a player"""
    name: str
    team: str
    points: str
    worth: str
    jersey: str
    position: str
    id: Optional[str] = None

@dataclass
class ValidationResult:
    """Data model for validation results"""
    score: int
    justification: str

@dataclass
class ExtractedPlayers:
    """Container for extracted players"""
    players: List[Player]
    
    def __len__(self):
        return len(self.players)
    
    def __iter__(self):
        return iter(self.players)
    
    def extend(self, other_players: List[Player]):
        self.players.extend(other_players)
    
    def append(self, player: Player):
        self.players.append(player)

@dataclass
class ProcessingResult:
    """Result of processing an image"""
    success: bool
    players: Optional[List[Player]] = None
    error_message: Optional[str] = None
    validation_score: Optional[int] = None
