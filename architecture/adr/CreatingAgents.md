# Title

Creating Agents in Azure AI Foundry

## Status

Proposed

## Context

There will be several agents (at this point the number is unknown) created and managed in this application. I need a easier way to create them.

## Decision

Using Azure AI Agent SDK the agents will be created **centrally**. This script will be run via Github workflow as a part of IaC scripts. 

## Consequences

Agents must be created first separately by modifying the central script and then run the pipeline to make it available before it can be used in the application code.

*#### Template is from [Documenting architecture decisions - Michael Nygard](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions).* 