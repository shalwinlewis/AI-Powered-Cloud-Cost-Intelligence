
import pandas as pd
import numpy as np
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = BASE_DIR / "datasets" / "daily_service_costs.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

# Load billing data
df = pd.read_csv(DATA_PATH)

df["usage_date"] = pd.to_datetime(df["usage_date"])
df["daily_cost"] = pd.to_numeric(df["daily_cost"], errors="coerce")

df = df.dropna(subset=["usage_date", "ServiceName", "daily_cost"])

# Aggregate service-level daily expenditure
df = (
    df.groupby(["usage_date", "ServiceName"], as_index=False)
    ["daily_cost"].sum()
)

anomalies = []

# Analyse each service independently
for service, group in df.groupby("ServiceName"):

    group = group.sort_values("usage_date").copy()
    costs = group["daily_cost"]

    if len(costs) < 7:
        continue

    median_cost = costs.median()
    mad = np.median(np.abs(costs - median_cost))

    if mad > 0:
        group["anomaly_score"] = (
            0.6745 * (costs - median_cost) / mad
        )

        detected = group[group["anomaly_score"] > 3.5]

    else:
        std = costs.std()

        if std == 0 or pd.isna(std):
            continue

        group["anomaly_score"] = (
            (costs - costs.mean()) / std
        )

        detected = group[group["anomaly_score"] > 2.5]

    if not detected.empty:
        anomalies.append(detected)

# Combine statistical anomalies
if anomalies:
    result = pd.concat(anomalies, ignore_index=True)
else:
    result = pd.DataFrame(
        columns=[
            "usage_date",
            "ServiceName",
            "daily_cost",
            "anomaly_score"
        ]
    )

# Classify financial significance
if not result.empty:

    result["severity"] = np.select(
        [
            result["daily_cost"] >= 10,
            result["daily_cost"] >= 5,
            result["daily_cost"] >= 1
        ],
        [
            "High",
            "Medium",
            "Low"
        ],
        default="Informational"
    )

    # Prioritize anomalies with at least $1 expenditure
    significant = result[
        result["daily_cost"] >= 1
    ].copy()

    significant = significant.sort_values(
        ["daily_cost", "anomaly_score"],
        ascending=False
    )

else:
    significant = result.copy()
    significant["severity"] = pd.Series(dtype="object")

# Save both reports
result.to_csv(
    OUTPUT_DIR / "all_statistical_anomalies.csv",
    index=False
)

significant.to_csv(
    OUTPUT_DIR / "financially_significant_anomalies.csv",
    index=False
)

# Display summary
print("\n========== FINOPS ANOMALY REPORT ==========")

print("Total billing records:", len(df))
print("Services analysed:", df["ServiceName"].nunique())
print("Statistical anomalies:", len(result))
print("Financially significant anomalies:", len(significant))

if not significant.empty:
    print("\nPrioritized anomalies:")
    print(significant.to_string(index=False))

print("\nReports saved successfully in outputs folder.")
