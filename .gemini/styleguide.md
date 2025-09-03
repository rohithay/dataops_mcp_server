# dbt project structure 🏗️ 

## Staging

### Folder structure & naming conventions

Within the staging folder, all folders should be related to a **single** source data asset.
A 'source data asset' is considered to be a single BigQuery dataset, so the structure is: `staging/<source>` where `<source>` is the BigQuery dataset name, e.g. `staging/adp_dm_masterdata_view`

Within individual source folders, there will be:

- **Models:** the `.sql` scripts that create the staging data assets. Naming convention: `stg_<source>__<data asset>`,  e.g. `stg_adp_dm_masterdata_view__dim_site_layoutmodule_item_v`
- **Model properties:** a single `.yml` (interchangeable with `.yaml`) file that define certain aspects of the model, such as overall & column definitions. Naming convention: `_<source>__models`, e.g. `_adp_dm_masterdata_view__models`
- **Source properties:** a single `.yml` file that define & describe aspects of the source data assets. Naming convention: `_<source>__sources`, e.g. `_adp_dm_masterdata_view__sources`

### Models

**Overall approach:**

- Each staging model will have a 1:1 relationship with a source data asset
- These are the **only** models that will use the `source` macro, i.e. the only scripts that ingest source data

**Permitted SQL transformations:**

- ✅ Select & rename columns
- ✅ Basic column manipulations
  - See example below for the type of thing that basic column manipulations involves
  - This should be done as often as possible in the staging layer, to avoid repeated code downstream
- ✅ Filter rows

**SQL transformations generally not permitted:**

- ❌ Joins
  - Sometimes joins and / or qualify [are necessary](https://docs.getdbt.com/best-practices/how-we-structure/2-staging)
- ❌ Aggregations

**Script structure:**

- Read in necessary columns & filter rows as a standalone CTE
- Perform column renaming & manipulations as a standalone CTE
- Finish with simple `SELECT * FROM <previous cte name>`
- For queries where there is only column selection from source, a single query can be used

**Example script:**

```sql
WITH source AS (
  SELECT
    id,
    orderid,
    paymentmethod,
    status,
    amount,
    created
  FROM {{ source('stripe', 'payment') }}
),

renamed AS (
  SELECT
    -- ids
    id AS payment_id,
    orderid AS order_id,
    -- strings
    paymentmethod AS payment_method,
    CASE
      WHEN payment_method IN ('stripe', 'paypal', 'credit_card', 'gift_card') THEN 'credit'
      ELSE 'cash'
    END AS payment_type,
    status,
    -- numerics
    amount AS amount_cents,
    amount / 100.0 AS amount,
    -- booleans
    COALESCE(status = 'successful', FALSE) AS is_completed_payment,
    -- dates
    DATE_TRUNC('day', created) AS created_date,
    -- timestamps
    created::TIMESTAMP_LTZ AS created_at
  FROM source
)

SELECT * FROM renamed
```

## Intermediate

### Folder structure & naming conventions

Within the intermediate folder, all folders should be related to a **single** intermediate model grouping. So the structure is: `intermediate/<sensible name to describe collection of models>`, e.g. `intermediate/alerts`. Intermediate model groupings should be based on a sensible collection of models that are related to each other in some way.

Within individual source folders, there will be:

- **Models:** the `.sql` scripts that create the intermediate data assets. Naming convention: `int_<sensible name to describe model>`, e.g. `int_site_article_lsm_alerts`
- **Model properties:** a single `.yml` file that define certain aspects of the model, such as overall & column definitions. Naming convention: `_int_<sensible name to describe collection of models>__models`, e.g. `_int_alerts__models`

### Models

**Overall approach:**

- These models should serve a clear & single purpose regarding transforming other models
- Intermediate models can reference other intermediate models, in addition to staging models
- End users should ***not*** be exposed to these models

**Key aims of these models:**

- **Structural simplification:** increase modularity of code base. It's better to break up pieces of logic, rather than having 8 staging tables joins in mart model, for example
- **Re-graining:** changing staging model data granularity, typically through aggregation, for use downstream
- **Isolating complex logic:** similarly to the first point, it's better to have multiple pieces of complex logic in a single mart model sourced from individual intermediate models (rather than all being created within the mart model). This makes editing & debugging easier

Note this list is ***not*** exhaustive

**Permitted SQL transformations:** all

**Script structure:**

- Read in necessary columns & rows from intermediate and / or staging models
- 1 CTE per input model
- Read in staging models first, then intermediate models
- Perform manipulations using as many CTEs as required
- Finish with simple `SELECT * FROM <previous cte name>`

**Example script:**

```sql
WITH
payments AS (
  SELECT
    order_id,
    status,
    amount
  FROM {{ ref('stg_stripe__payments') }}
),

pivot_and_aggregate_payments_to_order_grain AS (
  SELECT
    order_id,
    SUM(CASE WHEN status = 'success' THEN amount END) AS total_amount
  FROM payments
  GROUP BY 1
)

SELECT * FROM pivot_and_aggregate_payments_to_order_grain
```

## Marts

### Folder structure & naming conventions

Within the marts folder, all folders should be related to a **single** model grouping. So the structure is: `marts/<sensible name to describe collection of models>`, e.g. `marts/alert_comparison`. Mart model groupings should be based on a sensible collection of models that are related to each other in some way based on end users.

Within individual source folders, there will be:

- **Models:** the `.sql` scripts that create the mart data assets. Naming convention: `<fct or dim>_<sensible name to describe model>`, e.g. `fct_alert_comparison`. Info on fct vs. dim: [A complete guide to dimensional modeling with dbt | dbt Labs](https://docs.getdbt.com/terms/dimensional-modeling)
- **Model properties:** a single `.yml` file that contains info detailed [here](docs/dbt/documentation_strategy.md)

### Models

**Overall approach:**

- These models should serve a clear purpose regarding providing data for end users
- Mart models can reference other mart models, in addition to intermediate models. Note this should only be done to improve efficiency, as marts should typically be thought of as final outputs. They cannot reference staging models
- Data should be wide & denormalised to account for fact storage is relatively cheap compared to compute. Info on denormalisation: [What is denormalization?](https://www.techtarget.com/searchdatamanagement/definition/denormalization)

**Permitted SQL transformations:** all

**Script structure:**

- Read in necessary columns & rows from mart and / or intermediate models
- 1 CTE per input model
- Read in intermediate models, then mart models
- Perform manipulations using as many CTEs as required
- Finish with simple `SELECT * FROM <previous cte name>`

**Example script:**

```sql
WITH orders AS (
  SELECT
    order_id,
    customer_id,
    order_date
  FROM {{ ref('int_orders') }}
),

order_payments AS (
  SELECT
    order_id,
    total_amount,
    gift_card_amount
  FROM {{ ref('int_payments_pivoted_to_orders') }}
),

orders_and_order_payments_joined AS (
  SELECT
    orders.order_id,
    orders.customer_id,
    orders.order_date,
    COALESCE(order_payments.total_amount, 0) AS amount,
    COALESCE(order_payments.gift_card_amount, 0) AS gift_card_amount
  FROM orders
  LEFT OUTER JOIN order_payments
    USING (order_id)
)

SELECT * FROM orders_and_order_payments_joined
```

## External

`fa_dim`-specific layer for serving marts data to end users.

### Folder structure & naming conventions

Within the external folder, all folders should match a marts folder name with the `_external` suffix. Note that models don't necessarily have to be in a folder (they can be added directly to `external/`). So the structure is: `external/<marts folder>_external`, e.g. `external/dim_product_split_external`

Within individual workstream folders, there will be:

- **Models:** the `.sql` scripts that serve mart data to external consumers. Naming convention: `<entity_name>_external.sql` (uses alias config to remove suffix), e.g. `dim_product_long_external.sql` → served as `dim_product_long`
- **Model properties:** a single `.yml` file that contains info detailed [here](docs/dbt/documentation_strategy.md)

### Models

**Overall approach:**

- These models serve the marts layer outputs to end users
- Each external model corresponds to a single marts model

**Script structure:**

- Configure alias to remove `_external` suffix
- Simple `SELECT` statement using `dbt_utils.star()` or explicit column selection
- Reference a single marts model

**Example script:**

```sql
{{ config(alias='dim_product_long') }}

SELECT {{ dbt_utils.star(from=ref('dim_product_long')) }} FROM {{ ref('dim_product_long') }}
```

## DAG shape & dependencies

Our project creates an "arrowhead" shape:

- **Wide start:** many narrow staging models (1 per source)
- **Narrowing middle:** fewer modular intermediate models  
- **Focused end:** few targeted mart models
- **External layer:** clean presentation of marts for end users (same number as marts)

Flow: Sources → Staging → Intermediate → Marts → External

## Workstream organisation

Each workstream in `fa_dim` follows the same structural pattern:

```
models/
└── workstream_name/
    ├── staging/
    │   └── source_name/
    │       ├── stg_source__entity.sql
    │       ├── _source__models.yml
    │       └── _source__sources.yml
    ├── intermediate/
    │   └── int_workstream_specific_transformation.sql
    ├── marts/
    │   └── dim_or_fct_business_entity.sql
    └── external/
        └── dim_or_fct_business_entity_external.sql
```

# dbt SQL style guide 🎨

This guide outlines SQL coding standards for `fa_dim`. Following these ensures consistent, readable code across the project.

## SQL style guidelines

### CTE structure

- Optimise for readability, not fewer lines of code
- Split actions into multiple steps
- Use explicit column references, never `SELECT *` (except final CTE)
- End with `SELECT * FROM <previous cte name>`

For more info on SQL script structure guidelines, see [here](../dbt/project_structure.md).

### Joins & filtering

- `WHERE` filters left table only when used with joins
- Filter tables before joining when possible
- Fully qualify join types (`INNER JOIN`, `LEFT OUTER JOIN`)
- Use `IS TRUE`/`IS FALSE` for booleans

### Naming & formatting

- Views have `_v` suffix
- Use `lower_snake_case` for all objects
- dbt functions need whitespace: `{{ source('datamart', 'dim_date') }}`
- Reference columns with table names in joins, not aliases
- SQL keywords in UPPERCASE
- Use trailing commas
- Use `AS` for aliases
- Use `COALESCE()` not `IFNULL()`
- Tab space size of 2
- Blank lines between CTEs

For complete SQLFluff rules, see `.sqlfluff` in the repository root.

### Example:

```sql
WITH users_filter AS (
  SELECT
    user_id,
    first_name,
    last_name
  FROM users
  WHERE TRUE
    AND is_active IS TRUE
),

orders_filter AS (
  SELECT
    order_id,
    user_id,
    order_total
  FROM orders
  WHERE TRUE
    AND is_completed IS TRUE
),

users_orders_joined AS (
  SELECT
    users_filter.user_id,
    users_filter.first_name,
    users_filter.last_name,
    orders_filter.order_id,
    orders_filter.order_total
  FROM users_filter
  LEFT OUTER JOIN orders_filter
    USING (user_id)
),

users_orders AS (
  SELECT
    user_id,
    first_name,
    last_name,
    COUNT(order_id) AS total_orders,
    SUM(order_total) AS total_spent
  FROM users_orders_joined
  GROUP BY 1, 2, 3
  HAVING total_orders > 0
)

SELECT * FROM users_orders
```
