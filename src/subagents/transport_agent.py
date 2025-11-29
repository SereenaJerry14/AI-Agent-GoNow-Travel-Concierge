from typing import Dict, Any, List
import json 


class TransportAgent:
    # ... (init method remains the same) ...
    def __init__(self, tools, llm_model):
        self.tools = tools
        self.llm = llm_model
        print("    [Subagent] TransportAgent initialized.")

    def find_and_recommend_transport(self, origin: str, destination: str, group_details: str, start_date: str) -> Dict[str, Any]:
        
        if not self.llm:
             return {"error": "LLM not initialized for Transport analysis.", "round_trip_cost": 0.0}

        # 1. Execute Tool Calls (Remains the same)
        # ... (raw_data generation remains the same) ...
        flight_query = f"Cheapest round-trip flight price and travel time from {origin} to {destination} on {start_date}"
        # ... and so on for train and bus ...
        raw_flight_data = self.tools.search_google(flight_query)
        # ...
        raw_data = {
            "flights": raw_flight_data,
            # ... and so on ...
        }

        # 2. Construct Analysis Prompt for LLM Reasoning (Modified for reliability)
        analysis_prompt = f"""
        **TASK**: Act as a travel concierge. Analyze the following real-time travel data 
        for a trip from {origin} to {destination} for a group of: **{group_details}**.
        
        **CRITERIA**: Since this is a sudden trip, prioritize COMFORT and RELIABILITY 
        for the specific group (especially if seniors/kids are present) over marginal cost savings.
        
        **RAW DATA:**
        {json.dumps(raw_data, indent=2)}

        **OUTPUT FORMAT**: You MUST ONLY return a single JSON object. DO NOT include any introductory or explanatory text.
        
        {{
            "recommendation_text": "Detailed analysis and Trade-Off Table here.",
            "recommended_mode": "Flight | Train | Bus | Car",
            "round_trip_cost": 35000.0,  // Extract the most likely total cost for the recommended mode, as a number.
            "cost_currency": "INR"
        }}
        """

        # 3. Get LLM Analysis and Recommendation (REMOVED 'config' ARGUMENT)
        try:
            # Removed the problematic 'config' argument
            llm_response = self.llm.generate_content(analysis_prompt)
            
            # Use regex or simple string cleaning to extract the JSON block if the LLM adds text
            json_text = llm_response.text.strip()
            
            # In case the model wrapped the JSON in markdown fences (```json...```)
            if json_text.startswith("```json"):
                json_text = json_text.replace("```json", "").replace("```", "").strip()

            result = json.loads(json_text)
            
            # Ensure the cost is a float for the Budget Agent
            cost = float(result.get("round_trip_cost", 0.0))
            
            return {
                "recommendation_text": result.get("recommendation_text", "Analysis incomplete."),
                "recommended_mode": result.get("recommended_mode", "Uncertain"),
                "round_trip_cost": cost,
                "cost_currency": result.get("cost_currency", "Unknown")
            }
            
        except Exception as e:
            # Print the full error for debugging
            print(f"Transport LLM analysis failed: {e}") 
            print(f"LLM TEXT: {llm_response.text}") # Show what the LLM returned
            
            # This is the cost you had in your traceback, now hardcoded as a fallback
            return {
                "recommendation_text": f"Transport analysis failed. Error: {e}",
                "recommended_mode": "Manual Check Required",
                "round_trip_cost": 50000.0, 
                "cost_currency": "INR"
            }