# What is Apache Spark, and how does it compare to Hadoop? 

Apache Spark is a distributed computing framework for big data processing and analytics. It is designed for speed, ease of use, and in-memory processing, making it much faster than Hadoop’s MapReduce.

Key differences between Spark and Hadoop:
- Speed: Spark processes data 100x faster than Hadoop because it uses in-memory computation, while Hadoop writes intermediate data to disk.
- Ease of Use: Spark supports SQL, Python, Scala, Java, and R, while Hadoop requires writing low-level MapReduce programs.
- Processing Model: Spark supports batch, streaming, ML, and graph processing, while Hadoop is mainly batch-oriented.
Hadoop is better for cheap, large-scale storage (HDFS), while Spark is better for real-time and iterative computations.

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
# Explain Broadcast variables and their role in PySpark optimization
# How do you broadcast a variable, and when should you not use it?
# How does Apache Spark handle big data processing?
# Explain the use of partitions in Spark (and bucketing)
# Explain how the Spark DAG works. Can you explain what happends under the hood?
# What is the difference between narrow and wide transformations? (with examples)
# How does Spark handle small files (It's a performance killer if you don't handle it right)
# What happens if you cache a DataFrame but don't have enough memory?
# What's the difference between persist(StorageLevel.MEMORY_AND_DISK) and cache()?
# How do you handle memory related issues in PySpark?
# How does SparkSQL optimize query execution? (Catalyst optimizer isn't enough - explain)
# Why does Spark shuffle data, and how can you reduce shuffling?
# When would you use repartition() vs coalesce()?
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