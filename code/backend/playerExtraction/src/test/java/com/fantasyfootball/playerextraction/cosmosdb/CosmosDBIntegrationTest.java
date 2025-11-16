package com.fantasyfootball.playerextraction.cosmosdb;

import java.util.List;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import com.fantasyfootball.playerextraction.model.Player;


@SpringBootTest
public class CosmosDBIntegrationTest {

    private static final Logger logger = LoggerFactory.getLogger(CosmosDBIntegrationTest.class);

    @Autowired
    private PlayerService playerService;

    @Autowired
    private PlayerRepository playerRepository;

    @Test
    void saveFindDeletePlayer() {
        //Save new Player
        Player savedPlayer = playerService.savePlayer(new Player(null, "Feyenoord", "Abra Ca Dabra", "Goalkeeper", "0", "5M", "1"));
        Assertions.assertNotNull(savedPlayer.getId());
        logger.info("Saved player ID: {}", savedPlayer.getId());

        //Find Player by name
        List<Player> players = playerService.findPlayersByName("Abra Ca Dabra");
        Assertions.assertTrue(players.size() == 1, "Should find one player named 'Abra Ca Dabra'");
        for (Player player : players) {
            logger.info("Found player: {} with ID: {}", player.getName(), player.getId());
        }

        //Clean up - Delete Player
        playerRepository.deleteByName(players.get(0).getName());
        Assertions.assertTrue(playerService.findPlayersByName("Abra Ca Dabra").size() == 0, "Player 'Abra Ca Dabra' should be deleted");
    }
}
