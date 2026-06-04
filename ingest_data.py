import pandas as pd
from sqlalchemy import create_engine
from time import time

engine = create_engine("postgresql://root:root@localhost:5432/ny_taxi")

prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'

df_iter = pd.read_csv(prefix + 'yellow_tripdata_2021-01.csv.gz', iterator=True, chunksize=100000)

total_rows = 0

for df_chunk in df_iter:
    t_start = time()
    df_chunk.tpep_pickup_datetime = pd.to_datetime(df_chunk.tpep_pickup_datetime)
    df_chunk.tpep_dropoff_datetime = pd.to_datetime(df_chunk.tpep_dropoff_datetime)
   
    df_chunk.to_sql(
    name="yellow_taxi_data",
    con=engine,
    if_exists="append",
    index=False
    )
    t_end = time()
    total_rows+=len(df_chunk)
    print(f'Inserted another chunk..., took {t_end - t_start:.3f} seconds')

print(f"Inserted {total_rows} rows")