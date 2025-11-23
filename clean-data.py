import pandas as pd
import numpy as np
import re

# =====================================================
# LOAD RAW CSV
# =====================================================
df = pd.read_csv("banggood_scraped_data.csv")
print("Loaded rows:", len(df))


# =====================================================
# FUNCTION: Extract readable name from Banggood URL
# Example: "Wholesale-Bike-Lights-ca-6004" → "Bike Lights"
# =====================================================
def extract_name_from_url(url):
    try:
        part = url.split("Wholesale-")[1]
        part = part.split("-ca")[0]
        return part.replace("-", " ").strip().title()
    except:
        return url   # fallback


# =====================================================
# CLEAN CATEGORY NAME
# =====================================================
if "main_category" in df.columns:
    df["category"] = df["main_category"].apply(extract_name_from_url)


# =====================================================
# CLEAN SUBCATEGORY NAME (FINAL FIX)
# =====================================================
possible_sub_cols = ["subcategory", "subcategory_url", "sub_category", "subcat"]

for col in possible_sub_cols:
    if col in df.columns:
        df["subcategory"] = df[col].apply(extract_name_from_url)
        break


# Remove old URL-based fields
df = df.drop(columns=["main_category", "subcategory_url"], errors="ignore")


# =====================================================
# CLEAN PRICE (overwrite)
# =====================================================
def clean_price(p):
    if pd.isna(p):
        return np.nan
    p = re.sub(r"[^0-9.]", "", str(p))
    return float(p) if p else np.nan

df["price"] = df["price"].apply(clean_price)


# =====================================================
# CLEAN RATING (overwrite)
# =====================================================
def clean_rating(r):
    if pd.isna(r):
        return np.nan
    match = re.search(r"(\d+(\.\d+)?)", str(r))
    return float(match.group(1)) if match else np.nan

df["rating"] = df["rating"].apply(clean_rating)


# =====================================================
# CLEAN REVIEWS (overwrite)
# =====================================================
def clean_reviews(rv):
    if pd.isna(rv):
        return 0
    rv = str(rv).replace(",", "")
    match = re.search(r"(\d+)", rv)
    return int(match.group(1)) if match else 0

df["reviews"] = df["reviews"].apply(clean_reviews)


# =====================================================
# FILL MISSING VALUES
# =====================================================
df["price"] = df["price"].fillna(df["price"].median())
df["rating"] = df["rating"].fillna(df["rating"].median())
df["reviews"] = df["reviews"].fillna(0)


# =====================================================
# DERIVED FEATURE 1 — VALUE SCORE
# rating / price
# =====================================================
df["value_score"] = (df["rating"] / df["price"]).round(4)


# =====================================================
# DERIVED FEATURE 2 — POPULARITY SCORE
# rating × sqrt(reviews)
# =====================================================
df["popularity_score"] = (
    df["rating"] * np.sqrt(df["reviews"] + 1)
).round(4)


# =====================================================
# DERIVED FEATURE 3 — PRICE BUCKET
# Quartile-based segmentation
# =====================================================
df["price_bucket"] = pd.qcut(
    df["price"],
    q=4,
    labels=["Low", "Medium", "High", "Premium"]
)


# =====================================================
# EXPORT CLEANED CSV
# =====================================================
df.to_csv("banggood_scraped_data_clean.csv", index=False)

print("\n🔥 CLEANING COMPLETE!")
print("Saved → banggood_scraped_data_clean.csv")
print("Columns:", df.columns.tolist())
