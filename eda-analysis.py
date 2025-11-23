import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =====================================================
# LOAD CLEANED DATA
# =====================================================
df = pd.read_csv("banggood_scraped_data_clean.csv")
print("Loaded rows:", len(df))

sns.set(style="whitegrid")

# ==========================================================================
# 1. PRICE DISTRIBUTION PER CATEGORY
# ==========================================================================
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x="category", y="price")
plt.xticks(rotation=45, ha="right")
plt.title("Price Distribution per Category")
plt.show()


# ==========================================================================
# 2. RATING VS PRICE CORRELATION
# ==========================================================================
corr = df["price"].corr(df["rating"])
print(f"Correlation between price & rating : {corr:.3f}")

plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df,
    x="price",
    y="rating",
    hue="category",
    alpha=0.7
)
plt.title(f"Rating vs Price (Correlation = {corr:.2f})")
plt.show()


# ==========================================================================
# 3. TOP REVIEWED PRODUCTS (Top 10)
# ==========================================================================
top_reviewed = df.sort_values("reviews", ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=top_reviewed,
    x="reviews",
    y="title",
    palette="magma"
)
plt.title("Top 10 Most Reviewed Products")
plt.show()

print("\nTop Reviewed Products:")
print(top_reviewed[["title", "category", "reviews"]])


# ==========================================================================
# 4. BEST VALUE SCORE PER CATEGORY
# ==========================================================================
best_value = (
    df.sort_values("value_score", ascending=False)
      .groupby("category")
      .head(3)
)

plt.figure(figsize=(12, 6))
sns.barplot(
    data=best_value,
    x="value_score",
    y="title",
    hue="category",
    dodge=False
)
plt.title("Best Value Products per Category (Top 3 each)")
plt.show()

print("\nBest Value Products:")
print(best_value[["category", "title", "value_score"]])


# ==========================================================================
# 5. STOCK AVAILABILITY ANALYSIS
# (We assume: reviews == 0 → possibly out of stock)
# ==========================================================================
df["in_stock"] = np.where(df["reviews"] > 0, "Likely In Stock", "Possibly Out of Stock")

stock_summary = df.groupby(["category", "in_stock"]).size().unstack(fill_value=0)

stock_summary.plot(
    kind="bar",
    stacked=True,
    figsize=(12, 6),
    colormap="Set2"
)
plt.title("Stock Availability per Category")
plt.ylabel("Number of Products")
plt.show()

print("\nStock Availability Summary:")
print(stock_summary)
