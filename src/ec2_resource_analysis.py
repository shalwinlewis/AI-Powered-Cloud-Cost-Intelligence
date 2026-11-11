
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

# Load EC2 resource dataset
ec2_df = pd.read_csv("datasets/ec2_resources.csv")

print("========== EC2 RESOURCE ANALYSIS ==========")

# 1. Total resources
print("\nTotal EC2 resources:", len(ec2_df))

# 2. Resources by region
print("\n========== RESOURCES BY REGION ==========")
print(ec2_df["RegionName"].value_counts())

# 3. Resource types
print("\n========== RESOURCE TYPES ==========")
print(ec2_df["ResourceType"].value_counts(dropna=False))

# 4. Check duplicate IDs
print("\nDuplicate Resource IDs:",
      ec2_df["ResourceId"].duplicated().sum())

# 5. Missing values
print("\n========== MISSING VALUES ==========")
print(ec2_df.isnull().sum())

print("\nEC2 RESOURCE ANALYSIS COMPLETED!")
