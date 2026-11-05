# Module02 Reflection

## My Take-away

Module02 taught me how to examine an existing database and find problems in its design. I learned that a database can work even when it has missing keys, incorrect relationships, duplicate data, or poor data types.

My main take-away is "do not trust a database just because it works.” I learned to use SQL queries to prove problems instead of relying only on assumptions.

I also learned about entities, attributes, relationships, cardinality, natural keys, and surrogate keys. Creating a Pydantic and SQLAlchemy data contract helped me connect database design with application code.

## What Was Good?

I liked working with the deliberately flawed `legacy.db` because it gave me practical experience. I found problems such as duplicate `P-1003`, a maintenance job referring to a non-existing machine, and `unit_price` stored as text.

These examples helped me understand why proper database constraints and relationships are important.

## What Was Difficult?

Understanding cardinality, keys, normalization, and the difference between an entity and a relationship was difficult at first.

Creating the Pydantic and SQLAlchemy contract was also new to me. I needed some time to understand how the database structure could be represented in Python.

## Struggling and Exploration

During the pod study in class, we discussed the concepts in our group and shared our ideas. When we were unsure about something, we discussed it with the professor. This helped me understand the difficult concepts better.

One interesting example was `parts_used`, where multiple parts were stored in one text field. I learned that although this may look convenient, it creates problems for database design and relationships.

## Interaction with Peers and Instructor

Working with my group was very helpful. We discussed the tasks, compared our ideas, and helped each other understand difficult concepts.

The discussions with the professor were also valuable because I could ask questions and get clarification when my group was unsure.

## Help and Extra Work

My group helped me during the pod study by discussing the concepts and sharing ideas. The professor also helped clarify difficult points.

I spent extra time testing SQL queries against `legacy.db` to make sure the problems I found were actually present. I also created the Pydantic/SQLAlchemy contract and worked on the ER/EER modelling tasks.

## Overall Reflection

Module02 changed how I look at database design. I now understand that a good database needs clear relationships, correct keys, suitable data types, and integrity constraints.

The biggest lesson I learned is: A database should not only work; its structure and data should also make sense.

The combination of group discussion, professor feedback, and practical SQL work helped me understand the concepts better.