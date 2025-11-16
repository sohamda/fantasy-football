# Fantasy Football Round 1 Selector - Simplified

A streamlined Spring Boot application that uses Spring AI Agents and parallelization to analyze football players and provide position-based recommendations.

## Core Features

### 🎯 **Simplified Workflow**
1. **Read** player data (name, team, position, value in €) from Cosmos DB
2. **Enrich** each player with external API stats (last 3 months)
3. **Analyze** players per position using AI agents in parallel
4. **Recommend** top 7 players for each position (goalkeeper, midfielder, defender, forward)

### ⚡ **Parallelization Pattern**
- **4 positions processed in parallel** (goalkeeper, midfielder, defender, forward)
- **Up to 10 concurrent API calls** per position for stats enrichment
- **Async AI analysis** for each position using Spring AI agents

### 📊 **Player Data & Stats**
**From Cosmos DB:**
- Name, Team, Position, Value in Euro

**From External API (last 3 months):**
- Number of appearances
- Minutes played per match
- Goals & Assists
- Red & Yellow cards
- Current injury status

## Project Structure

```
src/main/java/com/fantasyfootball/round1selector/
├── Round1SelectorApplication.java           # Main application
├── model/
│   ├── Player.java                         # Player entity with stats
│   └── PositionRecommendations.java        # Position analysis results
├── service/
│   ├── CosmosDbService.java               # Cosmos DB integration
│   ├── ExternalStatsApiService.java       # External API for player stats
│   └── PlayerRecommendationService.java   # Main orchestration service
├── agent/
│   └── PositionAnalysisAgent.java         # Spring AI agent for position analysis
├── controller/
│   └── RecommendationController.java      # REST API endpoints
└── config/
    └── ApplicationConfig.java             # Configuration (AI, Cosmos, WebClient)
```

## API Endpoints

### Get All Position Recommendations (Parallel Processing)
```
GET /api/recommendations/all-positions
```
Returns recommendations for all 4 positions processed in parallel.

### Get Specific Position Recommendations
```
GET /api/recommendations/{position}
```
Where position is: `goalkeeper`, `midfielder`, `defender`, or `forward`

## Configuration

### Required Environment Variables
```bash
# OpenAI
OPENAI_API_KEY=your-openai-api-key

# Cosmos DB
COSMOS_DB_URI=https://your-account.documents.azure.com:443/
COSMOS_DB_KEY=your-cosmos-db-key
COSMOS_DB_DATABASE=fantasy-football
COSMOS_DB_CONTAINER=players

# External Stats API
EXTERNAL_API_URL=https://api.football-stats.com
EXTERNAL_API_KEY=your-external-api-key
```

## Sample Response

```json
[
  {
    "position": "forward",
    "recommendations": [
      {
        "name": "Kylian Mbappé",
        "team": "PSG",
        "position": "forward",
        "valueInEuro": 180000000,
        "stats": {
          "appearances": 12,
          "goals": 15,
          "assists": 8,
          "minutesPlayed": 1080,
          "averageMinutesPerMatch": 90.0,
          "redCards": 0,
          "yellowCards": 2,
          "injuryStatus": "Fit"
        }
      }
    ],
    "aiAnalysis": "Top 7 Forward Recommendations:\n1. Kylian Mbappé - Exceptional goal scoring rate..."
  }
]
```

## How It Works

1. **Data Collection**: Fetches all players from Cosmos DB grouped by position
2. **Stats Enrichment**: Parallel API calls to enrich each player with recent stats
3. **AI Analysis**: Each position is analyzed by Spring AI agent in parallel
4. **Recommendation**: Returns top 7 players per position with AI reasoning

## Run the Application

```bash
mvn spring-boot:run
```

Access the API at: `http://localhost:8080`
