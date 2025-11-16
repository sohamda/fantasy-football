# Player Extraction Spring Boot Application

## Project Overview
This is a comprehensive Spring Boot application that provides AI-powered image processing for football player data extraction and storage in Azure Cosmos DB.

## Features
- **Spring AI Integration**: Uses Spring AI framework for image processing (placeholder implementation due to API instability)
- **Azure Cosmos DB**: NoSQL database integration with Spring Data Cosmos
- **REST API**: Complete CRUD operations for player management
- **Docker Support**: Containerized deployment with docker-compose
- **Comprehensive Testing**: Unit tests for controller layer

## Architecture
```
├── src/main/java/com/fantasyfootball/playerextraction/
│   ├── PlayerExtractionApplication.java     # Main application class
│   ├── config/
│   │   ├── CosmosDbConfiguration.java       # Cosmos DB configuration
│   │   └── SpringAiConfig.java              # Spring AI configuration
│   ├── controller/
│   │   └── PlayerController.java            # REST API endpoints
│   ├── model/
│   │   └── Player.java                      # Player entity model
│   ├── repository/
│   │   └── PlayerRepository.java            # Cosmos DB repository
│   └── service/
│       ├── ImageExtractionService.java      # AI image processing service
│       └── PlayerService.java               # Business logic service
```

## API Endpoints

### Player Management
- `GET /api/players` - Get all players
- `GET /api/players/{id}` - Get player by ID
- `GET /api/players/team/{team}` - Get players by team
- `POST /api/players` - Create new player
- `PUT /api/players/{id}` - Update player
- `DELETE /api/players/{id}` - Delete player
- `GET /api/players/stats` - Get player statistics

### AI Integration
- `POST /api/players/dummy` - Create dummy player (demonstrates AI integration)
- `POST /api/players/extract` - Extract player from image (placeholder implementation)

## Configuration

### Environment Variables
```bash
# Cosmos DB Configuration
COSMOS_DB_URI=your-cosmos-db-uri
COSMOS_DB_KEY=your-cosmos-db-key
COSMOS_DB_DATABASE_NAME=your-database-name

# Spring AI Configuration (when available)
SPRING_AI_OPENAI_API_KEY=your-openai-api-key
```

### Application Properties
- `application.properties` - Main configuration
- `application-test.properties` - Test configuration with dummy values

## Dependencies
- **Spring Boot 3.2.1** - Main framework
- **Spring AI 1.0.0-M4** - AI integration framework
- **Azure Spring Data Cosmos 5.8.0** - Cosmos DB integration
- **Jackson** - JSON processing
- **Docker** - Containerization support

## Testing
- **Unit Tests**: `PlayerControllerUnitTest` - Tests controller logic without Spring context
- **Integration Tests**: Available but require Cosmos DB configuration

### Running Tests
```bash
# Run unit tests only
mvn test -Dtest=PlayerControllerUnitTest

# Compile without tests
mvn compile -DskipTests
```

## Docker Deployment
```bash
# Build and run with docker-compose
docker-compose up --build

# The application will be available at http://localhost:8080
```

## Build and Run

### Prerequisites
- Java 17+
- Maven 3.6+
- Docker (optional)

### Local Development
```bash
# Compile the application
mvn compile

# Run with profile (requires environment variables)
mvn spring-boot:run -Dspring-boot.run.profiles=dev

# Build JAR
mvn package -DskipTests
```

## Data Model

### Player Entity
```java
{
  "id": "string",
  "name": "string",
  "team": "string", 
  "position": "string",
  "age": 0,
  "nationality": "string",
  "marketValue": 0.0,
  "confidence": 0.0,
  "extractedAt": "timestamp",
  "imageUrl": "string"
}
```

## Future Enhancements
1. **Spring AI Vision Integration**: Complete implementation when API stabilizes
2. **Enhanced Testing**: Integration tests with test containers
3. **Authentication**: Add security layer
4. **Caching**: Implement Redis caching for better performance
5. **Monitoring**: Add application metrics and health checks

## Status
✅ **Complete**: Project structure, main application code, unit tests, Docker configuration
⚠️ **Placeholder**: Spring AI vision integration (API instability)
⚠️ **Pending**: Integration tests (Cosmos DB configuration challenges)

## Notes
- The application compiles successfully and passes unit tests
- Cosmos DB integration is fully configured but requires actual Azure resources for testing
- Spring AI integration uses placeholder implementation due to API changes in milestone versions
- Docker setup is complete and ready for deployment