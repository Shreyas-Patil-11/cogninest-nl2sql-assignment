from vanna_setup import get_agent, get_memory

class User:
    """Simple User class"""
    def __init__(self, user_id: str, email: str, name: str):
        self.user_id = user_id
        self.email = email
        self.name = name

def seed_agent_memory():
    """
    Seed the agent memory with 15 example Q&A pairs
    """
    
    print("Seeding agent memory with 15 example Q&A pairs...")
    
    agent = get_agent()
    memory = get_memory()
    
    # Create a default user for seeding
    default_user = User(
        user_id="system",
        email="system@clinic.com",
        name="System"
    )
    
    # 15 example Q&A pairs covering different query patterns
    examples = [
        # 1. Simple COUNT
        {
            "question": "How many patients do we have?",
            "sql": "SELECT COUNT(*) AS total_patients FROM patients"
        },
        
        # 2. Simple SELECT with columns
        {
            "question": "List all doctors and their specializations",
            "sql": "SELECT name, specialization, department FROM doctors ORDER BY name"
        },
        
        # 3. Date filtering
        {
            "question": "Show me appointments from last month",
            "sql": """SELECT a.id, p.first_name || ' ' || p.last_name AS patient_name, 
                     d.name AS doctor_name, a.appointment_date, a.status
                     FROM appointments a
                     JOIN patients p ON a.patient_id = p.id
                     JOIN doctors d ON a.doctor_id = d.id
                     WHERE DATE(a.appointment_date) >= DATE('now', '-1 month')
                     ORDER BY a.appointment_date DESC"""
        },
        
        # 4. Aggregation with GROUP BY
        {
            "question": "Which doctor has the most appointments?",
            "sql": """SELECT d.name, COUNT(*) AS appointment_count
                     FROM appointments a
                     JOIN doctors d ON a.doctor_id = d.id
                     GROUP BY d.id, d.name
                     ORDER BY appointment_count DESC
                     LIMIT 1"""
        },
        
        # 5. Financial aggregation
        {
            "question": "What is the total revenue?",
            "sql": "SELECT SUM(total_amount) AS total_revenue FROM invoices"
        },
        
        # 6. Multi-table JOIN with aggregation
        {
            "question": "Show revenue by doctor",
            "sql": """SELECT d.name, SUM(t.cost) AS total_revenue
                     FROM doctors d
                     JOIN appointments a ON d.id = a.doctor_id
                     JOIN treatments t ON a.id = t.appointment_id
                     GROUP BY d.id, d.name
                     ORDER BY total_revenue DESC"""
        },
        
        # 7. Status filtering with date range
        {
            "question": "How many cancelled appointments in the last 3 months?",
            "sql": """SELECT COUNT(*) AS cancelled_count
                     FROM appointments
                     WHERE status = 'Cancelled'
                     AND DATE(appointment_date) >= DATE('now', '-3 months')"""
        },
        
        # 8. TOP N with JOIN
        {
            "question": "Show top 5 patients by total spending",
            "sql": """SELECT p.first_name, p.last_name, SUM(i.total_amount) AS total_spending
                     FROM patients p
                     JOIN invoices i ON p.id = i.patient_id
                     GROUP BY p.id, p.first_name, p.last_name
                     ORDER BY total_spending DESC
                     LIMIT 5"""
        },
        
        # 9. Average with JOIN
        {
            "question": "What is the average treatment cost by specialization?",
            "sql": """SELECT d.specialization, AVG(t.cost) AS avg_cost
                     FROM treatments t
                     JOIN appointments a ON t.appointment_id = a.id
                     JOIN doctors d ON a.doctor_id = d.id
                     GROUP BY d.specialization
                     ORDER BY avg_cost DESC"""
        },
        
        # 10. Time series grouping
        {
            "question": "Show monthly appointment count for the past 6 months",
            "sql": """SELECT strftime('%Y-%m', appointment_date) AS month,
                     COUNT(*) AS appointment_count
                     FROM appointments
                     WHERE DATE(appointment_date) >= DATE('now', '-6 months')
                     GROUP BY month
                     ORDER BY month DESC"""
        },
        
        # 11. GROUP BY with ORDER BY
        {
            "question": "Which city has the most patients?",
            "sql": """SELECT city, COUNT(*) AS patient_count
                     FROM patients
                     WHERE city IS NOT NULL
                     GROUP BY city
                     ORDER BY patient_count DESC
                     LIMIT 1"""
        },
        
        # 12. HAVING clause
        {
            "question": "List patients who have had more than 3 appointments",
            "sql": """SELECT p.first_name, p.last_name, COUNT(*) AS appointment_count
                     FROM patients p
                     JOIN appointments a ON p.id = a.patient_id
                     GROUP BY p.id, p.first_name, p.last_name
                     HAVING COUNT(*) > 3
                     ORDER BY appointment_count DESC"""
        },
        
        # 13. Status filtering
        {
            "question": "Show all unpaid invoices",
            "sql": """SELECT i.id, p.first_name || ' ' || p.last_name AS patient_name,
                     i.invoice_date, i.total_amount, i.paid_amount,
                     (i.total_amount - i.paid_amount) AS balance
                     FROM invoices i
                     JOIN patients p ON i.patient_id = p.id
                     WHERE i.status IN ('Pending', 'Overdue')
                     ORDER BY i.invoice_date"""
        },
        
        # 14. Percentage calculation
        {
            "question": "What percentage of appointments are no-shows?",
            "sql": """SELECT 
                     ROUND(100.0 * SUM(CASE WHEN status = 'No-Show' THEN 1 ELSE 0 END) / COUNT(*), 2) 
                     AS no_show_percentage
                     FROM appointments"""
        },
        
        # 15. Department aggregation
        {
            "question": "Compare revenue between departments",
            "sql": """SELECT d.department, SUM(t.cost) AS total_revenue
                     FROM doctors d
                     JOIN appointments a ON d.id = a.doctor_id
                     JOIN treatments t ON a.id = t.appointment_id
                     GROUP BY d.department
                     ORDER BY total_revenue DESC"""
        }
    ]
    
    # Seed each example into memory
    for idx, example in enumerate(examples, 1):
        try:
            # Add to agent's memory
            agent.add_to_memory(example["question"], example["sql"])
            
            # Add to memory tracker
            memory.save_tool_use(
                user=default_user,
                question=example["question"],
                tool_name="run_sql",
                tool_args={"sql": example["sql"]},
                result={"success": True}
            )
            
            print(f"✓ Seeded ({idx}/15): {example['question']}")
        except Exception as e:
            print(f"✗ Failed to seed ({idx}/15): {example['question']}")
            print(f"  Error: {str(e)}")
    
    print(f"\n✓ Agent memory initialized with {len(examples)} examples")
    print("Memory seeding complete!")

if __name__ == '__main__':
    seed_agent_memory()