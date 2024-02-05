import mysql.connector


def execute_sql_file(file_path, database_config):
    try:
        connection = mysql.connector.connect(**database_config)
        cursor = connection.cursor()

        # Read SQL file
        with open(file_path, 'r') as sql_file:
            sql_script = sql_file.read()

        # Execute SQL script
        cursor.execute(sql_script)
        connection.commit()

        print("SQL script executed successfully!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Specify MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'database': 'classicmodels'
}

# SQL file path assignment
sql_file_path = 'mysqlsampledatabase.sql'

# Execute SQL file
execute_sql_file(sql_file_path, db_config)
