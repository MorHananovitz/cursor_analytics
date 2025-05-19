import os
import time
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Tuple

# Import modules
from curser_analytics.config.settings import settings
from curser_analytics.db.connection import MySQLConnection, get_mysql_connection
from curser_analytics.utils.logger import logger, setup_logger

# Create schema-specific logger
schema_logger = setup_logger('curser_analytics.db.schema')


class SchemaAnalyzer:
    def __init__(self, connection):
        self.connection = connection
        self.output_dir = settings.output_dir
    
    def analyze(self, **kwargs):
        raise NotImplementedError("Subclasses must implement analyze()")
    
    def save_results(self, results, filename):
        raise NotImplementedError("Subclasses must implement save_results()")


class MySQLSchemaAnalyzer(SchemaAnalyzer):    
    def __init__(self, connection: Optional[MySQLConnection] = None):
        if connection is None:
            connection = get_mysql_connection(for_schema_analysis=True)
        super().__init__(connection)
    
    def get_all_tables(self) -> pd.DataFrame:
        query = """
        SELECT 
            TABLE_NAME, 
            TABLE_ROWS,
            ENGINE, 
            TABLE_COLLATION,
            CREATE_TIME
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = DATABASE()
        ORDER BY TABLE_NAME
        """
        return self.connection.execute_query(query, timeout=30000, max_rows=10000)
    
    def get_table_columns(self, table_name: str) -> pd.DataFrame:
        query = """
        SELECT 
            COLUMN_NAME, 
            COLUMN_TYPE,
            IS_NULLABLE,
            COLUMN_KEY,
            COLUMN_DEFAULT,
            EXTRA
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE 
            TABLE_SCHEMA = DATABASE() AND 
            TABLE_NAME = %s
        ORDER BY ORDINAL_POSITION
        """
        return self.connection.execute_query(query, params=(table_name,), timeout=10000)
    
    def get_table_foreign_keys(self, table_name: str) -> pd.DataFrame:
        query = """
        SELECT 
            COLUMN_NAME,
            REFERENCED_TABLE_NAME,
            REFERENCED_COLUMN_NAME,
            CONSTRAINT_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE 
            TABLE_SCHEMA = DATABASE() AND
            TABLE_NAME = %s AND
            REFERENCED_TABLE_NAME IS NOT NULL
        """
        return self.connection.execute_query(query, params=(table_name,), timeout=10000)
    
    def get_database_name(self) -> str:
        query = "SELECT DATABASE() as db_name"
        result = self.connection.execute_query(query)
        if result is not None and not result.empty:
            return result.iloc[0]['db_name']
        return "unknown"
    
    def get_all_relationships(self) -> pd.DataFrame:
        query = """
        SELECT
            TABLE_NAME AS child_table,
            COLUMN_NAME AS child_column,
            CONSTRAINT_NAME,
            REFERENCED_TABLE_NAME AS parent_table,
            REFERENCED_COLUMN_NAME AS parent_column
        FROM
            information_schema.KEY_COLUMN_USAGE
        WHERE
            TABLE_SCHEMA = DATABASE()
            AND REFERENCED_TABLE_NAME IS NOT NULL
        ORDER BY
            parent_table, child_table
        """
        return self.connection.execute_query(query, timeout=30000)
    
    def analyze(self, limit: Optional[int] = None, **kwargs) -> Dict[str, Any]:
        start_time = time.time()
        
        db_name = self.get_database_name()
        
        tables_df = self.get_all_tables()
        if tables_df is None or tables_df.empty:
            schema_logger.error("No tables found or query failed.")
            return {'success': False, 'message': 'No tables found'}
        
        if limit is not None and limit > 0:
            tables_df = tables_df.head(limit)
        
        results = {
            'database': db_name,
            'tables_count': len(tables_df),
            'tables': [],
            'relationships': [],
            'analysis_time': 0,
            'success': True
        }
        
        for _, table_row in tables_df.iterrows():
            table_name = table_row['TABLE_NAME']
            table_info = {
                'name': table_name,
                'rows': table_row['TABLE_ROWS'],
                'engine': table_row['ENGINE'] if 'ENGINE' in table_row else None,
                'created': table_row['CREATE_TIME'] if 'CREATE_TIME' in table_row else None,
                'columns': [],
                'foreign_keys': []
            }
            
            columns_df = self.get_table_columns(table_name)
            if columns_df is not None and not columns_df.empty:
                for _, col in columns_df.iterrows():
                    column_info = {
                        'name': col['COLUMN_NAME'],
                        'type': col['COLUMN_TYPE'],
                        'nullable': col['IS_NULLABLE'],
                        'key': col['COLUMN_KEY'],
                        'default': col['COLUMN_DEFAULT'],
                        'extra': col['EXTRA']
                    }
                    table_info['columns'].append(column_info)
            
            fk_df = self.get_table_foreign_keys(table_name)
            if fk_df is not None and not fk_df.empty:
                for _, fk in fk_df.iterrows():
                    fk_info = {
                        'column': fk['COLUMN_NAME'],
                        'referenced_table': fk['REFERENCED_TABLE_NAME'],
                        'referenced_column': fk['REFERENCED_COLUMN_NAME'],
                        'constraint_name': fk['CONSTRAINT_NAME']
                    }
                    table_info['foreign_keys'].append(fk_info)
                    
                    relationship = {
                        'source_table': table_name,
                        'source_column': fk['COLUMN_NAME'],
                        'target_table': fk['REFERENCED_TABLE_NAME'],
                        'target_column': fk['REFERENCED_COLUMN_NAME']
                    }
                    results['relationships'].append(relationship)
            
            results['tables'].append(table_info)
        
        all_relationships_df = self.get_all_relationships()
        if all_relationships_df is not None and not all_relationships_df.empty:
            results['all_relationships'] = all_relationships_df.to_dict('records')
        
        elapsed_time = time.time() - start_time
        results['analysis_time'] = elapsed_time
        
        schema_logger.info(f"Schema analysis completed in {elapsed_time:.2f} seconds.")
        return results
    
    def generate_erd(self, results: Dict[str, Any], filename: str = 'database_erd.txt') -> str:
        output_path = os.path.join(self.output_dir, filename)
        
        with open(output_path, 'w') as f:
            f.write(f"ENTITY RELATIONSHIP DIAGRAM: {results['database']}\n")
            f.write("=" * 100 + "\n\n")
            
            f.write("RELATIONSHIPS\n")
            f.write("-" * 100 + "\n")
            f.write(f"{'CHILD TABLE':<30}{'CHILD COLUMN':<30}{'PARENT TABLE':<30}{'PARENT COLUMN':<30}{'CONSTRAINT NAME'}\n")
            f.write("-" * 100 + "\n")
            
            if 'all_relationships' in results:
                for rel in results['all_relationships']:
                    f.write(f"{rel['child_table']:<30}{rel['child_column']:<30}{rel['parent_table']:<30}{rel['parent_column']:<30}{rel['CONSTRAINT_NAME']}\n")
            
            f.write("\n\nTABLE REFERENCES\n")
            f.write("=" * 100 + "\n\n")
            
            referenced_tables = {}
            if 'all_relationships' in results:
                for rel in results['all_relationships']:
                    parent = rel['parent_table']
                    child = rel['child_table']
                    child_col = rel['child_column']
                    parent_col = rel['parent_column']
                    
                    if parent not in referenced_tables:
                        referenced_tables[parent] = []
                    
                    referenced_tables[parent].append(f"  - Table '{child}' via {child}.{child_col} -> {parent}.{parent_col}")
            
            for table in sorted(referenced_tables.keys()):
                f.write(f"Table '{table}' is referenced by:\n")
                for reference in sorted(referenced_tables[table]):
                    f.write(f"{reference}\n")
                f.write("\n")
        
        schema_logger.info(f"ERD generation completed and saved to {output_path}")
        return output_path
    
    def save_results(self, results: Dict[str, Any], filename: str = 'schema.txt') -> str:
        output_path = os.path.join(self.output_dir, filename)
        
        with open(output_path, 'w') as f:
            f.write(f"DATABASE SCHEMA: {results['database']}\n")
            f.write("=" * 100 + "\n\n")
            f.write(f"Total tables: {results['tables_count']}\n\n")
            
            f.write("TABLE OF CONTENTS\n")
            f.write("-" * 50 + "\n")
            for i, table in enumerate(results['tables']):
                f.write(f"{i+1}. {table['name']} (rows: {table['rows']})\n")
            
            f.write("\n\nDETAILED SCHEMA\n")
            f.write("=" * 100 + "\n\n")
            
            for table in results['tables']:
                f.write(f"TABLE: {table['name']}\n")
                f.write("=" * 100 + "\n")
                f.write(f"Rows: {table['rows']} | Engine: {table['engine']} | Created: {table['created']}\n")
                f.write("-" * 100 + "\n")
                
                f.write(f"{'COLUMN':<30}{'TYPE':<20}{'NULLABLE':<10}{'KEY':<10}{'DEFAULT':<20}{'EXTRA'}\n")
                f.write("-" * 100 + "\n")
                
                for col in table['columns']:
                    col_name = col['name']
                    col_type = col['type']
                    nullable = col['nullable']
                    key = col['key']
                    default = str(col['default']) if col['default'] is not None else "NULL"
                    extra = col['extra'] if col['extra'] is not None else ""
                    
                    f.write(f"{col_name:<30}{col_type:<20}{nullable:<10}{key:<10}{default:<20}{extra}\n")
                
                if table['foreign_keys']:
                    f.write("\nFOREIGN KEYS:\n")
                    f.write("-" * 100 + "\n")
                    f.write(f"{'COLUMN':<30}{'REFERENCES':<50}{'CONSTRAINT NAME'}\n")
                    f.write("-" * 100 + "\n")
                    
                    for fk in table['foreign_keys']:
                        col = fk['column']
                        ref = f"{fk['referenced_table']}.{fk['referenced_column']}"
                        constraint = fk['constraint_name']
                        
                        f.write(f"{col:<30}{ref:<50}{constraint}\n")
                
                f.write("\n\n")
            
            if results['relationships']:
                f.write("\nRELATIONSHIP SUMMARY\n")
                f.write("=" * 100 + "\n\n")
                
                source_to_target = {}
                for rel in results['relationships']:
                    source = rel['source_table']
                    if source not in source_to_target:
                        source_to_target[source] = []
                    
                    source_to_target[source].append({
                        'target': rel['target_table'],
                        'source_col': rel['source_column'],
                        'target_col': rel['target_column']
                    })
                
                target_to_source = {}
                for rel in results['relationships']:
                    target = rel['target_table']
                    if target not in target_to_source:
                        target_to_source[target] = []
                    
                    target_to_source[target].append({
                        'source': rel['source_table'],
                        'source_col': rel['source_column'],
                        'target_col': rel['target_column']
                    })
                
                f.write("OUTGOING REFERENCES:\n")
                f.write("-" * 100 + "\n")
                
                for source, targets in sorted(source_to_target.items()):
                    f.write(f"Table '{source}' references:\n")
                    for target in targets:
                        f.write(f"  - Table '{target['target']}' via {source}.{target['source_col']} -> {target['target']}.{target['target_col']}\n")
                    f.write("\n")
                
                f.write("\nINCOMING REFERENCES:\n")
                f.write("-" * 100 + "\n")
                
                for target, sources in sorted(target_to_source.items()):
                    f.write(f"Table '{target}' is referenced by:\n")
                    for source in sources:
                        f.write(f"  - Table '{source['source']}' via {source['source']}.{source['source_col']} -> {target}.{source['target_col']}\n")
                    f.write("\n")
            
            f.write("\nAnalysis completed in {:.2f} seconds\n".format(results['analysis_time']))
        
        schema_logger.info(f"Results saved successfully to {output_path}")
        return output_path


def analyze_mysql_schema(limit: Optional[int] = None, output_file: str = 'schema.txt') -> str:
    analyzer = MySQLSchemaAnalyzer()
    results = analyzer.analyze(limit=limit)
    return analyzer.save_results(results, filename=output_file) 