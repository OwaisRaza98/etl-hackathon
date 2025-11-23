import pandas as pd
import pyodbc

# =====================================================
# Load cleaned data
# =====================================================
df = pd.read_csv("banggood_scraped_data_clean.csv")
print("Loaded rows:", len(df))


# =====================================================
# Connect to the SQL Server *master* database first
# so we can create BanggoodDB if it doesn't exist.
# =====================================================
master_conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-4RKVM5J;"
    "Database=master;"
    "Trusted_Connection=yes;"
)
master_cursor = master_conn.cursor()

# =====================================================
# 1. CREATE DATABASE if NOT EXISTS
# =====================================================
create_db_query = """
IF NOT EXISTS (
    SELECT name FROM sys.databases WHERE name = 'BanggoodDB'
)
BEGIN
    CREATE DATABASE BanggoodDB;
END;
"""

master_cursor.execute(create_db_query)
master_conn.commit()
master_cursor.close()
master_conn.close()

print("✔ Database ready: BanggoodDB")


# =====================================================
# Reconnect to the new database
# =====================================================
conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-4RKVM5J;"
    "Database=BanggoodDB;"
    "Trusted_Connection=yes;"
)
cursor = conn.cursor()


# =====================================================
# 2. CREATE TABLE IF NOT EXISTS
# =====================================================
create_table_query = """
IF NOT EXISTS (
    SELECT * FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_NAME = 'Products'
)
BEGIN
    CREATE TABLE Products (
        product_id INT IDENTITY(1,1) PRIMARY KEY,
        category VARCHAR(255),
        subcategory VARCHAR(255),
        title VARCHAR(500),
        price FLOAT,
        rating FLOAT,
        reviews INT,
        value_score FLOAT,
        popularity_score FLOAT,
        price_bucket VARCHAR(50)
    );
END;
"""

cursor.execute(create_table_query)
conn.commit()

print("✔ Table ready: Products")


# =====================================================
# 3. INSERT Cleaned CSV into Products Table
# =====================================================

insert_query = """
INSERT INTO Products (
    category,
    subcategory,
    title,
    price,
    rating,
    reviews,
    value_score,
    popularity_score,
    price_bucket
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

for _, row in df.iterrows():
    cursor.execute(insert_query, (
        row["category"],
        row["subcategory"],
        row["title"],
        float(row["price"]),
        float(row["rating"]),
        int(row["reviews"]),
        float(row["value_score"]),
        float(row["popularity_score"]),
        row["price_bucket"]
    ))

conn.commit()
cursor.close()
conn.close()

print("🔥 Data Successfully Loaded Into SQL Server!")
