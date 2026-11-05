# Module03 Reflection

## What I learned

Module03 helped me understand how to write, analyze, optimize, and secure SQL queries.

### 1. Complex DQL queries

I practiced complex SQL using joins, aggregation, subqueries, and window functions. I also translated a SQL query into relational algebra using selection (σ), projection (π), joins (⋈), and grouping (γ). This helped me understand the meaning behind the SQL instead of only writing the syntax.

### 2. Reading EXPLAIN QUERY PLAN

I learned how to use `EXPLAIN QUERY PLAN` as evidence of what SQLite is actually doing. I learned the difference between `SCAN` and `SEARCH`, and I saw how SQLite can use indexes and temporary B-trees for grouping and ordering.

For example, I compared the query plans before and after creating an index. This helped me understand that a query plan can explain why a query is fast or slow.

### 3. Benchmarking indexes

I tested the effect of indexes using multiple runs and compared the median execution time. I learned that an index does not automatically make every query faster.

For example, the single-day lookup became much faster after adding `ix_orders_ordered_on`. However, another index changed the dashboard query plan but made the query slower. This showed me that index performance depends on the query and how the database planner chooses to execute it.

### 4. Using and verifying AI

I used an LLM to help generate SQL and alternative query approaches. However, I did not assume that the generated SQL or predicted query plan was correct.

I tested the queries against my SQLite database and used `EXPLAIN QUERY PLAN` to check the actual execution plan. I also compared different versions of the late-orders query, including the correlated subquery and window-function versions.

This taught me that AI can help with SQL, but the results still need to be tested and verified using a real database.

### 5. Preventing SQL injection

I reproduced a SQL injection using the payload:

```text
' OR '1'='1
```

The vulnerable query returned multiple customers because the input changed the SQL logic. I then fixed the problem using a bound parameter with `?`.

This helped me understand why user input should not be inserted directly into an SQL string and why parameterized queries are the correct solution.

## What was most interesting

The most interesting result was that adding an index could make a query slower. Before Module03, I thought an index generally made queries faster. The benchmark showed me that the database planner and the structure of the query are important.

I also found the window-function execution plan interesting because SQLite used several co-routines and temporary B-trees.

## How I verified my work

I verified my SQL by running the queries directly against `warehouse.db`. I recorded actual `EXPLAIN QUERY PLAN` output instead of relying only on predictions. I also used benchmark results from multiple runs and recorded the median.

For the SQL injection task, I tested both the vulnerable and parameterized versions and compared their results.

## Overall reflection

Module03 changed how I think about SQL. I now understand that writing a query that returns the correct result is only one part of database work. I also need to check the execution plan, measure performance, consider security, and verify AI-generated SQL.

The main lesson I take from this module is: **do not just trust that a query works — test what the database is actually doing.**