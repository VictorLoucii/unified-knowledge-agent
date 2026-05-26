from langchain_core.tools import tool

@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """Returns the current system time. Use this when the user asks for the time."""
    from datetime import datetime

    return datetime.now().strftime(format)
