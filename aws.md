# How is Amazon S3 used as a data lake?
Amazon S3 is commonly used as a data lake because it provides highly durable, scalable, and low-cost object storage that can store structured, semi-structured, and unstructured data. In a data lake setup, S3 acts as the system of record where raw and processed data is stored, while compute engines like Glue, EMR, Athena, or Redshift Spectrum read from and write to it. Storage and compute are decoupled, allowing independent scaling and cost control.

# What are best practices for S3 folder (prefix) structure in a data lake?
S3 folder structures should be logical, consistent, and optimised for query performance. A common best practice is to organise data by domain and processing stage (for example bronze, silver, gold), followed by dataset name and partitions such as date. Shallow, predictable prefixes make data easier to discover and manage, while avoiding overly nested or ad-hoc folder structures reduces operational complexity and query errors.

# Why is partitioning important in a data lake?
Partitioning improves query performance and cost efficiency by limiting how much data is scanned during reads. By partitioning data on commonly filtered columns such as date or region, query engines can skip irrelevant files entirely. Good partitioning reduces I/O, speeds up queries, and lowers costs for engines that charge per data scanned, such as Athena.

# How do you decide what to partition data on?
Partition keys should align with common query filters and have reasonable cardinality. Time-based partitions (for example by day or month) are the most common because they support incremental loads and time-bounded queries. High-cardinality columns should generally be avoided as partition keys because they create many small partitions and hurt performance.

# What is the difference between EMR and Databricks on AWS?
Amazon EMR is a managed service for running open-source big data frameworks like Spark and Hadoop, where the user is responsible for cluster configuration, tuning, and lifecycle management. Databricks is a higher-level managed platform built on Spark that provides optimised runtimes, collaborative notebooks, Delta Lake, and simplified cluster management. EMR offers more control and flexibility, while Databricks prioritises productivity, performance optimisations, and ease of use.

# What is AWS Glue and what are its main components?
AWS Glue is a serverless data integration service. Its two main components are the Glue Data Catalog and Glue Jobs. The Data Catalog stores metadata about datasets such as schemas and locations in S3 and is used by services like Athena and Redshift Spectrum. Glue Jobs are serverless Spark jobs used to perform ETL transformations and load data into or out of S3 and other systems.

# How does the Glue Data Catalog fit into an AWS data lake?
The Glue Data Catalog acts as a central metastore for the data lake. It defines tables, schemas, and partitions that point to data stored in S3. Query engines like Athena and Spark use the catalog to understand how to read the underlying files, enabling schema-on-read and consistent metadata across services.

# How does IAM control who can read and write data in S3?
IAM controls access through policies that define which users, roles, or services can perform actions like read, write, or delete on specific S3 buckets or prefixes. In data engineering, IAM roles are commonly attached to services like Glue or EMR so jobs can access only the data they need. Least-privilege access is a best practice to reduce security risk.

# What are common cost considerations when building a data lake on AWS?
Costs mainly come from storage, data scanning, compute, and data transfer. Poor partitioning or file layout can significantly increase query costs in Athena. Long-running or oversized clusters increase EMR or Glue costs. Managing file sizes, partitioning properly, and using lifecycle policies to move old data to cheaper storage tiers are key strategies for controlling cost at scale.

# How do you handle logging and error monitoring in AWS data pipelines?
Most AWS data services integrate with CloudWatch for logging and metrics. Glue and EMR jobs write execution logs to CloudWatch Logs, where failures and performance issues can be inspected. Metrics and alarms can be set up to detect job failures, long runtimes, or repeated retries. Centralised logging and alerting are essential for operating reliable pipelines at scale.