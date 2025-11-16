package com.fantasyfootball.round1selector.agent;

import com.fantasyfootball.round1selector.model.Player;
import org.springframework.ai.chat.ChatClient;
import org.springframework.ai.chat.ChatResponse;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.ai.chat.prompt.PromptTemplate;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;
import lombok.extern.slf4j.Slf4j;

import java.util.List;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.stream.Collectors;

@Component
@Slf4j
public class PositionAnalysisAgent {

    private final ChatClient chatClient;

    private static final String POSITION_ANALYSIS_TEMPLATE = """
        Analyze the following {position} players for fantasy football selection.
        
        Players data:
        {playersData}
        
        Based on the last 3 months performance, consider:
        1. Appearances and minutes played (consistency)
        2. Goals and assists (productivity)
        3. Disciplinary record (red/yellow cards)
        4. Current injury status
        5. Value in Euro (value for money)
        
        Please select the TOP 7 {position}s and provide:
        1. Ranked list of 7 recommended players with brief reasoning
        2. Key factors that influenced your selection
        3. Any players to avoid and why
        
        Position-specific criteria:
        - Goalkeeper: Clean sheets potential, save consistency, injury status
        - Defender: Defensive stability, attacking contribution, disciplinary record
        - Midfielder: Creativity, goal/assist contribution, work rate
        - Forward: Goal scoring record, consistency, injury concerns
        """;

    public PositionAnalysisAgent(ChatClient chatClient) {
        this.chatClient = chatClient;
    }

    @Async
    public CompletableFuture<String> analyzePosition(String position, List<Player> players) {
        log.info("Starting analysis for position: {} with {} players", position, players.size());
        
        try {
            PromptTemplate promptTemplate = new PromptTemplate(POSITION_ANALYSIS_TEMPLATE);
            
            String playersData = formatPlayersData(players);
            
            Map<String, Object> promptParameters = Map.of(
                "position", position,
                "playersData", playersData
            );
            
            Prompt prompt = promptTemplate.create(promptParameters);
            ChatResponse response = chatClient.call(prompt);
            
            String analysis = response.getResult().getOutput().getContent();
            log.info("Completed analysis for position: {}", position);
            
            return CompletableFuture.completedFuture(analysis);
            
        } catch (Exception e) {
            log.error("Error analyzing position: {}", position, e);
            return CompletableFuture.completedFuture("Error analyzing " + position + " players: " + e.getMessage());
        }
    }

    private String formatPlayersData(List<Player> players) {
        return players.stream()
            .map(this::formatPlayerData)
            .collect(Collectors.joining("\n\n"));
    }

    private String formatPlayerData(Player player) {
        return String.format(
            "Name: %s\n" +
            "Team: %s\n" +
            "Value: €%.2f\n" +
            "Appearances: %d\n" +
            "Minutes Played: %d\n" +
            "Average Minutes/Match: %.1f\n" +
            "Goals: %d\n" +
            "Assists: %d\n" +
            "Yellow Cards: %d\n" +
            "Red Cards: %d\n" +
            "Injury Status: %s",
            player.getName(),
            player.getTeam(),
            player.getValueInEuro(),
            player.getStats() != null ? player.getStats().getAppearances() : 0,
            player.getStats() != null ? player.getStats().getMinutesPlayed() : 0,
            player.getStats() != null ? player.getStats().getAverageMinutesPerMatch() : 0.0,
            player.getStats() != null ? player.getStats().getGoals() : 0,
            player.getStats() != null ? player.getStats().getAssists() : 0,
            player.getStats() != null ? player.getStats().getYellowCards() : 0,
            player.getStats() != null ? player.getStats().getRedCards() : 0,
            player.getStats() != null ? player.getStats().getInjuryStatus() : "Unknown"
        );
    }
}
