import os
import requests
from datetime import datetime, timezone

def get_shopify_metrics(date_str: str) -> dict:
    """
    Fetches total sales and calculates AOV from Shopify using the GraphQL Admin API for a specific date.
    Args:
        date_str (str): The date to query in YYYY-MM-DD format.
    Returns:
        dict: A dictionary containing 'shopify_sales' and 'shopify_aov'.
    """
    store_url = os.environ.get("SHOPIFY_STORE_URL")
    access_token = os.environ.get("SHOPIFY_ACCESS_TOKEN")
    
    if not store_url or not access_token:
        print("Warning: Missing Shopify API credentials.")
        return {"shopify_sales": 0.0, "shopify_aov": 0.0}
        
    # Format dates to cover the full 24 hours of the target date in UTC
    start_time = f"{date_str}T00:00:00Z"
    end_time = f"{date_str}T23:59:59Z"
    
    query = """
    query GetOrders($query: String!) {
      orders(first: 250, query: $query) {
        edges {
          node {
            totalPriceSet {
              shopMoney {
                amount
              }
            }
          }
        }
      }
    }
    """
    
    # We query paid orders within the exact timestamps
    variables = {
        "query": f"created_at:>='{start_time}' AND created_at:<='{end_time}' AND financial_status:paid"
    }
    
    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }
    
    url = f"https://{store_url}/admin/api/2024-01/graphql.json"
    
    try:
        response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        orders = data.get("data", {}).get("orders", {}).get("edges", [])
        
        total_sales = 0.0
        order_count = len(orders)
        
        for edge in orders:
            amount_str = edge['node']['totalPriceSet']['shopMoney']['amount']
            total_sales += float(amount_str)
            
        aov = total_sales / order_count if order_count > 0 else 0.0
        
        return {
            "shopify_sales": round(total_sales, 2),
            "shopify_aov": round(aov, 2)
        }
        
    except Exception as e:
        print(f"Error fetching Shopify metrics: {e}")
        return {"shopify_sales": 0.0, "shopify_aov": 0.0}
