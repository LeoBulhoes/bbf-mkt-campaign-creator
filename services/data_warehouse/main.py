"""
Main entry point for the Unified Data Warehouse ETL script.
Triggered via Cloud Scheduler nightly (e.g. 11:55 PM).
Extracts daily metrics from Meta, Shopify, and GA, formatting them into
a final report dictionary, and appends it to BigQuery.
"""

import os
from datetime import datetime, timedelta
import json

def run_etl():
    """Extracts, Transforms, and Loads the daily metrics."""
    # Target date is yesterday if not specified
    target_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    print(f"Starting ETL pipeline for Date: {target_date}")
    
    # Imports
    from extractors.meta_ads import get_meta_metrics
    from extractors.shopify import get_shopify_metrics
    from extractors.google_analytics import get_ga_metrics
    from loader.bigquery import load_metrics_to_bigquery
    
    # 1. Extract from Meta Ads
    meta_data = get_meta_metrics(target_date)
    print(f"Meta Metrics: {meta_data}")
    
    # 2. Extract from Shopify
    shopify_data = get_shopify_metrics(target_date)
    print(f"Shopify Metrics: {shopify_data}")
    
    # 3. Extract from Google Analytics
    ga_data = get_ga_metrics(target_date)
    print(f"GA4 Metrics: {ga_data}")
    
    # 4. Transform / Join data
    final_payload = {
        "date": target_date,
        **meta_data,
        **shopify_data,
        **ga_data
    }
    
    print(f"Final Payload: {json.dumps(final_payload, indent=2)}")
    
    # 5. Load to BigQuery
    load_metrics_to_bigquery(final_payload)


if __name__ == "__main__":
    # If we want to allow it to run as a web server on Cloud Run (e.g. triggered via HTTP)
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route("/", methods=["POST", "GET"])
    def http_trigger():
        try:
            run_etl()
            return jsonify({"status": "success", "message": "ETL complete"}), 200
        except Exception as e:
            print(f"ETL error: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500
            
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
