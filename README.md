# Banggood Product Trend Analysis (ETL + SQL + EDA)

## 📌 Overview
End-to-end ETL pipeline:
- Web Scraping (Selenium)
- Cleaning & Transformation (Pandas)
- Exploratory Data Analysis (Matplotlib/Seaborn)
- Load into SQL Server (pyodbc)
- SQL Aggregated Analysis
- Final Insights & Recommendations

## 🏗️ Architecture
(Insert architecture diagram)

## 📝 Data Pipeline
1. Scrape 5 categories + subcategories
2. Clean & normalize data
3. Generate derived features
4. Load into SQL Server unified table
5. Execute 5 SQL analytical queries
6. Visualize insights

## 🧼 Cleaning Includes
- Price normalization
- Rating cleanup
- Review count extraction
- Category / subcategory name parsing
- Missing value handling
- Derived features:
  - value_score
  - popularity_score
  - price_bucket

## 🧠 SQL Analysis
- Avg price per category
- Avg rating per category
- Product count per category
- Top reviewed per category
- Stock availability estimation

## 📦 Files
- scraper.py
- clean-data.py
- sql-load.py
- sql-analysis.py
- eda-analysis.py

## 🔥 Final Output
A complete automated data pipeline + dashboard-ready insights.
