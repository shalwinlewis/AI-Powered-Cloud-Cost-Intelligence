# Cloud Cost Anomaly Detection

## Objective
Identify unusual daily cloud expenditure patterns and prioritize anomalies based on their financial impact.

## Methodology
- Used Python and Pandas to analyse daily service-level billing data.
- Applied Median Absolute Deviation (MAD) to identify statistical anomalies.
- Used a statistical anomaly score to rank unusual expenditure.
- Introduced financial severity categories to prioritize investigation.

## Results

| Metric | Result |
|---|---:|
| Billing records | 935 |
| Services analysed | 48 |
| Statistical anomalies | 36 |
| Financially significant anomalies | 9 |

## Major Finding: Amazon CloudWatch

- Date: September 26, 2024
- Daily billed cost: $21.03
- Custom log ingestion: 41.0165 GB
- Custom log ingestion cost: $20.51
- Region: US East (N. Virginia)

Custom log ingestion accounted for approximately 97.5% of the day's CloudWatch expenditure.

## Recommendations
- Investigate unusually high log ingestion.
- Review application logging levels and duplicate events.
- Monitor daily expenditure by cloud service.
- Introduce financial thresholds for anomaly prioritization.
- Investigate recurring cost anomalies before recommending optimization.

## Limitations
- The dataset covers only September 2024.
- Statistical anomalies do not automatically indicate waste or incorrect billing.
- Financial severity thresholds are project-defined.
- Billing data identifies cost drivers but does not always reveal operational root causes.
- Operational metrics are needed to confirm the underlying causes of anomalies.