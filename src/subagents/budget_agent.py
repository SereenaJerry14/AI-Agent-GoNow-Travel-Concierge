import re
from typing import Dict, Any

class BudgetAgent:
    """
    Manages budget allocation by subtracting transport cost and setting 
    realistic limits for accommodation and daily spending.
    """
    def __init__(self, memory, tools, llm_model=None):
        """Initializes the agent with shared memory, tools, and optional LLM."""
        self.memory = memory
        self.tools = tools
        self.llm = llm_model
        print("    [Subagent] BudgetAgent initialized.")

    def _parse_budget_string(self, budget_str: str) -> float:
        """Cleans a budget string (e.g., '₹400,000') into a usable float (e.g., 400000.0)."""
        clean_str = re.sub(r'[^\d.]', '', str(budget_str).replace(',', ''))
        try:
            return float(clean_str)
        except ValueError:
            print(f"ERROR: Could not parse budget string: {budget_str}. Defaulting to 0.")
            return 0.0

    def determine_limits(self, duration: int, total_budget_str: str, 
                         estimated_transport_cost: float) -> Dict[str, float]:
        """
        Calculates the remaining budget and sets daily spending and accommodation limits.
        """
        
        total_budget = self._parse_budget_string(total_budget_str)
        
        # 1. Calculate Remaining Budget
        remaining_budget = total_budget - estimated_transport_cost
        
        if remaining_budget < 0:
            return {
                "error": f"Transport cost ({estimated_transport_cost:.0f}) exceeds total budget ({total_budget:.0f}). Please choose a cheaper transport option.",
                "remaining_budget": 0.0,
                "accommodation_limit_total": 0.0,
                "daily_spending_limit": 0.0,
                "safety_buffer": 0.0,
                "estimated_transport_cost": estimated_transport_cost
            }

        # 2. Allocation Ratios
        SAFETY_BUFFER_PERCENT = 0.10 
        ACCOMMODATION_ALLOCATION_RATIO = 0.60 
        
        safety_buffer = remaining_budget * SAFETY_BUFFER_PERCENT
        allocatable_budget = remaining_budget - safety_buffer
        
        # Split budget
        accommodation_limit_total = allocatable_budget * ACCOMMODATION_ALLOCATION_RATIO
        daily_and_food_budget = allocatable_budget * (1 - ACCOMMODATION_ALLOCATION_RATIO)
        
        # 3. Calculate Daily Spending Limit
        daily_spending_limit = daily_and_food_budget / duration if duration > 0 else 0
        
        print(f"    [BudgetAgent] Accommodation Limit: {accommodation_limit_total:.2f}, Daily Limit: {daily_spending_limit:.2f}")

        return {
            "remaining_budget": remaining_budget,
            "accommodation_limit_total": accommodation_limit_total, 
            "daily_spending_limit": daily_spending_limit,     
            "safety_buffer": safety_buffer,
            "estimated_transport_cost": estimated_transport_cost
        }
