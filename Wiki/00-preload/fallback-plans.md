# Fallback Plans

## Demo Fallback Strategy
- If live model calls fail, return cached responses for the canned demo prompts and mark them as cached.
- If the mixed eval cannot be completed in time, present a smaller precomputed eval set and state its scope clearly.
- If the verification path is unstable, restrict the demo to one or two known-good local source files.
- If the UI breaks, show the route response JSON directly in curl/Postman and narrate the branch choice.
- If the cheap model underperforms badly, tighten the router and send more cases to the strong path rather than pretending otherwise.
- If the broader architecture story becomes confusing, compress the explanation to the four branches only.

## What To Prepare Before The Event
- One canned example for each branch:
  - `wiki_answer`
  - `cheap_model`
  - `strong_model`
  - `verification_tool`
- One offline/local-only demo mode.
- One screenshot/video fallback.
- One small evaluation table comparing router vs `always_strong_model`.
- One 15-second explanation of why the system is more than a model wrapper.

## What To Document Later
- toggle/env flag for fallback mode
- mock data location
- reduced-scope demo commands
- which features are safe to disable under pressure

## Related
- [[judging-demo-narrative]]
- [[known-bugs-and-assumptions]]
- [[../design-doc|Design Doc]]
- [[../workflows/demo-flow|Demo Flow]]
