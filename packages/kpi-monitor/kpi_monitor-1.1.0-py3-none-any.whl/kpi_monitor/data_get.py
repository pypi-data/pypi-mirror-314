#!/usr/bin/env python3

# Import modules
#!/usr/bin/env python3

# Import modules
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os
import csv

# Get the root directory where the project is located
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Set the path relative to the root directory
output_dir = os.path.join(base_dir, 'data', 'raw')

# Ensure the directory exists
os.makedirs(output_dir, exist_ok=True)

# Load environment variables from the .env file
load_dotenv()

# Retrieve the credentials from environment variables
db_host = os.getenv("DB_HOST")
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Example use case: print the DB credentials (make sure to handle this securely in production)
print(f"Connecting to database at {db_host} with user {db_username}")

# Initialize connection variable
connection = None

try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(
        host=db_host,      # Your DB host
        user=db_username,    # Your DB username
        password=db_password, # Your DB password
        dbname=db_name,  # Your database name
        port=5432,        # The port (default for PostgreSQL is 5432)
        connect_timeout=30 # Connection timeout in seconds
    )
    print("Connection successful")
    
    cursor = connection.cursor()
    
    # Query price data
    schemas = ['marketdata', 'brokerage']  # Replace with your schema name
    tables = ['fcr_clearing_price', 'bids_event']    # Replace with your table name

    for i in range(len(schemas)):

        schema_name = schemas[i]
        table_name = tables[i]

        query = f"SELECT * FROM {schema_name}.{table_name};"
        cursor.execute(query)
        
        # Fetch all rows
        rows = cursor.fetchall()
        
        # Get column names
        column_names = [desc[0] for desc in cursor.description]
        
        # Save to CSV
        csv_file_path = os.path.join(output_dir, f"{table_name}.csv")

        with open(csv_file_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(column_names)  # Write column headers
            writer.writerows(rows)         # Write all rows

        print(f"Data successfully saved to {csv_file_path}")

except OperationalError as e:
    print("Error while connecting to PostgreSQL:", e)

finally:
    # Only close the connection if it was successfully established
    if connection:
        connection.close()
        print("Connection closed")

# src/kpi_monitor/data_get.py

def main():
    # Your code to fetch data
    print("Fetching data...")

if __name__ == "__main__":
    main()