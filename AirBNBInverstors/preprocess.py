import pandas as pd

def load_clean_data(file_path= "data/listings.csv"):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip().str.lower()
    print("Columns:", df.columns.tolist())
    df = df.dropna(subset=["latitude","longitude","price", "availability_365"])
    df['price']= df['price'].replace(r'[\$,]',"",regex=True).astype(float)
    df = df[(df['price']>10) & (df['price']<1000)]
    df['occupancy_rate'] = df['availability_365']/365 *100
    print("Cleaned rows:", len(df))
    return df
