import os
import sys
from dotenv import load_dotenv
import pandas as pd

# Import the database connection module
from curser_analytics.db.connection import get_mysql_connection
from curser_analytics.analytics import run_analysis, load_query_from_file

def debug_execute_query():
    print("=== MySQL Query Execution Debug ===")
    
    # Load environment variables
    load_dotenv()
    
    # Get connection
    print("\nAttempting to connect to MySQL...")
    connection = get_mysql_connection()
    
    # Check connection status
    if not connection or not connection.is_connected():
        print("Connection failed!")
        return
    
    print("Connection successful!")
    
    try:
        # Debug the execute_query method
        print("\nTesting execute_query method:")
        
        # 1. Test with SHOW TABLES query directly on connection
        print("\n1. Running SHOW TABLES directly on connection:")
        tables_result = connection.execute_query("SHOW TABLES")
        print(f"Result type: {type(tables_result)}")
        print(f"Is None: {tables_result is None}")
        print(f"Is empty: {tables_result.empty if tables_result is not None else 'N/A'}")
        print(f"First few results: {tables_result.head(5) if tables_result is not None and not tables_result.empty else 'None'}")
        
        # 2. Test with markets.sql using run_analysis
        print("\n2. Running markets.sql query using run_analysis:")
        query = load_query_from_file("markets")
        print(f"Query content: {query[:200]}...")  # Show first 200 chars of query
        
        analytics_result = run_analysis("mysql", query)
        print(f"Result type: {type(analytics_result)}")
        print(f"Is None: {analytics_result is None}")
        print(f"Is empty: {analytics_result.empty if analytics_result is not None else 'N/A'}")
        print(f"First few results: {analytics_result.head(5) if analytics_result is not None and not analytics_result.empty else 'None'}")
        
        # 3. Test with a simpler manually constructed query
        print("\n3. Testing a simpler query that should definitely return results:")
        simple_query = "SELECT * FROM clientmarketsettings LIMIT 5"
        direct_result = connection.execute_query(simple_query)
        print(f"Result type: {type(direct_result)}")
        print(f"Is None: {direct_result is None}")
        print(f"Is empty: {direct_result.empty if direct_result is not None else 'N/A'}")
        print(f"First few results: {direct_result.head(5) if direct_result is not None and not direct_result.empty else 'None'}")
        
    except Exception as e:
        print(f"Debug failed with error: {e}")
    finally:
        # Close connection
        if connection and connection.is_connected():
            connection.disconnect()
            print("\nConnection closed.")

if __name__ == "__main__":
    debug_execute_query() 