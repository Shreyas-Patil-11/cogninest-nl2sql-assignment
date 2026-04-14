

import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()

class AgentMemory:
    def __init__(self):
        self.items = []

    def save_tool_use(self, user, question, tool_name, tool_args, result):
        self.items.append({
            "question": question,
            "tool_name": tool_name,
            "tool_args": tool_args,
            "result": result
        })

    def get_count(self):
        return len(self.items)


class VannaAgent:
    def __init__(self, api_key, db_path):
        self.api_key = api_key
        self.db_path = db_path
        self.memory = []

        from groq import Groq
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

        # ✅ CACHE schema (IMPORTANT FIX)
        self.schema = self.get_schema()

    def get_schema(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        schema = "Database Schema:\n\n"

        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()

            schema += f"Table: {table_name}\n"
            for col in columns:
                schema += f"  - {col[1]} ({col[2]})\n"
            schema += "\n"

        conn.close()
        return schema

    def add_to_memory(self, question, sql):
        self.memory.append({"question": question, "sql": sql})

    def get_relevant_examples(self, question, limit=3):
        if not self.memory:
            return ""

        examples = "\n\nExamples:\n"
        for ex in self.memory[:limit]:
            examples += f"Q: {ex['question']}\nSQL: {ex['sql']}\n\n"
        return examples

    def generate_sql(self, question):
        prompt = f"""
You are a SQL expert. Generate SQL only.

{self.schema}

{self.get_relevant_examples(question)}

Question: {question}
SQL:
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=300
        )

        sql = response.choices[0].message.content.strip()

        # Clean formatting
        sql = sql.replace("```sql", "").replace("```", "").strip()
        return sql

    def run_sql(self, sql):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(sql)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return {"columns": columns, "rows": rows}

        except Exception as e:
            return {
                "columns": [],
                "rows": [],
                "error": str(e)
            }

        finally:
            conn.close()


vanna_agent = None
vanna_memory = None


def create_agent_and_memory():
    global vanna_agent, vanna_memory

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Missing GROQ_API_KEY")

    vanna_agent = VannaAgent(api_key, "clinic.db")
    vanna_memory = AgentMemory()

    return vanna_agent, vanna_memory


def get_agent():
    global vanna_agent
    if vanna_agent is None:
        create_agent_and_memory()
    return vanna_agent


def get_memory():
    global vanna_memory
    if vanna_memory is None:
        create_agent_and_memory()
    return vanna_memory