Data quality check	            Result
AWS records	                    94,351
Duplicate records	            0
Missing ResourceId	            8,453
Missing Tags	                31,270
Missing ServiceName	            0
Negative BilledCost records	    282
Negative EffectiveCost records	87


### Billed Cost vs Effective Cost Inconsistency

An additional billing consistency assessment identified records with positive `BilledCost` but zero `EffectiveCost`.

**Assessment results:**

| Metric | Result |
|---|---:|
| Total usage records | 94,060 |
| Affected records | 61,246 |
| Affected percentage | 65.11% |
| Total billed cost | $2,027.75 |
| Billed cost associated with affected records | $648.64 |

**Finding:** The inconsistency occurs across multiple cloud services, including Amazon EC2, Amazon RDS, Amazon VPC, Elastic Load Balancing and Amazon CloudWatch.

**Impact:** Effective-cost-based reporting may underrepresent expenditure for the affected records.

**Recommendation:** Use `BilledCost` for billed expenditure analysis in this project. Flag the inconsistency for further validation rather than assuming that the difference represents discounts or realized savings.