# 04 – Exploratory Data Analysis (EDA) Findings

## 1. Objective

The objective of EDA is to understand AWS cloud expenditure patterns and identify services, regions and environments contributing significantly to cloud costs.

## 2. Service-wise Cost Analysis

**Observation:**
Amazon Elastic Compute Cloud (EC2) emerged as the highest-cost service in the initial service analysis.

**Finding:**
EC2 recorded approximately $593.44 in billed cost.

**Business Insight:**
EC2 expenditure should be investigated further to identify potential resource optimization opportunities.

## 3. Region-wise Cost Analysis

**Observation:**
US East (N. Virginia) recorded the highest regional expenditure in the initial analysis.

**Business Insight:**
Regional expenditure should be monitored to understand geographical cost distribution and potential opportunities for optimization.

## 4. Environment-wise Cost Analysis

**Observation:**
Development expenditure was considerably higher than production expenditure in the initial environment analysis.

**Business Insight:**
Non-production resources should be investigated for unnecessary running hours and potential scheduling opportunities.

## 5. Resource Tagging Analysis

**Observation:**
31,270 AWS records were missing tags, representing 33.14% of AWS billing records.

**Business Insight:**
Missing tags create difficulties in allocating cloud expenditure to departments, applications and business units.

**Recommendation:**
Implement mandatory resource-tagging policies.

## 6. Business Unit Cost Allocation

Cloud expenditure was grouped by business unit using resource tags.

**Objective:**
Understand how cloud expenditure is distributed across different business units.

**Business Insight:**
Business-unit-level allocation helps organizations identify departments responsible for cloud expenditure.

## 7. Summary of EDA Findings

1. EC2 was the dominant service in the initial cost analysis.
2. US East (N. Virginia) had the highest regional expenditure.
3. Development expenditure was higher than production expenditure.
4. 33.14% of AWS billing records had missing tags.
5. Business-unit allocation provides visibility into departmental expenditure.

## 8. Conclusion

The exploratory analysis provided an understanding of AWS expenditure patterns and highlighted opportunities for improved cost allocation, resource monitoring and cloud cost optimization.

### CloudWatch Cost Anomaly — September 26, 2024

**Anomaly detected:** Python-based statistical anomaly detection identified an unusual increase in Amazon CloudWatch expenditure on September 26, 2024.

**Financial impact:**
- Daily CloudWatch billed cost: $21.03
- Custom log ingestion cost: $20.51
- Log ingestion volume: 41.0165 GB
- Log ingestion price: $0.50 per GB

**Root billing driver:** Custom log data ingestion in US East (N. Virginia) accounted for approximately 97.5% of the day's CloudWatch expenditure.

**Comparison:** The next-highest daily custom log ingestion volume was 0.1680 GB on September 4, substantially lower than the September 26 volume.

**FinOps recommendation:** Investigate application logging behaviour, excessive debug logs, duplicate events and retention settings. Introduce appropriate log filtering and ingestion monitoring.

**Limitation:** Billing data identifies the cost driver but does not establish why the log volume increased. Operational logs and application monitoring data would be required to confirm the underlying cause.