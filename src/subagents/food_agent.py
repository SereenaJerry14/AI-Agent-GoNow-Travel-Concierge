class FoodAgent:
    """
    Finds restaurant recommendations based on dietary preferences and reviews.
    """
    def __init__(self, tools, llm_model):
        self.tools = tools
        self.llm = llm_model
        print("    [Subagent] FoodAgent initialized.")

    def _food_search_query(self, destination, dietary):
        # Existing logic is good, just moved to a method
        if dietary.lower() in ["veg", "vegetarian"]:
            return f"best vegetarian restaurants in {destination} with good hygiene reviews"
        # ... (rest of the query logic for non-veg, vegan, etc.) ...
        else:
            return f"best family-friendly restaurants in {destination} with great reviews"

    def get_restaurants(self, destination, dietary_preference="vegetarian") -> str:
        
        query = self._food_search_query(destination, dietary_preference)
        
        # 1. Use the consistent tool call
        raw_results = self.tools.search_google(query)
        
        # 2. Use LLM to summarize the top 3 (The agentic value-add)
        if self.llm and raw_results:
            analysis_prompt = f"""
            Analyze the following top restaurant search results for {destination} (Preference: {dietary_preference}).
            Provide the top 3 best and safest options in a clean markdown list format (Name, Cuisine, Short reason).
            Raw Search Results: {raw_results}
            """
            response = self.llm.generate_content(analysis_prompt)
            return response.text
            
        return "Food recommendations failed or no results found."