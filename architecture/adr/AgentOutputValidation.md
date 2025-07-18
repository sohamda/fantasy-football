# Title

Instead of tests, add a validation step for each agentic operation.

## Status

Proposed

## Context

The Agent output needs to be validated. Ideally we can write tests for each agent and steps within the agent.

## Decision

Adding a validation step after each agent completes its task. So another agent or ai-module takes the original input and output of the preceding agent as input and validates if the agent did its task properly. Generate a % as output and pass it through if above 80%.

## Consequences

Added complexity in Agent implementation. Most of them have to follow ChatModel pattern with actual agent and validator agent as components within.

*#### Template is from [Documenting architecture decisions - Michael Nygard](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions).* 