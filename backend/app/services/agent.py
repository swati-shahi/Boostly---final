import json
from typing import List, Optional
from pydantic import BaseModel, Field
from app.core.config import settings

# Structured schema definitions for the LLM output
class ExtractedSubTask(BaseModel):
    title: str = Field(description="Actionable and specific title of the subtask")
    cognitive_load: float = Field(
        description="Estimated mental focus requirement from 0.1 (low/admin) to 1.0 (deep analytical work)",
        ge=0.1,
        le=1.0
    )
    estimated_minutes: int = Field(
        description="Estimated duration in minutes for this subtask",
        gt=0
    )

class DecomposedTaskResult(BaseModel):
    title: str = Field(description="Clean, concise summary title of the overall task")
    description: Optional[str] = Field(None, description="Detailed context or intent extracted from the user input")
    overall_cognitive_load: float = Field(description="Average or dominant cognitive load score (0.1 - 1.0)")
    total_estimated_minutes: int = Field(description="Total estimated time across subtasks")
    subtasks: List[ExtractedSubTask] = Field(description="List of ordered subtasks decomposed by the agent")


class TaskDecompositionAgent:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.llm = None
        
        # Initialize LangChain LLM if API key is present
        if self.api_key and self.api_key.startswith("sk-"):
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.2,
                api_key=self.api_key
            ).with_structured_output(DecomposedTaskResult)

    def process_prompt(self, raw_prompt: str) -> DecomposedTaskResult:
        """
        Parses unstructured natural language into structured subtasks with cognitive load ratings.
        Falls back to rule-based decomposition if LLM key is absent.
        """
        if self.llm:
            try:
                system_prompt = (
                    "You are Boostly's cognitive task decomposition agent. "
                    "Analyze the user's conversational task input. "
                    "Decompose it into 2 to 4 actionable, logically ordered subtasks. "
                    "Assign an estimated cognitive load (0.1 to 1.0) and estimated duration in minutes to each."
                )
                return self.llm.invoke(f"{system_prompt}\n\nUser Input: {raw_prompt}")
            except Exception as e:
                # In case of API failure, fall back gracefully
                print(f"[Agent Warning] LLM invocation failed: {e}. Defaulting to heuristic agent.")

        return self._heuristic_fallback(raw_prompt)

    def _heuristic_fallback(self, raw_prompt: str) -> DecomposedTaskResult:
        """
        Deterministic agentic parser ensuring the API works locally out-of-the-box
        without requiring immediate third-party API spend.
        """
        clean_title = raw_prompt.strip().capitalize()
        if len(clean_title) > 60:
            clean_title = clean_title[:57] + "..."

        subtasks = [
            ExtractedSubTask(
                title=f"Plan & research: {clean_title}",
                cognitive_load=0.7,
                estimated_minutes=30
            ),
            ExtractedSubTask(
                title=f"Execute core work: {clean_title}",
                cognitive_load=0.9,
                estimated_minutes=60
            ),
            ExtractedSubTask(
                title=f"Review & finalize: {clean_title}",
                cognitive_load=0.4,
                estimated_minutes=20
            ),
        ]

        total_mins = sum(s.estimated_minutes for s in subtasks)
        avg_load = round(sum(s.cognitive_load for s in subtasks) / len(subtasks), 2)

        return DecomposedTaskResult(
            title=clean_title,
            description=f"Automated decomposition generated from prompt: '{raw_prompt}'",
            overall_cognitive_load=avg_load,
            total_estimated_minutes=total_mins,
            subtasks=subtasks
        )

# Singleton instance
agent_service = TaskDecompositionAgent()