import os
import pandas as pd

# Import the database connection module
from cursor_analytics.db.connection import get_mysql_connection

def test_mysql_connection():
    print("=== MySQL Connection Test ===")
    
    # Environment variables should be loaded by the Makefile or system
    
    # Print environment variables (without showing passwords)
    print("\nEnvironment Variables:")
    print(f"MYSQL_HOST: {os.getenv('MYSQL_HOST', 'Not set')}")
    print(f"MYSQL_PORT: {os.getenv('MYSQL_PORT', 'Not set')}")
    print(f"MYSQL_USER: {os.getenv('MYSQL_USER', 'Not set')}")
    print(f"MYSQL_DATABASE: {os.getenv('MYSQL_DATABASE', 'Not set')}")
    print(f"MYSQL_PASSWORD: {'*****' if os.getenv('MYSQL_PASSWORD') else 'Not set'}")
    
    # Get connection
    print("\nAttempting to connect to MySQL...")
    connection = get_mysql_connection()
    
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
            print(f"Found {len(tables)} tables:")
            for i, row in tables.iterrows():
                print(f"  - {row.iloc[0]}")
        else:
            print("No tables found or query failed!")
            
        # Test database connection properties
        print("\nMySQL Server Information:")
        if hasattr(connection, "connection") and connection.connection:
            try:
                cursor = connection.connection.cursor()
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                print(f"Server Version: {version[0] if version else 'Unknown'}")
                
                cursor.execute("SELECT DATABASE()")
                db_name = cursor.fetchone()
                print(f"Current Database: {db_name[0] if db_name else 'None'}")
                
                cursor.execute("SHOW VARIABLES LIKE 'character_set_database'")
                charset = cursor.fetchone()
                print(f"Character Set: {charset[1] if charset else 'Unknown'}")
                
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
    test_mysql_connection() 