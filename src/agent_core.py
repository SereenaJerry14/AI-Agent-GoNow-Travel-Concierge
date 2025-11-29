from src.tools import Tools
from src.memory import Memory
from .subagents.budget_agent import BudgetAgent
from .subagents.events_agent import EventsAgent
from .subagents.food_agent import FoodAgent
from .subagents.hotel_agent import HotelAgent
from .subagents.transport_agent import TransportAgent
from .subagents.weather_agent import WeatherAgent
from .subagents.personalization_agent import PersonalizationAgent
from .subagents.safety_agent import SafetyAgent
from .subagents.travel_planner_agent import TravelPlannerAgent
import streamlit as st # Assuming Streamlit is used for output feedback

class GoNowTravelAgent:
    def __init__(self, llm_model):
        self.llm_model = llm_model
        self.tools = Tools() 
        self.memory = Memory() 

        # 1. Instantiate Subagents and provide them with necessary resources
        # Agents requiring LLM reasoning get self.llm_model
        self.weather_agent = WeatherAgent(tools=self.tools)
        self.transport_agent = TransportAgent(tools=self.tools, llm_model=self.llm_model)
        self.budget_agent = BudgetAgent(memory=self.memory, tools=self.tools) # LLM not strictly needed for calc
        self.hotel_agent = HotelAgent(tools=self.tools, llm_model=self.llm_model)
        self.food_agent = FoodAgent(tools=self.tools, llm_model=self.llm_model)
        self.events_agent = EventsAgent(tools=self.tools, llm_model=self.llm_model)
        self.safety_agent = SafetyAgent(tools=self.tools, llm_model=self.llm_model)
        self.personalization_agent = PersonalizationAgent(memory=self.memory, tools=self.tools, llm_model=self.llm_model)
        
        # Final Aggregator
        self.planner_agent = TravelPlannerAgent(llm_model=self.llm_model) 

    def plan_trip(self, origin, destination, group_details, budget, user_memory, stay_duration_days, start_date):
        """
        The main orchestration method, implementing the agent workflow.
        """
        # 0. Initialize Context and Memory
        self.memory.load_user_data(user_memory)
        st.write(f"Planning a {stay_duration_days}-day trip to **{destination}** for **{group_details}**.")
        

        st.info("Step 1/6: Checking destination weather forecast...")
        weather_summary = self.weather_agent.get_weather_forecast_summary(destination, stay_duration_days)
        self.memory.update_context("weather_summary", weather_summary)
        
        st.info("Step 2/6: Comparing Flight vs. Train vs. Car based on comfort, time, and budget...")
        transport_data = self.transport_agent.find_and_recommend_transport(
            origin=origin, 
            destination=destination, 
            group_details=group_details,
            start_date=start_date
        )
        transport_cost = transport_data.get("round_trip_cost", 0.0) 
        self.memory.update_context("transport_data", transport_data)
        
        st.info("Step 3/6: Calculating remaining budget and setting daily limits...")
        budget_data = self.budget_agent.determine_limits(
            duration=stay_duration_days,
            total_budget_str=budget,
            estimated_transport_cost=transport_cost
        )
        self.memory.update_context("budget_limits", budget_data) 
        
        st.info("Step 4/6: Searching for highly-rated last-minute accommodation...")
        accommodation_limit = budget_data.get('accommodation_limit_total', 0)
        accommodation_pick = self.hotel_agent.search_hotels(
            destination=destination, 
            group_details=group_details, 
            budget=accommodation_limit
        )
        self.memory.update_context("accommodation_pick", accommodation_pick)

        st.info("Step 5/6: Generating personalized packing list and safety tips...")
        packing_list = self.personalization_agent.generate_packing_list(
            group_details=group_details, 
            weather_summary=weather_summary
        )
        safety_tips = self.safety_agent.get_safety_recommendations(destination)
        
        st.info("Step 6/6: Compiling final structured travel plan...")
        final_report = self.planner_agent.generate_plan(
            origin, destination, group_details, budget, start_date, stay_duration_days,
            weather_summary, transport_data, budget_data, accommodation_pick, packing_list, safety_tips,
            # Placeholder calls for other agents (need to implement in full):
            food_recs=self.food_agent.get_restaurants(destination, self.memory.get_user_data().get("Dietary_Restrictions", "Any")),
            events=self.events_agent.get_events(destination, start_date)
        )

        return final_report
    
# NOTE: The 'plan_trip' function call in ui.py needs to be replaced with 
# agent.plan_trip(...) after the GoNowTravelAgent is instantiated.
