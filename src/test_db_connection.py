
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# Load environment variables
load_dotenv()

# Read database credentials
connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME")
)

# Create database engine
engine = create_engine(connection_url)

# Test connection
try:
    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT current_database(), version()")
        )

        database, version = result.fetchone()

        print("Connection successful!")
        print("Database:", database)
        print("PostgreSQL version:", version)

except Exception as e:
    print("Connection failed!")
    print("Error:", e)
