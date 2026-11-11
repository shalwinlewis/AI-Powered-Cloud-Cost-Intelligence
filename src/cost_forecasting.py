
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = BASE_DIR / "datasets" / "daily_total_cost.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

# Load daily expenditure
df = pd.read_csv(DATA_PATH)

df["usage_date"] = pd.to_datetime(df["usage_date"])
df["total_daily_cost"] = pd.to_numeric(
    df["total_daily_cost"], errors="coerce"
)

df = df.dropna(
    subset=["usage_date", "total_daily_cost"]
)

df = df.sort_values("usage_date").reset_index(drop=True)

# Ensure every calendar day is represented
df = (
    df.set_index("usage_date")
      .asfreq("D")
)

if df["total_daily_cost"].isna().any():
    raise ValueError(
        "Missing daily costs found. Investigate missing dates "
        "before forecasting; do not automatically treat them as zero."
    )

df = df.reset_index()

df["day_number"] = np.arange(len(df))

# Create chronological training and test sets
split_index = int(len(df) * 0.8)

train = df.iloc[:split_index].copy()
test = df.iloc[split_index:].copy()

# Use day number as the time feature
train["day_number"] = np.arange(len(train))
test["day_number"] = np.arange(len(train), len(df))

X_train = train[["day_number"]]
y_train = train["total_daily_cost"]

X_test = test[["day_number"]]
y_test = test["total_daily_cost"]

# Train Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

# Moving average baseline
moving_average = y_train.tail(7).mean()

baseline_predictions = np.full(
    len(test), moving_average
)

# Evaluate both approaches
linear_mae = mean_absolute_error(
    y_test, predictions
)

moving_mae = mean_absolute_error(
    y_test, baseline_predictions
)

linear_rmse = np.sqrt(
    mean_squared_error(y_test, predictions)
)

moving_rmse = np.sqrt(
    mean_squared_error(y_test, baseline_predictions)
)

print("\n========== FORECAST MODEL EVALUATION ==========")

print("Training days:", len(train))
print("Testing days:", len(test))

print("\nLinear Regression")
print("MAE:", round(linear_mae, 2))
print("RMSE:", round(linear_rmse, 2))

print("\n7-Day Moving Average")
print("MAE:", round(moving_mae, 2))
print("RMSE:", round(moving_rmse, 2))


# Select the best model based on test MAE
if linear_mae <= moving_mae:
    selected_model_name = "Linear Regression"

    # Retrain using all 30 days
    final_model = LinearRegression()

    final_model.fit(
        df[["day_number"]],
        df["total_daily_cost"]
    )

else:
    selected_model_name = "7-Day Moving Average"
    final_model = None

print("\nSelected model:", selected_model_name)

# Forecast the next 7 days
future_days = np.arange(len(df), len(df) + 7)

if final_model is not None:

    future_costs = final_model.predict(
        pd.DataFrame({"day_number": future_days})
    )

else:

    # Use the latest 7 observed days
    moving_average = df["total_daily_cost"].tail(7).mean()

    future_costs = np.full(7, moving_average)

future_costs = np.maximum(future_costs, 0)

future_dates = pd.date_range(
    start=df["usage_date"].max() + pd.Timedelta(days=1),
    periods=7,
    freq="D"
)

forecast_df = pd.DataFrame({
    "forecast_date": future_dates,
    "predicted_daily_cost": np.round(future_costs, 2)
})

forecast_df.to_csv(
    OUTPUT_DIR / "cloud_cost_forecast.csv",
    index=False
)

historical_total = df["total_daily_cost"].sum()
forecast_total = forecast_df["predicted_daily_cost"].sum()

print("\nHistorical September expenditure:",
      round(historical_total, 2))

print("Next 7 days forecast:",
      round(forecast_total, 2))

print("\n7-Day forecast:")
print(forecast_df.to_string(index=False))

# Plot actual costs and forecast
plt.figure(figsize=(12, 6))

plt.plot(
    df["usage_date"],
    df["total_daily_cost"],
    marker="o",
    label="Historical expenditure"
)

plt.plot(
    forecast_df["forecast_date"],
    forecast_df["predicted_daily_cost"],
    marker="o",
    linestyle="--",
    label="Forecast expenditure"
)

plt.title("Cloud Cost Forecast")
plt.xlabel("Date")
plt.ylabel("Daily Cost (USD)")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "cloud_cost_forecast.png"
)

plt.show()

print("\nForecast files saved successfully!")
