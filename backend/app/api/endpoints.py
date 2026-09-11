from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
import datetime

from app.core.database import get_db
from app.models import Task, SubTask, EnergyLog
from app.schemas import (
    TaskCreate, TaskResponse,
    NaturalLanguageTaskInput,
    EnergyLogCreate, EnergyLogResponse,
    BurnoutAssessmentResponse
)
from app.services import agent_service, analytics_engine

router = APIRouter()

# --- 1. Agentic NLP Decomposition & Zero-Click Task Creation ---
@router.post("/tasks/quick-log", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def quick_log_task(payload: NaturalLanguageTaskInput, db: Session = Depends(get_db)):
    """
    Zero-click ingestion: Decomposes raw prompt via LangChain agent
    and stores structured parent task and subtasks.
    """
    decomposed = agent_service.process_prompt(payload.raw_prompt)

    # Heuristic circadian default: place high-focus tasks in morning (10 AM), low-focus in afternoon (3 PM)
    default_hour = 10 if decomposed.overall_cognitive_load >= 0.6 else 15

    new_task = Task(
        title=decomposed.title,
        description=decomposed.description,
        cognitive_load=decomposed.overall_cognitive_load,
        estimated_minutes=decomposed.total_estimated_minutes,
        scheduled_hour=default_hour
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    for st in decomposed.subtasks:
        subtask_record = SubTask(
            task_id=new_task.id,
            title=st.title,
            cognitive_load=st.cognitive_load,
            estimated_minutes=st.estimated_minutes
        )
        db.add(subtask_record)

    db.commit()
    db.refresh(new_task)
    return new_task


# --- 2. Task Management & Schedule Endpoints ---
@router.get("/tasks", response_model=List[TaskResponse])
def get_all_tasks(db: Session = Depends(get_db)):
    """Retrieve all logged tasks with decomposed subtasks."""
    return db.query(Task).order_by(Task.created_at.desc()).all()


@router.post("/tasks/rebalance-circadian", response_model=List[TaskResponse])
def rebalance_tasks(db: Session = Depends(get_db)):
    """
    Matches unfinished tasks to hourly circadian energy patterns.
    """
    tasks = db.query(Task).filter(Task.completed == False).all()
    if not tasks:
        return []

    # Derive energy baseline from historical logs (fallback to typical human circadian curve)
    # Peak at 9-11 AM, dip at 2-3 PM, secondary peak at 5-6 PM
    circadian_curve = {
        8: 3.2, 9: 4.5, 10: 4.8, 11: 4.2, 12: 3.0,
        13: 2.5, 14: 2.2, 15: 3.0, 16: 3.8, 17: 4.0, 18: 3.5
    }

    task_dicts = [
        {"id": t.id, "title": t.title, "cognitive_load": t.cognitive_load}
        for t in tasks
    ]

    rebalanced = analytics_engine.match_tasks_to_circadian_rhythm(task_dicts, circadian_curve)

    for reb in rebalanced:
        db_task = db.query(Task).filter(Task.id == reb["id"]).first()
        if db_task:
            db_task.scheduled_hour = reb.get("scheduled_hour")

    db.commit()
    return db.query(Task).filter(Task.completed == False).all()


# --- 3. Telemetry & Energy Logging ---
@router.post("/telemetry/energy", response_model=EnergyLogResponse, status_code=status.HTTP_201_CREATED)
def log_energy(payload: EnergyLogCreate, db: Session = Depends(get_db)):
    """Log current biometric/self-reported energy level and hours worked."""
    log_entry = EnergyLog(
        hour_of_day=payload.hour_of_day,
        energy_level=payload.energy_level,
        hours_worked_today=payload.hours_worked_today
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry


# --- 4. Burnout Anomaly Detection ---
@router.get("/analytics/burnout-assessment", response_model=BurnoutAssessmentResponse)
def assess_burnout(db: Session = Depends(get_db)):
    """Runs IsolationForest on historical logs to detect burnout risks."""
    logs = db.query(EnergyLog).order_by(EnergyLog.timestamp.asc()).all()
    historical_data = [
        {"hours_worked_today": l.hours_worked_today, "energy_level": l.energy_level}
        for l in logs
    ]

    is_burnout, score, message = analytics_engine.detect_burnout_risk(historical_data)
    return BurnoutAssessmentResponse(
        burnout_detected=is_burnout,
        risk_score=score,
        message=message
    )