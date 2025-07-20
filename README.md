# Δemokraton

![Build Status](https://github.com/salawi45/thedemodeck/workflows/CI/badge.svg)  
![License](https://img.shields.io/github/license/salawi45/thedemodeck)

> Data = wisedome — A vote‐impact analysis platform.

## 🚀 Features
- Ingests Wikidata, ProPublica votes, Census metrics, LLM‐powered impact writeups  
- Predicts vote outcomes based on ideology  
- React frontend + Django REST backend
- (in progress) Predicts vote impact on daily life

## 🔧 Quick Start

### 1. Backend

cd MyUsaCandidateBackEnd/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


### 2. Frontend
cd ../../frontend
npm install
npm start

### 3. Structure
/demokraton
  /MyUsaCandidateBackEnd
    /backend           # Django REST + ETL scripts
    venv/              # Python virtualenv
  /frontend           # React app
  /docs               # (optional) extended documentation
  README.md
  CONTRIBUTING.md
  CODE_OF_CONDUCT.md
  LICENSE
  .gitignore
  /.github



