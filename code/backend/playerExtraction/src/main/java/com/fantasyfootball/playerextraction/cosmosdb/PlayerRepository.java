package com.fantasyfootball.playerextraction.cosmosdb;

import com.azure.spring.data.cosmos.repository.CosmosRepository;
import com.fantasyfootball.playerextraction.model.Player;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface PlayerRepository extends CosmosRepository<Player, String> {
    
    /**
     * Find players by name (case-insensitive)
     */
    List<Player> findByNameIgnoreCase(String name);

    void deleteByName(String name);
    
}