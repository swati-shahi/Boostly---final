# Boostly — AI-Powered Adaptive Productivity Platform

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React%2018-61DAFB?style=flat&logo=react)](https://react.dev)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-F7931E?style=flat&logo=scikitlearn)](https://scikit-learn.org)
[![LangChain](https://img.shields.io/badge/Agent-LangChain-1C3C3C?style=flat)](https://www.langchain.com)
[![Docker](https://img.shields.io/badge/Container-Docker-2496ED?style=flat&logo=docker)](https://www.docker.com)

Boostly is a full-stack predictive productivity platform engineered to move beyond static to-do lists. By combining agentic natural language task decomposition with human circadian energy matching and unsupervised burnout anomaly detection (`IsolationForest`), Boostly optimizes daily workflows around cognitive capacity.

---

## Key Features

- **Agentic Task Decomposition**: Conversational input is parsed via LangChain into actionable subtasks with automated cognitive load ratings ($0.1$ to $1.0$).
- **Circadian Energy-to-Task Matching**: Maps high-intensity tasks to peak biological focus windows while scheduling low-friction chores during energy slumps.
- **Burnout Anomaly Detection**: Uses Scikit-learn's `IsolationForest` to analyze workloads against energy telemetry and flag cognitive exhaustion patterns before burnout happens.
- **Tactile Editorial Interface**: Minimalist, distraction-free dashboard built with React and Tailwind CSS.

---

## Tech Stack

- **Frontend**: React 18, Tailwind CSS, Lucide Icons, Axios, Vite
- **Backend**: Python 3.11, FastAPI (Async REST APIs), Pydantic V2
- **Data & ORM**: PostgreSQL / SQLite, SQLAlchemy
- **AI & Analytics**: LangChain, OpenAI API, Scikit-learn (`IsolationForest`), NumPy, Pandas
- **Infrastructure**: Docker, Render

---

## System Architecture

```text
[ React Frontend ] 
       │ (JSON via HTTPS)
       ▼
[ FastAPI Gateway ] ─── (Pydantic Validation & CORS)
       │
       ├──► [ PostgreSQL / SQLite ] (Tasks, Subtasks, Energy Telemetry)
       │
       ├──► [ LangChain Agent ] (Zero-click NLP Decomposition & Cognitive Scoring)
       │
       └──► [ Scikit-Learn Engine ] (IsolationForest Anomaly Detector & Circadian Matcher)