
import pandas as pd
import numpy as np

# Load complete dataset
df = pd.read_csv(
    "datasets/focus_sample_100000.csv",
    low_memory=False
)

# Filter AWS records
aws_df = df[
    df["ProviderName"] == "AWS"
].copy()

# Dataset overview
print("========== DATASET OVERVIEW ==========")

print("Total records:", len(df))
print("AWS records:", len(aws_df))
print("Total columns:", len(aws_df.columns))

# Column information
print("\n========== COLUMN NAMES ==========")
print(aws_df.columns.tolist())

# Dataset structure
print("\n========== DATA TYPES ==========")
print(aws_df.dtypes)

# First five records
print("\n========== SAMPLE DATA ==========")
print(aws_df.head())

# Statistical summary
print("\n========== STATISTICAL SUMMARY ==========")
print(aws_df.describe(include="all"))
