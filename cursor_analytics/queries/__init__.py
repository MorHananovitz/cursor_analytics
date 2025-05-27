import os
from pathlib import Path
from typing import Optional, Dict, List

def get_query_path(query_name: str) -> Optional[Path]:
    queries_dir = Path(__file__).parent
    
    # Normalize the query name
    if not query_name.endswith('.sql'):
        query_name = f"{query_name}.sql"
    
    query_path = queries_dir / query_name
    return query_path if query_path.exists() else None

def load_query(query_name: str) -> Optional[str]:
    query_path = get_query_path(query_name)
    if not query_path:
        return None
        
    with open(query_path, 'r') as f:
        return f.read().strip()
        
def list_available_queries() -> List[str]:
    queries_dir = Path(__file__).parent
    return [f.name for f in queries_dir.glob('*.sql')] 