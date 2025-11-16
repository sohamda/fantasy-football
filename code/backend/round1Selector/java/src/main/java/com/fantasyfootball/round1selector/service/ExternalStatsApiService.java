package com.fantasyfootball.round1selector.service;

import com.fantasyfootball.round1selector.model.Player;
import com.fantasyfootball.round1selector.model.PlayerStats;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;
import lombok.extern.slf4j.Slf4j;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@Service
@Slf4j
public class ExternalStatsApiService {

    private final WebClient webClient;
    private final String apiKey;
    private final String baseUrl;

    public ExternalStatsApiService(WebClient.Builder webClientBuilder,
                                  @Value("${external.stats.api.key}") String apiKey,
                                  @Value("${external.stats.api.url}") String baseUrl) {
        this.webClient = webClientBuilder.baseUrl(baseUrl).build();
        this.apiKey = apiKey;
        this.baseUrl = baseUrl;
    }

    public Mono<PlayerStats> getPlayerStats(String playerName, String team) {
        // Calculate date 3 months ago
        LocalDateTime threeMonthsAgo = LocalDateTime.now().minusMonths(3);
        String fromDate = threeMonthsAgo.format(DateTimeFormatter.ofPattern("yyyy-MM-dd"));
        String toDate = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd"));

        return webClient.get()
                .uri(uriBuilder -> uriBuilder
                        .path("/players/stats")
                        .queryParam("name", playerName)
                        .queryParam("team", team)
                        .queryParam("from", fromDate)
                        .queryParam("to", toDate)
                        .queryParam("apikey", apiKey)
                        .build())
                .retrieve()
                .bodyToMono(ExternalPlayerStatsResponse.class)
                .map(this::mapToPlayerStats)
                .doOnSuccess(stats -> log.debug("Retrieved stats for player: {}", playerName))
                .doOnError(error -> log.error("Failed to retrieve stats for player: {}", playerName, error))
                .onErrorReturn(createDefaultStats()); // Return default stats on error
    }

    private PlayerStats mapToPlayerStats(ExternalPlayerStatsResponse response) {
        PlayerStats stats = new PlayerStats();
        stats.setAppearances(response.getAppearances());
        stats.setMinutesPlayed(response.getMinutesPlayed());
        stats.setGoals(response.getGoals());
        stats.setAssists(response.getAssists());
        stats.setRedCards(response.getRedCards());
        stats.setYellowCards(response.getYellowCards());
        stats.setInjuryStatus(response.getInjuryStatus());
        
        // Calculate average minutes per match
        if (response.getAppearances() > 0) {
            stats.setAverageMinutesPerMatch((double) response.getMinutesPlayed() / response.getAppearances());
        }
        
        return stats;
    }

    private PlayerStats createDefaultStats() {
        PlayerStats defaultStats = new PlayerStats();
        defaultStats.setAppearances(0);
        defaultStats.setMinutesPlayed(0);
        defaultStats.setGoals(0);
        defaultStats.setAssists(0);
        defaultStats.setRedCards(0);
        defaultStats.setYellowCards(0);
        defaultStats.setInjuryStatus("Unknown");
        defaultStats.setAverageMinutesPerMatch(0.0);
        return defaultStats;
    }

    // Response DTO for external API
    public static class ExternalPlayerStatsResponse {
        private int appearances;
        private int minutesPlayed;
        private int goals;
        private int assists;
        private int redCards;
        private int yellowCards;
        private String injuryStatus;

        // Getters and Setters
        public int getAppearances() { return appearances; }
        public void setAppearances(int appearances) { this.appearances = appearances; }
        public int getMinutesPlayed() { return minutesPlayed; }
        public void setMinutesPlayed(int minutesPlayed) { this.minutesPlayed = minutesPlayed; }
        public int getGoals() { return goals; }
        public void setGoals(int goals) { this.goals = goals; }
        public int getAssists() { return assists; }
        public void setAssists(int assists) { this.assists = assists; }
        public int getRedCards() { return redCards; }
        public void setRedCards(int redCards) { this.redCards = redCards; }
        public int getYellowCards() { return yellowCards; }
        public void setYellowCards(int yellowCards) { this.yellowCards = yellowCards; }
        public String getInjuryStatus() { return injuryStatus; }
        public void setInjuryStatus(String injuryStatus) { this.injuryStatus = injuryStatus; }
    }
}
