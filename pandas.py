import pandas as pd

df = pd.read_csv("raw_data.csv")  # Load CSV file into a DataFrame

# Loading and saving data
pd.read_csv()        # Read data from a CSV file
pd.read_parquet()    # Read data from a Parquet file
pd.read_json()       # Read data from a JSON file
pd.read_excel()      # Read data from an Excel file

df.to_csv()          # Write DataFrame to a CSV file
df.to_parquet()      # Write DataFrame to a Parquet file
df.to_excel()        # Write DataFrame to an Excel file
df.to_json()         # Write DataFrame to a JSON file

# Inspecting and understanding data
df.head()            # Show first 5 rows
df.tail()            # Show last 5 rows
df.sample()          # Show random rows

df.shape             # Get (rows, columns) count
df.columns           # List column names
df.dtypes            # Show data types of columns
df.info()            # Summary of DataFrame and null counts
df.describe()        # Statistical summary of numeric columns

# Selecting Data 
df['col']            # Select a single column
df[['col1', 'col2']] # Select multiple columns

df.loc[row_filter, col_filter]  # Label-based row and column selection
df.iloc[row_idx, col_idx]       # Position-based row and column selection

df.at[row, col]      # Fast access to a single value (label-based)
df.iat[row, col]     # Fast access to a single value (index-based)

# Cleaning data
df.isna()            # Detect missing values
df.notna()           # Detect non-missing values

df.dropna()          # Remove rows with missing values
df.fillna()          # Replace missing values
df.replace()         # Replace specific values

df.drop(columns=[...])           # Remove one or more columns
df.rename(columns={...})         # Rename columns

df.astype()          # Change column data types
df.copy()            # Create a deep copy of the DataFrame

# Filtering and sorting
df.query("col > 10") # Filter rows using SQL-like syntax

df.sort_values('col') # Sort rows by column values
df.sort_index()       # Sort rows by index

df.drop_duplicates()  # Remove duplicate rows
df.duplicated()       # Identify duplicate rows

# Aggregations & Stats
df.sum()             # Sum of values per column
df.mean()            # Mean of values per column
df.min()             # Minimum value per column
df.max()             # Maximum value per column
df.count()           # Count non-null values
df.nunique()         # Count unique values per column

# Grouping data
df.groupby('col').agg(...)  # Group data and apply multiple aggregations
df.groupby('col').sum()     # Group data and sum values
df.groupby('col').mean()    # Group data and calculate mean

# Joining and combining dataframes
pd.merge(df1, df2, on='id', how='inner')  # SQL-style join on a key
pd.concat([df1, df2])                     # Stack DataFrames vertically
df.join(df2)                              # Join DataFrames by index

# Reshaping Data
df.pivot()        # Reshape data (rows to columns)
df.pivot_table()  # Pivot with aggregation support
df.melt()         # Unpivot data from wide to long format
df.stack()        # Convert columns to rows
df.unstack()      # Convert rows back to columns

# String operations
df['col'].str.lower()    # Convert strings to lowercase
df['col'].str.upper()    # Convert strings to uppercase
df['col'].str.contains() # Check if string contains a pattern
df['col'].str.replace() # Replace substrings
df['col'].str.split()   # Split strings into lists
