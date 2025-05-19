"""
Database Connection Module

This module provides classes for connecting to different database types.
It implements a unified interface for establishing connections, executing queries,
and managing database resources for MySQL, PostgreSQL, and Snowflake databases.

Classes:
    DatabaseConnection: Abstract base class defining the connection interface
    MySQLConnection: Implementation for MySQL databases
    PostgreSQLConnection: Implementation for PostgreSQL databases
    SnowflakeConnection: Implementation for Snowflake data warehouses

Functions:
    get_mysql_connection: Factory function for MySQL connections
    get_postgres_connection: Factory function for PostgreSQL connections
    get_snowflake_connection: Factory function for Snowflake connections
"""

import os
import logging
from typing import Dict, Any, Optional, Union, List
import pandas as pd
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        
    def connect(self) -> bool:
        raise NotImplementedError("Subclasses must implement connect()")
    
    def disconnect(self) -> None:
        if self.connection:
            try:
                self.connection.close()
                logger.info("Database connection closed")
            except Exception as e:
                logger.error(f"Error closing connection: {e}")
    
    def is_connected(self) -> bool:
        return self.connection is not None
    
    def execute_query(
        self, 
        query: str, 
        params: Optional[Union[tuple, dict]] = None,
        timeout: int = 3000,
        max_rows: int = 1000
    ) -> Optional[pd.DataFrame]:
        raise NotImplementedError("Subclasses must implement execute_query()")


class MySQLConnection(DatabaseConnection):
    def __init__(self, for_schema_analysis: bool = False):
        super().__init__()
        self.for_schema_analysis = for_schema_analysis
        
        # Get configuration from environment variables
        self.config = {
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'port': int(os.getenv('MYSQL_PORT', '3306')),
            'user': os.getenv('MYSQL_USER'),
            'password': os.getenv('MYSQL_PASSWORD'),
            'database': os.getenv('MYSQL_DATABASE')
        }
        
        # Add additional options for schema analysis
        if for_schema_analysis:
            self.config.update({
                'get_warnings': True,
                'raise_on_warnings': False,
                'buffered': True
            })
    
    def connect(self) -> bool:
        try:
            import mysql.connector
            from mysql.connector import Error
            
            self.connection = mysql.connector.connect(**self.config)
            
            if self.connection.is_connected():
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to connect to MySQL database: {e}")
            return False
    
    def execute_query(
        self, 
        query: str, 
        params: Optional[Union[tuple, dict]] = None,
        timeout: int = 3000,
        max_rows: int = 1000
    ) -> Optional[pd.DataFrame]:
        if not self.is_connected():
            if not self.connect():
                return None
        
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True, buffered=True)
            
            # Set a query timeout and limit result size
            try:
                cursor.execute(f"SET SESSION MAX_EXECUTION_TIME={timeout}")
                cursor.execute(f"SET SESSION SQL_SELECT_LIMIT={max_rows}")
            except Exception as e:
                logger.warning(f"Failed to set execution parameters: {e}")
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Check if this is a SELECT-type query (includes SHOW, DESCRIBE, EXPLAIN)
            # Normalize the query by removing comments, extra whitespace
            query_start = query.lower().strip()
            
            # Handle SQL comments that might be at the start of the query
            if query_start.startswith("--"):
                # Skip comment lines
                lines = query_start.split("\n")
                for line in lines:
                    if not line.strip().startswith("--"):
                        query_start = line.strip()
                        break
            
            # Check for SELECT, SHOW, DESCRIBE, EXPLAIN at the start of the query
            is_select_query = any(query_start.startswith(prefix) for prefix in 
                                 ('select', 'show', 'describe', 'explain', 'with'))
            
            if is_select_query:
                try:
                    # Fetch data and create DataFrame
                    data = cursor.fetchall()
                    
                    # If no rows returned but it was a SELECT query, return empty DataFrame
                    if not data:
                        return pd.DataFrame()
                    
                    df = pd.DataFrame(data)
                    return df
                except Exception as e:
                    logger.error(f"Error fetching results: {e}")
                    return pd.DataFrame()  # Return empty DataFrame on error
            else:
                self.connection.commit()
                return None
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return None
        finally:
            if cursor:
                cursor.close()


class PostgreSQLConnection(DatabaseConnection):    
    def __init__(self):
        """Initialize PostgreSQL connection."""
        super().__init__()
        
        # Get configuration from environment variables
        self.config = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': int(os.getenv('POSTGRES_PORT', '5432')),
            'user': os.getenv('POSTGRES_USER'),
            'password': os.getenv('POSTGRES_PASSWORD'),
            'database': os.getenv('POSTGRES_DATABASE')
        }
    
    def connect(self) -> bool:
        try:
            import psycopg2
            
            self.connection = psycopg2.connect(**self.config)
            return True
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL database: {e}")
            return False
    
    def execute_query(
        self, 
        query: str, 
        params: Optional[Union[tuple, dict]] = None,
        timeout: int = 3000,
        max_rows: int = 1000
    ) -> Optional[pd.DataFrame]:
        if not self.is_connected():
            if not self.connect():
                return None
        
        cursor = None
        try:
            cursor = self.connection.cursor()
            
            # Set statement timeout
            with self.connection.cursor() as timeout_cursor:
                timeout_cursor.execute(f"SET statement_timeout = {timeout}")
            
            cursor = self.connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.lower().strip().startswith(('select', 'show', 'explain')):
                try:
                    columns = [desc[0] for desc in cursor.description]
                    data = cursor.fetchmany(max_rows)
                    df = pd.DataFrame(data, columns=columns)
                    return df
                except Exception as e:
                    logger.error(f"Error fetching results: {e}")
                    return pd.DataFrame()  # Return empty DataFrame on error
            else:
                self.connection.commit()
                return None
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return None
        finally:
            if cursor:
                cursor.close()


class SnowflakeConnection(DatabaseConnection):
    
    def __init__(self):
        super().__init__()
        
        # Get configuration from environment variables
        self.config = {
            'account': os.getenv('SNOWFLAKE_ACCOUNT'),
            'user': os.getenv('SNOWFLAKE_USER'),
            'password': os.getenv('SNOWFLAKE_PASSWORD'),
            'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
            'database': os.getenv('SNOWFLAKE_DATABASE'),
            'schema': os.getenv('SNOWFLAKE_SCHEMA')
        }
    
    def connect(self) -> bool:
        try:
            import snowflake.connector
            
            self.connection = snowflake.connector.connect(**self.config)
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Snowflake database: {e}")
            return False
    
    def execute_query(
        self, 
        query: str, 
        params: Optional[Union[tuple, dict]] = None,
        timeout: int = 3000,
        max_rows: int = 1000
    ) -> Optional[pd.DataFrame]:
        if not self.is_connected():
            if not self.connect():
                return None
        
        cursor = None
        try:
            cursor = self.connection.cursor()
            
            # Set query timeout
            with self.connection.cursor() as timeout_cursor:
                timeout_cursor.execute(f"ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = {timeout // 1000}")
            
            cursor = self.connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.lower().strip().startswith(('select', 'show', 'describe', 'explain')):
                try:
                    columns = [desc[0] for desc in cursor.description]
                    data = cursor.fetchmany(max_rows)
                    df = pd.DataFrame(data, columns=columns)
                    return df
                except Exception as e:
                    logger.error(f"Error fetching results: {e}")
                    return pd.DataFrame()  # Return empty DataFrame on error
            else:
                self.connection.commit()
                return None
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

# Helper functions to create and connect database instances

def get_mysql_connection(for_schema_analysis: bool = False) -> MySQLConnection:
    connection = MySQLConnection(for_schema_analysis)
    connection.connect()
    return connection

def get_postgres_connection() -> PostgreSQLConnection:
    connection = PostgreSQLConnection()
    connection.connect()
    return connection

def get_snowflake_connection() -> SnowflakeConnection:
    connection = SnowflakeConnection()
    connection.connect()
    return connection 