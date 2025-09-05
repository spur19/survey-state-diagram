from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class State(BaseModel):
    """Represents a single state in the survey state diagram."""

    depth: int = Field(..., ge=0, description="How far the question is from the starting question")
    prev_question: Optional[str] = Field(
        default=None, description="What the previous question was"
    )
    prev_question_answer: Optional[str] = Field(
        default=None, description="What the answer to the previous question was"
    )
    current_question: str = Field(..., description="What the current question is")
    next_question: Optional[str] = Field(
        default=None, description="What the next question is"
    )


class StateList(BaseModel):
    """Dictionary that maps question ids to a list of survey states, with an 8-letter UUID per question."""

    question_states: Dict[str, List[State]]

