from .system import get_system_time
from .stats import get_internship_stats
from .problem_index import get_problem_index
from .search import search_knowledge_base
from .weather_aqi import get_weather_and_aqi

tools = [
    get_system_time,
    get_internship_stats,
    get_problem_index,
    search_knowledge_base,
    get_weather_and_aqi,
]
