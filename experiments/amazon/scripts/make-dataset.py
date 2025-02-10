import argparse
import os
import pyspark.sql.functions as F
from datasets import load_dataset
from pyspark.sql import SparkSession


SPLITS = {
    "train": "train",
    "validation": "val",
    "test": "test"
}


def parse_args():
    parser = argparse.ArgumentParser("Download, prepare and dump dataset to a parquet file.")
    parser.add_argument("--root", help="Dataset root", default="data")
    return parser.parse_args()


def dataset2spark(dataset, name, cache_dir):
    spark = SparkSession.builder.getOrCreate()
    path = os.path.join(cache_dir, f"convert-{name}.parquet")
    dataset.to_parquet(path)
    dataset = spark.read.parquet(path)
    return dataset


def dump_parquet(df, path, n_partitions):
    df.sort(F.col("id")).repartition(n_partitions, "id").write.mode("overwrite").parquet(path)


def main(args):
    cache_dir = os.path.join(args.root, "cache")
    if not os.path.isdir(args.root):
        os.mkdir(args.root)
    if not os.path.isdir(cache_dir):
        os.mkdir(cache_dir)
    collection = load_dataset("easytpp/amazon", cache_dir=cache_dir)
    for part, name in SPLITS.items():
        dataset = collection[part]
        df = dataset2spark(dataset, name, cache_dir)
        df = df.selectExpr("seq_idx as id",
                           "time_since_start as timestamps",
                           "type_event as labels").persist()
        path = os.path.join(args.root, f"{name}.parquet")
        n_partitions = 32 if part == "train" else 1
        print(f"Dump {name} with {df.count()} records and {n_partitions} partitions to {path}")
        dump_parquet(df, path, n_partitions=n_partitions)
    print("OK")


if __name__ == "__main__":
    spark = SparkSession.builder.getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    main(parse_args())
