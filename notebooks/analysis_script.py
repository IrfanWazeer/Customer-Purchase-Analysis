# File: notebooks/analysis_script.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Step 1: Load the dataset
data_path = os.path.join("..", "data", "Online Retail.csv")
df = pd.read_csv(data_path, encoding='ISO-8859-1')

# Step 2: Show basic info
print("Original Dataset Shape:", df.shape)
print(df.info())

# Step 3: Drop missing CustomerIDs (very important for behavior analysis)
df.dropna(subset=["CustomerID"], inplace=True)

# Step 4: Remove cancelled orders (Quantity < 0 means product returned)
df = df[df["Quantity"] > 0]

# Step 5: Convert 'InvoiceDate' to datetime format
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], dayfirst=True)

# Step 6: Create TotalPrice column (Quantity × UnitPrice)
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

# Step 7: Reset index after cleaning
# ---- TOP 10 SELLING PRODUCTS ----
top_products = (
    df.groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Best-Selling Products:\n", top_products)

# ---- VISUALIZE TOP PRODUCTS ----
plt.figure(figsize=(10, 6))
sns.barplot(x=top_products.values, y=top_products.index, palette="viridis")
plt.title("Top 10 Selling Products")
plt.xlabel("Quantity Sold")
plt.ylabel("Product")
plt.tight_layout()

# Save to visuals folder
plt.savefig("../visuals/top_10_products.png")

# Show plot
plt.show()

# ---- TOTAL REVENUE BY COUNTRY ----
country_revenue = (
    df.groupby("Country")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)  # Top 10 countries
)

print("\nTop 10 Countries by Revenue:\n", country_revenue)
# ---- VISUALIZE TOP COUNTRIES BY REVENUE ----
plt.figure(figsize=(10, 6))
sns.barplot(x=country_revenue.values, y=country_revenue.index, palette="coolwarm")
plt.title("Top 10 Countries by Revenue")
plt.xlabel("Total Revenue (GBP)")
plt.ylabel("Country")
plt.tight_layout()

# Save chart
plt.savefig("../visuals/top_10_countries_revenue.png")

# Show chart
plt.show()
# ---- CREATE YEAR-MONTH COLUMN ----
df["InvoiceMonth"] = df["InvoiceDate"].dt.to_period("M")
# ---- MONTHLY REVENUE ----
monthly_revenue = (
    df.groupby("InvoiceMonth")["TotalPrice"]
    .sum()
    .reset_index()
)

# Convert to string for plotting
monthly_revenue["InvoiceMonth"] = monthly_revenue["InvoiceMonth"].astype(str)

print("\nMonthly Revenue:\n", monthly_revenue.head())
# ---- PLOT MONTHLY REVENUE ----
plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_revenue, x="InvoiceMonth", y="TotalPrice", marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Total Revenue (GBP)")
plt.xticks(rotation=45)
plt.tight_layout()

# Save chart
plt.savefig("../visuals/monthly_revenue_trend.png")

# Show chart
plt.show()
# ---- TOP 10 CUSTOMERS BY REVENUE ----
top_customers = (
    df.groupby("CustomerID")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Customers by Revenue:\n", top_customers)
# ---- VISUALIZE TOP CUSTOMERS ----
plt.figure(figsize=(10, 6))
sns.barplot(x=top_customers.values, y=top_customers.index.astype(str), palette="mako")
plt.title("Top 10 Customers by Revenue")
plt.xlabel("Total Revenue (GBP)")
plt.ylabel("Customer ID")
plt.tight_layout()

# Save chart
plt.savefig("../visuals/top_10_customers.png")

# Show chart
plt.show()
