from typing import TypedDict, List

class AgentState(TypedDict):
    question: str
    research_notes: List[str]
    answer: str
    satisfied: bool
 