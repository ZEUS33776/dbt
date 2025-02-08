from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQL Server connection settings matching dbt profile
SERVER = 'localhost'
PORT = '1433'
DATABASE = 'AdventureWorks2022'
DRIVER = 'ODBC Driver 18 for SQL Server'

# SQLAlchemy connection URL for SQL Server with Windows Authentication
SQLALCHEMY_DATABASE_URL = (
    f"mssql+pyodbc://{SERVER}:{PORT}/{DATABASE}?"
    f"driver={DRIVER}"
    "&trusted_connection=yes"
    "&Encrypt=no"  # Changed from encrypt=false to Encrypt=no
    "&TrustServerCertificate=yes"  # Changed Yes to yes for consistency
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # Set to False in production
    fast_executemany=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()