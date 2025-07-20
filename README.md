# Δemokraton

![Build Status](https://github.com/salawi45/thedemodeck/workflows/CI/badge.svg)  
![License](https://img.shields.io/github/license/salawi45/thedemodeck)

> Data = wisedome — A vote‐impact analysis platform.

## 🚀 Features
- Ingests Wikidata, ProPublica votes, Census metrics, LLM‐powered impact writeups  
- Predicts vote outcomes based on ideology  
- React frontend + Django REST backend

## 🔧 Quick Start

### 1. Backend
```bash
cd MyUsaCandidateBackEnd/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
