#  NL2SQL Clinic Chatbot

An AI-powered Natural Language to SQL (NL2SQL) system that allows users to query a clinic database using plain English. Built using FastAPI, SQLite, and Groq LLM.

---

##  Project Overview

This project converts natural language questions into SQL queries, executes them on a database, and returns structured results.

###  Pipeline

User Question → FastAPI → LLM (Groq) → SQL → SQLite DB → Results

---

##  Features

- Convert English questions to SQL queries
- Execute queries on real database
- Return structured results (rows, columns)
- Error handling for invalid queries
- Automated testing (20 test cases)
- Simple web UI (HTML frontend)
- Results saved in `RESULTS.md`

---

##  Tech Stack

- Python 3.10+
- FastAPI
- SQLite
- Groq (Llama 3.3)
- Pandas
- Plotly

---

##  Setup Instructions

```bash
pip install -r requirements.txt
python setup_database.py
python seed_memory.py
uvicorn main:app --reload --port 8000
```

---

##  Test Results

- Total Questions: 20  
- Passed: 20  
- Failed: 0  
- Success Rate: 100%

---

##  API Endpoints

### POST /chat

Request:
```json
{
  "question": "Show top 5 patients by spending"
}
```

Response:
```json
{
  "message": "Success",
  "sql_query": "SELECT ...",
  "columns": ["name", "amount"],
  "rows": [["John", 5000]],
  "row_count": 5
}
```

---

## 👨 Author

AI/ML Developer Intern Candidate
