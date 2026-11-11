
# 07 – EC2 Resource Analysis

## 1. Objective
Analyze AWS EC2 resource inventory to understand
resource distribution and prepare for billing
reconciliation.

## 2. Dataset Overview
- Total EC2 resources: 2,232
- Unique Resource IDs: 2,232
- Resource Type: EC2 Instance
- AWS Regions: 14
- Missing Values: 0
- Duplicate Records: 0

## 3. Key Findings
- US East (N. Virginia) contains 1,506 instances.
- US West (Oregon) contains 249 instances.
- EU (Frankfurt) contains 182 instances.
- Approximately 67.5% of resources are located
  in N. Virginia.

## 4. Data Quality
- No duplicate Resource IDs.
- No missing values.
- All records have valid resource identifiers,
  region names and resource types.

## 5. FinOps Implications
- Investigate high resource concentration in
  N. Virginia.
- Compare resource inventory with billing records.
- Identify resources without corresponding
  billing entries.
- Investigate resource-level spending.

## 6. Conclusion
The EC2 inventory dataset contains 2,232 unique
resources with complete information. It is ready
for reconciliation with AWS billing records.

### EC2 Billing Reconciliation – US East (N. Virginia)

The regional EC2 billing analysis initially showed a difference between resource-level expenditure and total regional expenditure.

Further investigation identified three components:

- Matched resource-level billing: $1,414.35
- Unmatched billing records: $48.70
- Account-level promotional credits without ResourceId: -$1,138.71

The promotional credits were classified as `Credit` under the charge description `AWS Open Source Promotional Credits`.

After accounting for these three components, the reconciled regional billed cost was $324.34.

**FinOps Insight:** Account-level promotional credits can substantially reduce net cloud expenditure. Since these credits do not have individual resource IDs, they should be analysed separately rather than attributed directly to individual EC2 instances.