# Cloud Cost Forecasting

## Objective
Forecast short-term cloud expenditure using historical daily billing data.

## Dataset
- Period: September 1–30, 2024
- Historical expenditure: $2,027.76
- Number of daily observations: 30

## Models Evaluated

| Model | MAE | RMSE |
|---|---:|---:|
| Linear Regression | $33.59 | $37.40 |
| 7-Day Moving Average | $39.33 | $44.97 |

Linear Regression was selected based on its lower test MAE.

## Forecast Results

The selected model was retrained using all 30 September observations.

| Date | Forecast |
|---|---:|
| October 1 | $130.53 |
| October 2 | $134.59 |
| October 3 | $138.65 |
| October 4 | $142.71 |
| October 5 | $146.78 |
| October 6 | $150.84 |
| October 7 | $154.90 |
| **Total** | **$999.00** |

## Business Application
- Estimate short-term cloud expenditure.
- Support cloud budget planning.
- Identify potential spending increases.
- Help FinOps teams prepare for future expenditure.

## Limitations
- Only one month of historical data was available.
- The evaluation used six test observations.
- Linear Regression assumes a relatively consistent trend.
- Seasonal patterns and workload changes are not captured.
- Forecasts should be validated against additional months of actual billing data.