from .system import get_system_time
from .search import search_knowledge_base
from .weather_aqi import get_weather_and_aqi

tools = [
    get_system_time,
    search_knowledge_base,
    get_weather_and_aqi,
]
