# Commands

## Current State
- The app project now exists under `project/` and the backend import path is live.
- `python -m unittest tests.test_router_eval_contract` is a working regression test for the router/eval contract.
- `python -m unittest tests.test_run_humaneval` is a working regression test for the HumanEval extraction and execution harness.
- The OpenRouter-backed Anthropic model slugs now target `anthropic/claude-haiku-4.5` and `anthropic/claude-sonnet-4.6` instead of the previous OpenAI defaults.
- `python scripts/run_eval.py` imports cleanly again after restoring `router.select_model()` compatibility.
- The surfaced router branch set is now limited to `memory_answer`, `cheap_model`, `mid_model`, and `strong_model`; project/codebase questions are memory-first instead of using a separate verification branch.

## Working Commands

| Task | Command | Expected Result | Notes |
| --- | --- | --- | --- |
| check clipping drift | `scripts\sync-clippings.cmd check` | reports files present in `Clippings/` but missing from tracking pages | run directly in shell |
| sync clipping pages | `scripts\sync-clippings.cmd sync` | updates clipping tracking pages | run directly in shell |
| direct PowerShell fallback | `powershell -ExecutionPolicy Bypass -File scripts/sync-clippings.ps1 check` | same as wrapper command | use if `.cmd` is inconvenient |
| router/eval regression test | `cd project && python -m unittest tests.test_router_eval_contract` | verifies `run_eval.py` and `router.py` agree on model selection | no API calls |
| HumanEval harness regression test | `cd project && python -m unittest tests.test_run_humaneval` | verifies body-only and full-function completions execute correctly | no API calls |
| HumanEval smoke run | `cd project && python scripts/run_humaneval.py --limit 5` | should produce non-zero pass rate and save `backend/humaneval_results.json` | uses live model calls |
| eval script import smoke test | `cd project && python -c "import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), 'scripts')); import run_eval; print('run_eval import OK')"` | confirms the previous import failure is fixed | no API calls |

## Planned Hackathon Commands

| Task | Planned Command | Expected Result | Notes |
| --- | --- | --- | --- |
| backend deps | `pip install -r requirements.txt` | Flask/httpx/CORS dependencies installed | include `python-dotenv` |
| frontend scaffold | `npx create-vite frontend --template react-ts` | React/Vite app scaffolded | one-time bootstrap |
| frontend deps | `npm install` | frontend dependencies installed | run inside `frontend/` |
| run backend | `python backend/app.py` | Flask API starts on port `5000` | primary backend entry |
| run frontend | `npm run dev` | Vite dev server starts | run inside `frontend/` |
| offline eval | `python scripts/run_eval.py` | writes `backend/eval_results.json` | precompute before demo if possible |
| health check | `curl http://localhost:5000/api/health` | returns `{ "ok": true }` | cheap smoke test |

## Minimum Command Set For The Demo
- install backend dependencies
- install frontend dependencies
- start Flask API
- start React UI
- run offline eval once
- hit `/api/health`
- run one canned demo query

## Related
- [[known-bugs-and-assumptions]]
- [[fallback-plans]]
- [[../design-doc|Design Doc]]
- [[../workflows/hackathon-build-loop|Hackathon Build Loop]]
