"""
Configuration settings for the Cursor Analytics package.

This module loads environment variables and provides
configuration settings for the package.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional

# Load environment variables from .env file if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed

# Base directory is the parent of the project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Default output directory
DEFAULT_OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Database connection parameters
DEFAULT_TIMEOUT = 5  # seconds
SCHEMA_ANALYSIS_TIMEOUT = 30  # seconds
DEFAULT_MAX_ROWS = 1000

class Settings:
    """
    Settings class for the Cursor Analytics package.
    """
    
    def __init__(self):
        # Database settings (can be overridden by environment variables)
        self.mysql_host = os.getenv("MYSQL_HOST", "localhost")
        self.mysql_port = int(os.getenv("MYSQL_PORT", "3306"))
        self.mysql_user = os.getenv("MYSQL_USER", "root")
        self.mysql_password = os.getenv("MYSQL_PASSWORD", "")
        self.mysql_database = os.getenv("MYSQL_DATABASE", "")
        
        # Output directory for generated files
        self.output_dir = os.getenv("OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    @property
    def mysql_connection_string(self) -> str:
        """
        Get the MySQL connection string from the current settings.
        
        Returns:
            str: MySQL connection string
        """
        return f"mysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"

    def get_mysql_config(self, for_schema_analysis: bool = False) -> Dict[str, Any]:
    
        config = {
            'host': self.mysql_host,
            'port': self.mysql_port,
            'user': self.mysql_user,
            'password': self.mysql_password,
            'database': self.mysql_database,
            'use_pure': True,        # Use pure Python implementation
            'buffered': True         # Use buffered cursors
        }
        
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

# Create a singleton instance of the settings
settings = Settings() 