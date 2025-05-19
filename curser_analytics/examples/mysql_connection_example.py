#!/usr/bin/env python3
"""
MySQL Connection Example

This example demonstrates how to use the Curser Analytics database connection module
to connect to MySQL and execute queries.
"""

import os
import sys
import pandas as pd

# Add the parent directory to the path to import from the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import our database connection utilities
from curser_analytics.db.connection import get_mysql_connection

def main():
    """Example showing MySQL connection and queries."""
    print("Connecting to MySQL database...")
    
    try:
        # Get a MySQL connection (this will use environment variables from .env file)
        mysql_conn = get_mysql_connection()
        
        if not mysql_conn.is_connected():
            print("Failed to connect to MySQL database.")
            return
        
        # Example 1: Execute a query to get MySQL version
        print("\nExample 1: Getting MySQL version")
        version_df = mysql_conn.execute_query("SELECT VERSION() as version")
        if version_df is not None and not version_df.empty:
            version = version_df.iloc[0]['version']
            print(f"MySQL Server Version: {version}")
        
        # Example 2: List databases
        print("\nExample 2: Listing databases")
        df_databases = mysql_conn.execute_query("SHOW DATABASES")
        print("\nAvailable databases:")
        print(df_databases)
        
        # Example 3: Run a more complex query against an example table (if it exists)
        print("\nExample 3: Querying a sample table (if it exists)")
        try:
            # Get the current database
            current_db = mysql_conn.execute_query("SELECT DATABASE() as current_db")
            if current_db is not None and not current_db.empty:
                db_name = current_db.iloc[0]['current_db']
                
                # Check if a sample table exists
                table_query = f"""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = '{db_name}'
                LIMIT 5
                """
                tables_df = mysql_conn.execute_query(table_query)
                
                if tables_df is not None and not tables_df.empty:
                    print("\nAvailable tables:")
                    print(tables_df)
                    
                    # Query the first table
                    first_table = tables_df.iloc[0]['table_name']
                    sample_query = f"SELECT * FROM {first_table} LIMIT 5"
                    print(f"\nSample data from {first_table}:")
                    sample_df = mysql_conn.execute_query(sample_query)
                    print(sample_df)
                else:
                    print(f"\nNo tables found in database {db_name}")
            else:
                print("Could not determine current database")
        except Exception as e:
            print(f"Error in example 3: {e}")
        
        # Close the connection
        mysql_conn.disconnect()
        print("\nConnection closed")
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        print("\nMake sure:")
        print("1. Your MySQL server is running")
        print("2. Your .env file contains the correct credentials")
        print("3. You've created the database mentioned in your .env file")

if __name__ == "__main__":
    main() 