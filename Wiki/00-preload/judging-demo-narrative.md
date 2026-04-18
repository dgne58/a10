# Judging and Demo Narrative

## Core Story
- This project tackles hackathon themes directly: task-aware routing and agentic workflows.
- The differentiator is not just model usage, but choosing the cheapest sufficient **execution path**.
- The local-first wiki is part of the product, not only internal documentation.
- The system is intentionally narrow: branch routing, grounded verification, and visible traces instead of a sprawling "AI platform" story.

## Likely Demo Arc
1. State the problem: most AI demos either overpay for every request or trust cheap models too much.
2. Show the four branches:
   - wiki answer
   - cheap model
   - strong model
   - verification tool
3. Demonstrate one example of each branch.
4. Show the visible trace:
   - selected path
   - rationale
   - latency
   - cost
   - fallback
5. Close with evidence: a small eval table showing lower cost than an `always_strong_model` baseline while staying within an acceptable quality band.

## Proof Points To Gather
- one example of each branch family
- one verification example with a local proof source
- one fallback/cached example
- measurable cost delta versus `always_strong_model`
- one concise explanation of why the product is more than provider switching
- one screenshot of the trace UI or response JSON

## Related
- [[fallback-plans]]
- [[../design-doc|Design Doc]]
- [[../architecture/hackathon-scope|Hackathon Scope]]
- [[../workflows/demo-flow|Demo Flow]]
