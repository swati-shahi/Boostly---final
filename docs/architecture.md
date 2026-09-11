# Boostly — System Architecture

## Overview
Boostly is an adaptive productivity platform engineered to align task scheduling with human circadian biology and prevent cognitive burnout.

## High-Level Architecture Flow

```text
[ React Frontend ] 
       │  (JSON REST via HTTPS)
       ▼
[ FastAPI Gateway ] ─── (Pydantic Validation & Security)
       │
       ├──► [ PostgreSQL ] (Task states, Circadian baseline, Biometric energy logs)
       │
       ├──► [ LangChain Agent ] (Zero-click NLP task ingestion & cognitive load scoring)
       │
       └──► [ Scikit-Learn Engine ] (IsolationForest burnout anomaly & circadian matching)