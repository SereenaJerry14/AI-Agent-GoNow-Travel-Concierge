

class TravelPlannerAgent:
    """
    The final compilation agent. It takes all processed data from the
    workflow and formats it into the final structured travel plan report.
    """
    def __init__(self, llm_model):
        self.llm_model = llm_model
        print("    [Subagent] TravelPlannerAgent initialized (Final Compiler).")

    def generate_plan(
        self, 
        origin, 
        destination, 
        group_details, 
        budget, 
        start_date, 
        stay_duration_days,
        weather_summary, 
        transport_data, 
        budget_data, 
        accommodation_pick, 
        packing_list, 
        safety_tips,
        food_recs,
        events 
    ) -> str:
        
        if not self.llm_model:
            return "Final report generation failed: LLM not available."
        final_prompt = f"""
        **TASK**: You are the final editor for the GoNow Travel Agent. Your job is to 
        take all processed data and compile it into a single, comprehensive, and 
        user-friendly travel plan. Use clear markdown headers and emojis.
        
        **ALL DATA POINTS (Processed):**
        - TRIP OVERVIEW: {origin} to {destination} for {group_details}
        - WEATHER: {weather_summary}
        - TRANSPORT (Recommendation): {transport_data.get('recommendation_text', 'N/A')}
        - ACCOMMODATION (Pick): {accommodation_pick}
        - BUDGET BREAKDOWN: Total remaining: {budget_data.get('remaining_budget', 'N/A'):.2f}, Daily Limit: {budget_data.get('daily_spending_limit', 'N/A'):.2f}
        - PACKING LIST: {packing_list}
        - SAFETY: {safety_tips}
        - FOOD RECS: {food_recs}
        - EVENTS: {events}

        **MANDATORY OUTPUT STRUCTURE (Use the results above to populate):**

        # 🚀 GoNow: Your Spontaneous Travel Plan
        
        ## 🧭 Transport Comparator (How to Get There)
        - **Best Choice**: {transport_data.get('recommended_mode', 'N/A')}
        - **Total Cost**: {transport_data.get('round_trip_cost', 'N/A')} {transport_data.get('cost_currency', 'N/A')}
        - **Agent Rationale**: [Why it was chosen over others (summarized from recommendation_text)]
        
        ## 🏨 Safe Stay Scout (Accommodation)
        - **Recommendation**: [Hotel Name/Summary from accommodation_pick]
        - **Budget Status**: {budget_data.get('accommodation_limit_total', 'N/A'):.2f} (Total Limit)
        
        ## 💰 Budget Breakdown
        - **Total Budget**: {budget}
        - **Remaining for Trip (Stay/Food/Activities)**: {budget_data.get('remaining_budget', 'N/A'):.2f}
        - **Recommended Daily Spend Limit**: {budget_data.get('daily_spending_limit', 'N/A'):.2f}
        
        ## 🎒 Smart Mom Packing List
        - {packing_list}

        ## 🍽️ Food & Restaurant Picks
        - {food_recs}

        ## 🎉 Events & Activities Guide
        - {events}
        
        ## 🛡 Critical Safety Advisory
        - {safety_tips}
        """
        response = self.llm_model.generate_content(final_prompt)
        return response.text