# Title

Player Data Processing

## Status

Accepted

## Context

Player details (name, team, position, price) is needed to select a 18 player team. This data will be used later by AI Agents to find the right combination of player within the budget Scorito gives to form a team for each round.

## Decision

1. An AI module to process the screenshots using GPT 4.1 to extract JSON.
2. Then using name, team and jersey description use Bing API to finalize the team. Since Scorito gives 2 team names in the image and AI driven OCR cannot determine the correct team the player belongs to.
3. Validation AI module to verify the extracted name, team and position.
4. Store the info in Cosmos DB.

## Consequences

This is a tabular data, so choosing a Document DB (Cosmos) might not be the right choice. But it is easy to change if required later. 

*#### Template is from [Documenting architecture decisions - Michael Nygard](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions).* 