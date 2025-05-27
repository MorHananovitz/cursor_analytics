#!/usr/bin/env python
"""
Script to run the MySQL schema analyzer and generate an Entity Relationship Diagram (ERD).
"""

import sys
import os
# Add parent directory to path to ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cursor_analytics.db.schema import MySQLSchemaAnalyzer

if __name__ == "__main__":
    print("Starting MySQL schema analysis...")
    
    # Create the analyzer instance
    analyzer = MySQLSchemaAnalyzer()
    
    # Run the analysis
    results = analyzer.analyze()
    
    # Save the schema analysis
    schema_file = analyzer.save_results(results, filename="mysql_data_schema.txt")
    print(f"Schema analysis complete. Results saved to: {schema_file}")
    
    # Generate and save the ERD
    erd_file = analyzer.generate_erd(results, filename="mysql_data_erd.txt")
    print(f"ERD generation complete. Saved to: {erd_file}") 