#!/usr/bin/env python3
"""
Test script for BingService with Azure AI Agents integration
"""

import asyncio
import sys
from pathlib import Path

# Add the parent directory to the path so we can import modules
sys.path.append(str(Path(__file__).parent))

from config import settings
from utils import LogAnalyticsLogger
from services import BingService
from models import Player

async def test_bing_service():
    """Test the new BingService with Azure AI Agents"""
    
    # Initialize logger
    logger = LogAnalyticsLogger(
        workspace_id=settings.log_analytics_workspace_id,
        shared_key=settings.log_analytics_shared_key,
        log_type=settings.log_analytics_log_type
    )
    
    print("Testing BingService with Azure AI Agents...")
    
    # Test with mock player data
    mock_players = [
        Player(
            name="Lionel Messi",
            team="Unknown Team",
            points="100",
            worth="15.0",
            jersey="10",
            position="F"
        ),
        Player(
            name="Cristiano Ronaldo",
            team="Unknown Team",
            points="95",
            worth="14.5",
            jersey="7",
            position="F"
        )
    ]
    
    try:
        # Initialize BingService with async context manager
        async with BingService(
            foundry_agent_endpoint=settings.foundry_agent_endpoint,
            bing_connection_id=settings.bing_connection_id,
            logger=logger,
            openai_deployment=settings.openai_deployment
        ) as bing_service:
            
            print(f"✅ BingService initialized successfully")
            print(f"🤖 Agent ID: {bing_service.agent.id if bing_service.agent else 'None'}")
            
            # Test batch validation
            print("\n📋 Testing batch validation...")
            validated_players = await bing_service.finalize_extraction_with_bing(mock_players)
            
            print(f"✅ Batch validation completed")
            print(f"📊 Validated {len(validated_players)} players:")
            
            for i, player in enumerate(validated_players, 1):
                print(f"   {i}. {player.name} - Team: {player.team} - Position: {player.position}")
            
            # Test individual validation
            print("\n👤 Testing individual validation...")
            test_player = Player(
                name="Kylian Mbappé",
                team="Unknown Team",
                points="90",
                worth="13.5",
                jersey="9",
                position="F"
            )
            
            validated_player = await bing_service.validate_individual_player(test_player)
            print(f"✅ Individual validation completed")
            print(f"👤 {validated_player.name} - Team: {validated_player.team} - Position: {validated_player.position}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n🎉 All tests completed successfully!")
    return True

if __name__ == "__main__":
    success = asyncio.run(test_bing_service())
    if success:
        print("✅ BingService with Azure AI Agents is working correctly!")
    else:
        print("❌ BingService test failed!")
        sys.exit(1)
