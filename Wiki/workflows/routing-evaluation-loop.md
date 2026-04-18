# Routing Evaluation Loop

## Overview
- Routing quality is not self-evident.
- This page captures how to evaluate whether a router is actually improving cost, latency, or reliability.

## Why This Page Exists
- Evaluation is mentioned across routing, demo, and judging pages.
- The concept deserves its own hub because it ties together:
  - routing policy
  - evaluation records
  - demo evidence
  - future tuning

## Evaluation Inputs
- [[../data-models/routed-request|Routed Request]]
- router trace
- outcome quality signal
- latency
- estimated cost
- fallback behavior

## Basic Loop

```text
define scenario set
  -> run baseline path
  -> run routed path
  -> compare quality, cost, latency, and failure behavior
  -> write records
  -> refine router policy or thresholds
```

## Scenario Types
- wiki-answerable query
- simple narrow-domain query
- tool-required query
- risky or approval-requiring query
- hard reasoning or synthesis query

## Baselines
- always use strongest model
- always use cheaper model
- wiki-first plus rules-based router

The most practical hackathon comparison is often:
- naive strongest-model baseline
- transparent routed policy

## What To Measure

| Metric | Why it matters |
| --- | --- |
| quality score | proves the routed path is still acceptable |
| latency | shows user-facing performance impact |
| estimated cost | makes the routing story concrete |
| failure mode | shows whether the system degrades gracefully |
| trace quality | shows whether judges can understand why a route happened |

## Quality Signals
- exact-match or rubric for narrow tasks
- human judgment for demo scenarios
- "task completed or not" for tool paths
- partial credit for graceful fallback

## Data Model Tie-In
- Each run should be stored as an [[../data-models/evaluation-record|Evaluation Record]].
- Consistency is more important than scientific perfection in a hackathon setting.

## Design Guidance
- keep the scenario set small and stable
- compare against at least one baseline
- measure the same fields every time
- preserve enough notes that tomorrow's tuning still makes sense

## Related Topics
- [[../components/router|Router]]
- [[../workflows/demo-flow|Demo Flow]]
- [[../00-preload/judging-demo-narrative|Judging and Demo Narrative]]
- [[../data-models/evaluation-record|Evaluation Record]]
