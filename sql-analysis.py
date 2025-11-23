import pyodbc
import pandas as pd

# =====================================================
# SQL SERVER CONNECTION
# =====================================================
conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-4RKVM5J;"
    "Database=BanggoodDB;"
    "Trusted_Connection=yes;"
)

print("Connected to SQL Server\n")


def run_query(query):
    """Utility function to run a SQL query and return a pandas DataFrame"""
    return pd.read_sql_query(query, conn)


# =====================================================
# 1. AVERAGE PRICE PER CATEGORY
# =====================================================
print("\n================ AVERAGE PRICE PER CATEGORY ================\n")

q1 = """
SELECT 
    category,
    AVG(price) AS avg_price
FROM Products
GROUP BY category
ORDER BY avg_price DESC;
"""

df1 = run_query(q1)
print(df1)


# =====================================================
# 2. AVERAGE RATING PER CATEGORY
# =====================================================
print("\n================ AVERAGE RATING PER CATEGORY ================\n")

q2 = """
SELECT
    category,
    AVG(rating) AS avg_rating
FROM Products
GROUP BY category
ORDER BY avg_rating DESC;
"""

df2 = run_query(q2)
print(df2)


# =====================================================
# 3. PRODUCT COUNT PER CATEGORY
# =====================================================
print("\n================ PRODUCT COUNT PER CATEGORY ================\n")

q3 = """
SELECT 
    category,
    COUNT(*) AS total_products
FROM Products
GROUP BY category
ORDER BY total_products DESC;
"""

df3 = run_query(q3)
print(df3)


# =====================================================
# 4. TOP 5 REVIEWED PRODUCTS PER CATEGORY
# =====================================================
print("\n================ TOP 5 REVIEWED PRODUCTS PER CATEGORY ================\n")

q4 = """
SELECT *
FROM (
        SELECT 
            category,
            title,
            reviews,
            ROW_NUMBER() OVER (PARTITION BY category ORDER BY reviews DESC) AS rank
        FROM Products
     ) AS ranked
WHERE rank <= 5
ORDER BY category, reviews DESC;
"""

df4 = run_query(q4)
print(df4)


# =====================================================
# 5. STOCK AVAILABILITY STATISTICS
# =====================================================
print("\n================ STOCK AVAILABILITY ================\n")

q5 = """
SELECT 
    category,
    SUM(CASE WHEN reviews > 0 THEN 1 ELSE 0 END) AS in_stock,
    SUM(CASE WHEN reviews = 0 THEN 1 ELSE 0 END) AS out_of_stock,
    ROUND(
        100.0 * SUM(CASE WHEN reviews > 0 THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS in_stock_percentage,
    ROUND(
        100.0 * SUM(CASE WHEN reviews = 0 THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS out_of_stock_percentage
FROM Products
GROUP BY category
ORDER BY in_stock_percentage DESC;
"""

df5 = run_query(q5)
print(df5)


print("\n🎉 SQL Analysis Complete! All results printed above.")
conn.close()
