# Title
Player Data - Scraping

## Status
Accepted

## Context

Scorito requires me to create 18 player team. The selection of player for each position, only available in the mobile app.
The APIs behind it is not open.

## Decision

Take screenshot of the all the available players. So that we have data about their Name, Team, Position, Price.

## Consequences

Any and every update to the player list in Scorito requires a new set of screenshot and post-processing.
Also would be hard to find out what has changed, since I have not found any info page on that in Scorito app.


*#### Template is from [Documenting architecture decisions - Michael Nygard](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions).* 