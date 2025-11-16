package com.fantasyfootball.round1selector.service;

import com.fantasyfootball.round1selector.agent.PositionAnalysisAgent;
import com.fantasyfootball.round1selector.model.Player;
import com.fantasyfootball.round1selector.model.PositionRecommendations;
import org.springframework.stereotype.Service;
import lombok.extern.slf4j.Slf4j;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

import java.util.Arrays;
import java.util.List;
import java.util.concurrent.CompletableFuture;

@Service
@Slf4j
public class PlayerRecommendationService {

    private final CosmosDbService cosmosDbService;
    private final ExternalStatsApiService externalStatsApiService;
    private final PositionAnalysisAgent positionAnalysisAgent;

    private final List<String> POSITIONS = Arrays.asList("goalkeeper", "defender", "midfielder", "forward");

    public PlayerRecommendationService(CosmosDbService cosmosDbService,
                                     ExternalStatsApiService externalStatsApiService,
                                     PositionAnalysisAgent positionAnalysisAgent) {
        this.cosmosDbService = cosmosDbService;
        this.externalStatsApiService = externalStatsApiService;
        this.positionAnalysisAgent = positionAnalysisAgent;
    }

    public Mono<List<PositionRecommendations>> generateAllPositionRecommendations() {
        log.info("Starting parallel analysis for all positions");

        return Flux.fromIterable(POSITIONS)
                .parallel(4) // Process 4 positions in parallel
                .runOn(Schedulers.boundedElastic())
                .flatMap(this::processPosition)
                .sequential()
                .collectList()
                .doOnSuccess(results -> log.info("Completed analysis for all positions"))
                .doOnError(error -> log.error("Error in parallel processing", error));
    }

    private Mono<PositionRecommendations> processPosition(String position) {
        log.info("Processing position: {}", position);

        return Mono.fromCallable(() -> cosmosDbService.getPlayersByPosition(position))
                .subscribeOn(Schedulers.boundedElastic())
                .flatMap(players -> enrichPlayersWithStats(players))
                .flatMap(playersWithStats -> analyzePositionWithAI(position, playersWithStats))
                .doOnSuccess(result -> log.info("Completed processing for position: {}", position))
                .doOnError(error -> log.error("Error processing position: {}", position, error));
    }

    private Mono<List<Player>> enrichPlayersWithStats(List<Player> players) {
        log.info("Enriching {} players with external stats", players.size());

        return Flux.fromIterable(players)
                .parallel(10) // Process up to 10 players concurrently for stats retrieval
                .runOn(Schedulers.boundedElastic())
                .flatMap(player -> 
                    externalStatsApiService.getPlayerStats(player.getName(), player.getTeam())
                        .map(stats -> {
                            player.setStats(stats);
                            return player;
                        })
                        .onErrorReturn(player) // Return player without stats if API fails
                )
                .sequential()
                .collectList();
    }

    private Mono<PositionRecommendations> analyzePositionWithAI(String position, List<Player> playersWithStats) {
        log.info("Starting AI analysis for position: {} with {} players", position, playersWithStats.size());

        return Mono.fromFuture(() -> positionAnalysisAgent.analyzePosition(position, playersWithStats))
                .map(analysis -> {
                    PositionRecommendations recommendations = new PositionRecommendations();
                    recommendations.setPosition(position);
                    recommendations.setRecommendations(extractTop7Players(playersWithStats, analysis));
                    recommendations.setAiAnalysis(analysis);
                    return recommendations;
                })
                .subscribeOn(Schedulers.boundedElastic());
    }

    private List<Player> extractTop7Players(List<Player> players, String analysis) {
        // Simple implementation - in production, this would parse the AI response
        // to extract the actual recommended players
        return players.stream()
                .sorted((p1, p2) -> {
                    // Sort by value for money and performance metrics
                    double score1 = calculatePlayerScore(p1);
                    double score2 = calculatePlayerScore(p2);
                    return Double.compare(score2, score1);
                })
                .limit(7)
                .toList();
    }

    private double calculatePlayerScore(Player player) {
        if (player.getStats() == null) {
            return 0.0;
        }

        double appearanceScore = player.getStats().getAppearances() * 2.0;
        double goalScore = player.getStats().getGoals() * 5.0;
        double assistScore = player.getStats().getAssists() * 3.0;
        double disciplinaryPenalty = (player.getStats().getRedCards() * -10.0) + (player.getStats().getYellowCards() * -2.0);
        double valueScore = player.getValueInEuro() > 0 ? (appearanceScore + goalScore + assistScore) / (player.getValueInEuro() / 1000000) : 0;

        return appearanceScore + goalScore + assistScore + disciplinaryPenalty + valueScore;
    }

    public Mono<PositionRecommendations> generateRecommendationsForPosition(String position) {
        log.info("Generating recommendations for specific position: {}", position);
        return processPosition(position);
    }
}
