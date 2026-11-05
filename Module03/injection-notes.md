# Module03 Task 3 — The Injection Drill

## Payload Used

The SQL injection payload was:

```text
' OR '1'='1
```

## Output

```text
normal   : [(1, 'Customer 1')]
injected : [(1, 'Customer 1'), (2, 'Customer 2'), (3, 'Customer 3')] ...
safe     : []
```

## Explanation

The vulnerable query builds the SQL statement by directly inserting the user's input into the SQL string. Therefore, the payload `' OR '1'='1` changes the meaning of the SQL condition. Instead of searching for one specific customer, the condition becomes true for all rows.

Escaping or filtering apostrophes by hand is not a reliable security fix. It is easy to miss different SQL contexts, such as identifiers, numeric values, encodings, or other special cases. The application would have to correctly understand and escape the input for every possible SQL context.

Bound parameters are the correct fix because the database receives the SQL statement and the user input separately. The database treats the parameter value as data rather than as part of the SQL command. Therefore, the payload cannot change the meaning of the query.

In this test, the vulnerable query returned customer records, while the parameterized query returned an empty result:

```text
safe     : []
```

This demonstrates why parameterized queries should be used instead of building SQL statements with user input.