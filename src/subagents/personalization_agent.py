# src/subagents/personalization_agent.py

class PersonalizationAgent:
    """
    Module C: The "Smart Mom" Packer. Generates weather-aware packing lists and personal tips.
    """
    def __init__(self, memory, tools, llm_model):
        self.memory = memory
        self.tools = tools
        self.llm = llm_model
        print("    [Subagent] PersonalizationAgent initialized.")

    def generate_packing_list(self, group_details: str, weather_summary: str) -> str:
        """
        Uses weather data and group demographics to create a specific packing list.
        """
        if not self.llm:
            return "Packing list generation failed: LLM not available."
            
        packing_prompt = f"""
        **TASK**: Generate a concise, categorized packing checklist.
        
        **INPUTS**:
        - Group Composition: {group_details}
        - Weather Forecast: {weather_summary}
        
        **INSTRUCTIONS**:
        1. Categorize items by **Must-Haves** (e.g., meds, charger), **Climate-Specific** (based on weather), and **Group-Specific** (e.g., senior comfort, kid entertainment).
        2. Format the output clearly using markdown lists.
        """
        
        response = self.llm.generate_content(packing_prompt)
        return response.text