package com.fantasyfootball.playerextraction.cosmosdb;

import com.fantasyfootball.playerextraction.model.Player;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Service
public class PlayerService {
    
    private static final Logger logger = LoggerFactory.getLogger(PlayerService.class);
    
    private final PlayerRepository playerRepository;
    
    public PlayerService(PlayerRepository playerRepository) {
        this.playerRepository = playerRepository;
    }
    
    /**
     * Save player to Cosmos DB
     */
    public Player savePlayer(Player player) {
        try {
            // Generate ID if not present
            if (player.getId() == null || player.getId().isEmpty()) {
                player.setId(UUID.randomUUID().toString());
            }
            
            Player savedPlayer = playerRepository.save(player);
            logger.info("Successfully saved player: {} with ID: {}", savedPlayer.getName(), savedPlayer.getId());
            
            return savedPlayer;
            
        } catch (Exception e) {
            logger.error("Error saving player: {}", player.getName(), e);
            throw new RuntimeException("Failed to save player to database", e);
        }
    }
    
    /**
     * Find players by name (case-insensitive)
     */
    public List<Player> findPlayersByName(String name) {
        try {
            return playerRepository.findByNameIgnoreCase(name);
        } catch (Exception e) {
            logger.error("Error finding players by name: {}", name, e);
            throw new RuntimeException("Failed to find players by name", e);
        }
    }
}