"""
Cursor Analytics

A Python toolkit for data analysis and experimentation.

This package provides modules for connecting to various databases,
running SQL queries, and analyzing data. It includes utilities for
schema analysis, query management, and database connectivity.
"""

__version__ = '0.1.0'
__author__ = 'Cursor Analytics Team'

# Import commonly used modules for easier access
from cursor_analytics.db.connection import get_mysql_connection

# Expose key functions at the package level
__all__ = ['get_mysql_connection'] 