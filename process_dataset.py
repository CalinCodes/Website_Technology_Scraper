import pandas as pd
import sqlite3

filename = "dataset.snappy.parquet"
df = pd.read_parquet(filename)

conn = sqlite3.connect("dataset.db")
df.to_sql("dataset", conn, if_exists="replace", index=False)
conn.close()
