#!/usr/bin/env python
"""
Example demonstrating how to use the multi-database functionality.
"""

import os
import sys
import pandas as pd

# Add parent directory to path to ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.connection import get_mysql_connection, execute_query, execute_query_multi_db

def main():
    # Example 1: Connect to a specific database
    print("Example 1: Connecting to a specific database")
    db_name = os.getenv('MYSQL_DATABASE_1')  # First database from .env
    conn = get_mysql_connection(database=db_name)
    
    # Run a simple query
    query = "SHOW TABLES"
    results = execute_query(conn, query)
    print(f"Tables in {db_name}:")
    print(results)
    print("\n" + "-"*50 + "\n")
    
    # Example 2: Switch databases on an existing connection
    print("Example 2: Switching databases on an existing connection")
    db_name_2 = os.getenv('MYSQL_DATABASE_2')  # Second database from .env
    conn.switch_database(db_name_2)
    
    # Run the same query on the second database
    results_2 = execute_query(conn, query)
    print(f"Tables in {db_name_2}:")
    print(results_2)
    print("\n" + "-"*50 + "\n")
    
    # Example 3: Execute the same query on multiple databases
    print("Example 3: Execute the same query on multiple databases")
    databases = [
        os.getenv('MYSQL_DATABASE_1'),
        os.getenv('MYSQL_DATABASE_2')
    ]
    
    multi_results = execute_query_multi_db(conn, query, databases)
    for db, df in multi_results.items():
        print(f"Tables in {db}:")
        print(df)
        print()
    
    conn.disconnect()

if __name__ == "__main__":
    main() 