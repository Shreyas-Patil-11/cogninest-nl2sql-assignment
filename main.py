from unittest import result

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import re
import sqlite3
from vanna_setup import get_agent, get_memory
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Initialize FastAPI app
app = FastAPI(
    title="NL2SQL Clinic Chatbot",
    description="Natural Language to SQL conversion for clinic management system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple User class
class User:
    def __init__(self, user_id: str, email: str, name: str):
        self.user_id = user_id
        self.email = email
        self.name = name

class RequestContext:
    def __init__(self, request_id: str):
        self.request_id = request_id

# Request/Response Models
class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500, description="Natural language question")

class ChatResponse(BaseModel):
    message: str
    sql_query: Optional[str] = None
    columns: Optional[List[str]] = None
    rows: Optional[List[List[Any]]] = None
    row_count: Optional[int] = None
    chart: Optional[Dict[str, Any]] = None
    chart_type: Optional[str] = None

class ErrorResponse(BaseModel):
    error: str
    sql_query: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    database: str
    agent_memory_items: int
    llm_provider: str
    database_stats: Optional[Dict[str, int]] = None

# SQL Validation
def validate_sql(sql: str) -> tuple[bool, Optional[str]]:
    """
    Validate SQL query for security
    Returns: (is_valid, error_message)
    """
    if not sql or not sql.strip():
        return False, "Empty SQL query"
    
    sql_upper = sql.upper().strip()
    
    # 1. Must be SELECT only
    if not sql_upper.startswith('SELECT'):
        return False, "Only SELECT queries are allowed"
    
    # 2. Check for dangerous keywords
    dangerous_keywords = [
        'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER',
        'TRUNCATE', 'EXEC', 'EXECUTE', 'XP_', 'SP_',
        'GRANT', 'REVOKE', 'SHUTDOWN', 'ATTACH', 'DETACH'
    ]
    
    for keyword in dangerous_keywords:
        # Use word boundaries to avoid false positives
        pattern = r'\b' + keyword + r'\b'
        if re.search(pattern, sql_upper):
            return False, f"SQL validation failed: Dangerous keyword '{keyword}' detected"
    
    # 3. Check for system table access
    system_tables = ['sqlite_master', 'sqlite_sequence', 'sqlite_stat1']
    for table in system_tables:
        if table.upper() in sql_upper:
            return False, f"Access to system table '{table}' is not allowed"
    
    # 4. Prevent multiple statements
    if ';' in sql.rstrip(';'):
        return False, "Multiple SQL statements are not allowed"
    
    return True, None

# Helper functions
def get_database_stats() -> Dict[str, int]:
    """Get counts from all tables"""
    try:
        conn = sqlite3.connect('clinic.db')
        cursor = conn.cursor()
        
        stats = {}
        tables = ['patients', 'doctors', 'appointments', 'treatments', 'invoices']
        
        for table in tables:
            cursor.execute(f'SELECT COUNT(*) FROM {table}')
            stats[table] = cursor.fetchone()[0]
        
        conn.close()
        return stats
    except Exception as e:
        return {}

def format_results(sql: str, columns: List[str], rows: List[tuple]) -> str:
    """Format query results into a human-readable message"""
    if not rows:
        return "No results found for your query."
    
    row_count = len(rows)
    
    # For simple COUNT queries
    if len(columns) == 1 and any(word in columns[0].lower() for word in ['count', 'total', 'percentage']):
        return f"Result: {rows[0][0]}"
    
    # For aggregate queries with few results
    if row_count <= 5:
        message = f"Found {row_count} result(s):\n\n"
        for row in rows:
            row_parts = []
            for col, val in zip(columns, row):
                if val is not None:
                    row_parts.append(f"{col}: {val}")
            message += "  • " + ", ".join(row_parts) + "\n"
        return message.strip()
    
    # For larger result sets
    return f"Query returned {row_count} rows successfully."

# API Endpoints
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "NL2SQL Clinic Chatbot API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Check system health and status"""
    try:
        # Check database connection
        conn = sqlite3.connect('clinic.db')
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        conn.close()
        db_status = "connected"
        
        # Get database stats
        stats = get_database_stats()
        
        # Get agent memory count
        memory = get_memory()
        memory_count = memory.get_count()
        
        return HealthResponse(
            status="ok",
            database=db_status,
            agent_memory_items=memory_count,
            llm_provider="Groq (Llama 3.3 70B)",
            database_stats=stats
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


from fastapi.responses import JSONResponse

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        question = request.question.strip()
        print("\n📩 Question:", question)

        agent = get_agent()

        import time
        start = time.time()

        sql_query = agent.generate_sql(question)

        print("⚡ SQL generated in:", round(time.time() - start, 2), "sec")
        print("🧾 SQL:", sql_query)

        result = agent.run_sql(sql_query)

        # ✅ ALWAYS return proper JSON
        return JSONResponse(content={
            "message": "Success",
            "sql_query": sql_query,
            "columns": result.get("columns", []),
            "rows": result.get("rows", []),
            "row_count": len(result.get("rows", []))
        })

    except Exception as e:
        print("❌ ERROR:", str(e))

        # ✅ NEVER return None
        return JSONResponse(content={
            "error": str(e),
            "sql_query": None,
            "columns": [],
            "rows": [],
            "row_count": 0
        })

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/ui", tags=["UI"])
async def serve_ui():
    """Serve the web UI"""
    return FileResponse("static/index.html")

# Run with: uvicorn main:app --reload --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
 