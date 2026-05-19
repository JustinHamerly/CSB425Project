import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os

def main() -> None:
    cleaned_df = pd.read_csv("data/cleaned/cleaned_data.csv")

    print(f"Row count: {cleaned_df.shape[0]}")
    print(f"Column count: {cleaned_df.shape[1]}")
    print(f"Data types:\n{cleaned_df.dtypes}")

    table = pa.Table.from_pandas(cleaned_df)

    pq.write_to_dataset(table, root_path="data/processed", partition_cols=["subject"])

    partition_folders = [f for f in os.listdir("data/processed") if os.path.isdir(os.path.join("data/processed", f))]
    print(f"Partition folders created: {partition_folders}")

if __name__ == "__main__":
    main()