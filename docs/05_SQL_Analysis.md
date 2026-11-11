# 05 – SQL-Based FinOps Analysis

## 1. Objective

PostgreSQL was used to perform financial analysis, cost allocation and resource-level investigations on the AWS FOCUS billing dataset.

## 2. Service-wise Cost Analysis

**SQL concepts used:** GROUP BY, SUM(), ORDER BY, LIMIT.

**Objective:** Identify the highest-cost AWS services.

**Finding:** EC2 emerged as the dominant service in the initial analysis.

## 3. Environment Cost Allocation

**SQL concepts used:** JSON extraction, GROUP BY, SUM().

**Objective:** Compare development and production cloud expenditure.

**Finding:** Development expenditure was higher than production expenditure.

## 4. Business Unit Cost Allocation

**SQL concepts used:** JSON extraction, GROUP BY, COUNT(), SUM().

**Objective:** Allocate cloud expenditure across business units.

**Finding:** Identified business units contributing to cloud expenditure.

## 5. Resource Tagging Analysis

**Objective:** Identify the financial impact of missing resource tags.

**Finding:**
- Records without tags: 31,270
- Percentage without tags: 33.14%
- Net billed cost of untagged records: -$1,047.31

**Recommendation:** Improve resource tagging and cost allocation practices.

## 6. Promotional Credit Investigation

**Objective:** Investigate negative EC2 billing records.

**Finding:**
- Credit records: 134
- Credit amount: -$1,163.57
- Charge category: Credit
- Charge frequency: One-Time
- Description: AWS Open Source Promotional Credits

**Conclusion:** Negative billing entries were identified as promotional credits rather than evidence of wasted EC2 resources.

## 7. Resource-Level Cost Analysis

**Objective:** Identify expensive EC2 resources and understand resource distribution.

**Finding:**
- EC2 instances identified: 2,084
- EBS volumes identified: 5,026
- Records with missing ResourceType were also investigated.

## 8. Missing Resource Investigation

**Objective:** Investigate EC2 records without ResourceId.

**Finding:**
- Total records: 136
- Credit records: 134
- Tax records: 2

**Conclusion:** Missing resource identifiers were associated with credits and tax entries rather than unidentified positive-cost usage records.

## 9. Conclusion

SQL analysis helped investigate cloud expenditure, promotional credits, resource allocation, tagging gaps and resource-level costs.

These findings will be used as inputs for the next stage of the FinOps optimization solution.