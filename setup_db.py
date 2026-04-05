import pandas as pd
from sqlalchemy import create_engine
import psycopg2

print("Starting Database Setup...")

# 1. Restore historical data using Pandas + SQLAlchemy
try:
    engine = create_engine('postgresql://postgres:root@localhost:5432/fire_db')
    file_path = r"C:\Users\MSI\Documents\ai projects\forest-fire-prediction-main\dataset\Algerian_forest_fires_dataset_UPDATE.csv"
    
    # Read CSV and skip the broken title row
    df = pd.read_csv(file_path, header=1)
    
    # Force all columns to lowercase and strip spaces
    df.columns = df.columns.str.strip().str.lower()
    
    # Upload back to Postgres
    df.to_sql('ml_task', engine, if_exists='replace', index=False)
    print("✅ Historical dataset successfully restored to 'ml_task' table.")
except Exception as e:
    print(f"❌ Failed to restore CSV: {e}")

# 2. Create the prediction log table using psycopg2
try:
    conn = psycopg2.connect(host='localhost', database='fire_db', user='postgres', password='root')
    cursor = conn.cursor()
    
    # Create a separate table just for the website data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prediction_logs (
            id SERIAL PRIMARY KEY,
            temperature FLOAT,
            ws FLOAT,
            ffmc FLOAT,
            dmc FLOAT,
            isi FLOAT,
            prediction FLOAT
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Created 'prediction_logs' table for saving web inputs.")
except Exception as e:
    print(f"❌ Failed to create prediction_logs table: {e}")