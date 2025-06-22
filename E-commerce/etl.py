import pandas as pd
import mysql.connector
from datetime import datetime

file_path = "data/data.csv"

df= pd.read_csv(file_path, encoding='ISO-8859-1')


#Loading and Inspecting Data
print(" Data loaded successfully.")
print(f"Total rows:{df.shape[0]}, Total columns:{df.shape[1]}")
print("\nColumns:")
print(df.columns.tolist())
print("\nSample Data:")
print(df.head())
print("\nMissing Values:")
print(df.isnull().sum())

#Transform the Data(Clean and Prepare for MySQL)

df= df.dropna(subset=['CustomerID'])
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

df['Total'] = df['Quantity'] * df['UnitPrice']
df.columns = df.columns.str.replace(' ','_')
df.columns = df.columns.str.strip()
print(df.head())
print(df.dtypes)

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="ecommerce_db",
)

cursor = conn.cursor()
print("Connected to MySQL")

for _, row in df.iterrows():
    sql = """
        INSERT INTO ecommerce_orders 
        (InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country, Total)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        row.InvoiceNo,
        row.StockCode,
        row.Description,
        int(row.Quantity),
        row.InvoiceDate.to_pydatetime(),
        float(row.UnitPrice),
        int(row.CustomerID),
        row.Country,
        float(row.Total)
    )
    cursor.execute(sql, values)
conn.commit()
print("Data inserted successfully.")
cursor.close()
conn.close()
