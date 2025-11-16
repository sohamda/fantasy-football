package com.fantasyfootball.round1selector.model;

import lombok.Data;

import java.util.List;

@Data
public class PositionRecommendations {
    private String position;
    private List<Player> recommendations;
    private String aiAnalysis;
}
