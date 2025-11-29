class SafetyAgent:
    """
    Provides critical safety and advisory warnings for the destination.
    """
    def __init__(self, tools, llm_model):
        self.tools = tools
        self.llm = llm_model
        print("    [Subagent] SafetyAgent initialized.")

    def get_safety_recommendations(self, destination: str) -> str:
        query = f"Critical safety advisories and tourist scams to avoid in {destination}."
        
        raw_results = self.tools.search_google(query)
        
        # Use LLM to clean and structure the safety advisory
        if self.llm and raw_results:
            analysis_prompt = f"""
            Analyze the search results for safety advisories in {destination}. 
            Generate a short, urgent list of 5 critical safety tips and scams to avoid, focusing on group safety.
            Raw Search Results: {raw_results}
            """
            response = self.llm.generate_content(analysis_prompt)
            return response.text
            
        return "Safety information service is currently unavailable."