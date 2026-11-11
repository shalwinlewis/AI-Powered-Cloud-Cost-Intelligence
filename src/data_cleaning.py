
import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv(
    "datasets/focus_sample_100000.csv",
    low_memory=False
)

# Filter AWS
aws_df = df[df["ProviderName"] == "AWS"].copy()

print("\n========== DATA QUALITY REPORT ==========")

# 1. Missing values
print("\n1. MISSING VALUES")

missing = aws_df.isnull().sum()

missing_report = pd.DataFrame({
    "Missing_Count": missing,
    "Missing_Percentage": (
        missing / len(aws_df) * 100
    ).round(2)
})

print(
    missing_report[
        missing_report["Missing_Count"] > 0
    ].sort_values(
        "Missing_Percentage",
        ascending=False
    )
)

# 2. Duplicate records
print("\n2. DUPLICATE RECORDS")

print("Duplicates:", aws_df.duplicated().sum())

# 3. Negative billing values
print("\n3. NEGATIVE COST RECORDS")

print(
    "Negative BilledCost:",
    (aws_df["BilledCost"] < 0).sum()
)

print(
    "Negative EffectiveCost:",
    (aws_df["EffectiveCost"] < 0).sum()
)

# 4. Currency analysis
print("\n4. BILLING CURRENCIES")

print(aws_df["BillingCurrency"].value_counts())

# 5. Date validation
print("\n5. DATE VALIDATION")

date_columns = [
    "BillingPeriodStart",
    "BillingPeriodEnd",
    "ChargePeriodStart",
    "ChargePeriodEnd"
]

for col in date_columns:
    aws_df[col] = pd.to_datetime(
        aws_df[col],
        errors="coerce",
        utc=True
    )

    print(
        col,
        "Invalid dates:",
        aws_df[col].isna().sum()
    )

# 6. Missing resource information
print("\n6. RESOURCE INFORMATION")

print(
    "Missing Resource IDs:",
    aws_df["ResourceId"].isna().sum()
)

print(
    "Missing Service Names:",
    aws_df["ServiceName"].isna().sum()
)

# 7. Service analysis
print("\n7. SERVICE DISTRIBUTION")

print(
    aws_df["ServiceName"].value_counts().head(10)
)

print("\nDATA QUALITY ASSESSMENT COMPLETED!")
