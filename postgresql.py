import psycopg2
import pandas as pd

class postgresqlconnection:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = None

    def getConnection(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return self.conn
        except Exception as e:
            print(f"Error connecting to PostgreSQL: {e}")
            raise e

    def getdata(self, tableName):
        try:
            conn = self.getConnection()
            query = f"SELECT * FROM {tableName}"
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df.to_dict('records')
        except Exception as e:
            print(f"Error retrieving data: {e}")
            raise e
def save_prediction(self, data_tuple):
    try:
        conn = self.getConnection()
        cursor = conn.cursor()
        # Ensure the column names match your database table exactly
        query = """INSERT INTO ml_task (temperature, ws, ffmc, dmc, isi, prediction) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, data_tuple)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error saving data: {e}")
# Method to store the web inputs and the prediction result
    def insert_prediction(self, data_tuple):
        try:
            conn = self.getConnection()
            cursor = conn.cursor()
            
            # FIX: Target the new dedicated table
            query = """INSERT INTO prediction_logs (temperature, ws, ffmc, dmc, isi, prediction) 
                       VALUES (%s, %s, %s, %s, %s, %s)"""
                       
            cursor.execute(query, data_tuple)
            conn.commit()
            cursor.close()
            conn.close()
            print("Entry stored in database successfully.")
        except Exception as e:
            print(f"Error saving to database: {e}")# Method to store the web inputs and the prediction result
    def insert_prediction(self, data_tuple):
        try:
            conn = self.getConnection()
            cursor = conn.cursor()
            
            # FIX: Target the new dedicated table
            query = """INSERT INTO prediction_logs (temperature, ws, ffmc, dmc, isi, prediction) 
                       VALUES (%s, %s, %s, %s, %s, %s)"""
                       
            cursor.execute(query, data_tuple)
            conn.commit()
            cursor.close()
            conn.close()
            print("Entry stored in database successfully.")
        except Exception as e:
            print(f"Error saving to database: {e}")