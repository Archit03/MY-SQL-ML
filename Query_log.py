import random
import mysql.connector
import logging
import time
import pandas as pd

# Specify  MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'database': 'classicmodels',
}

# Set up logging
logging.basicConfig(filename='query_logs.csv', level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')

# List of tables in the database
tables = ['customers', 'employees', 'offices', 'orderdetails', 'orders', 'payments', 'productlines', 'products']

# Establish a connection to the database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# DataFrames to store metrics
df_list = []


# Function to fetch a row from each table to populate column names
def fetch_column_names():
    for table in tables:
        cursor.execute(f'SELECT * FROM {table} LIMIT 1;')
        cursor.fetchall()  # Fetch and discard the result


fetch_column_names()  # Fetch at least one row from each table


# Function to generate a random query
def generate_random_query():
    table = random.choice(tables)

    # Fetch column names for the selected table
    cursor.execute(f'SELECT * FROM {table} LIMIT 1;')
    column_names = [desc[0] for desc in cursor.description]

    # Initialize query variable
    query = ''

    # Generate a random query type
    query_type = random.choice(['SELECT', 'INSERT', 'UPDATE', 'DELETE'])

    if query_type == 'SELECT':
        query = f'SELECT * FROM {table} LIMIT 1;'
    elif query_type == 'INSERT':
        # For simplicity, insert a single row with random values
        values = ', '.join([f"'{random.randint(1, 100)}'" for _ in column_names])
        query = f'INSERT INTO {table} ({", ".join(column_names)}) VALUES ({values});'
    elif query_type == 'UPDATE':
        # For simplicity, update a random row with a random value
        set_clause = f'{random.choice(column_names)} = {random.randint(1, 100)}'
        query = f'UPDATE {table} SET {set_clause} WHERE {random.choice(column_names)} = {random.randint(1, 100)};'
    elif query_type == 'DELETE':
        # For simplicity, delete a random row
        where_clause = f'{random.choice(column_names)} = {random.randint(1, 100)}'
        query = f'DELETE FROM {table} WHERE {where_clause};'

    return query, query_type


# Generate and execute 50,000 random queries
for i in range(50000):
    query, query_type = generate_random_query()

    # Execute the query and log the execution time and outcome
    start_time = time.time()
    try:
        cursor.execute(query)
        connection.commit()
        outcome = 'success'
    except Exception as e:
        connection.rollback()
        outcome = f'failure: {str(e)}'
    end_time = time.time()

    execution_time = (end_time - start_time) * 1000
    logging.info(f'{query} [{execution_time:.2f} ms] [{outcome}]')

    # Append data to DataFrame list
    df_list.append(pd.DataFrame({'Execution Time': [execution_time], 'QueryType': [query_type], 'Queries': [query]}))

# Concatenate DataFrames
df = pd.concat(df_list, ignore_index=True)

# Save DataFrame to a single CSV file
df.to_csv('query_logs_df.csv', index=False)

# Close the database connection
connection.close()
