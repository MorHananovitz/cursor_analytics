"""
Configuration settings for the Curser Analytics package.

This module loads configuration from environment variables and provides access to settings.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional

# Define base paths
ROOT_DIR = Path(__file__).parent.parent.parent.absolute()
ENV_FILE = os.path.join(ROOT_DIR, '.env')

# Database connection parameters
DEFAULT_TIMEOUT = 5  # seconds
SCHEMA_ANALYSIS_TIMEOUT = 30  # seconds
DEFAULT_MAX_ROWS = 1000

class Settings:
  
    def __init__(self, env_file: str = ENV_FILE):
        """
        Initialize settings.
        
        Args:
            env_file: Path to the .env file (no longer used directly, environment variables
                      should be loaded by the Makefile or system)
        """
        # Environment variables should be loaded by the Makefile or system
        
        # MySQL connection settings
        self.mysql_config = {
            'host': os.getenv('MYSQL_HOST'),
            'port': int(os.getenv('MYSQL_PORT', '3306')),
            'user': os.getenv('MYSQL_USER'),
            'password': os.getenv('MYSQL_PASSWORD'),
            'database': os.getenv('MYSQL_DATABASE'),
            'use_pure': True,        # Use pure Python implementation
            'buffered': True         # Use buffered cursors
        }
        
        # PostgreSQL connection settings
        self.postgres_config = {
            'host': os.getenv('POSTGRES_HOST'),
            'port': int(os.getenv('POSTGRES_PORT', '5432')),
            'user': os.getenv('POSTGRES_USER'),
            'password': os.getenv('POSTGRES_PASSWORD'),
            'database': os.getenv('POSTGRES_DATABASE'),
        }
        
        # Snowflake connection settings
        self.snowflake_config = {
            'account': os.getenv('SNOWFLAKE_ACCOUNT'),
            'user': os.getenv('SNOWFLAKE_USER'),
            'password': os.getenv('SNOWFLAKE_PASSWORD'),
            'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
            'database': os.getenv('SNOWFLAKE_DATABASE'),
            'schema': os.getenv('SNOWFLAKE_SCHEMA'),
        }
        
        # Output settings
        self.output_dir = os.getenv('OUTPUT_DIR', os.path.join(ROOT_DIR, 'output'))
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def get_mysql_config(self, for_schema_analysis: bool = False) -> Dict[str, Any]:
    
        config = self.mysql_config.copy()
        
        # Use different timeout settings based on operation
        if for_schema_analysis:
            # Longer timeouts for schema analysis (metadata queries)
            config.update({
                'connection_timeout': SCHEMA_ANALYSIS_TIMEOUT,
                'read_timeout': SCHEMA_ANALYSIS_TIMEOUT,
                'connect_timeout': SCHEMA_ANALYSIS_TIMEOUT,
            })
        else:
            # Shorter timeouts for regular queries
            config.update({
                'connection_timeout': DEFAULT_TIMEOUT,
                'read_timeout': DEFAULT_TIMEOUT,
                'connect_timeout': DEFAULT_TIMEOUT,
            })
        
        return config
    
    def get_postgres_config(self) -> Dict[str, Any]:
        return self.postgres_config.copy()
    
    def get_snowflake_config(self) -> Dict[str, Any]:
        return self.snowflake_config.copy()

# Create a global settings instance
settings = Settings() 