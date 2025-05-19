import os
from dotenv import load_dotenv
import pandas as pd

# Import the database connection module
from curser_analytics.db.connection import get_snowflake_connection

def test_snowflake_connection():
    print("=== Snowflake Connection Test ===")
    
    # Load environment variables
    load_dotenv()
    
    # Print environment variables (without showing passwords)
    print("\nEnvironment Variables:")
    print(f"SNOWFLAKE_ACCOUNT: {os.getenv('SNOWFLAKE_ACCOUNT', 'Not set')}")
    print(f"SNOWFLAKE_USER: {os.getenv('SNOWFLAKE_USER', 'Not set')}")
    print(f"SNOWFLAKE_PASSWORD: {'*****' if os.getenv('SNOWFLAKE_PASSWORD') else 'Not set'}")
    print(f"SNOWFLAKE_WAREHOUSE: {os.getenv('SNOWFLAKE_WAREHOUSE', 'Not set')}")
    print(f"SNOWFLAKE_DATABASE: {os.getenv('SNOWFLAKE_DATABASE', 'Not set')}")
    print(f"SNOWFLAKE_SCHEMA: {os.getenv('SNOWFLAKE_SCHEMA', 'Not set')}")

    # Get connection
    print("\nAttempting to connect to Snowflake...")
    connection = get_snowflake_connection()
    
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
        
        # Test SHOW TABLES query
        print("\nTesting SHOW TABLES query:")
        tables = connection.execute_query("SHOW TABLES")
        if tables is not None and not tables.empty:
            # Snowflake's SHOW TABLES returns multiple columns, 'name' is typically the table name.
            # Adjust column name if different based on actual Snowflake driver output.
            table_name_column = 'name' # Common column name for table names in SHOW TABLES result
            if table_name_column not in tables.columns:
                # Fallback if 'name' column is not present, use the first column
                print(f"Warning: Column '{table_name_column}' not found in SHOW TABLES result. Using first column.")
                table_name_column = tables.columns[0]

            print(f"Found {len(tables)} tables in database '{connection.config.get('database')}' and schema '{connection.config.get('schema')}':")
            for i, row in tables.iterrows():
                print(f"  - {row[table_name_column]}")
        else:
            print("No tables found or query failed!")
            
        # Test database connection properties
        print("\nSnowflake Session Information:")
        if hasattr(connection, "connection") and connection.connection:
            try:
                cursor = connection.connection.cursor()
                
                cursor.execute("SELECT CURRENT_VERSION()")
                version = cursor.fetchone()
                print(f"Server Version: {version[0] if version else 'Unknown'}")
                
                cursor.execute("SELECT CURRENT_DATABASE()")
                db_name = cursor.fetchone()
                print(f"Current Database: {db_name[0] if db_name else 'None'}")

                cursor.execute("SELECT CURRENT_SCHEMA()")
                schema = cursor.fetchone()
                print(f"Current Schema: {schema[0] if schema else 'None'}")

                cursor.execute("SELECT CURRENT_WAREHOUSE()")
                warehouse = cursor.fetchone()
                print(f"Current Warehouse: {warehouse[0] if warehouse else 'None'}")
                
                cursor.execute("SELECT CURRENT_ROLE()")
                role = cursor.fetchone()
                print(f"Current Role: {role[0] if role else 'Unknown'}")

                cursor.close()
            except Exception as e:
                print(f"Error getting session info: {e}")
    except Exception as e:
        print(f"Test failed with error: {e}")
    finally:
        # Close connection
        if connection and connection.is_connected():
            connection.disconnect()
            print("\nConnection closed.")

if __name__ == "__main__":
    test_snowflake_connection() 