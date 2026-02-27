import os
from google.cloud import bigquery

def fetch_last_7_days_metrics() -> list:
    """
    Retrieves the last 7 days of aggregated marketing metrics from BigQuery.
    Returns:
        A list of dictionaries representing the last 7 days of performance.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "bluebullfly-5cc16")
    dataset_id = "marketing_data"
    table_id = "daily_metrics"
    
    client = bigquery.Client(project=project_id)
    
    query = f"""
        SELECT 
            date, 
            meta_spend, 
            meta_impressions, 
            shopify_sales, 
            shopify_aov, 
            ga_active_users, 
            ga_sessions
        FROM `{project_id}.{dataset_id}.{table_id}`
        ORDER BY date DESC
        LIMIT 7
    """
    
    try:
        query_job = client.query(query)
        results = query_job.result()
        
        metrics = []
        for row in results:
            metrics.append({
                "date": str(row.date),
                "meta_spend": float(row.meta_spend) if row.meta_spend else 0.0,
                "meta_impressions": int(row.meta_impressions) if row.meta_impressions else 0,
                "shopify_sales": float(row.shopify_sales) if row.shopify_sales else 0.0,
                "shopify_aov": float(row.shopify_aov) if row.shopify_aov else 0.0,
                "ga_active_users": int(row.ga_active_users) if row.ga_active_users else 0,
                "ga_sessions": int(row.ga_sessions) if row.ga_sessions else 0
            })
            
        return metrics
    except Exception as e:
        print(f"Error fetching BigQuery metrics: {e}")
        return []
