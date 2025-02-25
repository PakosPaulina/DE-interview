# What is Apache Spark, and how does it compare to Hadoop? 

Apache Spark is a distributed computing framework for big data processing and analytics. It is designed for speed, ease of use, and in-memory processing, making it much faster than Hadoop’s MapReduce.

Key differences between Spark and Hadoop:
- Speed: Spark processes data 100x faster than Hadoop because it uses in-memory computation, while Hadoop writes intermediate data to disk.
- Ease of Use: Spark supports SQL, Python, Scala, Java, and R, while Hadoop requires writing low-level MapReduce programs.
- Processing Model: Spark supports batch, streaming, ML, and graph processing, while Hadoop is mainly batch-oriented.
Hadoop is better for cheap, large-scale storage (HDFS), while Spark is better for real-time and iterative computations.

# How does Apache Spark handle big data processing?

Apache Spark processes big data using a distributed computing framework that follows a resilient distributed dataset (RDD) model.

How It Works:
- Parallel Processing: Data is split into partitions and processed across multiple worker nodes.
- Lazy Evaluation: Transformations are not executed immediately, optimizing execution plans before running.
- In-Memory Computation: Unlike Hadoop MapReduce, Spark caches intermediate data in memory for faster processing.
- Fault Tolerance: If a worker node fails, Spark can recompute lost data using lineage information.

# How does Apache Spark differ from PySpark?

* Apache Spark is the big data processing engine written in Scala and Java, running on distributed clusters.
* PySpark is the Python API for Apache Spark, allowing developers to use Spark's power with Python.
* PySpark provides Python-based DataFrame APIs, ML libraries (MLlib), and streaming support, making Spark accessible to Python developers.

# Explain the difference between RDD (Resilient Distributed Dataset), DataFrame and DataSet in PySpark

In Spark, there are three main types of data structures that are commonly used: RDD, DataFrame, and Dataset. Each of these structures has its own unique characteristics and purposes, making them suitable for different scenarios.

* RDD (Resilient Distributed Dataset):

- The low-level data structure in Spark.
- Immutable, distributed collection of objects.
- Requires manual transformations (map, filter, reduce).
- Less optimized compared to DataFrames.

* DataFrame:

- A distributed, tabular structure similar to Pandas DataFrames.
- Uses schema-based processing (columns have names & types).
- More optimized with Catalyst Optimizer for SQL-like queries.
- Easier to use with select, filter, groupBy functions.

* Dataset (only available in Scala/Java, not PySpark):

- A type-safe version of DataFrames with strong typing. Type-safe meaning compiler checks data types before execution which prevents errors like wrong column access or incorrect transformations, which might otherwise cause runtime failures.
- Not used in PySpark, since Python is dynamically typed.

* You would typically use DataFrames for most tasks in PySpark. 
* DataFrames are best for structured data and SQL-like operations, while RDDs are more flexible and performant for distributed computing environments.
* Datasets offer a balance between the two, with support for both structured data and distributed computing, making them suitable for a wide range of use cases.

# How do you create a Spark Session in PySpark?

```
    from pyspark.sql import SparkSession

    # Create a Spark Session
    spark = SparkSession.builder \
        .appName("MySparkApp") \
        .getOrCreate()
```
# What are the advantages of using PySpark over traditional Python libraries like Pandas?

* Scalability – PySpark can process terabytes of data across multiple machines, while Pandas is limited to a single machine's memory.
* Speed – PySpark uses in-memory distributed computing, making it significantly faster for large datasets compared to Pandas, which processes data in a single thread.
* Distributed Computing – PySpark runs on clusters using Spark’s execution engine, allowing parallel processing, whereas Pandas operates on a single machine.
* Integration with Big Data Ecosystem – PySpark works seamlessly with Hadoop, Hive, HDFS, and cloud storage solutions, whereas Pandas is primarily used for local data processing.
* Support for Streaming and Machine Learning – PySpark includes built-in libraries for real-time data processing (Structured Streaming) and machine learning (MLlib), which Pandas lacks.
* SQL Support – PySpark DataFrames allow SQL-like querying with Spark SQL, making it easier to work with structured data.

# Explain lazy evaluation in PySpark

Lazy evaluation means that Spark does not execute transformations immediately when they are called. Instead, it builds a logical execution plan and only runs computations when an action is triggered.

Why is lazy evaluation important?
- Optimizes performance by combining multiple transformations into a single execution step.
- Reduces unnecessary computations, preventing redundant data processing.
- Improves efficiency by leveraging Spark’s query optimizer before executing code.

```
df = spark.read.csv("data.csv", header=True)  # No execution yet
filtered_df = df.filter(df["age"] > 30)       # Still no execution
filtered_df.show()                            # Triggers execution
```

# How do you read/write a csv file using Pyspark?

To read a CSV file in PySpark, you use the read.csv() function from SparkSession.
```
    df = spark.read.csv("data.csv", header=True, inferSchema=True)
    df.show(5)  # Display first 5 rows
```

header=True – Uses the first row as column names.
inferSchema=True – Automatically detects data types for each column.

By default, PySpark saves the output as multiple small files because it runs in distributed mode. To write a single CSV file, use .coalesce(1).
```
    df.coalesce(1).write.csv("output_folder", header=True)
```
coalesce(1): Combines all partitions into a single file.

# Explain the actions and transformations in PySpark with examples.

PySpark operations are divided into transformations (lazy operations that define computations) and actions (operations that trigger execution).

* Transformations (Lazy Operations)
Transformations do not execute immediately; they build a logical plan. Examples:

.filter() – Filters rows based on a condition.
.select() – Selects specific columns.
.groupBy() – Groups data based on a column.
.withColumn() – Adds or modifies a column.

* Actions (Trigger Execution)
Actions execute transformations and return results. Examples:

.show() – Displays the DataFrame.
.collect() – Brings all data to the driver.
.count() – Returns the number of rows.
.write() – Saves the DataFrame.

# What are the various ways to select columns in a PySpark DataFrame?

* Using .select() (Explicit Column Selection)
```
    df.select("name", "age").show()
```
* Using column objects
```
    from pyspark.sql.functions import col
    df.select(col("name"), col("age")).show()
```
* Using df["column_name"] Syntax
```
df.select(df[name"], df["age"]).show()
```
* Using df.column_name Syntax
```
    df.select(df.name, df.age).show()
```

# Explain the difference between map() and flatMap() functions in Spark

Both functions apply a transformation to each element in an RDD, but they behave differently in terms of output structure.

map() – Applies a function to each element and returns a list where each input maps to a single output.
flatMap() – Applies a function to each element and flattens the results, allowing each input to map to multiple outputs.

```
    rdd = spark.sparkContext.parallelize(["hello world", "pyspark tutorial"])

    # map() keeps the structure (each string remains a single element)
    mapped_rdd = rdd.map(lambda x: x.split(" "))
    print(mapped_rdd.collect())  # [['hello', 'world'], ['pyspark', 'tutorial']]

    # flatMap() flattens the results (each word becomes a separate element)
    flat_mapped_rdd = rdd.flatMap(lambda x: x.split(" "))
    print(flat_mapped_rdd.collect())  # ['hello', 'world', 'pyspark', 'tutorial']

```
# How do you handle missing or null values in PySpark DataFrames?

* Dropping Null Values - this removes rows containing null values.
```
    df.na.drop().show()
```
* Filling Null values with a Default value - this replaces null in string columns with "Unknown"
```
    df.na.fill("Unknown").show()
```
* Filling Null Values Based on Column Type
```
    df.na.fill({"age": 0, "name": "No name"}).show()
```
* Replacing Specific Values
```
df.replace("NA", "Unknown").show()
```
# How do you perform joins in PySpark DataFrames?

* INNER JOIN        df1.join(df2, df1.id == df2.id, "inner").show()
* LEFT JOIN         df1.join(df2, df1.id == df2.id, "left").show()
* RIGHT JOIN        df1.join(df2, df1.id == df2.id, "right").show()
* FULL OUTER JOIN   df1.join(df2, df1.id == df2.id, "outer").show()
* CROSS JOIN        df1.crossJoin(df2).show()
* BROADCAST JOIN    
```
    from pyspark.sql.functions import broadcast

    small_df = spark.read.csv("small_table.csv", header=True)
    large_df = spark.read.csv("large_table.csv", header=True)

    joined_df = large_df.join(broadcast(small_df), "id", "inner")
    joined_df.show()
```
A broadcast join is used when one of the tables is small enough to fit in memory. Spark broadcasts the small table to all worker nodes, reducing expensive data shuffling across partitions.

When to Use
- One table is small (a few MBs or less) and the other is large.
- You want to avoid costly shuffle operations in large cluster environments.

* SHUFFLE HASH JOIN (Default for Large Datasets)
```
    df1.join(df2, "id", "inner").show()
```
If both tables are large, Spark shuffles data across nodes and applies a hash join. This is slower than a broadcast join but necessary when both tables are too large to fit in memory.

How it Works
- Spark hashes the join keys and distributes rows to the corresponding partition.
- Matching keys are joined within the same partition.

# Explain the significance of caching in PySpark and how it's implemented

Caching in PySpark helps improve performance by storing intermediate results in memory (RAM) or disk, reducing expensive recomputation. This is especially useful when a DataFrame is used multiple times in an application.

How to Cache a DataFrame?
* Using .cache() (Stores in Memory if Possible). If memory is insufficient, some partitions may be recomputed when accessed.
```
    df = df.cache()
    df.count()  # Triggers caching
```

* Using .persist() (Gives More Control)
```
    from pyspark import StorageLevel

    df = df.persist(StorageLevel.MEMORY_AND_DISK)
    df.count()  # Triggers caching
```
Persists data based on storage level, e.g., memory, disk, or both.
MEMORY_AND_DISK ensures data is saved to disk if memory is full.

* Common Storage Levels in .persist()
- MEMORY_ONLY – Fastest, but data is lost if memory is full.
- MEMORY_AND_DISK – Saves to disk when memory is full (safer but slightly slower).
- DISK_ONLY – Stores only on disk (useful for very large datasets).
- MEMORY_AND_DISK_SER – Stores serialized data, reducing memory usage.

* When to Use Caching?
- When a DataFrame is reused multiple times in transformations or actions.
- When performing complex aggregations or joins.
- When iterating over the same dataset in ML model training.

* Clearing cache
df.unpersist()

# What are UDFs (User Defined Functions) and when would you use them?

A User Defined Function (UDF) in PySpark allows you to define custom transformations that cannot be easily expressed using Spark’s built-in functions. UDFs operate on each row like a Python function but run within Spark’s distributed environment.

Converting name to upeer-case:
```
    from pyspark.sql.functions import udf
    from pyspark.sql.types import StringType

    def capitalize_name(name):
        return name.upper() if name else None  # Custom logic

    capitalize_udf = udf(capitalize_name, StringType())  # Define UDF

    df = df.withColumn("capitalized_name", capitalize_udf(df["name"]))  # Apply UDF
    df.show()
```

When to Avoid UDFs?
- If the operation can be done with built-in functions, avoid UDFs (they are slower).
- If performance is a concern, prefer Pandas UDFs over standard UDFs.

# How do you aggregate data in Spark?

Aggregation in Spark is done using grouping and aggregation functions available in PySpark DataFrame API and SQL. Aggregations help summarize, count, or perform mathematical operations on large datasets efficiently in a distributed computing environment.

* Aggregation Using groupBy()
The most common way to aggregate data is using groupBy(), which groups rows based on a specific column and applies aggregation functions.

Aggregate by counting orders per customer
```
    df.groupBy("customer").agg(count("order_id").alias("total_orders")).show()
```
* Using Multiple Aggregations with agg()
```
    from pyspark.sql.functions import max

    df.groupBy("customer").agg(
        count("order_id").alias("total_orders"),
        max("order_id").alias("max_order_id")
    ).show()
```

* Using rollup() for Hierarchical Aggregation
```
    df.rollup("category", "customer").count().show()
```
This will return aggregated counts at different levels, including per category, per customer, and an overall total.

* Window Aggregation (Running Totals, Moving Averages)

Example: Running Total of Orders by Customer
```
    from pyspark.sql.window import Window
    from pyspark.sql.functions import sum

    window_spec = Window.partitionBy("customer").orderBy("order_id").rowsBetween(-1, 0)

    df.withColumn("running_total", sum("order_id").over(window_spec)).show()
```

* Using SQL for Aggregation
You can also run SQL queries on a DataFrame after creating a temporary view.
```
    df.createOrReplaceTempView("orders")

    spark.sql("""
        SELECT customer, COUNT(order_id) AS total_orders
        FROM orders
        GROUP BY customer
    """).show()
```

# Explain Window functions and their usage in PySpark

Window functions in PySpark allow performing calculations across a subset of rows (a window) in a DataFrame without collapsing the dataset like GROUP BY does. These functions are used for running totals, ranking, moving averages, and lead/lag calculations.

Example: Running Total of Sales Per Customer
```
    from pyspark.sql import SparkSession
    from pyspark.sql.window import Window
    from pyspark.sql.functions import sum

    spark = SparkSession.builder.appName("WindowFunctions").getOrCreate()

    df = spark.createDataFrame([
        ("Alice", "2024-01-01", 100),
        ("Alice", "2024-01-02", 200),
        ("Bob", "2024-01-01", 50),
        ("Bob", "2024-01-03", 150),
    ], ["customer", "date", "sales"])

    window_spec = Window.partitionBy("customer").orderBy("date").rowsBetween(Window.unboundedPreceding, 0)

    df.withColumn("running_total", sum("sales").over(window_spec)).show()
```
# Explain Broadcast variables and their role in PySpark optimization

Broadcast variables optimize performance by caching a small dataset.

Why Use Broadcast Variables?
- Avoids expensive shuffles by keeping small reference datasets in memory across worker nodes.
- Speeds up joins when one table is small and the other is large.

# How do you broadcast a variable, and when should you not use it?

from pyspark.sql.functions import broadcast
broadcasted_df = broadcast(small_df)

When NOT to Use Broadcasting:

- If the dataset is large, broadcasting can cause memory issues.
- If a table changes frequently, repeated broadcasting is inefficient.

# Explain the use of partitions in Spark (and bucketing)

* Partitions in Spark:
- A partition is a logical chunk of data processed in parallel.
- Spark automatically determines partitions, but users can control them manually.
- Too few partitions → under-utilized resources
- Too many partitions → high overhead

* Bucketing groups data by a specific column to reduce shuffling in joins.
```
    df.write.format("parquet").bucketBy(4, "customer").saveAsTable("bucketed_table")
```
# Explain how the Spark DAG works. Can you explain what happends under the hood?

Apache Spark uses a Directed Acyclic Graph (DAG) to represent the logical execution plan of a job.

* How DAG Works Under the Hood:
1. User Submits a Job:
When you run a transformation (e.g., df.filter(...)), Spark does not execute it immediately (lazy evaluation).

2. DAG Construction:
Spark creates a DAG that represents the logical flow of operations.
Each transformation adds a new node in the DAG.

3. DAG Splitting into Stages:
Spark divides the DAG into stages based on shuffle boundaries (wide transformations).
Narrow transformations (like map, filter) stay within the same stage.
Wide transformations (like groupBy, join) create new stages due to data shuffling.

4. Task Execution in Executors:
Each stage is further divided into tasks, which are distributed to worker nodes.
Spark optimizes execution before running tasks, minimizing data movement.

5. Execution & Fault Tolerance:
If a task fails, Spark reruns only that partition rather than the entire job.

# What is the difference between narrow and wide transformations? (with examples)

* Narrow Transformations:
- Data movement occurs within the same partition.
- No shuffling required, so it’s faster.
- Example operations: map(), filter(), flatMap().

* Data needs to be shuffled across partitions (expensive).
- Triggers a new stage in the DAG.
- Example operations: groupBy(), join(), reduceByKey().

# How does Spark handle small files (It's a performance killer if you don't handle it right)

Small files are a performance killer because each file creates a new task, leading to:

- High overhead on the driver.
- Too many partitions with too little data.

How to fix it?
1. Increase spark.sql.files.maxPartitionBytes - Spark will combine small files into larger partitions
```
    spark.conf.set("spark.sql.files.maxPartitionBytes", "256MB")
```
2. Use Coalesce or Repartition - Reduce unnecessary partitions to optimize reads.
```
    df.coalesce(10)  # Merges data into fewer partitions
    df.repartition(10)  # Redistributes data across partitions
```
3. Use Bucketing (for frequent joins on the same column)
- Saves data in predefined buckets, reducing shuffle.
- Merge Small Files Before Loading

If working with Parquet or ORC, compact files using a batch job.

# What happens if you cache a DataFrame but don't have enough memory?

If you cache a large DataFrame but don’t have enough memory, Spark will:
- Evict older cached data (Least Recently Used - LRU).
- Spill to disk, slowing down performance.
- If disk space is also low, the job may fail with an OutOfMemory (OOM) error.

# What's the difference between persist(StorageLevel.MEMORY_AND_DISK) and cache()?

cache() is a shortcut for persist(StorageLevel.MEMORY_ONLY), meaning it only stores data in memory. If there’s not enough memory, Spark will recompute the DataFrame instead of saving it to disk.
persist(StorageLevel.MEMORY_AND_DISK) stores the DataFrame in memory first. If there’s insufficient memory, Spark writes the remaining data to disk instead of recomputing it.

When to Use Each?
Use cache() if you have enough memory and want faster performance.
Use persist(StorageLevel.MEMORY_AND_DISK) when memory is limited, and you want to avoid recomputation.

# How do you handle memory related issues in PySpark?

Memory issues in PySpark often occur due to large datasets, inefficient transformations, or excessive shuffling. 

Troubleshooting:
- Adjust Executor Memory: Increase memory allocated to executors.
- Use coalesce() Instead of repartition() Where Possible: repartition() increases shuffling, while coalesce() reduces the number of partitions efficiently.
- Use persist() Instead of cache() to spill data to disk when necessary.
- Broadcast Small Datasets: If joining a small table with a large one, broadcast the small table to prevent shuffling.
- Use Columnar Storage Formats: Use Parquet or ORC instead of CSV for better memory efficiency.
- Enable Off-Heap Storage: If working with large datasets, enable off-heap memory to avoid excessive garbage collection.

# How does SparkSQL optimize query execution? (Catalyst optimizer isn't enough - explain)

SparkSQL does more than just Catalyst Optimizer to speed up queries. It optimizes execution in the following ways:

- Catalyst Optimizer: Generates the most efficient query plan by reordering joins, pruning columns, and pushing filters down.
- Tungsten Execution Engine: Uses bytecode generation to speed up execution by optimizing CPU usage.
- Whole-Stage Code Generation: Converts query plans into optimized Java bytecode, reducing CPU overhead.
- Adaptive Query Execution (AQE): Dynamically adjusts partitions and joins at runtime based on actual data.
- Predicate Pushdown: Pushes filter conditions to the data source (Parquet, ORC, etc.) to reduce data scanned.

# Why does Spark shuffle data, and how can you reduce shuffling?

Shuffling happens when Spark moves data across partitions for operations like groupBy(), join(), and repartition(). It's expensive because it requires disk I/O, network transfer, and CPU processing.

How to Reduce Shuffling?
- Use broadcast() for small datasets instead of regular joins.
- Use coalesce() instead of repartition() when reducing the number of partitions.
- Avoid distinct() or groupBy() if possible. Consider using map() and reduceByKey() for aggregations instead.
- Optimize join order using broadcast joins or bucketing to keep related data in the same partitions.

# Can you explain how checkpointing works in Spark Streaming?
# Discuss the concept of accumulators in PySpark
# How do you work with JSON nested data in PySpark?
# How do you integrate PySpark with other Python libraries NumPy or Pandas?
# Explain the process of deploying PySpark applications in a cluster
# How do you debug PySpark Applications effectively?


Advanced:
# What is Speculative Execution in Spark?
# How does Spark handle data skew, and what are some strategies to fix it?
# What is the difference between Tungsten vs Catalyst optimizations?
# Why is the number of partitions in Spark important? How do you tune it?
# What's the difference between DataFrame and DataSet? When would you use DataSet?
# How does Spark handleback backpressure in structured streaming?
# Explain the role of WAL (Write-Ahead Logs) in Spark Streaming
# If you have 500GB of data and 20 executors, how would you determine the ideal number of partitions?
# What is the Impact of using EDFs in Spark, and how can you make them more efficient?
# How do you optimize joins in Spark when dealing with large datasets? (BroadCast, sort-merge, shuffle - what's the best choice?)