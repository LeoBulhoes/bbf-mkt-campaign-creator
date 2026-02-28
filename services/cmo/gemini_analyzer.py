import os
import json
from google import genai

# Using structured outputs via Gemini pydantic schema
from pydantic import BaseModel, Field

# Define the expected JSON output format
class AdCommand(BaseModel):
    action: str = Field(description="The action to take: 'PAUSE', 'SCALE_UP', 'SCALE_DOWN', or 'NO_ACTION'")
    adset_id: str = Field(description="The Meta AdSet ID this action applies to")
    reasoning: str = Field(description="One sentence explaining why this decision was made against the constraints")
    percentage: int = Field(description="If scaling, the percentage to scale budget (10-20%). 0 if PAUSE or NO_ACTION.")

class DailyMarketingDecisions(BaseModel):
    summary: str = Field(description="A brief 2-sentence summary of overall account health.")
    commands: list[AdCommand]

def analyze_performance(metrics: list, target_roas: float = 3.5, target_cpa: float = 20.0, current_campaigns: list = None) -> DailyMarketingDecisions | None:
    """
    Feeds the historical metrics and current campaign status to Gemini to make budget decisions.
    Args:
        metrics (list): The past 7 days of BigQuery data.
        target_roas (float): The brand's break-even/target ROAS.
        target_cpa (float): The brand's maximum allowable Cost Per Acquisition.
        current_campaigns (list): Live data fetched from Meta today about active adsets.
    Returns:
        DailyMarketingDecisions: Parsed JSON commands to execute.
    """
    api_key = os.environ.get("GOOGLE_AISTUDIO_API_KEY")
    if not api_key:
        print("Error: Missing GOOGLE_AISTUDIO_API_KEY")
        return None
        
    client = genai.Client(api_key=api_key)
    
    # We use gemini-2.5-flash as it is fast and excellent at JSON schema abiding
    model_id = 'gemini-2.5-flash'
    
    prompt = f"""
    You are the AI Chief Marketing Officer for BlueBullFly, an e-commerce brand.
    Your goal is to maximize profit by strictly enforcing our target KPIs.
    
    Constraints:
    - Target Blended ROAS: >= {target_roas}
    - Max Acceptable CPA: <= ${target_cpa}
    
    Historical 7-Day Performance (from BigQuery):
    {json.dumps(metrics, indent=2)}
    
    Current Active Meta AdSets (Live):
    {json.dumps(current_campaigns, indent=2) if current_campaigns else "No live adset data provided."}
    
    Rules for Action:
    1. If an AdSet has spent > $50 and has 0 purchases, PAUSE it.
    2. If an AdSet's CPA > ${target_cpa * 1.25} over the last 3 days, PAUSE it.
    3. If an AdSet's CPA < ${target_cpa * 0.8} and has >= 3 purchases, SCALE_UP by 20%.
    4. Otherwise, NO_ACTION.
    
    Analyze the data and output the required actions.
    """
    
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': DailyMarketingDecisions,
                'temperature': 0.1 # Low temperature for deterministic financial logic
            },
        )
        
        # Pydantic validates and parses the JSON response
        return DailyMarketingDecisions.model_validate_json(response.text)
        
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return None
