package com.fantasyfootball.round1selector.controller;

import com.fantasyfootball.round1selector.model.PositionRecommendations;
import com.fantasyfootball.round1selector.service.PlayerRecommendationService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;
import lombok.extern.slf4j.Slf4j;

import java.util.List;

@RestController
@RequestMapping("/api/recommendations")
@CrossOrigin(origins = "*")
@Slf4j
public class RecommendationController {

    private final PlayerRecommendationService playerRecommendationService;

    public RecommendationController(PlayerRecommendationService playerRecommendationService) {
        this.playerRecommendationService = playerRecommendationService;
    }

    @GetMapping("/all-positions")
    public Mono<ResponseEntity<List<PositionRecommendations>>> getAllPositionRecommendations() {
        log.info("Received request for all position recommendations");
        
        return playerRecommendationService.generateAllPositionRecommendations()
                .map(recommendations -> {
                    log.info("Returning recommendations for {} positions", recommendations.size());
                    return ResponseEntity.ok(recommendations);
                })
                .onErrorReturn(ResponseEntity.internalServerError().build());
    }

    @GetMapping("/{position}")
    public Mono<ResponseEntity<PositionRecommendations>> getPositionRecommendations(@PathVariable String position) {
        log.info("Received request for {} position recommendations", position);
        
        return playerRecommendationService.generateRecommendationsForPosition(position)
                .map(recommendations -> {
                    log.info("Returning recommendations for position: {}", position);
                    return ResponseEntity.ok(recommendations);
                })
                .onErrorReturn(ResponseEntity.internalServerError().build());
    }
}
