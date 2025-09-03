# dataops-mcp-server Project Copilot Instructions

When responding to prompts about the dataops-mcp-server project:

## 1. Clarity First Approach

- Request specific clarification when faced with ambiguous requirements
- Take the time necessary to consider all options
- Suggest fundamental alternatives when a different approach would yield better outcomes
- Identify potential downstream impacts of proposed solutions

## 2. Iterative Feedback Process

- Present a representative sample of suggested changes before delivering comprehensive recommendations
- Include clear rationale explaining the purpose and benefit of each proposed change
- Establish checkpoints for confirmation before proceeding with extensive modifications
- Only ever make modifications when explicitly asked to

## 3. Technology Stack Alignment

- Prioritise dbt-centric solutions where relevant to leverage existing infrastructure
- Frame recommendations within dbt methodologies and best practices
- Suggest dbt package extensions rather than external solutions when possible

## 4. Implementation Feasibility

- Verify compatibility with current software versions before proposing solutions
- Consider existing package dependencies and constraints
- Provide alternative approaches when version limitations prevent ideal solutions

## dbt Project Structure Guidelines

### Model Organisation
Our dbt models follow a three-layer architecture. When creating or suggesting models, place them in the appropriate layer:

#### 1. Staging Models (`staging/`)
- **Purpose**: 1-1 relationship with source data assets
- **Naming**: `stg_<source>__<data_asset>` (note the double underscore)
- **Example**: `stg_adp_dm_masterdata_view__dim_site_layoutmodule_item_v`

When working with staging models:
- Only use the `{{ source() }}` macro here - these are the only models that ingest raw data
- Keep transformations minimal: column selection, renaming, basic manipulations, row filtering
- Avoid joins and aggregations (unless absolutely necessary with QUALIFY)
- Structure CTEs as: source selection → column transformations → final SELECT *

#### 2. Intermediate Models (`intermediate/`)
- **Purpose**: Purpose-built transformation steps
- **Naming**: `int_<descriptive_name>`
- **Example**: `int_site_article_lsm_alerts`

When working with intermediate models:
- These should serve clear, single purposes
- Can reference staging and other intermediate models
- Use for structural simplification, re-graining, or isolating complex logic
- Not exposed to end users

#### 3. Mart Models (`marts/`)
- **Purpose**: Business-defined entities for end users
- **Naming**: `<fct|dim>_<descriptive_name>` 
- **Example**: `fct_alert_comparison`

When working with mart models:
- Denormalise data for performance (storage is cheap, compute is expensive)
- Can reference intermediate and other mart models, but NOT staging models directly
- Use `fct_` prefix for fact tables, `dim_` prefix for dimension tables

### Model Property Files
Each folder should have a corresponding properties file:
- Staging: `_<source>__models.yml`
- Intermediate: `_int_<grouping>__models.yml`
- Marts: `_<fct|dim>_<grouping>__models.yml`

## SQL Style Guidelines

When generating SQL code, strictly follow these conventions:

### Keywords and Identifiers
- **ALL** SQL keywords must be UPPERCASE: `SELECT`, `FROM`, `WHERE`, `JOIN`
- **ALL** identifiers (tables, columns) must be lowercase_snake_case
- Views must have `_v` suffix

### CTE Structure
```sql
WITH source AS (
  SELECT
    column_1,
    column_2
  FROM {{ source('schema', 'table') }}
  WHERE
    is_active IS TRUE
),

transformed AS (
  SELECT
    source.column_1,
    source.column_2,
    COALESCE(source.amount, 0) AS amount
  FROM source
)

SELECT * FROM transformed
```

Key CTE principles:
- Optimise for readability, not fewer lines
- One CTE per input source/table
- Filter before joining
- Always end with `SELECT * FROM <final_cte>`
- Use meaningful CTE names that describe the transformation

### Specific Requirements
- **Never** use `SELECT *`, except in final CTE
- **Always** qualify columns with table names in joins, e.g. `users.user_id`
- Use `!=` not `<>` for inequality
- Use `COALESCE()` not `IFNULL()`
- Fully qualify joins: `LEFT OUTER JOIN`, not just `LEFT JOIN`
- For boolean filters, use `IS TRUE/FALSE` not `= TRUE/FALSE`
- Use trailing commas in SELECT lists
- Indent with 2 spaces (not 4)

### BigQuery-Specific Considerations
- Use `DATE_TRUNC('day', date_column)` for date truncation
- Consider partitioning and clustering strategies for large tables
- Use `EXCEPT()` and `REPLACE()` for column operations when appropriate
- Leverage ARRAY and STRUCT types where they make sense

## Common Patterns and Anti-Patterns

### Good Patterns to Follow
- Break complex logic into multiple intermediate models
- Use descriptive CTE names that explain the transformation
- Keep staging models simple and close to source

### Anti-Patterns to Avoid
- Subqueries (use CTEs instead)
- Joins in staging models (push to intermediate layer)
- Direct staging-to-mart references (use intermediate layer)
- Complex logic in single models (break into intermediate steps)
- Hardcoded values without documentation

## Example Responses

### When asked to create a staging model:

```sql

WITH source AS (
  SELECT
    product_id,
    product_name,
    category_code,
    is_active,
    created_date,
    modified_date
  FROM {{ source('adp_dm_masterdata_view', 'product_master') }}
  WHERE
    is_active IS TRUE
),

renamed AS (
  SELECT
    product_id,
    product_name,
    category_code,
    COALESCE(is_active, FALSE) AS is_active_flag,
    DATE_TRUNC('day', created_date) AS created_date,
    DATE_TRUNC('day', modified_date) AS modified_date
  FROM source
)

SELECT * FROM renamed
```

## Remember

- Always use Australian English conventions in responses and code comments
- Consider BigQuery costs - prefer columnar operations over row-by-row
- Follow the established patterns even if you might personally prefer alternatives
- Suggest improvements that align with the existing architecture
