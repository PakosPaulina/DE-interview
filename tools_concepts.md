# What is ETL? Explain its phases and tools you have worked with
ETL stands for Extract, Transform, Load, a process used to move, clean, and load data from multiple sources into a data warehouse or analytics system.

* Extraction sources:
✅ Databases (SQL Server, PostgreSQL, MySQL)
✅ APIs (REST, SOAP)
✅ Flat Files (CSV, JSON, XML)
✅ Cloud Storage (AWS S3, Google Cloud Storage)
✅ Web Scraping

* Transform stage:
This stage converts raw data into a structured, usable format by performing:
✅ Cleaning (Handling NULLs, removing duplicates)
✅ Standardization (Converting formats, e.g., date formats)
✅ Deduplication (Removing redundant data)
✅ Aggregation (Summing sales, averaging prices)
✅ Business Logic Application (Currency conversion, category mapping)

Loading Stage:
The final step loads the transformed data into a data warehouse like Snowflake, Redshift, BigQuery, or Databricks.

✅ Full Load – First-time data insertion
✅ Incremental Load – Only new or changed records

# Whats the difference between ETL and ELT, use cases
ETL (Extract → Transform → Load)
- Transformation happens before loading
- Best for structured data warehouses

Works best for: relational databases, strict regulatory environments (like GDPR), when a data transformation is complex and must be done before loading and when working with smaller, structured datasets

ELT (Extract → Load → Transform)
- Data is loaded first, then transformed inside the warehouse
- Used in modern cloud-based warehouses like Snowflake & BigQuery

Works best for: when using cloud-based warehouses, when dealing with large, unstructured data (JSON, logs, IoT data), when raw data needs to be stored for later processing, for ML and & AI workloads

# What is the difference between batch processing and stream processing?

Batch processing handles data in large, scheduled chunks, while stream processing handles data continuously in real time. Batch processing is best for historical analysis, reports, and ETL workflows that do not require immediate updates. Stream processing is used when low latency is essential, such as fraud detection, stock market tracking, and IoT sensor monitoring.

# Describe how you would design a data pipeline for processing real-time data?

A real-time data pipeline starts with a data ingestion layer, using tools like Apache Kafka or AWS Kinesis to collect and buffer incoming data. The data is then processed using stream processing frameworks such as Apache Flink, Spark Streaming, or AWS Lambda, which clean, enrich, and analyze the data. The processed data is stored in a fast, queryable database such as Apache Druid, ClickHouse, or Elasticsearch. Finally, a visualization tool like Grafana or Tableau is used to monitor real-time trends.

For example, in a real-time fraud detection system, bank transactions flow into Kafka, a Flink job detects suspicious patterns, and flagged transactions are sent to an alert system in under a second.

# How do you monitor and maintain data pipelines?

Monitoring involves setting up logging, alerting, and performance tracking for each pipeline stage. Logs and metrics can be collected using tools like Prometheus, Datadog, or AWS CloudWatch. Alerts can be configured to notify engineers when a job fails, runs longer than expected, or produces unexpected results.

Maintaining pipelines requires handling failures with retries, detecting schema changes to prevent breakages, and automating testing using tools like Great Expectations. Version control with Git helps track changes and rollback issues when needed.

For example, in Apache Airflow, you can set up retry logic for a failing job and send an email alert if it still fails after multiple attempts.

# What is the role of Apache Kafka in data engineering?

Apache Kafka is a real-time event streaming platform that acts as a central hub for data movement between systems. It ensures fault tolerance, scalability, and low-latency processing of high-volume event data.

Kafka is commonly used for real-time data pipelines where data producers (like web apps, IoT devices, or databases) send events to Kafka topics. Consumers (such as Spark Streaming or Flink) process these events for analytics, monitoring, or machine learning applications.

For example, in ride-hailing applications, Kafka can capture real-time trip updates from drivers and update customer apps instantly.

# How do you ensure data quality during ETL processes?

Ensuring data quality involves validating, cleaning, and monitoring data before, during, and after processing. Validation checks for missing, duplicate, or incorrectly formatted data before loading it into the system. Schema enforcement ensures data types and structures remain consistent.

Automated data quality frameworks like Great Expectations and dbt can catch data inconsistencies early. Anomaly detection techniques, such as statistical checks or machine learning models, help flag unusual patterns.

For example, before loading a customer dataset into a warehouse, an ETL pipeline might check for missing emails and enforce a rule that customer IDs must be unique.

# What is the difference between OLAP and OLTP databases?

OLAP (Online Analytical Processing) and OLTP (Online Transaction Processing) serve different purposes in data systems.

OLTP databases are optimized for handling fast, real-time transactions, such as processing e-commerce purchases or banking transactions. They use normalized schemas to minimize data redundancy and ensure high concurrency.

OLAP databases are designed for analytical queries on large datasets. They aggregate and process historical data for reporting and business intelligence. OLAP systems often use denormalized schemas, like star or snowflake schemas, to optimize query performance.

For example, an OLTP system might handle a customer's order placement, while an OLAP system would generate a report analyzing monthly sales trends.

# Describe the architecture of a cloud-based data warehouse like Snowflake or BigQuery.

Cloud data warehouses like Snowflake and BigQuery follow a decoupled architecture where storage and compute resources are separate, allowing them to scale independently.

* Storage Layer: Stores structured and semi-structured data in a columnar format, enabling efficient querying and compression.
* Compute Layer: Handles query execution using distributed computing. In Snowflake, this is called a Virtual Warehouse, while BigQuery relies on Google's Dremel execution engine.
* Query Engine: Uses SQL to process queries across large datasets with automatic scaling and optimization.
* Caching & Optimization: Both systems cache query results to speed up repeated queries and optimize resource usage.

For example, in Snowflake, data is stored in cloud object storage, and queries run in compute clusters that can be dynamically resized without affecting data storage.

# How do you handle schema changes in an ETL pipeline

Schema changes, such as adding, removing, or renaming columns, can break an ETL pipeline if not handled properly. Strategies for managing schema evolution include:

* Schema Detection: Use schema inference tools like dbt or Great Expectations to track changes before they impact the pipeline.
* Backward Compatibility: Ensure new columns do not break existing queries by making updates optional before enforcing changes.
* Versioned Schemas: Store historical schema versions to allow gradual migration.
* Automated Testing: Implement tests to detect unexpected schema changes before deployment.

For example, if a new column is added to a customer dataset, the ETL job can be updated to populate it without failing for existing records.

# What is spilling to disk mean in distributed compute?

"Spilling to disk" occurs when a distributed computing system runs out of memory (RAM) and must temporarily store data on disk to complete a computation. This happens when processing large datasets that exceed available memory.

Why It Happens? Queries or transformations that require large joins, aggregations, or sorting can exceed available memory.
Performance Impact? Disk operations are significantly slower than in-memory processing, leading to performance bottlenecks.
How to Prevent It? Optimizations like increasing cluster memory, partitioning data, and using efficient file formats like Parquet can reduce the need for spilling.
For example, in Apache Spark, if a large groupBy operation exceeds available memory, intermediate results are written to disk, slowing down the job.