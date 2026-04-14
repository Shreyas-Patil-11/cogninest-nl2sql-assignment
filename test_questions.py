

import requests
import time
from datetime import datetime

API_URL = "http://localhost:8000/chat"

TEST_QUESTIONS = [
    "How many patients do we have?",
    "List all doctors and their specializations",
    "Show me appointments for last month",
    "Which doctor has the most appointments?",
    "What is the total revenue?",
    "Show revenue by doctor",
    "How many cancelled appointments last quarter?",
    "Top 5 patients by spending",
    "Average treatment cost by specialization",
    "Show monthly appointment count for the past 6 months",
    "Which city has the most patients?",
    "List patients who visited more than 3 times",
    "Show unpaid invoices",
    "What percentage of appointments are no-shows?",
    "Show the busiest day of the week for appointments",
    "Revenue trend by month",
    "Average appointment duration by doctor",
    "List patients with overdue invoices",
    "Compare revenue between departments",
    "Show patient registration trend by month"
]


def test_question(question):
    try:
        response = requests.post(
            API_URL,
            json={"question": question},
            timeout=60
        )

        print("RAW RESPONSE:", response.text)

        if response.status_code == 200:
            if not response.text.strip():
                return {"error": "Empty response"}

            try:
                return response.json()
            except Exception:
                return {"error": "Invalid JSON"}
        else:
            return {"error": f"HTTP {response.status_code}"}

    except requests.exceptions.Timeout:
        return {"error": "Timeout"}

    except requests.exceptions.ConnectionError:
        return {"error": "Connection failed"}

    except Exception as e:
        return {"error": str(e)}


def run_all_tests():
    print("=" * 80)
    print("NL2SQL CHATBOT - TEST RESULTS")
    print("=" * 80)

    start_time = datetime.now()
    print(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Testing {len(TEST_QUESTIONS)} questions...\n")

    passed = 0
    failed = 0
    results_log = []

    for idx, question in enumerate(TEST_QUESTIONS, 1):
        print(f"[{idx}/{len(TEST_QUESTIONS)}] {question}")

        result = test_question(question) or {}

        if "error" in result:
            failed += 1
            print(f"  ❌ FAIL: {result.get('error')}")
        else:
            row_count = result.get("row_count", 0)
            sql = result.get("sql_query", "")

            if row_count > 0:
                passed += 1
                print(f"  ✅ PASS: {row_count} rows returned")
            else:
                print("  ⚠️ PARTIAL: No data")

            if sql:
                short_sql = sql[:120] + "..." if len(sql) > 120 else sql
                print(f"  🧾 SQL: {short_sql}")

        print()

        results_log.append({
            "question": question,
            "result": result
        })

        time.sleep(2)  # prevent API overload

    # =========================
    # SAVE RESULTS TO FILE
    # =========================
    with open("RESULTS.md", "w", encoding="utf-8") as f:
        f.write("# NL2SQL Test Results\n\n")
        f.write(f"**Started at:** {start_time}\n\n")

        for i, item in enumerate(results_log, 1):
            q = item["question"]
            r = item["result"]

            f.write(f"## {i}. {q}\n")

            if not r or "error" in r:
                f.write(f"- ❌ Error: {r.get('error', 'Unknown')}\n\n")
            else:
                f.write(f"- ✅ Rows Returned: {r.get('row_count')}\n\n")
                f.write("**SQL Query:**\n")
                f.write("```sql\n")
                f.write(r.get("sql_query", ""))
                f.write("\n```\n\n")

        f.write("---\n")
        f.write(f"**Total:** {len(TEST_QUESTIONS)}\n")
        f.write(f"**Passed:** {passed}\n")
        f.write(f"**Failed:** {failed}\n")
        f.write(f"**Success Rate:** {(passed/len(TEST_QUESTIONS))*100:.1f}%\n")

    # =========================
    # PRINT SUMMARY
    # =========================
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total: {len(TEST_QUESTIONS)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/len(TEST_QUESTIONS))*100:.1f}%")
    print("=" * 80)

    print("\n📄 Results saved to RESULTS.md")


if __name__ == "__main__":
    print("\n⚠️ Make sure FastAPI server is running at http://localhost:8000")
    print("Run: uvicorn main:app --reload\n")

    input("Press Enter to start testing...")

    run_all_tests()