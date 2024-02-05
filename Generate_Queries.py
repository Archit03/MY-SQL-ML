import random
import mysql.connector

# Specify your MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'database': 'classicmodels',
}

# List of tables in the database
tables = ['customers', 'employees', 'offices', 'orderdetails', 'orders', 'payments', 'productlines', 'products']

# Establish a connection to the database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor(buffered=True)


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
        #   Insert a single row with random values
        values = ', '.join([f"'{random.randint(1, 100)}'" for _ in column_names])
        query = f'INSERT INTO {table} ({", ".join(column_names)}) VALUES ({values});'
    elif query_type == 'UPDATE':
        # Update a random row with a random value
        set_clause = f'{random.choice(column_names)} = {random.randint(1, 100)}'
        query = f'UPDATE {table} SET {set_clause} WHERE {random.choice(column_names)} = {random.randint(1, 100)};'
    elif query_type == 'DELETE':
        # Delete a random row
        where_clause = f'{random.choice(column_names)} = {random.randint(1, 100)}'
        query = f'DELETE FROM {table} WHERE {where_clause};'

    return query


# Generate 50,000 random queries
for i in range(50001):
    query = generate_random_query()
    print(i, query)

# Close the database connection
connection.close()
