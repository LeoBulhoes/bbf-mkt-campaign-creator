import os
from google.cloud import bigquery

def load_metrics_to_bigquery(metrics_data: dict):
    """
    Appends the daily metrics payload to the BigQuery Unified Data Warehouse.
    Args:
        metrics_data (dict): The dictionary containing date and all combined metrics.
    """
    # Assuming the table is in the format GCP_PROJECT_ID.dataset_id.table_id
    GCP_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "bluebullfly-5cc16")
    dataset_id = "marketing_data"
    table_id = "daily_metrics"
    
    table_ref = f"{GCP_PROJECT_ID}.{dataset_id}.{table_id}"
    
    try:
        client = bigquery.Client(project=GCP_PROJECT_ID)
        
        # We append a single row to the BigQuery table
        errors = client.insert_rows_json(table_ref, [metrics_data])
        
        if errors:
            print(f"Encountered errors while inserting rows: {errors}")
        else:
            print(f"Successfully loaded {metrics_data.get('date')} metrics to BigQuery.")
            
    except Exception as e:
        print(f"Error loading to BigQuery: {e}")
