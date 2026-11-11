
import os
import pandas as pd

from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# Project directory
BASE_DIR = Path(__file__).resolve().parents[1]

# Load credentials
load_dotenv(BASE_DIR / ".env")

# Database connection
connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME")
)

engine = create_engine(connection_url, pool_pre_ping=True)

# Load EC2 inventory
csv_path = BASE_DIR / "datasets" / "ec2_resources.csv"

ec2_df = pd.read_csv(csv_path)

# Validate required columns
required_columns = [
    "ResourceId",
    "RegionName",
    "ResourceType",
    "ServiceName"
]

if not all(col in ec2_df.columns for col in required_columns):
    raise ValueError("Required columns are missing!")

# Remove duplicate resource IDs if any
ec2_df = ec2_df.drop_duplicates(subset=["ResourceId"])

# Load into PostgreSQL
ec2_df.to_sql(
    name="ec2_inventory",
    con=engine,
    schema="public",
    if_exists="replace",
    index=False
)

print("EC2 inventory successfully loaded!")
print("Total records:", len(ec2_df))

engine.dispose()
