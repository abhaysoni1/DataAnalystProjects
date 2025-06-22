import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="ecommerce_db"
)

query = """
SELECT Description, SUM(Total) AS Total_Revenue
FROM ecommerce_orders
GROUP BY Description
ORDER BY Total_Revenue DESC
LIMIT 10;
"""

df= pd.read_sql(query, conn)

conn.close()
print(df)
plt.figure(figsize=(10, 5))
sns.barplot(data=df, x="Total_Revenue", y="Description", palette="Blues_d")
plt.title("Top 10 Products by Revenue")
plt.xlabel("Total Revenue ($)")
plt.ylabel("Product")
plt.tight_layout()
plt.show()
