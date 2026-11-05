# Module03 Reflection

## My Take-away

Module03 helped me understand how to write, analyze, optimize, and secure SQL queries.

My biggest take-away is “do not just trust that a query works — check what the database is actually doing.” I learned to use `EXPLAIN QUERY PLAN` to see whether SQLite uses a scan, search, index, or temporary B-tree.

I also learned that an index does not always make a query faster, and that SQL injection can be prevented by using bound parameters.

## What Was Good?

I liked the practical experiments in this module. I compared queries before and after adding indexes and used actual execution times to see the difference.

I also worked with complex SQL using joins, grouping, subqueries, and window functions. Comparing the correlated subquery with the window-function version helped me understand that different SQL approaches can produce similar results but have different plans and complexity.

## What Was Difficult?

The most difficult part was understanding `EXPLAIN QUERY PLAN` and why SQLite sometimes chooses one approach instead of another.

The window-function query was also difficult because the execution plan was more complicated. Understanding indexes and why one index could make a query slower also took some time.

## Struggling and Exploration

I explored different indexes and measured their performance instead of assuming that an index would always improve the query.

One interesting result was that an index changed the execution plan but made the dashboard query slower. This showed me that database optimization is not simply about adding more indexes.

I also tested SQL injection using the payload:

`' OR '1'='1`

and then compared the vulnerable query with the safe version using a bound parameter.

## Interaction with Peers

I discussed the SQL tasks and problems with my group. Comparing our ideas helped me understand complex SQL concepts and execution plans more clearly.

When I was unsure about something, discussing it with others helped me find a better way to test and verify the result.

## Help and Extra Work

I spent extra time testing SQL queries, checking execution plans, benchmarking indexes, and testing the SQL injection example.

I also documented the results in my portfolio, including the query plans, benchmark results, relational algebra, and SQL notes.

## Overall Reflection

Module03 taught me that writing correct SQL is only one part of database work. I also need to consider performance, security, and verification.

The most important lesson I want to remember is: “Do not trust the query just because it gives an answer. Check the result, the execution plan, and the performance.”