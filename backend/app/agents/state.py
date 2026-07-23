from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    user_id: str
    current_date: str
    athlete_profile: dict
    active_focus: str
    macro_plan: dict
    current_week: dict
    fitness_data: dict
    wellness_data: dict
    recent_activities: list
    analysis_template: str
    human_feedback: dict
    messages: Annotated[list, add_messages]
