# When to Use Which Database?

## Use NoSQL When

- The data is unstructured and requires a flexible schema.

  **Examples:**

  - Reviews and recommendations in an e-commerce application

- You need high availability, scalability (storing large amounts of data that do not fit on one server), and low latency. NoSQL supports these requirements through horizontal scaling and sharding.

  **Examples:**

  - Posts, likes, comments, and messages in a social media application
  - Large amounts of real-time data, such as driver locations in a delivery application

## Use SQL When

- The data is structured and has a fixed schema.

  **Examples:**

  - Customer account tables in an e-commerce application

- You need data integrity and consistency. SQL databases support these requirements through ACID properties.

  **Examples:**

  - Financial transactions and account balances in a banking application
  - Orders and payments in an e-commerce application
  - Stock-trading platforms

- You need to perform complex queries, joins, and aggregations. These operations are commonly required for data analytics, so store the relevant data in a SQL database.
