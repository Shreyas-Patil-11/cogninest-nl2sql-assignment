import sqlite3
import random
from datetime import datetime, timedelta

def create_database():
    """Create SQLite database with clinic management schema and dummy data"""
    
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    
    # Drop existing tables if they exist
    cursor.execute('DROP TABLE IF EXISTS invoices')
    cursor.execute('DROP TABLE IF EXISTS treatments')
    cursor.execute('DROP TABLE IF EXISTS appointments')
    cursor.execute('DROP TABLE IF EXISTS doctors')
    cursor.execute('DROP TABLE IF EXISTS patients')
    
    # Create patients table
    cursor.execute('''
    CREATE TABLE patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        date_of_birth DATE,
        gender TEXT,
        city TEXT,
        registered_date DATE
    )
    ''')
    
    # Create doctors table
    cursor.execute('''
    CREATE TABLE doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT,
        department TEXT,
        phone TEXT
    )
    ''')
    
    # Create appointments table
    cursor.execute('''
    CREATE TABLE appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        appointment_date DATETIME,
        status TEXT,
        notes TEXT,
        FOREIGN KEY (patient_id) REFERENCES patients(id),
        FOREIGN KEY (doctor_id) REFERENCES doctors(id)
    )
    ''')
    
    # Create treatments table
    cursor.execute('''
    CREATE TABLE treatments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_id INTEGER,
        treatment_name TEXT,
        cost REAL,
        duration_minutes INTEGER,
        FOREIGN KEY (appointment_id) REFERENCES appointments(id)
    )
    ''')
    
    # Create invoices table
    cursor.execute('''
    CREATE TABLE invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        invoice_date DATE,
        total_amount REAL,
        paid_amount REAL,
        status TEXT,
        FOREIGN KEY (patient_id) REFERENCES patients(id)
    )
    ''')
    
    conn.commit()
    print("✓ Created database schema")
    
    # Insert dummy data
    insert_doctors(cursor)
    insert_patients(cursor)
    insert_appointments(cursor)
    insert_treatments(cursor)
    insert_invoices(cursor)
    
    conn.commit()
    
    # Print summary
    cursor.execute('SELECT COUNT(*) FROM patients')
    patient_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM doctors')
    doctor_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM appointments')
    appointment_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM treatments')
    treatment_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM invoices')
    invoice_count = cursor.fetchone()[0]
    
    print(f"✓ Inserted {doctor_count} doctors across 5 specializations")
    print(f"✓ Inserted {patient_count} patients across 10 cities")
    print(f"✓ Inserted {appointment_count} appointments")
    print(f"✓ Inserted {treatment_count} treatments")
    print(f"✓ Inserted {invoice_count} invoices")
    print("Database setup complete: clinic.db")
    
    conn.close()

def insert_doctors(cursor):
    """Insert 15 doctors across 5 specializations"""
    doctors = [
        ('Dr. Sarah Johnson', 'Dermatology', 'Dermatology', '555-0101'),
        ('Dr. Michael Chen', 'Dermatology', 'Dermatology', '555-0102'),
        ('Dr. Emily Rodriguez', 'Dermatology', 'Dermatology', '555-0103'),
        ('Dr. James Wilson', 'Cardiology', 'Cardiology', '555-0201'),
        ('Dr. Lisa Anderson', 'Cardiology', 'Cardiology', '555-0202'),
        ('Dr. Robert Taylor', 'Cardiology', 'Cardiology', '555-0203'),
        ('Dr. Jennifer Martinez', 'Orthopedics', 'Orthopedics', '555-0301'),
        ('Dr. David Brown', 'Orthopedics', 'Orthopedics', '555-0302'),
        ('Dr. Maria Garcia', 'Orthopedics', 'Orthopedics', '555-0303'),
        ('Dr. William Lee', 'General', 'General Medicine', '555-0401'),
        ('Dr. Patricia White', 'General', 'General Medicine', '555-0402'),
        ('Dr. Thomas Harris', 'General', 'General Medicine', '555-0403'),
        ('Dr. Jessica Clark', 'Pediatrics', 'Pediatrics', '555-0501'),
        ('Dr. Christopher Lewis', 'Pediatrics', 'Pediatrics', '555-0502'),
        ('Dr. Amanda Walker', 'Pediatrics', 'Pediatrics', '555-0503'),
    ]
    
    cursor.executemany('''
    INSERT INTO doctors (name, specialization, department, phone)
    VALUES (?, ?, ?, ?)
    ''', doctors)

def insert_patients(cursor):
    """Insert 200 patients with realistic data"""
    first_names = [
        'James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph',
        'Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Barbara', 'Susan', 'Jessica',
        'Thomas', 'Charles', 'Daniel', 'Matthew', 'Sarah', 'Karen', 'Nancy', 'Lisa',
        'Mark', 'Donald', 'Steven', 'Paul', 'Andrew', 'Joshua', 'Kenneth', 'Kevin',
        'Betty', 'Helen', 'Sandra', 'Donna', 'Carol', 'Ruth', 'Sharon', 'Michelle',
        'Christopher', 'Jason', 'Ryan', 'Jacob', 'Nicholas', 'Emily', 'Amanda', 'Melissa'
    ]
    
    last_names = [
        'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
        'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
        'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Thompson', 'White',
        'Harris', 'Clark', 'Lewis', 'Robinson', 'Walker', 'Hall', 'Allen', 'Young'
    ]
    
    cities = [
        'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
        'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'Austin'
    ]
    
    genders = ['M', 'F']
    
    patients = []
    for i in range(200):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        # 10% chance of NULL email/phone
        email = f"{first_name.lower()}.{last_name.lower()}@email.com" if random.random() > 0.1 else None
        phone = f"555-{random.randint(1000, 9999)}" if random.random() > 0.1 else None
        
        # Age between 1 and 90 years
        age_days = random.randint(365, 365 * 90)
        dob = datetime.now() - timedelta(days=age_days)
        
        # Registration date within last 5 years
        reg_days = random.randint(1, 365 * 5)
        reg_date = datetime.now() - timedelta(days=reg_days)
        
        gender = random.choice(genders)
        city = random.choice(cities)
        
        patients.append((
            first_name, last_name, email, phone,
            dob.strftime('%Y-%m-%d'),
            gender, city,
            reg_date.strftime('%Y-%m-%d')
        ))
    
    cursor.executemany('''
    INSERT INTO patients (first_name, last_name, email, phone, date_of_birth, gender, city, registered_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', patients)

def insert_appointments(cursor):
    """Insert 500 appointments over the past 12 months"""
    statuses = ['Scheduled', 'Completed', 'Cancelled', 'No-Show']
    status_weights = [0.2, 0.6, 0.1, 0.1]  # 60% completed, 20% scheduled, etc.
    
    notes_templates = [
        'Regular checkup',
        'Follow-up appointment',
        'Patient reported pain',
        'Routine examination',
        None,  # 20% will have no notes
        None,
        'Urgent care needed',
        'Annual physical'
    ]
    
    appointments = []
    for i in range(500):
        patient_id = random.randint(1, 200)
        doctor_id = random.randint(1, 15)
        
        # Appointments spread over last 12 months
        days_ago = random.randint(0, 365)
        appointment_date = datetime.now() - timedelta(days=days_ago)
        
        # Add random hour (8 AM to 5 PM)
        hour = random.randint(8, 17)
        minute = random.choice([0, 15, 30, 45])
        appointment_date = appointment_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # Future appointments are always "Scheduled"
        if days_ago < 0:
            status = 'Scheduled'
        else:
            status = random.choices(statuses, weights=status_weights)[0]
        
        notes = random.choice(notes_templates)
        
        appointments.append((
            patient_id, doctor_id,
            appointment_date.strftime('%Y-%m-%d %H:%M:%S'),
            status, notes
        ))
    
    cursor.executemany('''
    INSERT INTO appointments (patient_id, doctor_id, appointment_date, status, notes)
    VALUES (?, ?, ?, ?, ?)
    ''', appointments)

def insert_treatments(cursor):
    """Insert 350 treatments linked to completed appointments"""
    cursor.execute("SELECT id FROM appointments WHERE status = 'Completed'")
    completed_appointments = [row[0] for row in cursor.fetchall()]
    
    treatment_types = [
        ('Skin Examination', 150, 30),
        ('Acne Treatment', 200, 45),
        ('Mole Removal', 500, 60),
        ('Cardiac Stress Test', 800, 90),
        ('ECG', 300, 30),
        ('Echocardiogram', 1200, 60),
        ('X-Ray', 250, 20),
        ('MRI Scan', 2500, 45),
        ('Physical Therapy Session', 150, 60),
        ('Blood Test', 100, 15),
        ('Vaccination', 75, 10),
        ('Consultation', 200, 30),
        ('Minor Surgery', 3000, 120),
        ('Prescription Refill', 50, 10),
        ('Allergy Test', 400, 45)
    ]
    
    treatments = []
    # Randomly select 350 completed appointments for treatments
    selected_appointments = random.sample(completed_appointments, min(350, len(completed_appointments)))
    
    for appointment_id in selected_appointments:
        treatment_name, base_cost, base_duration = random.choice(treatment_types)
        
        # Add some variance to cost and duration
        cost = base_cost * random.uniform(0.8, 1.2)
        duration = int(base_duration * random.uniform(0.9, 1.1))
        
        treatments.append((appointment_id, treatment_name, round(cost, 2), duration))
    
    cursor.executemany('''
    INSERT INTO treatments (appointment_id, treatment_name, cost, duration_minutes)
    VALUES (?, ?, ?, ?)
    ''', treatments)

def insert_invoices(cursor):
    """Insert 300 invoices with varied payment statuses"""
    cursor.execute('''
    SELECT DISTINCT patient_id FROM appointments WHERE status = 'Completed'
    ''')
    patients_with_completed = [row[0] for row in cursor.fetchall()]
    
    statuses = ['Paid', 'Pending', 'Overdue']
    status_weights = [0.6, 0.25, 0.15]  # 60% paid, 25% pending, 15% overdue
    
    invoices = []
    for i in range(300):
        patient_id = random.choice(patients_with_completed)
        
        # Invoice date within last 12 months
        days_ago = random.randint(1, 365)
        invoice_date = datetime.now() - timedelta(days=days_ago)
        
        # Total amount between 100 and 5000
        total_amount = round(random.uniform(100, 5000), 2)
        
        status = random.choices(statuses, weights=status_weights)[0]
        
        # Determine paid amount based on status
        if status == 'Paid':
            paid_amount = total_amount
        elif status == 'Pending':
            paid_amount = round(total_amount * random.uniform(0, 0.5), 2)
        else:  # Overdue
            paid_amount = round(total_amount * random.uniform(0, 0.3), 2)
        
        invoices.append((
            patient_id,
            invoice_date.strftime('%Y-%m-%d'),
            total_amount,
            paid_amount,
            status
        ))
    
    cursor.executemany('''
    INSERT INTO invoices (patient_id, invoice_date, total_amount, paid_amount, status)
    VALUES (?, ?, ?, ?, ?)
    ''', invoices)

if __name__ == '__main__':
    create_database()