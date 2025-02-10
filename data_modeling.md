# What are fact, dimension and aggregate tables?

* Fact Tables store measurable, numerical data such as sales, revenue, or transactions. They contain foreign keys that link to dimension tables.
* Dimension Tables store descriptive attributes about facts, such as product names, customer details, or locations. They provide context for fact tables.
* Aggregate Tables store precomputed summary data (e.g., total sales per month), improving query performance by reducing computations on raw fact tables.

# How do you approach data modelling as a data engineer?

1. Understand Business and Data Requirements
- Work closely with analysts, data scientists, and business stakeholders to understand what insights or applications the data needs to support.
- Identify data sources (databases, APIs, files, streaming data).
- Determine if the model should support real-time analytics, batch processing, or machine learning workflows.

2. Choose the Right Data Model Type
Data engineers typically work with three main types of data models:

- Relational (Normalized) Model – Ideal for OLTP (transactional) systems to avoid redundancy. Used in source databases before ETL processing.
- Dimensional Model – Used for OLAP (analytical) systems like data warehouses. It includes fact and dimension tables (e.g., Star or Snowflake Schema).
- Data Lake / Semi-Structured Model – Used for big data processing in data lakes. This includes Parquet, JSON, or Avro formats with schema-on-read.

3. Select an Appropriate Storage Solution

- Traditional Databases: PostgreSQL, MySQL for small structured datasets.
- Cloud Data Warehouses: Snowflake, BigQuery, Redshift for analytical workloads.
- Data Lakes: AWS S3, Azure Data Lake, or Google Cloud Storage for raw and semi-structured data.
- Lakehouse Solutions: Databricks (Delta Lake) for combining data lake flexibility with warehouse-style transactions.

4. Define Data Schemas and Table Structures
For OLTP (Transactional Databases): Use normalized schemas to avoid redundancy.
For OLAP (Analytical Databases): Use Star Schema (denormalized) or Snowflake Schema for performance.
For Data Lakes: Define partitioning strategies and use columnar file formats like Parquet for efficient querying.

5. Handle Slowly Changing Dimensions (SCDs) Correctly
If tracking changes in customer attributes (e.g., address, membership level), decide on the SCD type (Type 1, 2, or 3).
Use versioning columns (Start_Date, End_Date) or history tables to retain historical records.

6. Optimize for Query Performance
- Use indexes on frequently filtered columns.
- Apply partitioning (by date, region, or category) for large tables.
- Use clustering in Snowflake, or Z-Ordering in Databricks to speed up queries.
- Implement materialized views or aggregate tables for precomputed summaries.

7. Ensure Data Quality and Integrity
- Define primary and foreign keys to enforce relationships.
- Use constraints (e.g., NOT NULL, UNIQUE) to prevent data inconsistencies.
- Implement data validation checks during ETL using tools like dbt, Great Expectations, or Apache Deequ.

8. Document Everything
- Maintain ER diagrams and data dictionaries so teams understand relationships.
- Use metadata management tools (e.g., DataHub, Amundsen, or Apache Atlas) for tracking lineage.

9. Monitor and Maintain Data Pipelines
- Set up alerting for pipeline failures (e.g., using Airflow or Datadog).
- Track query performance and optimize storage to prevent cost overruns.
- Regularly reprocess historical data if schema changes or data inconsistencies occur.

# What is a star schema vs a snowflake schema?

* Star Schema: The fact table is at the center, and dimension tables directly connect to it. It is simple and fast for queries but may contain data redundancy.
* Snowflake Schema: Dimension tables are normalized into sub-tables to remove redundancy, improving storage efficiency but making queries more complex.
Example:

* In Star Schema, a Product table has all product details.
* In Snowflake Schema, Product is split into separate Category and Brand tables.

Star Schema is better for performance, while Snowflake Schema is better for storage efficiency.

# What is data normalization and 3rd normal form?

Data normalization is the process of structuring a database to eliminate redundancy and ensure data integrity.

1st Normal Form (1NF): Remove duplicate rows and ensure atomic values (no multiple values in a single column).
2nd Normal Form (2NF): Remove partial dependencies (every column must depend on the entire primary key, not just part of it).
3rd Normal Form (3NF): Remove transitive dependencies (non-key columns must depend only on the primary key, not on other non-key columns).
Example of 3NF: Instead of storing Customer_ID, Customer_Name, Region_Name in a sales table, we separate Region_Name into a Region table linked by Region_ID.

# Describe and efficient table design such as cumulative

Cumulative tables store pre-aggregated historical data to speed up queries. Instead of recalculating metrics on raw transactional data, cumulative tables store running totals.

Example: Instead of querying daily sales and summing them up for reports, a cumulative table stores Total Sales Until Date, reducing computation overhead.

Techniques for efficient table design:

Partitioning: Divide large tables by date or category for faster access.
Indexing: Use indexes on frequently queried columns for better lookup performance.
Denormalization: Store pre-joined data for reporting speed when query performance matters more than storage.

# Explain these complex data types like MAP, ARRAY, STRUCT

These are nested data types used in databases like Hive, Spark, and BigQuery for handling semi-structured data.

ARRAY: Stores an ordered list of values, useful for handling multiple values in a single field.

Example: ['Red', 'Blue', 'Green'] in a Color column.
MAP: Stores key-value pairs, similar to a dictionary in Python.

Example: {'size': 'L', 'color': 'Blue'} for storing product attributes.
STRUCT: Groups multiple fields into a single column, similar to a nested JSON object.

Example: {"Address": {"Street": "123 Main St", "City": "NYC"}} in a single column.
These types are useful for handling JSON-like data in modern analytical databases.