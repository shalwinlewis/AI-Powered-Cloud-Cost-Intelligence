
import os
import pandas as pd

from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# ==========================================
# 1. PROJECT CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[1]

load_dotenv(BASE_DIR / ".env")

CSV_PATH = BASE_DIR / "datasets" / "focus_sample_100000.csv"

# ==========================================
# 2. DATABASE CONNECTION
# ==========================================

connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME")
)

engine = create_engine(
    connection_url,
    pool_pre_ping=True
)

# ==========================================
# 3. EXTRACT DATA
# ==========================================

print("\n========== EXTRACTING DATA ==========")

df = pd.read_csv(
    CSV_PATH,
    low_memory=False
)

print("Total records extracted:", len(df))

# ==========================================
# 4. TRANSFORM DATA
# ==========================================

print("\n========== TRANSFORMING DATA ==========")

# Filter AWS billing records
aws_df = df[
    df["ProviderName"]
    .astype("string")
    .str.strip()
    .str.casefold()
    .eq("aws")
].copy()

print("AWS records:", len(aws_df))

# Preserve original FOCUS billing values.
# Do not remove negative costs or missing values.

# ==========================================
# 5. LOAD DATA INTO POSTGRESQL
# ==========================================

print("\n========== LOADING INTO POSTGRESQL ==========")

table_name = "cloud_billing"

try:
    with engine.begin() as connection:

        aws_df.to_sql(
            name=table_name,
            con=connection,
            schema="public",
            if_exists="replace",
            index=False,
            chunksize=5000
        )

    print("Data successfully loaded!")

except Exception as e:
    print("ETL loading failed:", e)
    raise

# ==========================================
# 6. VALIDATE DATABASE RECORDS
# ==========================================

print("\n========== DATABASE VALIDATION ==========")

with engine.connect() as connection:

    result = connection.execute(
        text("""
            SELECT
                COUNT(*) AS total_records,
                SUM("BilledCost") AS total_billed_cost
            FROM public.cloud_billing
        """)
    )

    row = result.fetchone()

    print("Records in PostgreSQL:", row[0])
    print("Total billed cost:", row[1])

# ==========================================
# 7. COMPLETION
# ==========================================

print("\n===================================")
print("ETL PIPELINE COMPLETED SUCCESSFULLY")
print("===================================")

engine.dispose()
