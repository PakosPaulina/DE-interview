from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark = SparkSession.builder.getOrCreate()  # Create Spark session

df = spark.read.csv("raw_data.csv", header=True)  # Load CSV into DataFrame

# Loading and saving data
spark.read.csv()        # Read CSV files
spark.read.parquet()    # Read Parquet files
spark.read.json()       # Read JSON files
spark.read.table()      # Read table from metastore

df.write.csv()          # Write DataFrame to CSV
df.write.parquet()      # Write DataFrame to Parquet
df.write.json()         # Write DataFrame to JSON
df.write.saveAsTable()  # Save DataFrame as a Spark table

# Inspecting and understanding data
df.show()               # Display rows in tabular format
df.take(5)              # Return first N rows as a list
df.count()              # Count number of rows
df.display()            # Pretty print DataFrame

df.columns              # List column names
df.dtypes               # Column names and data types
df.printSchema()        # Display schema tree
df.describe().show()    # Summary statistics

# Selecting data
df.select("col")                    # Select a single column
df.select("col1", "col2")            # Select multiple columns
df.select(col("col"))                # Select using column expression

df.selectExpr("col * 2 as col2")     # SQL-style expressions

# Filtering data
df.filter(col("col") > 10)           # Filter rows
df.where(col("col") > 10)            # Same as filter()

# Adding and modifying columns
df.withColumn("new_col", col("col") * 2)  # Add or replace a column
df.withColumnRenamed("old", "new")         # Rename a column

# Cleaning data
df.dropna()             # Drop rows with nulls
df.fillna(0)            # Replace nulls with value
df.dropDuplicates()     # Remove duplicate rows

# Sorting data
df.orderBy("col")               # Sort by column (ascending)
df.orderBy(col("col").desc())   # Sort descending

# Aggregations & stats
df.groupBy().count()    # Count all rows
df.groupBy("col").sum() # Group and sum
df.groupBy("col").avg() # Group and average
df.agg(
    sum("col"),         # Aggregate sum
    avg("col"),         # Aggregate average
    count("col")        # Aggregate count
)

# Common functions (VERY important)
col("col")              # Reference a column
lit(1)                  # Create a literal value
when(col("a") > 0, 1)   # Conditional logic
otherwise(0)            # Else condition

# String functions
lower(col("col"))       # Convert string to lowercase
upper(col("col"))       # Convert string to uppercase
trim(col("col"))        # Trim whitespace
split(col("col"), ",")  # Split string into array
length(col("col"))      # String length

# Date & time functions
current_date()          # Current date
current_timestamp()     # Current timestamp
to_date(col("col"))     # Convert to date
year(col("date"))       # Extract year
month(col("date"))      # Extract month

# Joins
df.join(df2, on="id", how="inner")  # Inner join
df.join(df2, on="id", how="left")   # Left join
df.join(df2, on="id", how="right")  # Right join

# Window functions
from pyspark.sql.window import Window

window = Window.partitionBy("col").orderBy(col("date").desc())  # Define window
row_number().over(window)     # Assign row numbers
rank().over(window)           # Rank rows
dense_rank().over(window)     # Dense rank rows

# Exploding arrays & structs
explode(col("array_col"))     # Turn array elements into rows
col("struct_col.field")       # Access struct field

# Performance & optimization
df.cache()             # Cache DataFrame in memory
df.persist()           # Persist DataFrame with storage level
df.repartition(10)     # Increase or rebalance partitions
df.coalesce(1)         # Reduce number of partitions

# SQL
df.createOrReplaceTempView("my_view")  # Create temp SQL view
spark.sql("SELECT * FROM my_view")     # Query using Spark SQL
