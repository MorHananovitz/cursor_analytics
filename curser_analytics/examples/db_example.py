"""
Database Connection Example

This script demonstrates how to use the database connection module to connect to
different database systems and execute queries.
"""

import pandas as pd
from db_connection import (
    get_mysql_connection,
    get_postgres_connection, 
    get_snowflake_connection,
    execute_query
)

def mysql_example():
    """Example of connecting to MySQL and executing a query."""
    print("\n=== MySQL Example ===")
    
    try:
        # Get connection
        connection = get_mysql_connection()
        
        # Execute a simple query
        query = "SELECT * FROM sample_table LIMIT 10"
        result = execute_query(connection, query)
        
        # Display results
        print(f"Query returned {len(result)} rows")
        print(result.head())
        
        # Close connection
        connection.close()
        print("Connection closed successfully")
        
    except Exception as e:
        print(f"Error: {str(e)}")

def postgres_example():
    """Example of connecting to PostgreSQL and executing a query."""
    print("\n=== PostgreSQL Example ===")
    
    try:
        # Get connection
        connection = get_postgres_connection()
        
        # Execute a simple query
        query = "SELECT * FROM sample_table LIMIT 10"
        result = execute_query(connection, query)
        
        # Display results
        print(f"Query returned {len(result)} rows")
        print(result.head())
        
        # Close connection
        connection.close()
        print("Connection closed successfully")
        
    except Exception as e:
        print(f"Error: {str(e)}")

def snowflake_example():
    """Example of connecting to Snowflake and executing a query."""
    print("\n=== Snowflake Example ===")
    
    try:
        # Get connection
        connection = get_snowflake_connection()
        
        # Execute a simple query
        query = "SELECT * FROM sample_table LIMIT 10"
        result = execute_query(connection, query)
        
        # Display results
        print(f"Query returned {len(result)} rows")
        print(result.head())
        
        # Close connection
        connection.close()
        print("Connection closed successfully")
        
    except Exception as e:
        print(f"Error: {str(e)}")

def example_with_parameters():
    """Example of executing a parameterized query."""
    print("\n=== Parameterized Query Example ===")
    
    try:
        # Get connection (using PostgreSQL for this example)
        connection = get_postgres_connection()
        
        # Define parameters
        params = {
            'limit': 5,
            'category': 'electronics'
        }
        
        # Execute a parameterized query
        query = """
        SELECT * FROM products 
        WHERE category = %(category)s
        LIMIT %(limit)s
        """
        
        result = execute_query(connection, query, params)
        
        # Display results
        print(f"Query returned {len(result)} rows")
        print(result.head())
        
        # Close connection
        connection.close()
        print("Connection closed successfully")
        
    except Exception as e:
        print(f"Error: {str(e)}")

def example_with_custom_config():
    """Example of connecting with custom configuration."""
    print("\n=== Custom Config Example ===")
    
    try:
        # Define custom configuration
        config = {
            'host': 'custom-host.example.com',
            'port': 5432,
            'database': 'custom_db',
            'user': 'custom_user',
            'password': 'custom_password',
            'schema': 'custom_schema'
        }
        
        # Get connection with custom config
        connection = get_postgres_connection(config)
        
        # Execute a simple query
        query = "SELECT * FROM custom_table LIMIT 5"
        result = execute_query(connection, query)
        
        # Display results
        print(f"Query returned {len(result)} rows")
        print(result.head())
        
        # Close connection
        connection.close()
        print("Connection closed successfully")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Database Connection Examples")
    print("----------------------------")
    print("Make sure to set up your .env file with proper credentials before running this example.")
    print("You can rename .env.template to .env and update the values.")
    
    # Uncomment the examples you want to run
    # mysql_example()
    # postgres_example()
    # snowflake_example()
    # example_with_parameters()
    # example_with_custom_config()
    
    print("\nAll examples are commented out by default.")
    print("Uncomment the ones you want to run in the if __name__ == '__main__' block.") 