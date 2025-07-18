# Title

GPT 4.1 for Image processing 

## Status

Accepted

## Context

Screenshots from Scorito app on the player details needs to extracted and stored.

## Decision

Use of GPT4.1 model to extract information(name, team, position, price) from screenshots. Choice made over standard OCR and Azure Content understanding.

## Consequences

Although it made easier to implement, but needed to add an extra step to validate the team name using Bing API.

*#### Template is from [Documenting architecture decisions - Michael Nygard](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions).* 