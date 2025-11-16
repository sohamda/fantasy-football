package com.fantasyfootball.round1selector.service;

import com.fantasyfootball.round1selector.model.Player;
import com.azure.cosmos.CosmosClient;
import com.azure.cosmos.CosmosContainer;
import com.azure.cosmos.CosmosDatabase;
import com.azure.cosmos.models.CosmosQueryRequestOptions;
import com.azure.cosmos.util.CosmosPagedIterable;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import lombok.extern.slf4j.Slf4j;

import java.util.List;
import java.util.ArrayList;

@Service
@Slf4j
public class CosmosDbService {

    private final CosmosClient cosmosClient;
    private final String databaseName;
    private final String containerName;

    public CosmosDbService(CosmosClient cosmosClient,
                          @Value("${azure.cosmos.database}") String databaseName,
                          @Value("${azure.cosmos.container}") String containerName) {
        this.cosmosClient = cosmosClient;
        this.databaseName = databaseName;
        this.containerName = containerName;
    }

    public List<Player> getAllPlayers() {
        try {
            CosmosDatabase database = cosmosClient.getDatabase(databaseName);
            CosmosContainer container = database.getContainer(containerName);
            
            String query = "SELECT * FROM c WHERE c.name IS NOT NULL AND c.team IS NOT NULL AND c.position IS NOT NULL AND c.valueInEuro IS NOT NULL";
            
            CosmosPagedIterable<Player> items = container.queryItems(
                query, 
                new CosmosQueryRequestOptions(), 
                Player.class
            );
            
            List<Player> players = new ArrayList<>();
            items.forEach(players::add);
            
            log.info("Retrieved {} players from Cosmos DB", players.size());
            return players;
            
        } catch (Exception e) {
            log.error("Error retrieving players from Cosmos DB", e);
            throw new RuntimeException("Failed to retrieve players from Cosmos DB", e);
        }
    }

    public List<Player> getPlayersByPosition(String position) {
        try {
            CosmosDatabase database = cosmosClient.getDatabase(databaseName);
            CosmosContainer container = database.getContainer(containerName);
            
            String query = String.format("SELECT * FROM c WHERE c.position = '%s'", position);
            
            CosmosPagedIterable<Player> items = container.queryItems(
                query, 
                new CosmosQueryRequestOptions(), 
                Player.class
            );
            
            List<Player> players = new ArrayList<>();
            items.forEach(players::add);
            
            log.info("Retrieved {} players for position {} from Cosmos DB", players.size(), position);
            return players;
            
        } catch (Exception e) {
            log.error("Error retrieving players by position from Cosmos DB", e);
            throw new RuntimeException("Failed to retrieve players by position from Cosmos DB", e);
        }
    }
}
