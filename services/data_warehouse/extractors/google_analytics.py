import os
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

def get_ga_metrics(date_str: str) -> dict:
    """
    Fetches active users and sessions from Google Analytics 4 for the given date.
    Args:
        date_str (str): The date to query in YYYY-MM-DD format.
    Returns:
        dict: A dictionary containing 'ga_active_users' and 'ga_sessions'.
    """
    property_id = os.environ.get("GA4_PROPERTY_ID")
    
    if not property_id:
        print("Warning: Missing GA4_PROPERTY_ID. Skipping GA extraction.")
        return {"ga_active_users": 0, "ga_sessions": 0}
        
    try:
        # Uses Application Default Credentials (ADC) implicitly
        client = BetaAnalyticsDataClient()

        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="date")],
            metrics=[
                Metric(name="activeUsers"),
                Metric(name="sessions")
            ],
            date_ranges=[DateRange(start_date=date_str, end_date=date_str)],
        )
        
        response = client.run_report(request)
        
        if not response.rows:
            return {"ga_active_users": 0, "ga_sessions": 0}
            
        row = response.rows[0]
        
        return {
            "ga_active_users": int(row.metric_values[0].value),
            "ga_sessions": int(row.metric_values[1].value)
        }
        
    except Exception as e:
        print(f"Error fetching Google Analytics metrics: {e}")
        return {"ga_active_users": 0, "ga_sessions": 0}
