import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse

def ingest_data(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name

    engine = create_engine(
        f"postgresql://{user}:{password}@{host}:{port}/{db}"
    )

    url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

    df_iter = pd.read_csv(
        url,
        iterator=True,
        chunksize=100000,
        parse_dates=[
            "tpep_pickup_datetime",
            "tpep_dropoff_datetime"
        ],
        low_memory=False
    )

    total_rows = 0

    for i, df in enumerate(df_iter):
        t_start = time()

        if i == 0:
            df.head(0).to_sql(
                name=table_name,
                con=engine,
                if_exists="replace",
                index=False
            )

        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="append",
            index=False
        )

        total_rows += len(df)

        t_end = time()

        print(
            f"Inserted chunk {i + 1}, rows: {len(df)}, "
            f"time: {t_end - t_start:.2f} seconds"
        )

    print(f"Inserted total rows: {total_rows}")


def main():
    parser = argparse.ArgumentParser(description="Ingest CSV data to PostgreSQL")

    parser.add_argument("--user", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", required=True)
    parser.add_argument("--db", required=True)
    parser.add_argument("--table_name", required=True)

    args = parser.parse_args()

    ingest_data(args)


if __name__ == "__main__":
    main()