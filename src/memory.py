USER_MEMORY_BANK = {
    "Preferred_Transport": "Train",
    "Dietary_Restrictions": "Vegetarian",
    "Group_History": [],
    "Budget_Limits": None,
    "Travel_Companions": []
}

# Save a new preference
def save_memory(key, value):
    print(f"DEBUG: Saving '{key}': '{value}' to memory.")
    USER_MEMORY_BANK[key] = value

# Add a travel history entry
def add_trip_history(trip_info):
    if "Group_History" not in USER_MEMORY_BANK:
        USER_MEMORY_BANK["Group_History"] = []
    USER_MEMORY_BANK["Group_History"].append(trip_info)

# Clear all memory
def clear_memory():
    global USER_MEMORY_BANK
    USER_MEMORY_BANK = {}
    print("DEBUG: Cleared memory.")
class Memory:
    """
    Manages all user memory, context, and potentially state for the agents.
    """
    def __init__(self, data_source=USER_MEMORY_BANK):
        # Initialize memory storage, often by loading data from a file or database
        self._user_data = data_source
        self._trip_context = {} # Stores current trip details during planning
    def load_user_data(self, data: dict):
        """
        Loads or overwrites the persistent user memory store 
        with data passed from the main script.
        """
        print(f"DEBUG: Loading {len(data)} user memory key(s) into agent memory.")
        self._user_data = data
    def get_user_data(self, user_id="Trivandrum_user"):
        """Retrieves persistent data for a specific user."""
        return self._user_data.get(user_id, {})

    def update_context(self, key, value):
        """Updates the running context for the current trip (e.g., 'chosen_hotel')."""
        self._trip_context[key] = value
        
    def get_context(self, key=None):
        """Retrieves the current trip context."""
        if key:
            return self._trip_context.get(key)
        return self._trip_context