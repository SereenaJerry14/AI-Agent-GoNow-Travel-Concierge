# src/subagents/hotel_agent.py

class HotelAgent:
    """
    Module B: The "Safe Stay" Scout. Fetches hotel/hostel recommendations.
    """
    def __init__(self, tools, llm_model):
        self.tools = tools
        self.llm = llm_model
        print("    [Subagent] HotelAgent initialized.")


    def search_hotels(self, destination: str, group_details: str, budget: float) -> str:
        """
        Searches for top-rated accommodation within the calculated budget limit.
        """
        query = (
            f"top rated safe hotels or hostels in {destination} for {group_details} "
            f"max price per night equivalent to {budget} clean reviews family friendly"
        )
        
        # Uses the corrected search_google method
        raw_results = self.tools.search_google(query)
        
        # Use LLM to summarize the top result and ensure it matches criteria
        if self.llm and raw_results:
            analysis_prompt = f"""
            Analyze the top search result below for a safe, highly-rated hotel/hostel. 
            The maximum total accommodation budget is {budget}. 
            Provide a clean summary of the single best recommendation (Name, estimated total price, reason for selection).
            Raw Search Results: {raw_results[0]}
            """
            response = self.llm.generate_content(analysis_prompt)
            return response.text
            
        return "Accommodation search failed or no results found."