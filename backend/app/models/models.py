import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    cognitive_load = Column(Float, nullable=False, default=0.5)  # 0.1 (trivial) to 1.0 (deep focus)
    estimated_minutes = Column(Integer, default=30)
    scheduled_hour = Column(Integer, nullable=True)             # 0 to 23
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    subtasks = relationship("SubTask", back_populates="parent_task", cascade="all, delete-orphan")


class SubTask(Base):
    __tablename__ = "subtasks"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    title = Column(String(255), nullable=False)
    cognitive_load = Column(Float, nullable=False, default=0.5)
    estimated_minutes = Column(Integer, default=15)
    completed = Column(Boolean, default=False)

    parent_task = relationship("Task", back_populates="subtasks")


class EnergyLog(Base):
    __tablename__ = "energy_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    hour_of_day = Column(Integer, nullable=False)               # 0 to 23
    energy_level = Column(Integer, nullable=False)              # 1 (exhausted) to 5 (peak energy)
    hours_worked_today = Column(Float, nullable=False, default=0.0)
    burnout_flag = Column(Boolean, default=False)               # Populated by ML