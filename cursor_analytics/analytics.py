import os
import sys
import logging
import argparse
from typing import Optional, Dict, Any, Callable, Union
import pandas as pd
from pathlib import Path
import datetime
import pickle

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import our database connection classes
from cursor_analytics.db.connection import (
    get_mysql_connection,
    get_postgres_connection,
    get_snowflake_connection,
    DatabaseConnection
)

# Import query utilities
from cursor_analytics.queries import load_query, list_available_queries

# Map database types to their connection functions
DB_CONNECTIONS = {
    'mysql': get_mysql_connection,
    'postgres': get_postgres_connection,
    'snowflake': get_snowflake_connection
}

def get_connection(db_type: str) -> Optional[DatabaseConnection]:
    if db_type.lower() not in DB_CONNECTIONS:
        supported_dbs = ", ".join(DB_CONNECTIONS.keys())
        raise ValueError(f"Unsupported database type: {db_type}. Supported types: {supported_dbs}")
    
    logger.info(f"Getting connection for database type: {db_type}")
    connection_func = DB_CONNECTIONS[db_type.lower()]
    
    try:
        return connection_func()
    except Exception as e:
        logger.error(f"Error creating {db_type} connection: {e}")
        return None

def load_query_from_file(query_path: str) -> Optional[str]:
    try:
        # First, try to load from the new package structure
        query = load_query(query_path)
        if query:
            return query
            
        # If that failed, try treating it as a direct file path
        path = Path(query_path)
        if path.exists():
            logger.info(f"Loading query from file: {path}")
            with open(path, 'r') as f:
                query = f.read().strip()
            
            if not query:
                logger.warning(f"Query file is empty: {path}")
                return None
                
            return query
                
        logger.error(f"Query file not found: {query_path}")
        available_queries = list_available_queries()
        if available_queries:
            logger.info(f"Available queries: {', '.join(available_queries)}")
        return None
    except Exception as e:
        logger.error(f"Error loading query from file: {e}")
        return None

def run_analysis(
    db_type: str, 
    query: str, 
    params: Optional[Dict[str, Any]] = None
) -> Optional[pd.DataFrame]:
    connection = None
    try:
        # Get the appropriate database connection
        connection = get_connection(db_type)
        
        if not connection or not connection.is_connected():
            logger.error(f"Failed to connect to {db_type} database")
            return None
        
        # Execute the query
        logger.info("Executing query...")
        
        results = connection.execute_query(query, params)
        
        if results is None or results.empty:
            logger.warning("Query returned no results")
            return pd.DataFrame()
        
        logger.info(f"Query returned {len(results)} rows")
        return results
        
    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        return None
    finally:
        # Always close the connection
        if connection and connection.is_connected():
            connection.disconnect()
            logger.info("Database connection closed")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Run database queries')
    
    parser.add_argument(
        '--db', '-d',
        type=str,
        default='mysql',
        choices=['mysql', 'postgres', 'snowflake'],
        help='Database type to connect to'
    )
    
    parser.add_argument(
        '--query', '-q',
        type=str,
        required=True,
        help='Name of query in the queries package or path to a query file'
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List available queries in the queries package'
    )
    
    return parser.parse_args()

def save_results_as_pickle(results: pd.DataFrame, query_name: str) -> str:
    # Create outputs directory if it doesn't exist
    outputs_dir = Path('outputs')
    outputs_dir.mkdir(exist_ok=True)
    
    # Extract the query name without extension or path
    query_base = Path(query_name).stem
    
    # Get current date in YYYY-MM-DD format
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # Create filename
    filename = f"{query_base}_{today}.pkl"
    filepath = outputs_dir / filename
    
    # Save DataFrame to pickle file
    results.to_pickle(filepath)
    logger.info(f"Results saved to pickle file: {filepath}")
    
    return str(filepath)

def main() -> None:
    # Environment variables should be loaded by the Makefile or system
    
    # Parse command line arguments
    args = parse_arguments()
    
    # If --list flag is set, just list available queries and exit
    if args.list:
        available_queries = list_available_queries()
        if available_queries:
            print("Available queries:")
            for query in available_queries:
                print(f"  - {query}")
        else:
            print("No queries available in the package.")
        return
    
    # Load the query from the specified file or name
    query = load_query_from_file(args.query)
    if not query:
        print(f"Could not load query: {args.query}")
        print("Use --list to see available queries")
        return
    
    # Run the analysis
    logger.info(f"Starting {args.db} analysis...")
    print(f"Executing query '{args.query}' against {args.db} database...")
    
    results = run_analysis(args.db, query)
    
    # Display results
    if results is not None and not results.empty:
        print("\nQuery Results:")
        print("==============")
        print(results)
        
        # Save results to pickle file
        pickle_path = save_results_as_pickle(results, args.query)
        print(f"\nResults saved to: {pickle_path}")
    else:
        print("\nNo results returned from query.")
        print(f"Check the database connection and that your query is valid for {args.db}.")
        print(f"Make sure your .env file contains the correct {args.db.upper()} credentials.")

if __name__ == "__main__":
    main() 