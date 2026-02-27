import os
import json
from datetime import datetime
from bigquery_client import fetch_last_7_days_metrics
from gemini_analyzer import analyze_performance
from meta_executor import apply_cmo_decisions

def run_cmo_agent(dry_run: bool = True):
    """
    Main orchestration loop for the AI CMO Script.
    """
    print(f"--- Starting AI CMO Agent Run at {datetime.now().isoformat()} ---")
    
    # 1. Fetch Historical Data
    metrics = fetch_last_7_days_metrics()
    print(f"Retrieved {len(metrics)} days of historical metrics.")
    
    # In a real environment, we'd fetch active campaigns from Meta here.
    # We will mock the active campaign state for the prompt.
    mock_active_adsets = [
        {"adset_id": "123456", "name": "Broad Audience - Video", "daily_budget": 50, "spend_today": 45, "purchases_today": 0},
        {"adset_id": "789012", "name": "Retargeting - Static", "daily_budget": 20, "spend_today": 12, "purchases_today": 2, "cpa_3d": 12.50}
    ]
    
    if not metrics:
        print("No BigQuery metrics found. Aborting analysis.")
        return
        
    # 2. Analyze with Gemini
    print("Requesting strategic analysis from Gemini-2.5-Flash...")
    decisions = analyze_performance(
        metrics=metrics,
        target_roas=3.5,
        target_cpa=15.0,
        current_campaigns=mock_active_adsets
    )
    
    if not decisions:
        print("Failed to generate decisions from Gemini.")
        return
        
    print(f"\n[AI CMO SUMMARY]: {decisions.summary}\n")
    
    # 3. Execute Decisions
    print(f"Executing {len(decisions.commands)} adset commands...")
    
    # Force dry_run=True here to prevent accidental spend on the user's account during testing
    apply_cmo_decisions(decisions.commands, dry_run=True)
    
    print("--- AI CMO Agent Run Complete ---")

if __name__ == "__main__":
    # If we want to allow it to run as a web server on Cloud Run 
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route("/", methods=["POST", "GET"])
    def http_trigger():
        try:
            run_cmo_agent(dry_run=True)
            return jsonify({"status": "success", "message": "CMO processing finished"}), 200
        except Exception as e:
            print(f"CMO error: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500
            
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
