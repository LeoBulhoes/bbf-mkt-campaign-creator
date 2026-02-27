import os
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

def get_meta_metrics(date_str: str) -> dict:
    """
    Fetches ad spend and impressions from Meta Ads for the given date.
    Args:
        date_str (str): The date to query in YYYY-MM-DD format.
    Returns:
        dict: A dictionary containing 'meta_spend' and 'meta_impressions'.
    """
    app_id = os.environ.get("META_APP_ID")
    app_secret = os.environ.get("META_APP_SECRET")
    access_token = os.environ.get("META_ACCESS_TOKEN")
    ad_account_id = os.environ.get("META_AD_ACCOUNT_ID")
    
    if not all([app_id, app_secret, access_token, ad_account_id]):
        print("Warning: Missing Meta API credentials. Returning empty metrics.")
        return {"meta_spend": 0.0, "meta_impressions": 0}
        
    try:
        FacebookAdsApi.init(app_id, app_secret, access_token)
        account = AdAccount(f"act_{ad_account_id}")
        
        # We use time_range to fetch a specific day
        params = {
            'time_range': {'since': date_str, 'until': date_str},
            'level': 'account'
        }
        
        # We request spend and impressions
        fields = ['spend', 'impressions']
        
        insights = account.get_insights(fields=fields, params=params)
        
        if not insights:
            return {"meta_spend": 0.0, "meta_impressions": 0}
            
        data = insights[0]
        return {
            "meta_spend": float(data.get('spend', 0.0)),
            "meta_impressions": int(data.get('impressions', 0))
        }
        
    except Exception as e:
        print(f"Error fetching Meta metrics: {e}")
        return {"meta_spend": 0.0, "meta_impressions": 0}
