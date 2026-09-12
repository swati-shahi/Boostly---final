# Boostly — Adaptive Circadian Productivity Platform

[![Live Demo](https://img.shields.io/badge/Live_Demo-Render-46E3B7?style=flat&logo=render)](https://boostly-final.onrender.com/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React%2018-61DAFB?style=flat&logo=react)](https://react.dev)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-F7931E?style=flat&logo=scikitlearn)](https://scikit-learn.org)
[![LangChain](https://img.shields.io/badge/Agent-LangChain-1C3C3C?style=flat)](https://www.langchain.com)
[![Docker](https://img.shields.io/badge/Container-Docker-2496ED?style=flat&logo=docker)](https://www.docker.com)

Boostly is a full-stack predictive productivity platform engineered to move beyond static to-do lists. By combining agentic natural language task decomposition with human circadian energy matching and unsupervised burnout anomaly detection (`IsolationForest`), Boostly optimizes daily workflows around actual cognitive capacity.

🔗 **Live Application:** [https://boostly-final.onrender.com/](https://boostly-final.onrender.com/)  
🔗 **Backend API:** [https://boostly-api-0l3f.onrender.com/docs](https://boostly-api-0l3f.onrender.com/docs)

---

## Key Features

* **Agentic Task Decomposition**: Conversational input is parsed via LangChain into bite-sized, actionable milestones with automated cognitive load ratings ($0.1$ to $1.0$).
* **Circadian Energy-to-Task Matching**: Maps high-intensity tasks to peak biological focus windows while scheduling low-friction chores during energy slumps.
* **Burnout Anomaly Detection**: Uses Scikit-learn's `IsolationForest` to analyze workloads against energy telemetry and flag cognitive exhaustion patterns before burnout occurs.
* **Tactile Editorial Interface**: Minimalist, distraction-free dashboard built with React, Vite, and Tailwind CSS.

---

## Tech Stack

* **Frontend**: React 18, Tailwind CSS, Lucide Icons, Axios, Vite
* **Backend**: Python 3.11, FastAPI (Async REST APIs), Pydantic V2
* **Database & ORM**: SQLite / PostgreSQL, SQLAlchemy ORM
* **AI & Machine Learning**: LangChain, Scikit-learn (`IsolationForest`), NumPy, Pandas
* **Infrastructure & Deployment**: Docker, Render Cloud

---
## System Architecture

```text
[ React 18 Client ]
       │ (JSON via HTTPS)
       ▼
[ FastAPI Gateway ] ─── (Pydantic Validation & CORS)
       │
       ├──► [ SQLite / PostgreSQL ] (Tasks, Subtasks, Energy Telemetry via SQLAlchemy)
       │
       ├──► [ LangChain Agent ] (Zero-click NLP Decomposition & Cognitive Scoring)
       │
       └──► [ Scikit-Learn Engine ] (IsolationForest Anomaly Detector & Circadian Matcher)
```

---

## Getting Started Locally

### 1. Backend Service

```bash
# Clone the repository
git clone [https://github.com/swati-shahi/Boostly---final.git](https://github.com/swati-shahi/Boostly---final.git)
cd Boostly---final

# Setup virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies and start server
pip install -r backend/requirements.txt
uvicorn app.main:app --reload --app-dir backend
```

*Interactive Swagger documentation available at `http://127.0.0.1:8000/docs`.*

### 2. Frontend Client

```bash
cd frontend
npm install
npm run dev
```

*Client runs locally at `http://localhost:5173`.*

---

## API Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/tasks` | Fetches all tasks and nested decomposed milestones |
| `POST` | `/api/v1/tasks/quick-log` | Parses raw text via LangChain and assigns cognitive load |
| `POST` | `/api/v1/tasks/rebalance-circadian` | Optimizes schedule against circadian peak windows |
| `POST` | `/api/v1/telemetry/energy` | Ingests subjective energy ratings and hours worked |
| `GET` | `/api/v1/analytics/burnout-assessment` | Evaluates burnout risk score via `IsolationForest` |


