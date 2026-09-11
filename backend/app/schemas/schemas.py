from pydantic import BaseModel, Field
from typing import List, Optional
import datetime

# --- SubTask Schemas ---
class SubTaskBase(BaseModel):
    title: str
    cognitive_load: float = Field(ge=0.1, le=1.0, description="Estimated cognitive load from 0.1 to 1.0")
    estimated_minutes: int = Field(gt=0, description="Duration in minutes")

class SubTaskCreate(SubTaskBase):
    pass

class SubTaskResponse(SubTaskBase):
    id: int
    task_id: int
    completed: bool

    class Config:
        from_attributes = True


# --- Task Schemas ---
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    cognitive_load: float = Field(default=0.5, ge=0.1, le=1.0)
    estimated_minutes: int = Field(default=30, gt=0)

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    scheduled_hour: Optional[int] = None
    completed: bool
    created_at: datetime.datetime
    subtasks: List[SubTaskResponse] = []

    class Config:
        from_attributes = True


# --- Agentic NLP Input Schema ---
class NaturalLanguageTaskInput(BaseModel):
    raw_prompt: str = Field(..., min_length=3, example="Finish investor deck slides tomorrow, will take 2 hours")


# --- Energy Log Schemas ---
class EnergyLogCreate(BaseModel):
    hour_of_day: int = Field(ge=0, le=23)
    energy_level: int = Field(ge=1, le=5)
    hours_worked_today: float = Field(ge=0.0)

class EnergyLogResponse(EnergyLogCreate):
    id: int
    timestamp: datetime.datetime
    burnout_flag: bool

    class Config:
        from_attributes = True


# --- Analytics Response ---
class BurnoutAssessmentResponse(BaseModel):
    burnout_detected: bool
    risk_score: float
    message: str