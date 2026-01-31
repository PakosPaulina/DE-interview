# What is Databricks and how does it differ from Apache Spark?
Databricks is a unified data analytics platform built on Apache Spark that provides additional features like collaborative notebooks, managed clusters, optimized runtime, Delta Lake, and native integrations to simplify data engineering, data science, and ML workflows.

# Explain the Databricks Delta Lake architecture.
Delta Lake is an open-source storage layer on top of data lakes that supports ACID transactions, schema enforcement, time travel, and more. It enables reliable data pipelines and simplifies batch/streaming unification.

# What are the advantages of Delta Lake over traditional data lakes?
- ACID transactions
- Schema enforcement prevents dirty data ("RESTORE TABLE table_name TO VERSION AS OF 123")
- Time travel enables rollback and historical queries
- Upserts and deletes supported in batch/stream
- Optimized data files with Z-Ordering for faster queries

# How does the Databricks Runtime differ from open-source Apache Spark?
Databricks Runtime is a proprietary, optimized build of Apache Spark that includes performance improvements, additional libraries, and deeper integration with the Databricks platform. While it is fully compatible with standard Spark APIs, it adds optimizations such as faster I/O connectors to cloud storage, improved query planning, better autoscaling behaviour, and built-in support for Delta Lake.

In newer runtimes it can also leverage Photon, a native execution engine that accelerates many SQL and DataFrame operations. In practice this means the same Spark code often runs noticeably faster and more reliably on Databricks Runtime than on vanilla open-source Spark.

# What is Photon and when does it improve performance?
Photon is a native (C++), vectorized execution engine used by Databricks to accelerate SQL and DataFrame workloads. Instead of relying purely on the JVM like standard Spark, Photon executes many operators (scans, filters, joins, aggregations) in highly optimised native code.

It provides the biggest gains for:
- SQL queries
- DataFrame transformations
- Large joins and aggregations on Parquet/Delta data

It does not significantly accelerate:

- RDD-based code
- Heavy Python UDF usage

So to benefit from Photon you generally stick to Spark SQL and built-in DataFrame functions rather than custom Python logic.

# Why is it better to run Spark native functions rather than python UDFs
In Databricks (and Spark in general) there are two very different ways your code can run:

- Spark native functions (built-in SQL/DataFrame functions)
- Python UDFs (your own Python code applied row by row)

Native Spark functions run inside Spark’s execution engine on the JVM (and often inside Photon’s native C++ engine on Databricks). Python UDFs run in a separate Python process and Spark has to ship data back and forth between the JVM and Python for every batch of rows.

That difference is why native functions are almost always better.

Performance:
Native functions are vectorised and operate on whole columns at once. Spark can optimise them, fuse multiple operations together, and run them very efficiently in parallel.

A Python UDF is essentially a black box that Spark must call like:
“for each row, send data to Python, run this function, send the result back”.

That extra serialisation and cross-process communication is expensive and becomes a major bottleneck on large datasets.

# Explain the medallion architecture (bronze, silver, gold)
The medallion architecture is a layered data design pattern used to progressively improve data quality and structure.

Bronze contains raw ingested data exactly as received from the source. It is append-only and preserves history for traceability and reprocessing.

Silver contains cleaned and standardised data. Typical operations here are deduplication, type casting, basic validation, flattening nested fields, and applying business keys such as isCurrent flags for slowly changing dimensions.

Gold contains curated, business-ready datasets optimised for analytics and reporting. This layer applies business logic, aggregations, and joins across domains to create fact and dimension tables or feature tables.

This separation improves reliability and reusability because you can always rebuild higher layers from lower ones without going back to the original source.

# How does Databricks handle concurrent writes to the same Delta table?

Delta Lake uses optimistic concurrency control. Each write operation reads the current table version, writes new data files, and then attempts to commit a new version to the transaction log.

If another writer has committed changes in the meantime that conflict with the same data, the commit fails instead of corrupting the table. The job must then retry using the newer table version.

This guarantees ACID properties: readers always see a consistent snapshot and writers never leave the table in a partially updated state.

# What is the Delta transaction log?

The Delta transaction log is a series of JSON and checkpoint files stored alongside the table in the _delta_log folder. It records every change made to the table.

Each commit contains metadata such as:

- which data files were added or removed
- schema and table properties
- operation type (append, merge, delete, etc.)

Readers reconstruct the current state of the table by replaying this log. Because each commit is atomic, the table always has a well-defined version history, which enables ACID transactions and time travel.

# When and why would you run OPTIMIZE on a Delta table?
OPTIMIZE compacts many small data files into fewer larger files. This reduces metadata overhead and improves query performance because Spark has fewer files to open and scan.

"OPTIMIZE my_catalog.my_schema.my_table;"

Small files commonly appear after frequent incremental writes or streaming ingestion. Running OPTIMIZE periodically keeps file sizes in an efficient range (often around hundreds of MB), which speeds up both reads and writes.

OPTIMIZE can optionally be combined with ZORDER to also improve data skipping for specific query columns.

# What is Z-ORDER and how is it different from partitioning?
Partitioning splits data into separate folders based on a column (for example date=2026-01-31). Queries that filter on the partition column can skip entire folders.

"OPTIMIZE my_catalog.my_schema.my_table
ZORDER BY (country, event_type);"

Z-ORDER does not create new partitions. Instead, it physically clusters related values together inside the existing files. This improves data skipping for columns that are frequently filtered but are not good partition keys (for example high-cardinality IDs).

In short:

- Partitioning = coarse folder-level pruning
- Z-ORDER = fine-grained clustering inside files

They are often used together.

# What is Liquid Clustering in Delta Lake?
Liquid Clustering is a Delta Lake feature that allows you to define clustering columns without being locked into a fixed physical partitioning scheme. Unlike traditional partitioning, where data is permanently laid out in folders based on a partition column, liquid clustering lets Databricks continuously reorganise data in the background to keep related rows close together.

This means you can change or refine your clustering strategy over time without rewriting the entire table. As new data is written and maintenance operations like OPTIMIZE run, Delta incrementally reclusters the data based on the defined clustering columns.

The benefits are:
- Better query performance through improved data skipping
- No risk of creating millions of tiny partitions from high-cardinality columns
- Flexibility to evolve clustering as query patterns change

In practice, liquid clustering replaces many traditional partitioning use cases. You typically avoid hard partitions except for very coarse filters like date, and rely on liquid clustering for frequently filtered columns such as IDs or categories.

# What is Auto Loader?
Auto Loader is a Databricks feature for incremental file ingestion from cloud object storage. Instead of scanning the entire directory each time, it tracks which files have already been processed using a checkpoint.

It can automatically infer and evolve schemas and is designed to handle very large and continuously growing directories efficiently.

This makes it ideal for building streaming or micro-batch bronze ingestion pipelines without reprocessing old files.

# Can batch and streaming workloads write to the same Delta table?
Yes. Because Delta Lake provides ACID transactions and snapshot isolation, both batch and streaming jobs can safely write to the same table.

Each write creates a new committed version in the transaction log. Readers always see a consistent snapshot, and concurrent writers do not corrupt each other’s results.

This enables patterns like:
- continuous streaming ingestion into bronze
- periodic batch upserts into silver or gold

on the same underlying Delta tables.

# What is Unity Catalog and why is it important?
Unity Catalog is Databricks’ centralised governance layer for data and AI assets. It provides a unified metastore across workspaces with fine-grained permissions on catalogs, schemas, tables, views, and even columns.

It also enables features like data lineage, auditing, and consistent access control regardless of which cluster or notebook is used.

Instead of managing permissions at the raw storage (S3/ADLS) level, you manage them at the data object level, which is safer and easier to reason about for analytics use cases.

# How would you debug a slow Spark job in Databricks?
You would start with the Spark UI to identify the slow stages. Key things to inspect are:
- task duration and skew (some tasks much slower than others)
- shuffle read/write sizes
- number of partitions and file sizes
- whether joins are causing large shuffles

Common fixes include:
- repartitioning data to avoid skew
- using broadcast joins for small dimension tables
- reducing small files via OPTIMIZE
- voiding Python UDFs in favour of built-in functions

The goal is to minimise shuffles and ensure work is evenly distributed across executors.

# How can you make a pipeline idempotent in Databricks?
An idempotent pipeline can be safely rerun without creating duplicates or corrupting data.

In Databricks this is typically achieved by:
- using deterministic keys
- writing with MERGE INTO (upserts) instead of blind appends
- avoiding in-place updates of files
- committing results atomically to Delta tables

If the same input is processed twice, the MERGE will match existing rows and update them rather than inserting duplicates, so the final table state is correct no matter how many retries occur.

# What types of clusters are available in Databricks and when would you use them?
Databricks provides two main Spark cluster types and a separate compute type for SQL:

All-purpose clusters are interactive, shared clusters used for development and exploration. Multiple users can attach notebooks to the same cluster, making them convenient for ad hoc analysis and collaborative work. They stay running until manually terminated (or auto-terminated after idle time), so they are less cost-efficient for scheduled production jobs but great for day-to-day development.

Job clusters are ephemeral clusters created specifically for a job run and terminated automatically when the job finishes. Each run gets a fresh environment, which improves isolation, reproducibility, and cost control. They are the recommended choice for production pipelines and scheduled ETL because you only pay while the job is actually running.

SQL warehouses (formerly SQL endpoints) are specialised compute for SQL analytics and BI workloads. They are optimised for low-latency, high-concurrency queries from dashboards and external BI tools using JDBC/ODBC. They scale independently from Spark clusters and are typically used for serving gold-layer data to analysts rather than for heavy data transformations.

# What is Delta Live Tables (DLT) / Lakeflow Declarative Pipelines in Databricks?
Delta Live Tables is a declarative framework for building reliable data pipelines on Databricks. Instead of writing imperative ETL code that manually creates and updates tables, you define tables and transformations using SQL or Python decorators, and Databricks manages execution, dependencies, retries, and quality checks.

DLT automatically handles orchestration, incremental processing, schema enforcement, and data quality rules. It stores all outputs as Delta tables and maintains a pipeline graph so tables are built in the correct order based on their dependencies.

This reduces boilerplate ETL code and makes pipelines more reliable and maintainable.

# How does DLT handle incremental processing?
DLT processes data incrementally by default when reading from streaming sources or using the APPLY CHANGES INTO pattern. It keeps track of what data has already been processed using checkpoints and Delta transaction logs.

When new files or records arrive, only the new data is processed and appended or merged into the target tables. This avoids reprocessing the entire dataset and makes pipelines efficient for continuously arriving data.

# What are “live tables” and “streaming tables” in DLT?
A live table is a managed Delta table defined as part of the pipeline. It is updated automatically whenever the pipeline runs.

A streaming table is a special type of live table that continuously ingests new data from a streaming source (for example cloud storage using Auto Loader). It uses Structured Streaming under the hood and updates the target table incrementally as new data arrives.

Both end up as Delta tables, but streaming tables are continuously updated whereas batch live tables are recomputed per pipeline run.

# How do you enforce data quality in DLT?
DLT provides built-in expectations (data quality rules) that can be declared as part of the table definition.

You can define rules such as “column A must not be null” or “value must be greater than zero” and choose what happens when a record violates the rule:
- drop the bad record
- fail the pipeline
- just log the violation

DLT tracks expectation metrics so you can monitor data quality over time without writing custom validation logic.

# What is the difference between DLT and a normal Databricks job with notebooks?
A normal job requires you to manually orchestrate notebook execution order, handle retries, manage checkpoints, and implement data quality checks yourself.

DLT pipelines are declarative. You define the end state (tables and transformations) and Databricks automatically:
- builds the dependency graph
- runs steps in the correct order
- manages state and checkpoints
- applies quality rules
- provides built-in monitoring UI

DLT is opinionated and managed, while normal jobs are more flexible but require more manual engineering.

# What is Spark Structured Streaming?
Spark Structured Streaming is a high-level API for processing streaming data using the same DataFrame and SQL abstractions as batch Spark.

You write queries as if you were processing a static table, and Spark executes them incrementally on new data as it arrives. Internally it uses micro-batches and maintains state and checkpoints to guarantee correct results.

This allows unified batch and streaming logic using the same code patterns.

# What is a micro-batch in Structured Streaming?
A micro-batch is a small batch of new data processed at regular intervals. Instead of processing each record individually, Spark groups new records into small batches and runs the query on each batch.

This approach simplifies fault tolerance and allows Spark to reuse its batch execution engine while still providing near real-time processing.

# What is a checkpoint in Structured Streaming?
A checkpoint is a location in durable storage where Spark saves progress and state information such as offsets, processed files, and aggregation state.

If the job fails or restarts, Spark reads the checkpoint and continues from where it left off instead of reprocessing all data. This is what enables fault tolerance and exactly-once processing semantics when used with Delta Lake.

# What output modes are available in Structured Streaming?
- Append mode writes only new rows to the output.
- Update mode writes only rows that changed since the last trigger (used for aggregations that evolve over time).
- Complete mode rewrites the entire result table on every trigger (used for full aggregations, but can be expensive for large outputs).

The choice depends on the type of query and downstream requirements.

# How does Structured Streaming guarantee exactly-once processing with Delta Lake?
Spark tracks processed data using checkpoints and writes results using Delta Lake transactions.

Each micro-batch is committed atomically to the Delta table. If a failure happens before commit, the batch is retried. If it fails after commit, the checkpoint ensures it is not processed again.

This combination of checkpointing and Delta’s ACID transactions ensures each input record affects the output exactly once.

# What is watermarking in Structured Streaming?
Watermarking is a way to handle late arriving data in event-time aggregations.

You define how late data is allowed to arrive (for example 10 minutes). Spark keeps state for that window and will update results if late data arrives within the watermark. Data arriving later than the watermark is dropped to prevent unbounded state growth.

This balances correctness with memory usage.

# How do DLT and Structured Streaming work together?
DLT can use Structured Streaming as the execution engine for streaming tables. When you define a streaming live table from a streaming source, DLT manages the streaming query, checkpoints, and fault tolerance automatically.

This means you get continuous ingestion and transformation without manually writing writeStream, triggers, or checkpoint logic.

# When would you choose DLT over hand-written Structured Streaming jobs?
Choose DLT when you want:
- managed orchestration
- built-in data quality checks
- simpler incremental pipelines
- less operational overhead

Choose hand-written Structured Streaming when you need:
- very custom streaming logic
- fine-grained control over triggers and sinks
- non-Delta or specialised outputs

In many enterprise ETL pipelines, DLT is preferred for maintainability and reliability, while raw Structured Streaming is used for advanced or highly custom streaming applications.