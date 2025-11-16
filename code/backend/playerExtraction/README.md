# Player Extraction Service

A Spring Boot application that uses Spring AI to extract player information from images and stores the data in Azure Cosmos DB.

## Features

- **Image Processing**: Extract player information from football/soccer player images using Spring AI with OpenAI's GPT-4 Vision
- **Data Storage**: Store extracted player data in Azure Cosmos DB
- **REST API**: Full CRUD operations for player data
- **Validation**: Input validation and error handling
- **Testing**: Comprehensive test coverage

## Tech Stack

- **Spring Boot 3.2.1**: Main framework
- **Spring AI**: AI integration for image processing
- **Azure Cosmos DB**: NoSQL database for data storage
- **OpenAI GPT-4 Vision**: AI model for image analysis
- **Maven**: Dependency management
- **Java 17**: Programming language

## Prerequisites

- Java 17 or higher
- Maven 3.6+
- Azure Cosmos DB account
- OpenAI API key

## Configuration

### Environment Variables

Create a `.env` file or set the following environment variables:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key

# Azure Cosmos DB Configuration
COSMOS_DB_URI=https://your-cosmos-account.documents.azure.com:443/
COSMOS_DB_KEY=your-cosmos-db-primary-key
COSMOS_DB_DATABASE=fantasy-football
```

### Application Properties

The application uses the following configuration properties:

```properties
# Spring AI Configuration
spring.ai.openai.api-key=${OPENAI_API_KEY}
spring.ai.openai.chat.options.model=gpt-4-vision-preview
spring.ai.openai.chat.options.temperature=0.1

# Azure Cosmos DB Configuration
azure.cosmos.uri=${COSMOS_DB_URI}
azure.cosmos.key=${COSMOS_DB_KEY}
azure.cosmos.database=${COSMOS_DB_DATABASE:fantasy-football}

# Application Configuration
spring.application.name=player-extraction
server.port=8081
```

## Installation & Running

1. **Clone and navigate to the project directory**:
   ```bash
   cd code/backend/playerExtraction
   ```

2. **Set environment variables**:
   ```bash
   # Windows (PowerShell)
   $env:OPENAI_API_KEY="your-openai-api-key"
   $env:COSMOS_DB_URI="https://your-cosmos-account.documents.azure.com:443/"
   $env:COSMOS_DB_KEY="your-cosmos-db-primary-key"
   $env:COSMOS_DB_DATABASE="fantasy-football"

   # Linux/Mac
   export OPENAI_API_KEY="your-openai-api-key"
   export COSMOS_DB_URI="https://your-cosmos-account.documents.azure.com:443/"
   export COSMOS_DB_KEY="your-cosmos-db-primary-key"
   export COSMOS_DB_DATABASE="fantasy-football"
   ```

3. **Build and run the application**:
   ```bash
   mvn clean install
   mvn spring-boot:run
   ```

The application will start on `http://localhost:8081`

## API Endpoints

### Player Extraction
- `POST /api/players/extract` - Extract player info from uploaded image
- `POST /api/players/dummy` - Create a dummy player for testing

### Player Management
- `GET /api/players` - Get all players
- `GET /api/players/{id}` - Get player by ID
- `GET /api/players/team/{team}` - Get players by team
- `GET /api/players/position/{position}` - Get players by position
- `GET /api/players/search/{name}` - Search players by name
- `PUT /api/players/{id}` - Update player information
- `DELETE /api/players/{id}` - Delete player by ID
- `GET /api/players/stats` - Get player statistics

### Example Usage

#### Extract Player from Image
```bash
curl -X POST -F "image=@player-image.jpg" http://localhost:8081/api/players/extract
```

#### Create Dummy Player
```bash
curl -X POST http://localhost:8081/api/players/dummy
```

#### Get All Players
```bash
curl http://localhost:8081/api/players
```

## Data Model

The Player entity includes the following fields:

```json
{
  "id": "uuid",
  "name": "Player Name",
  "team": "Team Name",
  "position": "Position",
  "age": 25,
  "nationality": "Country",
  "jerseyNumber": 10,
  "marketValue": "€50.00M",
  "contractUntil": "2025-12-31",
  "preferredFoot": "Right",
  "height": "180 cm",
  "skills": ["Dribbling", "Finishing"],
  "imageUrl": "image-url",
  "extractedAt": "2024-01-01T10:00:00",
  "confidence": 0.95
}
```

## Testing

Run tests with:
```bash
mvn test
```

## Docker Support

To run with Docker:

```dockerfile
FROM openjdk:17-jdk-slim
COPY target/player-extraction-0.0.1-SNAPSHOT.jar app.jar
EXPOSE 8081
ENTRYPOINT ["java", "-jar", "/app.jar"]
```

## Troubleshooting

1. **OpenAI API Issues**: Ensure your API key is valid and has sufficient credits
2. **Cosmos DB Connection**: Verify URI and key are correct and network access is allowed
3. **Image Upload**: Check file size limits (max 10MB)
4. **Memory Issues**: Increase JVM heap size if processing large images

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.