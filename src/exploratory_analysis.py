
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv(
    "datasets/focus_sample_100000.csv",
    low_memory=False
)

# Filter AWS
aws_df = df[
    df["ProviderName"] == "AWS"
].copy()

print("========== SERVICE-WISE COST ANALYSIS ==========")

service_analysis = (
    aws_df.groupby("ServiceName")
    .agg(
        Total_Billed_Cost=("BilledCost", "sum"),
        Total_Effective_Cost=("EffectiveCost", "sum"),
        Record_Count=("ServiceName", "size")
    )
    .sort_values(
        "Total_Billed_Cost",
        ascending=False
    )
)

print(service_analysis.head(10))

# Top 10 services visualization
top_services = service_analysis.head(10)

plt.figure(figsize=(12, 6))

top_services["Total_Billed_Cost"].sort_values().plot(
    kind="barh"
)

plt.title("Top 10 AWS Services by Billed Cost")
plt.xlabel("Billed Cost (USD)")
plt.ylabel("AWS Services")

plt.tight_layout()
plt.savefig("top_10_services.png")
plt.show()


print("\n========== RESOURCE-LEVEL COST ANALYSIS ==========")

resource_analysis = (
    aws_df.dropna(subset=["ResourceId"])
    .groupby(
        ["ResourceId", "ServiceName"]
    )
    .agg(
        Total_Cost=("BilledCost", "sum"),
        Record_Count=("ResourceId", "size")
    )
    .sort_values(
        "Total_Cost",
        ascending=False
    )
)

print(resource_analysis.head(10))


print("\n========== REGION-WISE COST ANALYSIS ==========")

region_analysis = (
    aws_df.groupby("RegionName")
    .agg(
        Total_Cost=("BilledCost", "sum"),
        Record_Count=("RegionName", "size")
    )
    .sort_values(
        "Total_Cost",
        ascending=False
    )
)

print(region_analysis.head(10))

# Visualization
region_analysis["Total_Cost"].head(10).plot(
    kind="bar",
    figsize=(10, 5)
)

plt.title("AWS Cost by Region")
plt.xlabel("Region")
plt.ylabel("Billed Cost (USD)")
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig("region_cost.png")
plt.show()



print("\n========== ENVIRONMENT COST ANALYSIS ==========")

import json

# Step 1: Extract environment tags
def extract_tag(tag_string, key):
    try:
        tags = json.loads(tag_string)
        return tags.get(key)
    except (TypeError, ValueError):
        return None

aws_df["Environment"] = aws_df["Tags"].apply(
    lambda x: extract_tag(x, "environment")
)

# Step 2: Separate positive and negative costs
aws_df["Cost_Type"] = np.where(
    aws_df["BilledCost"] < 0,
    "Credit / Adjustment",
    "Positive Charge"
)

# Step 3: Group costs
environment_analysis = (
    aws_df.groupby(
        ["Environment", "Cost_Type"],
        dropna=False
    )["BilledCost"]
    .sum()
    .unstack(fill_value=0)
)

print(environment_analysis)

# Step 4: Calculate net expenditure
environment_analysis["Net_Cost"] = (
    environment_analysis.sum(axis=1)
)

print("\nNet environment expenditure:")
print(
    environment_analysis[["Net_Cost"]]
    .sort_values("Net_Cost", ascending=False)
)

# Step 5: Visualize
environment_analysis[
    ["Positive Charge", "Credit / Adjustment"]
].plot(
    kind="bar",
    figsize=(10, 6)
)

plt.title("AWS Environment Cost Breakdown")
plt.xlabel("Environment")
plt.ylabel("Billed Cost (USD)")
plt.xticks(rotation=0)
plt.axhline(y=0, linewidth=0.8)

plt.tight_layout()
plt.savefig("environment_cost_improved.png")
plt.show()



print("\n========== TAGGING ANALYSIS ==========")

total_cost = aws_df["BilledCost"].sum()

missing_tag_df = aws_df[
    aws_df["Tags"].isna()
    | (aws_df["Tags"].astype(str).str.strip() == "")
]

missing_tag_cost = missing_tag_df["BilledCost"].sum()

missing_tag_percentage = (
    len(missing_tag_df) / len(aws_df)
) * 100

print("Total AWS cost:", total_cost)

print("Records without tags:", len(missing_tag_df))

print("Cost without tags:", missing_tag_cost)

print(
    "Percentage of records without tags:",
    round(missing_tag_percentage, 2),
    "%"
)

print(
    "Share of net billed cost without tags:",
    round(
        (missing_tag_cost / total_cost) * 100,
        2
    ),
    "%"
)



print("\n========== TAGGING COST ANALYSIS ==========")

aws_df["Tag_Status"] = np.where(
    aws_df["Tags"].isna(),
    "Missing Tags",
    "Tags Present"
)

tag_analysis = (
    aws_df.groupby("Tag_Status")
    .agg(
        Record_Count=("BilledCost", "size"),
        Net_Billed_Cost=("BilledCost", "sum"),
        Positive_Cost=(
            "BilledCost",
            lambda x: x[x > 0].sum()
        ),
        Negative_Adjustments=(
            "BilledCost",
            lambda x: x[x < 0].sum()
        )
    )
)

print(tag_analysis)

print("\nPercentage of records without tags:")

missing_percentage = (
    (aws_df["Tag_Status"] == "Missing Tags").mean()
    * 100
)

print(round(missing_percentage, 2), "%")
