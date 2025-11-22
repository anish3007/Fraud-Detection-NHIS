# AI Prompt Journal

This file stores the exact prompts and LLM outputs used during development for traceability.

How to use
- Each entry contains: prompt, model used, date, and the raw output. Paste the exact LLM output under each prompt.

1) Prompt: "Propose a simple, explainable heuristic to assign a fraud likelihood score (0-100) for healthcare claims using fields like billed_amount, procedure_code, and provider_id. Return a clear formula and edge-case handling."
Model: <model>
Date: <YYYY-MM-DD>
Output:
```
<paste LLM output here>
```

2) Prompt: "Generate a Python function that implements the heuristic: inputs are a claim row dict, and output is an integer score between 0 and 100. Include docstring and unit-test example."
Model: <model>
Date: <YYYY-MM-DD>
Output:
```
<paste LLM output here>
```

3) Prompt: "Recommend a minimal FastAPI project structure for an MVP that serves a dashboard and a paginated claims API; include endpoints and data flow."
Model: <model>
Date: <YYYY-MM-DD>
Output:
```
<paste LLM output here>
```

4) Prompt: "Write a pytest unit test for the fraud scoring function that verifies low/medium/high buckets and edge-case values."
Model: <model>
Date: <YYYY-MM-DD>
Output:
```
<paste LLM output here>
```

5) Prompt: "Compare SQLite vs Postgres for a prototype claims auditor dashboard and recommend which to use for quick MVP deployment."
Model: <model>
Date: <YYYY-MM-DD>
Output:
```
<paste LLM output here>
```

Notes
- Prompts were iteratively refined (temperature, constraints, and expected return types) to produce concise, testable code snippets.
- Add the full raw LLM outputs for submission traceability. Keep the model and date fields accurate.
- The final submission will include the exact prompts used and the final LLM outputs in the repository `README` before delivery.
