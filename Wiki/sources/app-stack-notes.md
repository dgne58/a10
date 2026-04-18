---
tags: [flask, api, rest, workflow-automation, app-stack, edge, serverless, faas]
sources: [Best Practices for Flask API Development, Flask-RESTful docs, n8n docs, Cloudflare edge/serverless docs]
last_updated: 2026-04-15
---

# App Stack Notes

## Provenance
- Theme: `app-stack-and-delivery`
- Registry: [[clipping-registry]]
- Inventory: [[clipping-inventory]]
- Raw-source verification: [[../workflows/raw-source-verification|Raw Source Verification]]

## Why This Theme Matters

The hackathon needs a working API backend to demonstrate routing and agentic workflows. The clippings support a lightweight Python API and optional workflow automation, without requiring a heavy platform choice up front.

## Backend Shape Supported By The Corpus

The Flask and Flask-RESTful material supports:
- app factory structure
- separation between routes and services
- explicit REST-style endpoints
- request parsing and response marshalling

Example high-level layout:

```text
app/
  __init__.py
  routes/
  services/
  schemas/
  models/
tests/
```

Key principle:
- route handlers stay thin
- service layer owns business logic

## REST Conventions

| Pattern | Preferred style |
| --- | --- |
| Collection resource | `/v1/requests` |
| Single resource | `/v1/requests/{id}` |
| Sub-resource | `/v1/requests/{id}/traces` |
| Case | lowercase |
| Actions | use HTTP methods instead of verbs in the URI |

Useful verbs:
- `GET`: read
- `POST`: create or trigger
- `PUT`: full replace
- `PATCH`: partial update
- `DELETE`: remove

## Flask-RESTful Relevance

The Flask-RESTful docs in `Clippings/` are useful for:
- resource-oriented route structure
- request parsing
- output fields and marshalling
- extension points for a small API surface

That makes it a practical choice if the team already knows Flask.

## n8n Relevance

n8n is relevant as an optional workflow layer or demo fallback.

Use it when:
- the Python orchestrator is not ready
- a visual workflow helps explain the system
- you need a quick integration bridge to external services

Possible role in this project:
- webhook in
- classify task
- choose wiki-first vs tool path
- call API or model
- write result back to the wiki or logs

## Hackathon Interpretation

Good baseline options supported by the corpus:
- Flask or Flask-RESTful for the API layer
- a simple React or TypeScript frontend for trace display
- n8n only if it simplifies the demo rather than adding another moving part

The most important choice is not framework prestige. It is picking one path early and documenting its commands and routes in preload pages.

## Edge And Serverless Patterns

### What the new sources add
- **Edge computing** moves execution closer to users or data sources to reduce latency and bandwidth usage.
- **Serverless computing** shifts backend provisioning to a vendor-managed pay-per-use model.
- **FaaS** is the narrow execution primitive inside serverless: small event-driven functions with short-lived execution.

### Useful distinctions

| Model | Where code runs | Best for | Main tradeoff |
| --- | --- | --- | --- |
| Traditional app server | one or a few origins | long-lived APIs, orchestrators, stateful services | more ops and capacity planning |
| Serverless / FaaS | provider-managed ephemeral workers | webhooks, event handlers, bursty traffic, lightweight API glue | harder debugging, cold starts, vendor coupling |
| Edge serverless | geographically distributed edge locations | latency-sensitive validation, auth checks, request shaping, caching logic | stricter runtime limits, careful state design |

### Where this repo's architecture fits
- The **orchestrator** is usually a poor fit for pure FaaS if it needs long-lived state, multi-step retries, or durable execution.
- The **policy/gateway edge** is a strong fit for edge execution:
  - authentication and request filtering
  - rate limiting and abuse controls
  - request normalization
  - cheap-path classification before heavier orchestration
- The **UI/API entrypoint** can be:
  - a small Flask app for local demo simplicity, or
  - an edge/serverless entrypoint if low-latency global access matters more than debugging comfort

### Benefits relevant to the hackathon
- fast deployment and rollback
- auto-scaling for bursty demo traffic
- lower idle cost than permanently provisioned servers
- proximity to users or upstream APIs for lower latency

### Risks and limits
- cold starts still matter on some providers
- long-running orchestration loops are a bad fit
- local debugging and end-to-end test fidelity are weaker than with a persistent app server
- vendor-specific event and runtime models can create lock-in

### Practical recommendation
- Keep the main agentic control loop in a conventional app process unless the runtime is explicitly designed for durable workflows.
- Use edge/serverless only for thin ingress logic, stateless transforms, or high-fanout event handlers.

## API Specification Standards

### JSON Schema 2020-12
Current JSON Schema version. Split into two specs:
- **Core** (`json-schema-core`): defines the schema model (types, references, composition)
- **Validation** (`json-schema-validation`): defines validation keywords (`type`, `minimum`, `maxLength`, `enum`, `required`, etc.)

**Relevance**: OpenAI function calling uses JSON Schema for tool parameter definitions. Flask-RESTful uses JSON Schema (or Marshmallow) for request validation.

Key: OpenAPI 3.1 is fully aligned with JSON Schema 2020-12 (earlier OAS 3.0 was only a subset).

### OpenAPI Specification v3.1.0
Standard language-agnostic HTTP API description format.

Structure of an OpenAPI document:
```yaml
openapi: 3.1.0
info:
  title: Routing API
  version: 1.0.0
paths:
  /v1/requests:
    post:
      operationId: createRequest
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RoutingRequest'
      responses:
        '200':
          description: Routing decision
components:
  schemas:
    RoutingRequest:
      type: object
      required: [query]
      properties:
        query:
          type: string
        context:
          type: object
```

Key objects: `paths`, `components/schemas`, `components/parameters`, `components/responses`.

Data types: `integer` (int32/int64), `number` (float/double), `string`, `boolean`, `array`, `object`. Format modifiers extend the base type.

**Hackathon use**: Document the `/v1/requests` routing API using OpenAPI 3.1.0. Generate client SDK or validation automatically from the spec.

---

## Risks And Caveats

- The secondary web-app ecosystem is broad and easy to overbuild.
- This page should stay anchored to clipped material, not drift into generic framework advice.
- Do not document commands or package choices here unless they exist in the repo.

## Related

- [[app-stack-and-delivery]]
- [[../00-preload/api-routes-and-schemas|API Routes and Schemas]]
- [[../00-preload/commands|Commands]]
- [[../components/orchestrator|Orchestrator]]
- [[../components/policy-gateway|Policy Gateway]]
- [[network-protocols]]
