# AI-Agent-GoNow-Travel-Concierge
# ✈️ GoNow: AI Travel Concierge Agent

## 🌟 Project Overview

**GoNow** is a sophisticated, multi-agent system designed to plan **spontaneous, personalized, and budget-constrained trips** instantly. It uses a specialized team of sub-agents to gather real-time data, process user memory, and compile a cohesive, actionable travel report.

This project demonstrates **advanced agentic workflow** using the Gemini API for complex reasoning and planning.

### 🎯 Key Features

* **Real-Time Data Integration:** Uses Serper Search and OpenWeatherMap (via the `Tools` class) for current transport prices, events, and weather.
* **Budget Orchestration:** Dynamically calculates spending limits based on the remaining budget after transport and accommodation costs are secured.
* **Personalization:** Utilizes persistent `USER_MEMORY` (dietary needs, preferred transport) to tailor recommendations.
* **Structured Output:** A dedicated `TravelPlannerAgent` compiles all data into a clean, markdown-formatted final report.

---

## 🧠 System Architecture

The system operates as a **Core Orchestrator** (`agent_core.py`) that manages a team of 8 specialized **Sub-Agents**.

### The Agent Team

| Agent | Responsibility | Output |
| :--- | :--- | :--- |
| **TransportAgent** | Finds and recommends the best travel mode (Flight, Train, Bus). | `round_trip_cost`, `recommended_mode` |
| **BudgetAgent** | Calculates safe limits for accommodation and daily spending. | `accommodation_limit`, `daily_spending_limit` |
| **HotelAgent** | Searches for safe accommodation options within the budget limit. | `accommodation_pick` |
| **WeatherAgent** | Fetches the current forecast for packing guidance. | `weather_summary` |
| **FoodAgent** | Recommends restaurants based on dietary preferences. | `food_recs`  |
| **EventsAgent** | Finds local tourist-friendly events and activities. | `events` |
| **SafetyAgent** | Provides critical safety and scam advisories for the location. | `safety_tips` |
| **TravelPlannerAgent** | Compiles all data into the final, comprehensive report. | Complete `README.md` |



---

## 🛠️ Setup and Installation

Follow these steps to get a copy of the project running on your local machine.

### 1. Clone the Repository

If you used Git:
```bash
git clone [https://github.com/YOUR_USERNAME/GoNow-AI-Travel-Concierge.git](https://github.com/YOUR_USERNAME/GoNow-AI-Travel-Concierge.git)
cd GoNow-AI-Travel-Concierge
````

### 2\. Create Virtual Environment

It is highly recommended to use a virtual environment:

```bash
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate
# On Linux/macOS or Git Bash:
source venv/bin/activate
```

### 3\. Install Dependencies

You'll need `google-genai` for the LLM and `streamlit` for the UI, among other packages (`requests`, `python-dotenv`).

Create a file named **`requirements.txt`** with these dependencies (adjust versions if needed):

```
google-genai
streamlit
python-dotenv
requests
```

Then run:

```bash
pip install -r requirements.txt
```

### 4\. Configure API Keys (The `.env` File)

You need API keys for the Gemini LLM and the Serper Search tool. Create a file named **`.env`** in the root directory and fill it with your keys.
**.env**

```
# Get your key from Google AI Studio
GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE" 

# Get your key from Serper
SERPER_API_KEY="YOUR_SERPER_API_KEY_HERE"

# For OpenWeatherMap (used by WeatherAgent)
OPENWEATHER_API_KEY="YOUR_OPENWEATHER_API_KEY_HERE"
```

-----

## ▶️ How to Run the Agent

You can run the agent in two modes:

### A. Console Mode

This runs the main script with hardcoded inputs defined in `main.py`.

```bash
python main.py
```

### B. Interactive Web UI

Use Streamlit to launch the interactive web application.

```bash
streamlit run ui.py
```

A browser window will open, allowing you to input the origin, destination, budget, and group details before generating the plan.
