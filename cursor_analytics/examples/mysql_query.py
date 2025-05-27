"""
MySQL Query Example

This script connects to MySQL and runs a specific query.
"""

from db_connection import get_mysql_connection, execute_query

def run_mysql_query(query):
    """Run a specific MySQL query and print results."""
    print(f"Executing query: {query}")
    
    # Connect to MySQL
    connection = get_mysql_connection()
    
    if connection:
        print("Connection successful!")
        
        # Execute the query
        result = execute_query(connection, query)
        
        if result is not None:
            print("\nQuery results:")
            print(result)
            
            # Print column info
            print("\nColumn information:")
            for col in result.columns:
                print(f"- {col}: {result[col].dtype}")
            
            print(f"\nTotal rows: {len(result)}")
        else:
            print("\nQuery returned no results or was not a SELECT query.")
        
        # Close connection
        connection.close()
        print("\nConnection closed.")
    else:
        print("Failed to connect to MySQL. Check your credentials in the .env file.")

if __name__ == "__main__":
    # You can change this query to any query you want to run
    query = "SHOW TABLES"
    
    # To view data from a specific table, uncomment the line below and replace 'table_name' with your table
    # query = "SELECT * FROM table_name LIMIT 10"
    
    run_mysql_query(query) 