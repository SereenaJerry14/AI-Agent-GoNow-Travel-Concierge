import os
import google.generativeai as genai
from src.agent_core import GoNowTravelAgent 
from src.memory import USER_MEMORY_BANK 
from dotenv import load_dotenv

load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY") 
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel('gemini-2.5-flash')

print("\n\n--- RUNNING THE GoNow TRAVEL AGENT ---")

# 2. Initialize the Agent Class
# This is where all subagents are created and connected
agent = GoNowTravelAgent(llm_model=model)

# 3. Call the plan_trip METHOD on the instantiated agent
final_plan = agent.plan_trip(
    origin="Trivandrum", 
    destination="Meghalaya", 
    group_details="5 girls (age 25 to 30)", 
    budget="100000",
    # USER_MEMORY_BANK should now be managed internally by the agent's memory component, 
    # so we might remove it from this call if the agent loads it on init.
    # For now, if your agent_core still needs it, pass it.
    user_memory=USER_MEMORY_BANK,
    stay_duration_days=3,
    start_date="Dec 30, 2025"
    # llm_model is now passed during class initialization, not in the method call
)

print(final_plan)