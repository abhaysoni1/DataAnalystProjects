import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "data/Sample - Superstore.csv"

df = pd.read_csv(file_path, encoding='latin1')
print("Data loaded successfully")
print(df.head(10))
print("\n Shape of data", df.shape)
print(df.columns.tolist())

df.columns = [col.strip() for col in df.columns]
print("\n Column names:", df.columns.tolist())
df["TotalSale"]=df["Quantity"]*df["Sales"]
df["TotalSale"]=df["TotalSale"].fillna(0)
df['Order Date'] = pd.to_datetime(df['Order Date'])
high_sales = df[df["TotalSale"] > 1000]

print("\nNumber of sales records with TotalSale > 1000:", high_sales.shape[0])
print("\nSample high sales records:")
print(high_sales.head())

df.to_csv("output/cleaned_superstore.csv", index=False)
high_sales.to_csv("output/high_value_sales.csv", index=False)

print("✅ Full cleaned data saved to 'output/cleaned_superstore.csv'")
print("✅ High-value sales saved to 'output/high_value_sales.csv'")

region_sales = df.groupby("Region")["TotalSale"].sum().sort_values(ascending=False)
region_sales.plot(kind='bar', title='Total Sales by Region', figsize=(8,5), color='skyblue')
plt.ylabel("Total Sales ($)")
plt.xlabel("Region")
plt.tight_layout()
plt.show()

category_sales = df.groupby("Category")["TotalSale"].sum().sort_values()
sns.barplot(x=category_sales.values, y=category_sales.index, palette="pastel")
plt.title("Total Sales by Product Category")
plt.xlabel("Total Sales ($)")
plt.ylabel("Category")
plt.tight_layout()
plt.show()

monthly_sales = df.resample("M", on="Order Date")["TotalSale"].sum()
monthly_sales.plot(figsize=(10,5), marker='o', title="Monthly Sales Trend")
plt.ylabel("Total Sales ($)")
plt.xlabel("Month")
plt.tight_layout()
plt.show()

top_customers = df.groupby("Customer Name")["TotalSale"].sum().sort_values(ascending=False).head(10)
sns.barplot(x=top_customers.values, y=top_customers.index, palette="mako")
plt.title("Top 10 Customers by Total Sales")
plt.xlabel("Total Sales ($)")
plt.ylabel("Customer Name")
plt.tight_layout()
plt.show()
