# Explain the difference between a clustered and non-clustered index
A clustered index determines the physical order of data in a table and can only exist once per table. The primary key automatically creates a clustered index. A non-clustered index, on the other hand, is a separate structure that stores pointers to the actual data without changing its physical order. A table can have multiple non-clustered indexes, which improve search performance but require extra storage.
```
    - Clustered Index (automatically created for Primary Key)
        CREATE TABLE Employees (
            EmployeeID INT PRIMARY KEY,  -- Clustered Index on EmployeeID
            Name VARCHAR(100),
            Department VARCHAR(50)
        );

    - Non-Clustered Index (for faster searches on Name)
        CREATE INDEX idx_name ON Employees(Name);

```
# What are window functions in SQL? Provide examples
Window functions perform calculations across a set of rows related to the current row without collapsing them into a single result. These are often used for running totals, ranking, and moving averages.

- Common Window Functions:

ROW_NUMBER(): Assigns a unique number to each row.
RANK(): Assigns ranks; ties get the same rank and skip the next.
DENSE_RANK(): Similar to RANK(), but does not skip numbers.
SUM() OVER(): Running total.
AVG() OVER(): Moving average.

# What's the difference between RANK vs DENSE_RANK vs ROW_NUMBER?
All three are window functions used to assign a rank or number to rows based on a specified order. However, they behave differently when there are duplicate (tied) values.

* ROW_NUMBER() - assigns a unique row number to each row within a partition, with no gaps (so no duplicates)
* RANK() - Assigns the same rank to duplicate values but skips the next ranks(s)
* DENSE_RANK() - Similar to RANK(), but does NOT skip numbers after duplicates.

# What's QUALIFY?
It's a filtering clause used in some databases (e.g., Snowflake, BigQuery, Teradata) to filter results based on window (analytic) functions after they have been calculated.

* Why Use QUALIFY?
Normally, WHERE and HAVING cannot filter the results of window functions because they are applied before window functions are processed.

WHERE → Filters before window functions
HAVING → Filters after aggregation
QUALIFY → Filters after window function execution

```
    SELECT EmployeeID, Name, Department, Salary,
       RANK() OVER (PARTITION BY Department ORDER BY Salary DESC) AS RankNum
    FROM Employees
    QUALIFY RankNum = 1;

```
Without QUALIFY, you would need a subquery to filter the results.

Spark and Databricks don't support it.

# How would you optimize a query that takes too long to execute?
- Use indexing:
    CREATE INDEX idx_order_date ON Orders(OrderDate);
- Avoid SELECT * (only select require columns)
- Use joins efficiently (inner or outer joins)
- Optimize WHERE clauses. Avoid functions on indexed columns (WHERE YEAR(date) = 2023 is slow), instead use range-based filtering:
    WHERE date BETWEEN '2023-01-01' AND '2023-12-31'
- Use CTEs or TEMP Tables for Complex queries
- Check Query execution plan:
    Use EXPLAIN (MySQL/PostgreSQL) or EXECUTION PLAN (SQL Server) to analyze performance bottlenecks (Also .explain() in Spark)

# Write a query to find duplicate records in a table.

```
        WITH deduped AS (
        SELECT 
        *, 
        ROW_NUMBER() OVER (PARTITION BY game_id, team_id, player_id) AS row_num
        FROM game_details
    )
    SELECT * FROM deduped
    WHERE row_num = 1;
```
OR

```
    SELECT column1, column2, COUNT(*)
    FROM TableName
    GROUP BY column1, column2
    HAVING COUNT(*) > 1;

```
# How do you handle null values in SQL?
- Replace NULL values with a default value using COALESCE()
    SELECT name, COALESCE(salary, 0) AS salary FROM employees;
- Filter NULL values using IS NOT NULL or IS NULL
    SELECT * FROM employees WHERE salary IS NULL;
- Use NULL-safe comparisons WITH CASE WHEN
    SELECT name,
       CASE WHEN salary IS NULL THEN 'Not Available' ELSE salary END AS salary_status FROM employees;

# Explain the difference between DELETE, TRUNCATE and DROP
- DELETE: Removes specific rows from a table using a WHERE clause. It can be rolled back (if inside a transaction). We can also remove all data from a table with a DELETE FROM table;
- TRUNCATE: Removes all rows from a table but keeps the table structure. It is faster than DELETE and cannot be rolled back in most databases.
    TRUNCATE TABLE employees;
- DROP: Completely removes a table (including its structure), making it irreversible.

# What is a CTE (Common table expression) and how is it different from a subquery. 
A CTE is a temporary result set that improves query readability and reusability. Unlike subqueries, CTEs can be referenced multiple times in the main query (deduped above is a CTE). Subqueries are embedded inside other queries and are executed once per use.

Subquery:
    SELECT EmployeeID, Name, Salary 
    FROM Employees 
    WHERE Salary > (SELECT AVG(Salary) FROM Employees);

# Write a query to calculate a running total of sales for each month. 
```
    SELECT OrderDate, 
        SUM(Sales) OVER (PARTITION BY YEAR(OrderDate), MONTH(OrderDate) ORDER BY OrderDate) AS RunningTotal
    FROM Orders;
```
# Explain the difference between INNER JOIN, LEFT JOIN, SELF-JOIN and FULL OUTER JOIN
- INNER JOIN: Returns only matching rows from both tables
- LEFT JOIN: Returns all rows from the left table and matching rows from the right table. If no match is found, NULL is returned.
- FULL OUTER JOIN: Returns all rows from both tables. If no match is found, NULL is returned in place of missing values.
- SELF-JOIN: is when a table is joined with itself.
```
    SELECT e1.EmployeeID, e1.Name AS Employee, e2.Name AS Manager
    FROM Employees e1
    LEFT JOIN Employees e2 ON e1.ManagerID = e2.EmployeeID;
```

* e1 represents the employee.
* e2 represents the manager (who is also an employee in the same table).
* The LEFT JOIN ensures employees without a manager (e.g., the CEO) are still included.

The self-join works best when a table contains hierarchical or relational data where rows need to be compared to other rows in the same table. It can also be used for matching related records (eg., customers who share the same address).

Another use is to find dupes within the same table (there's better ways to do this though):
```
    SELECT a.Name, a.Department
    FROM Employees a
    JOIN Employees b ON a.Name = b.Name AND a.EmployeeID <> b.EmployeeID;
```

- CROSS-JOIN: produces the Cartesian product of two tables, meaning every row from the first table is paired with every row from the second table. This can lead to a large result set, especially if both tables have many rows. Unlike INNER JOIN, LEFT JOIN, or FULL OUTER JOIN, a CROSS JOIN does not require a matching condition (ON clause).

# What is a stored procedure and how would you use it?
It's a precompiled SQL script that is stored in the database and can be executed multiple times. It helps in automation, performance optimization, and code reuse. 
Example: Creating a stored procedure to fetch employees from a specific department:
```
    CREATE PROCEDURE GetEmployeesByDepartment(IN dept_name VARCHAR(50))
    BEGIN
        SELECT EmployeeID, Name, Salary
        FROM Employees
        WHERE Department = dept_name;
    END;
```
To execute:
```
    CALL GetEmployeesByDepartment('HR');
```

Benefits:
* Avoid rewriting the same queries over and over again
* Precompile for faster execution

# How do you ensure data quality in a data warehouse? 
* Using constraints (NOT NULL, CHECK, UNIQUE)
* Remove duplicates with DISTINCT or ROW_NUMBER() OVER() 
* Handle NULL values with COALESCE() or CASE WHEN

- For ETL best practices:
* Use staging table to validate data before loading into the final warehouse (production) (check WAP pattern)
* Implement data transformation rules to standardize formats

-Data Integrity checks:
* Use PRIMARY and FOREIGN KEYs (referencing other tables) in TABLE SCHEMA design
* Use triggers or stored procedures to enforce business rules

- Visualizations:
* Automated data quality reports (SQL scripts or BI tools like Tableau/PowerBI)

Advanced:
# Advanced Analytical Functions like Grouping sets, rollup, cube
# Arrays: how to CROSS JOIN UNNEST / LATERAL VIEW EXPLODE
# How to TRANSFORM and REDUCE array values