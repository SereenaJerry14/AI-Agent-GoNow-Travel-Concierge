class EventsAgent:
    """
    Finds local events, festivals, concerts happening during travel dates.
    """
    def __init__(self, tools, llm_model):
        self.tools = tools
        self.llm = llm_model
        print("    [Subagent] EventsAgent initialized.")

    def get_events(self, destination, travel_date) -> str:
        query = (
            f"events festivals concerts things to do in {destination} on {travel_date} "
            f"tourist friendly"
        )
        
        raw_results = self.tools.search_google(query)
        
        # Use LLM to filter and summarize relevant events
        if self.llm and raw_results:
            analysis_prompt = f"""
            Analyze the following search results for events/activities in {destination} near {travel_date}.
            Provide the top 3 most interesting and family-friendly activities in a clean markdown list format.
            Raw Search Results: {raw_results}
            """
            response = self.llm.generate_content(analysis_prompt)
            return response.text
            
        return "Events search unavailable or no relevant events found."