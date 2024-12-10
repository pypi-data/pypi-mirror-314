import json
import os

def generate_index_report(data, db_name, report_name="Index Report", filename='index_report', report_path='/tmp/'):
    """
    Generate a JSON report of index information.

    Parameters:
        data (list of lists): Raw index data where each inner list contains index properties.
        report_name (str): Name of the report.

    Returns:
        str: JSON formatted string representing the index report.
    """
    headers = ['Database Name', 'Schema Name', 'Index Name', 'Index Type','Index Size', 'Category']
    indexes = [dict(zip(headers, row)) for row in data]
    report = {
        "report_name": report_name,
        "database_name": db_name,
        "total_index_count": len(indexes),
        "indexes": indexes
    }
    with open(f'''{report_path}{filename}.json''', 'w') as output_json:
        json.dump(report, output_json, indent=4)
        return True
    return False

def generate_command(category,schema_name,index_name):
    
    if category=="Bloated":
        execute_sql=f'''REINDEX INDEX CONCURRENTLY {schema_name}.{index_name};'''
        return execute_sql
    else:
        execute_sql=f'''DROP INDEX CONCURRENTLY {schema_name}.{index_name};'''
        return execute_sql