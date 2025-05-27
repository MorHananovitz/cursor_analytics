"""
MySQL Connection Test

This script tests the connection to MySQL and executes a simple query.
"""

from db_connection import get_mysql_connection, execute_query

def test_mysql_connection():
    """Test MySQL connection and run a simple query."""
    print("Testing MySQL connection...")
    
    # Connect to MySQL
    connection = get_mysql_connection()
    
    if connection:
        print("Connection successful!")
        
        # Show databases
        query = "SHOW DATABASES"
        result = execute_query(connection, query)
        
        if result is not None:
            print("\nAvailable databases:")
            print(result)
            
            # Show tables in the connected database
            query = "SHOW TABLES"
            tables = execute_query(connection, query)
            
            if tables is not None and not tables.empty:
                print("\nTables in current database:")
                print(tables)
                
                # Get first table name
                first_table = tables.iloc[0, 0]
                
                # Show sample data from first table
                query = f"SELECT * FROM {first_table} LIMIT 5"
                sample_data = execute_query(connection, query)
                
                if sample_data is not None and not sample_data.empty:
                    print(f"\nSample data from {first_table}:")
                    print(sample_data)
            else:
                print("\nNo tables found in the current database.")
        
        # Close connection
        connection.close()
        print("\nConnection closed.")
    else:
        print("Failed to connect to MySQL. Check your credentials in the .env file.")

if __name__ == "__main__":
    test_mysql_connection() 