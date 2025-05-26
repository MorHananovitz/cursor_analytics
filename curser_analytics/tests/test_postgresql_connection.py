import os
import pandas as pd

# Import the database connection module
from curser_analytics.db.connection import get_postgres_connection

def test_postgresql_connection():
    print("=== PostgreSQL Connection Test ===")
    
    # Environment variables should be loaded by the Makefile or system
    
    # Print environment variables (without showing passwords)
    print("\nEnvironment Variables:")
    print(f"POSTGRES_HOST: {os.getenv('POSTGRES_HOST', 'Not set')}")
    print(f"POSTGRES_PORT: {os.getenv('POSTGRES_PORT', 'Not set')}")
    print(f"POSTGRES_USER: {os.getenv('POSTGRES_USER', 'Not set')}")
    print(f"POSTGRES_DATABASE: {os.getenv('POSTGRES_DATABASE', 'Not set')}")
    print(f"POSTGRES_PASSWORD: {'*****' if os.getenv('POSTGRES_PASSWORD') else 'Not set'}")
    
    # Get connection
    print("\nAttempting to connect to PostgreSQL...")
    connection = get_postgres_connection()
    
    # Check connection status
    if not connection or not connection.is_connected():
        print("Connection failed!")
        return
    
    print("Connection successful!")
    
    try:
        # Test simple query
        print("\nTesting simple query: SELECT 1")
        result = connection.execute_query("SELECT 1 as test")
        if result is not None and not result.empty:
            print(f"Query successful. Result: {result.iloc[0]['test']}")
        else:
            print("Query returned no results!")
        
        # Test SHOW TABLES query (adapted for PostgreSQL)
        print("\nTesting query to list tables:")
        # List tables in the current schema (usually 'public' if not specified)
        tables_query = "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = current_schema()"
        tables = connection.execute_query(tables_query)
        if tables is not None and not tables.empty:
            print(f"Found {len(tables)} tables in schema '{connection.config.get('database')}.{connection.connection.cursor().execute('SELECT current_schema()').fetchone()[0] if connection.connection else 'unknown'}':")
            for i, row in tables.iterrows():
                print(f"  - {row.iloc[0]}") # Assuming 'tablename' is the first column
        else:
            print("No tables found or query failed!")
            
        # Test database connection properties
        print("\nPostgreSQL Server Information:")
        if hasattr(connection, "connection") and connection.connection:
            try:
                cursor = connection.connection.cursor()
                
                cursor.execute("SELECT version()")
                version = cursor.fetchone()
                print(f"Server Version: {version[0] if version else 'Unknown'}")
                
                cursor.execute("SELECT current_database()")
                db_name = cursor.fetchone()
                print(f"Current Database: {db_name[0] if db_name else 'None'}")

                cursor.execute("SHOW server_encoding")
                encoding = cursor.fetchone()
                print(f"Server Encoding: {encoding[0] if encoding else 'Unknown'}")
                
                cursor.execute("SELECT current_schema()")
                schema = cursor.fetchone()
                print(f"Current Schema: {schema[0] if schema else 'Unknown'}")

                cursor.close()
            except Exception as e:
                print(f"Error getting server info: {e}")
    except Exception as e:
        print(f"Test failed with error: {e}")
    finally:
        # Close connection
        if connection and connection.is_connected():
            connection.disconnect()
            print("\nConnection closed.")

if __name__ == "__main__":
    test_postgresql_connection() 