# AnalyzeQueryCostTool Evals

## Overview

These evaluations validates the critical path of `AnalyzeQueryCostTool` — a BigQuery
pre-execution cost analysis tool that estimates query costs, detects optimization opportunities,
and gates high-risk executions before they hit production.

The four evaluations here are ordered by blast radius. They cover the failure modes
that cause real damage: wrong cost estimates, missed optimizations, misclassified risk levels,
and unsafe inputs reaching the BigQuery API.

---

## Evaluation Summary

| ID | Name | What It Protects Against |
|---|---|---|
| eval_001 | Cost Estimation and Tier Classification | Wrong pricing math silently misinforming engineers |
| eval_002 | Optimization Pattern Detection | Anti-patterns going undetected, money left on the table |
| eval_003 | Critical Risk Gate | Runaway queries executing without a warning |
| eval_004 | Input Validation | Malformed or destructive SQL reaching the BigQuery API |

---

## Evaluations

### eval_001 — Cost Estimation and Tier Classification

**Why it matters:** Cost estimation is the entire value proposition of this tool. If
`_calculate_cost_estimates()` produces wrong numbers or assigns the wrong tier, every
downstream decision — approval workflows, optimization thresholds, PR creation triggers —
is made on bad data. This is the contract the tool makes with its callers.

**What it tests:**
- Byte-to-terabyte conversion accuracy
- Cost formula: `(bytes / 1024⁴) * $6.25`
- Correct `LOW` tier assignment for sub-$1 queries
- `price_per_tb` surfaced correctly in `cost_breakdown`

**Pass condition:** Estimated cost within 1% of $0.0916 for a 15GB dry-run result, tier
classified as `LOW`.

---

### eval_002 — Optimization Pattern Detection — Multiple Violations

**Why it matters:** A query with `SELECT *`, no `WHERE`, and `ORDER BY` without `LIMIT`
against a large table is a textbook expensive query. If the pattern matcher misses any
of these, the engineer gets incomplete guidance and the optimization opportunity is lost.
In aggregate across many queries, missed patterns represent significant unnecessary spend.

**What it tests:**
- `select_star` pattern match via regex
- `no_where_clause` pattern match via regex
- `no_limit_with_order` pattern match via regex
- Deduplication — all three suggestions appear exactly once
- `include_optimization=false` returns an empty list (no false positives when disabled)

**Pass condition:** Exactly 3 distinct suggestions returned, one per anti-pattern.
Zero suggestions when `include_optimization=false`.

---

### eval_003 — Critical Risk Gate — High Cost Query Should Block Execution

**Why it matters:** This is the primary safety mechanism of the tool. A `CRITICAL` risk
query against a 2TB table with no filters should never get a green light. If the risk
score accumulation logic has an off-by-one error or a missing condition, a single
unreviewed execution could generate a five-figure BigQuery bill. The
`execution_recommendation` field is what pipeline engineers check before running queries
in automated workflows.

**What it tests:**
- Risk score accumulates correctly across multiple independent risk factors
- 2TB full-table scan with `SELECT *` and no `WHERE` reaches `risk_score >= 8`
- `risk_level` is classified as `CRITICAL`
- `execution_recommendation` contains the "DO NOT EXECUTE" directive
- `mitigation_steps` is populated (not empty)

**Pass condition:** `risk_level = CRITICAL`, `risk_score >= 8`, recommendation includes
"DO NOT EXECUTE", mitigation steps present.

---

### eval_004 — Input Validation — Malformed and Dangerous SQL

**Why it matters:** Validation failures that reach the BigQuery dry-run API waste quota,
can surface cryptic GCP errors as unhandled exceptions, and in the case of DML statements,
represent a safety gap — a `DROP TABLE` call with `dry_run=True` is still a network request
that shouldn't be made. Validation must be a pure in-process gate that fires before any I/O.

**What it tests:**
- Empty string rejected without any API call
- Whitespace-only string rejected without any API call
- DML statement (`DROP TABLE`) rejected with a distinct, clear error message
- No internal stack traces or class names leaked in error responses
- All three cases return sub-50ms (confirms no I/O occurred)

**Pass condition:** All three inputs return `success: false`. No BigQuery API calls made.
Error messages are human-readable and do not expose implementation internals.

---

## Running the Evaluations

Each evaluation should be run as an integration test with a mocked BigQuery client to
control `bytes_processed` values returned by the dry-run:

```python
from unittest.mock import MagicMock, patch
import pytest

@pytest.mark.asyncio
async def test_eval_001_cost_estimation():
    tool = AnalyzeQueryCostTool(project_id="test-project")

    mock_job = MagicMock()
    mock_job.total_bytes_processed = 16_106_127_360  # 15GB
    mock_job.schema = []

    with patch.object(tool.bq_client, "query", return_value=mock_job):
        result = json.loads(await tool.execute(
            "SELECT user_id FROM `project.dataset.events` WHERE created_at >= '2024-01-01'"
        ))

    assert result["success"] is True
    assert abs(result["analysis"]["estimated_cost_usd"] - 0.0916) < 0.001
    assert result["analysis"]["cost_tier"] == "LOW"
```

Repeat the pattern for eval_002 through eval_004, adjusting `bytes_processed` and
SQL inputs per scenario.

---

## Failure Triage

| Symptom | Likely Cause | Where to Look |
|---|---|---|
| eval_001 cost is off | Byte→TB conversion error | `_calculate_cost_estimates()` |
| eval_001 wrong tier | Tier boundary logic | `cost_tiers` dict in `__init__` |
| eval_002 missing suggestion | Regex not matching | `optimization_patterns` regex strings |
| eval_002 duplicate suggestions | `list(set(...))` not applied | `_generate_optimization_suggestions()` return |
| eval_003 risk score too low | Missing risk factor condition | `_assess_execution_risk()` scoring block |
| eval_003 wrong recommendation | Mapping mismatch | `_get_execution_recommendation()` |
| eval_004 API call on invalid input | Validation not called first | Top of `execute()` method |
| eval_004 stack trace in response | Bare `except Exception` logging | `execute()` error handler |

---
