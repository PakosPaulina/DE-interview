# How would you use python for data cleaning and transformation?

#######################################################################################################################
import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("raw_data.csv")

# 1. Handle Missing Values
df.fillna({
    "age": df["age"].median(),  # Fill missing ages with median
    "salary": df["salary"].mean(),  # Fill missing salary with mean
    "city": "Unknown"  # Fill missing city with "Unknown"
}, inplace=True)

# 2. Remove Duplicates
df.drop_duplicates(inplace=True)

# 3. Convert Data Types
df["date_of_birth"] = pd.to_datetime(df["date_of_birth"], errors="coerce")  # Convert date column
df["salary"] = df["salary"].astype(float)  # Convert salary to float

# 4. Standardize  Text Columns
df["name"] = df["name"].str.strip().str.title()  # Remove whitespace and capitalize names
df["email"] = df["email"].str.lower()  # Convert emails to lowercase
df["description"] = df["description"].str.replace(r"[^a-zA-Z0-9 ]", "", regex=True)  # Remove special characters

# 5. Create New Features
df["age_group"] = pd.cut(df["age"], bins=[0, 18, 35, 60, 100], labels=["Child", "Young", "Adult", "Senior"])
df["year_of_birth"] = df["date_of_birth"].dt.year

# 6. Handle Outliers (Remove extreme values in salary)
df = df[(df["salary"] > df["salary"].quantile(0.05)) & (df["salary"] < df["salary"].quantile(0.95))]

# 7. Export Cleaned Data
df.to_csv("cleaned_data.csv", index=False)

print("Data cleaning complete. Cleaned data saved to cleaned_data.csv 🚀")
#######################################################################################################################

# Write a python script to connect to a database and fetch data using sql queries.

#######################################################################################################################
import pandas as pd
from sqlalchemy import create_engine

# Define database credentials
db_url = "postgresql://username:password@host:port/database_name"

# Create a connection
engine = create_engine(db_url)

# Write an SQL query
query = "SELECT * FROM customers WHERE country = 'USA'"

# Fetch data into a pandas DataFrame
df = pd.read_sql(query, engine)

# Print first few rows
print(df.head())

# Close the connection
engine.dispose()

#######################################################################################################################

# How would you handle exceptions in a python based ETL pipeline?
'''
    1. Use try-except blocks around key ETL stages (Extract, Transform, Load).
    2. Log errors using logging instead of print().
    3. Handle specific exceptions (ValueError, KeyError, IOError, etc.).
    4. Retry failed operations (e.g., using retrying or tenacity).
    5. Alert failures (email, Slack, monitoring tools).
'''
#Example:

import pandas as pd
import logging

# Configure logging
logging.basicConfig(filename="etl_errors.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

try:
    # Extract
    df = pd.read_csv("data.csv")  # Read CSV file

    # Transform
    df["date"] = pd.to_datetime(df["date"])  # Convert to datetime
    df["sales"] = df["sales"].astype(float)  # Convert sales column to float

    # Load
    df.to_csv("cleaned_data.csv", index=False)

except FileNotFoundError as e:
    logging.error(f"File not found: {e}")

except ValueError as e:
    logging.error(f"Data type conversion error: {e}")

except Exception as e:
    logging.error(f"Unexpected error: {e}")

print("ETL process completed with error logging.")      
    
# What libraries have you used for data processing? Pandas, PySpark, NumPy, Pyodbc, SQLAlchemy, requests
# How do you write a good data check?
'''
Schema Validation → Ensure correct column names & data types
    Missing Values Check → Identify NaN, None, or empty values
    Duplicate Data Check → Remove redundant rows
    Outliers & Anomalies → Detect extreme values using statistical methods
    Business Rules Validation → Ensure domain-specific constraints (e.g., age > 0)
'''
#Example:
import pandas as pd

# Load data
df = pd.read_csv("data.csv")

# Check 1: Validate Schema (Ensure Expected Columns Exist)
expected_columns = ["id", "name", "age", "salary"]
missing_columns = [col for col in expected_columns if col not in df.columns]
if missing_columns:
    raise ValueError(f"Missing columns: {missing_columns}")

# Check 2: Check for Missing Values
missing_values = df.isnull().sum()
print("Missing Values:\n", missing_values)

# Check 3: Identify Duplicates
duplicates = df.duplicated().sum()
print(f"Number of duplicate rows: {duplicates}")

# Check 4: Outlier Detection (Using Z-Score)
from scipy.stats import zscore
df["salary_zscore"] = zscore(df["salary"])
outliers = df[df["salary_zscore"].abs() > 3]
print("Outliers Detected:\n", outliers)

# Check 5: Business Rule Validation (Example: Age Cannot Be Negative)
if (df["age"] < 0).any():
    raise ValueError("Negative ages found!")

print("Data quality checks completed successfully.")

# How can you implement the WAP (write-audit-publish) pattern in your pipelines?
'''
The WAP (Write-Audit-Publish) pattern is all about data quality checks before loading into production tables.
Raw data is written to a temporary staging table (e.g., staging_table). There are no direct writes to the production tables. 
It then performs data validation checks. If data passes all checks, it is moved to a final production table (e.g., prod_table).
'''