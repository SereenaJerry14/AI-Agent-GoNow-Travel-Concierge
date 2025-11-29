import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from src.agent_core import GoNowTravelAgent 
from src.memory import USER_MEMORY_BANK 


load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
try:
    genai.configure(api_key=gemini_key)
    LLM_MODEL = genai.GenerativeModel('gemini-2.5-flash')
    AGENT = GoNowTravelAgent(llm_model=LLM_MODEL)
    AGENT_INITIALIZED = True
except Exception as e:
    st.error(f"Could not initialize Gemini API or Agent: {e}")
    AGENT_INITIALIZED = False


st.set_page_config(page_title="GoNow Travel Agent", page_icon="✈️", layout="wide")

st.title("🌍 GoNow — AI Travel")
st.write("Plan smart, last-minute trips instantly with real-world data.")

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    origin = st.text_input("Origin City", "Trivandrum")
    destination = st.text_input("Destination City", "Meghalaya") 
    group_details = st.text_input("Group Details", "5 girls (age 25 to 30)")
    budget = st.text_input("Budget (₹)", "100000") 

with col2:
    stay_duration_days = st.number_input("Stay Duration (Days)", 1, 30, 3)
    start_date = st.text_input("Trip Start Date", "Dec 30, 2025")
    st.write("User Memory Loaded:")
    st.json(USER_MEMORY_BANK)

st.markdown("### ✨ When you're ready, click below!")


if st.button("Generate Travel Plan 🚀") and AGENT_INITIALIZED:
    with st.spinner("GoNow Agent is preparing your travel plan..."):
        try:
            final_report = AGENT.plan_trip(
                origin=origin,
                destination=destination,
                group_details=group_details,
                budget=budget,
                user_memory=USER_MEMORY_BANK,
                stay_duration_days=stay_duration_days,
                start_date=start_date
            )
            st.success("Plan Generated!")
            st.markdown(final_report)
            
        except Exception as e:
            st.error(f"An unexpected error occurred during planning: {e}")
            st.info("Check your API keys and the latest traceback in the console.")