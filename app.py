"""
GCP Cost Optimization MCP Server — Gradio Interface
Wraps rohithay/dataops-mcp-server tools with a web UI + MCP SSE endpoint.
"""

import gradio as gr
import os
import json
from typing import Optional

# ── Import your actual server modules here ───────────────────────────────────
# from dataops_mcp_server.bigquery import get_bigquery_costs, analyze_query_cost
# from dataops_mcp_server.anomalies import detect_cost_anomalies
# from dataops_mcp_server.optimize import optimize_query, create_optimization_pr
# from dataops_mcp_server.alerts import send_cost_alert
# from dataops_mcp_server.dbt import get_dbt_model_costs
# from dataops_mcp_server.sla import monitor_sla_compliance
# from dataops_mcp_server.forecast import forecast_costs
# from dataops_mcp_server.slack import slack_post_message
# ─────────────────────────────────────────────────────────────────────────────


# ── Tool wrapper functions ────────────────────────────────────────────────────
# Each function:
#   1. Has the same name as your MCP tool
#   2. Has a clear docstring (becomes the MCP tool description)
#   3. Has type hints (become the MCP tool schema)
#   4. Calls your real server module (replace the stub return)

def get_bigquery_costs(
    days: int = 7,
    project_id: Optional[str] = None,
    include_predictions: bool = True,
    group_by: str = "date",
    include_query_details: bool = False
) -> str:
    """
    Retrieve comprehensive BigQuery cost analysis for specified time periods.

    Args:
        days: Number of days to analyze (1-90)
        project_id: Specific GCP project ID (optional)
        include_predictions: Include ML-based cost forecasting
        group_by: Grouping dimension - date, user, dataset, or query_type
        include_query_details: Include individual query cost breakdowns
    """
    # TODO: replace stub with → from dataops_mcp_server.bigquery import get_bigquery_costs as _get; return _get(...)
    return json.dumps({"tool": "get_bigquery_costs", "days": days, "project_id": project_id, "status": "stub"}, indent=2)


def analyze_query_cost(
    sql: str,
    project_id: Optional[str] = None,
    include_optimization: bool = True,
    optimization_model: str = "claude",
    create_pr_if_savings: bool = False
) -> str:
    """
    Predict cost of a SQL query before execution and get optimization suggestions.

    Args:
        sql: SQL query to analyze (required)
        project_id: GCP project ID (optional)
        include_optimization: Include AI-powered optimization suggestions
        optimization_model: Model to use - claude or gpt-4
        create_pr_if_savings: Create GitHub PR if savings exceed threshold
    """
    return json.dumps({"tool": "analyze_query_cost", "sql_preview": sql[:100], "model": optimization_model, "status": "stub"}, indent=2)


def detect_cost_anomalies(
    days: int = 30,
    sensitivity: str = "medium",
    project_id: Optional[str] = None,
    alert_threshold: float = 0.25,
    send_slack_alert: bool = False
) -> str:
    """
    Use ML to detect cost spikes, anomalies, and early signs of overruns.

    Args:
        days: Historical days to analyze
        sensitivity: Detection sensitivity - low, medium, or high
        project_id: GCP project ID (optional)
        alert_threshold: Fractional increase to trigger alert e.g. 0.25 means 25 percent
        send_slack_alert: Send Slack alert if anomalies are found
    """
    return json.dumps({"tool": "detect_cost_anomalies", "days": days, "sensitivity": sensitivity, "threshold": alert_threshold, "status": "stub"}, indent=2)


def optimize_query(
    sql: str,
    optimization_goals: str = "cost,performance",
    preserve_results: bool = True,
    include_explanation: bool = True,
    target_savings_pct: int = 30,
    dbt_model_path: Optional[str] = None
) -> str:
    """
    LLM-powered query optimization with cost-saving recommendations.

    Args:
        sql: SQL query to optimize (required)
        optimization_goals: Comma-separated objectives e.g. cost,performance
        preserve_results: Ensure query results remain unchanged
        include_explanation: Include explanation of changes made
        target_savings_pct: Target savings percentage
        dbt_model_path: Path to dbt model for additional context (optional)
    """
    return json.dumps({"tool": "optimize_query", "sql_preview": sql[:100], "goals": optimization_goals, "target_pct": target_savings_pct, "status": "stub"}, indent=2)


def create_optimization_pr(
    optimization_id: str,
    repository: str = "data-platform",
    base_branch: str = "main",
    title_prefix: str = "🚀 Cost Optimization",
    assign_reviewers: bool = True,
    include_tests: bool = True
) -> str:
    """
    Auto-create GitHub PRs with optimized SQL and validation tests.

    Args:
        optimization_id: Optimization analysis ID from a previous optimize_query call
        repository: GitHub repository name
        base_branch: Base branch for the PR
        title_prefix: Prefix for the PR title
        assign_reviewers: Auto-assign reviewers to the PR
        include_tests: Generate validation tests for the PR
    """
    return json.dumps({"tool": "create_optimization_pr", "optimization_id": optimization_id, "repo": repository, "status": "stub"}, indent=2)


def send_cost_alert(
    alert_type: str,
    cost_data: str,
    severity: str = "medium",
    channel: str = "#data-ops-alerts",
    mention_users: str = "",
    include_remediation: bool = True
) -> str:
    """
    Send actionable cost alerts to Slack with rich context.

    Args:
        alert_type: Type of alert - anomaly, budget_warning, or optimization_opportunity
        cost_data: JSON string of cost data to include in the alert
        severity: Alert severity - low, medium, or high
        channel: Slack channel for the alert
        mention_users: Comma-separated Slack user IDs to mention
        include_remediation: Include suggested fix in the alert
    """
    return json.dumps({"tool": "send_cost_alert", "type": alert_type, "severity": severity, "channel": channel, "status": "stub"}, indent=2)


def get_dbt_model_costs(
    model_path: Optional[str] = None,
    include_dependencies: bool = True,
    materialization_analysis: bool = True,
    days: int = 7,
    suggest_optimizations: bool = True
) -> str:
    """
    Analyze dbt model execution costs and optimization opportunities.

    Args:
        model_path: Specific dbt model path (optional)
        include_dependencies: Analyze downstream dependency impacts
        materialization_analysis: Suggest materialization strategy improvements
        days: Time period for analysis
        suggest_optimizations: Include cost-saving suggestions
    """
    return json.dumps({"tool": "get_dbt_model_costs", "model_path": model_path, "days": days, "status": "stub"}, indent=2)


def monitor_sla_compliance(
    sla_type: str = "all",
    time_window: str = "24h",
    include_cost_correlation: bool = True,
    alert_on_breach: bool = False,
    optimization_suggestions: bool = True
) -> str:
    """
    Monitor pipeline SLAs and correlate with cost-performance metrics.

    Args:
        sla_type: SLA type to monitor - latency, freshness, success_rate, or all
        time_window: Time window for analysis e.g. 24h, 7d
        include_cost_correlation: Link SLA metrics with cost data
        alert_on_breach: Send alerts when SLA is breached
        optimization_suggestions: Suggest cost-aware fixes for breaches
    """
    return json.dumps({"tool": "monitor_sla_compliance", "sla_type": sla_type, "window": time_window, "status": "stub"}, indent=2)


def forecast_costs(
    forecast_days: int = 30,
    include_confidence_intervals: bool = True,
    breakdown_by: str = "service",
    scenario_analysis: bool = False,
    budget_recommendations: bool = True
) -> str:
    """
    Forecast future GCP spend using ML and scenario modeling.

    Args:
        forecast_days: Number of days to forecast
        include_confidence_intervals: Include prediction confidence ranges
        breakdown_by: Forecast breakdown dimension - service or project
        scenario_analysis: Include optimistic and pessimistic scenarios
        budget_recommendations: Suggest budget allocations based on forecast
    """
    return json.dumps({"tool": "forecast_costs", "days": forecast_days, "breakdown": breakdown_by, "status": "stub"}, indent=2)


def slack_post_message(channel_id: str, text: str) -> str:
    """
    Post a message to a Slack channel.

    Args:
        channel_id: ID of the Slack channel
        text: Message text to post
    """
    return json.dumps({"tool": "slack_post_message", "channel_id": channel_id, "text_preview": text[:100], "status": "stub"}, indent=2)


# ── Gradio UI ─────────────────────────────────────────────────────────────────

with gr.Blocks(title="GCP Cost Optimization", theme=gr.themes.Soft()) as demo:

    gr.Markdown("""
    # ☁️ GCP Cost Optimization MCP Server
    Test tools directly in the browser · Connect any MCP client via the SSE endpoint below.
    """)

    with gr.Tab("📊 BigQuery Costs"):
        with gr.Row():
            bq_days = gr.Slider(1, 90, value=7, label="Days")
            bq_project = gr.Textbox(label="Project ID (optional)")
            bq_group_by = gr.Dropdown(["date", "user", "dataset", "query_type"], value="date", label="Group By")
        with gr.Row():
            bq_predictions = gr.Checkbox(value=True, label="Include Predictions")
            bq_details = gr.Checkbox(value=False, label="Include Query Details")
        gr.Button("Get BigQuery Costs", variant="primary").click(
            get_bigquery_costs, [bq_days, bq_project, bq_predictions, bq_group_by, bq_details],
            gr.Code(language="json", label="Result"))

    with gr.Tab("🔍 Analyze Query Cost"):
        aq_sql = gr.Code(language="sql", label="SQL Query", lines=8)
        with gr.Row():
            aq_project = gr.Textbox(label="Project ID (optional)")
            aq_model = gr.Dropdown(["claude", "gpt-4"], value="claude", label="Model")
        with gr.Row():
            aq_opt = gr.Checkbox(value=True, label="Include Optimization")
            aq_pr = gr.Checkbox(value=False, label="Create PR if Savings Found")
        aq_out = gr.Code(language="json", label="Result")
        gr.Button("Analyze", variant="primary").click(
            analyze_query_cost, [aq_sql, aq_project, aq_opt, aq_model, aq_pr], aq_out)

    with gr.Tab("🚨 Detect Anomalies"):
        with gr.Row():
            an_days = gr.Slider(1, 90, value=30, label="Historical Days")
            an_sens = gr.Dropdown(["low", "medium", "high"], value="medium", label="Sensitivity")
            an_thresh = gr.Slider(0.05, 1.0, value=0.25, step=0.05, label="Alert Threshold")
        with gr.Row():
            an_project = gr.Textbox(label="Project ID (optional)")
            an_slack = gr.Checkbox(value=False, label="Send Slack Alert")
        an_out = gr.Code(language="json", label="Result")
        gr.Button("Detect Anomalies", variant="primary").click(
            detect_cost_anomalies, [an_days, an_sens, an_project, an_thresh, an_slack], an_out)

    with gr.Tab("⚡ Optimize Query"):
        opt_sql = gr.Code(language="sql", label="SQL Query", lines=8)
        with gr.Row():
            opt_goals = gr.CheckboxGroup(["cost", "performance", "readability"], value=["cost", "performance"], label="Goals")
            opt_pct = gr.Slider(10, 80, value=30, label="Target Savings %")
        with gr.Row():
            opt_preserve = gr.Checkbox(value=True, label="Preserve Results")
            opt_explain = gr.Checkbox(value=True, label="Include Explanation")
        opt_dbt = gr.Textbox(label="dbt Model Path (optional)")
        opt_out = gr.Code(language="json", label="Result")
        gr.Button("Optimize", variant="primary").click(
            lambda sql, goals, preserve, explain, pct, dbt: optimize_query(sql, ",".join(goals), preserve, explain, pct, dbt),
            [opt_sql, opt_goals, opt_preserve, opt_explain, opt_pct, opt_dbt], opt_out)

    with gr.Tab("🔀 Create PR"):
        with gr.Row():
            pr_id = gr.Textbox(label="Optimization ID")
            pr_repo = gr.Textbox(value="data-platform", label="Repository")
        with gr.Row():
            pr_branch = gr.Textbox(value="main", label="Base Branch")
            pr_prefix = gr.Textbox(value="🚀 Cost Optimization", label="Title Prefix")
        with gr.Row():
            pr_reviewers = gr.Checkbox(value=True, label="Auto-assign Reviewers")
            pr_tests = gr.Checkbox(value=True, label="Include Tests")
        pr_out = gr.Code(language="json", label="Result")
        gr.Button("Create PR", variant="primary").click(
            create_optimization_pr, [pr_id, pr_repo, pr_branch, pr_prefix, pr_reviewers, pr_tests], pr_out)

    with gr.Tab("🔔 Cost Alerts"):
        with gr.Row():
            al_type = gr.Dropdown(["anomaly", "budget_warning", "optimization_opportunity"], label="Alert Type")
            al_sev = gr.Dropdown(["low", "medium", "high"], value="medium", label="Severity")
        al_data = gr.Code(language="json", label="Cost Data (JSON)", value="{}", lines=4)
        with gr.Row():
            al_channel = gr.Textbox(value="#data-ops-alerts", label="Slack Channel")
            al_users = gr.Textbox(label="Mention Users (comma-separated)")
        al_rem = gr.Checkbox(value=True, label="Include Remediation")
        al_out = gr.Code(language="json", label="Result")
        gr.Button("Send Alert", variant="primary").click(
            send_cost_alert, [al_type, al_data, al_sev, al_channel, al_users, al_rem], al_out)

    with gr.Tab("🔧 dbt Costs"):
        with gr.Row():
            dbt_path = gr.Textbox(label="dbt Model Path (optional)")
            dbt_days = gr.Slider(1, 30, value=7, label="Days")
        with gr.Row():
            dbt_deps = gr.Checkbox(value=True, label="Include Dependencies")
            dbt_mat = gr.Checkbox(value=True, label="Materialization Analysis")
            dbt_opt = gr.Checkbox(value=True, label="Suggest Optimizations")
        dbt_out = gr.Code(language="json", label="Result")
        gr.Button("Analyze dbt Costs", variant="primary").click(
            get_dbt_model_costs, [dbt_path, dbt_deps, dbt_mat, dbt_days, dbt_opt], dbt_out)

    with gr.Tab("📈 SLA Monitoring"):
        with gr.Row():
            sla_type = gr.Dropdown(["all", "latency", "freshness", "success_rate"], value="all", label="SLA Type")
            sla_window = gr.Dropdown(["1h", "6h", "24h", "7d", "30d"], value="24h", label="Time Window")
        with gr.Row():
            sla_cost = gr.Checkbox(value=True, label="Cost Correlation")
            sla_alert = gr.Checkbox(value=False, label="Alert on Breach")
            sla_opt = gr.Checkbox(value=True, label="Optimization Suggestions")
        sla_out = gr.Code(language="json", label="Result")
        gr.Button("Monitor SLA", variant="primary").click(
            monitor_sla_compliance, [sla_type, sla_window, sla_cost, sla_alert, sla_opt], sla_out)

    with gr.Tab("🔮 Forecast Costs"):
        with gr.Row():
            fc_days = gr.Slider(7, 90, value=30, label="Forecast Days")
            fc_breakdown = gr.Dropdown(["service", "project"], value="service", label="Breakdown By")
        with gr.Row():
            fc_ci = gr.Checkbox(value=True, label="Confidence Intervals")
            fc_scenario = gr.Checkbox(value=False, label="Scenario Analysis")
            fc_budget = gr.Checkbox(value=True, label="Budget Recommendations")
        fc_out = gr.Code(language="json", label="Result")
        gr.Button("Forecast", variant="primary").click(
            forecast_costs, [fc_days, fc_ci, fc_breakdown, fc_scenario, fc_budget], fc_out)

    with gr.Tab("💬 Slack"):
        sl_channel = gr.Textbox(label="Channel ID")
        sl_text = gr.Textbox(label="Message", lines=4)
        sl_out = gr.Code(language="json", label="Result")
        gr.Button("Post Message", variant="primary").click(
            slack_post_message, [sl_channel, sl_text], sl_out)

    gr.Markdown("""
    ---
    ### 🔌 MCP Client Config
    ```json
    {
      "mcpServers": {
        "gcp-cost-optimization": {
          "url": "https://<your-hf-username>-gcp-cost-optimization.hf.space/gradio_api/mcp/sse"
        }
      }
    }
    ```
    """)

if __name__ == "__main__":
    demo.launch(mcp_server=True)