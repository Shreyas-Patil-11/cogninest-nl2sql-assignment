# NL2SQL Test Results

**Started at:** 2026-04-14 11:08:06.101606

## 1. How many patients do we have?
- ✅ Rows Returned: 1

**SQL Query:**
```sql
SELECT COUNT(id) FROM patients;
```

## 2. List all doctors and their specializations
- ✅ Rows Returned: 15

**SQL Query:**
```sql
SELECT name, specialization 
FROM doctors;
```

## 3. Show me appointments for last month
- ✅ Rows Returned: 41

**SQL Query:**
```sql
SELECT * 
FROM appointments 
WHERE STRFTIME('%Y-%m', appointment_date) = STRFTIME('%Y-%m', DATE('now', '-1 month'));
```

## 4. Which doctor has the most appointments?
- ✅ Rows Returned: 1

**SQL Query:**
```sql
SELECT d.name, COUNT(a.id) as num_appointments
FROM doctors d
JOIN appointments a ON d.id = a.doctor_id
GROUP BY d.name
ORDER BY num_appointments DESC
LIMIT 1;
```

## 5. What is the total revenue?
- ✅ Rows Returned: 1

**SQL Query:**
```sql
SELECT SUM(total_amount) AS total_revenue 
FROM invoices;
```

## 6. Show revenue by doctor
- ✅ Rows Returned: 15

**SQL Query:**
```sql
SELECT 
  d.name, 
  SUM(t.cost) AS revenue
FROM 
  treatments t
  JOIN appointments a ON t.appointment_id = a.id
  JOIN doctors d ON a.doctor_id = d.id
GROUP BY 
  d.name
ORDER BY 
  revenue DESC;
```

## 7. How many cancelled appointments last quarter?
- ✅ Rows Returned: 1

**SQL Query:**
```sql
SELECT COUNT(*) 
FROM appointments 
WHERE status = 'cancelled' 
AND appointment_date >= DATE('now', '-3 months') 
AND appointment_date < DATE('now');
```

## 8. Top 5 patients by spending
- ✅ Rows Returned: 5

**SQL Query:**
```sql
SELECT p.first_name, p.last_name, SUM(i.total_amount) AS total_spending
FROM patients p
JOIN invoices i ON p.id = i.patient_id
GROUP BY p.id, p.first_name, p.last_name
ORDER BY total_spending DESC
LIMIT 5;
```

## 9. Average treatment cost by specialization
- ✅ Rows Returned: 5

**SQL Query:**
```sql
SELECT 
  d.specialization, 
  AVG(t.cost) AS average_treatment_cost
FROM 
  treatments t
  JOIN appointments a ON t.appointment_id = a.id
  JOIN doctors d ON a.doctor_id = d.id
GROUP BY 
  d.specialization
```

## 10. Show monthly appointment count for the past 6 months
- ✅ Rows Returned: 7

**SQL Query:**
```sql
SELECT 
  STRFTIME('%Y-%m', appointment_date) AS month,
  COUNT(*) AS appointment_count
FROM 
  appointments
WHERE 
  appointment_date >= DATE('now', '-6 months')
GROUP BY 
  STRFTIME('%Y-%m', appointment_date)
ORDER BY 
  month;
```

## 11. Which city has the most patients?
- ✅ Rows Returned: 1

**SQL Query:**
```sql
SELECT city, COUNT(*) as patient_count
FROM patients
GROUP BY city
ORDER BY patient_count DESC
LIMIT 1;
```

## 12. List patients who visited more than 3 times
- ✅ Rows Returned: 53

**SQL Query:**
```sql
SELECT p.id, p.first_name, p.last_name, COUNT(a.id) AS visit_count
FROM patients p
JOIN appointments a ON p.id = a.patient_id
GROUP BY p.id, p.first_name, p.last_name
HAVING COUNT(a.id) > 3;
```

## 13. Show unpaid invoices
- ✅ Rows Returned: 99

**SQL Query:**
```sql
SELECT * 
FROM invoices 
WHERE paid_amount < total_amount AND status != 'paid';
```

## 14. What percentage of appointments are no-shows?
- ✅ Rows Returned: 1

**SQL Query:**
```sql
SELECT 
    (COUNT(CASE WHEN status = 'no-show' THEN 1 END) * 1.0 / COUNT(*)) * 100 
AS no_show_percentage
FROM appointments;
```

## 15. Show the busiest day of the week for appointments
- ✅ Rows Returned: 1

**SQL Query:**
```sql
SELECT 
  CASE 
    WHEN STRFTIME('%w', appointment_date) = '0' THEN 'Sunday'
    WHEN STRFTIME('%w', appointment_date) = '1' THEN 'Monday'
    WHEN STRFTIME('%w', appointment_date) = '2' THEN 'Tuesday'
    WHEN STRFTIME('%w', appointment_date) = '3' THEN 'Wednesday'
    WHEN STRFTIME('%w', appointment_date) = '4' THEN 'Thursday'
    WHEN STRFTIME('%w', appointment_date) = '5' THEN 'Friday'
    WHEN STRFTIME('%w', appointment_date) = '6' THEN 'Saturday'
  END AS day_of_week,
  COUNT(*) as num_appointments
FROM 
  appointments
GROUP BY 
  STRFTIME('%w', appointment_date)
ORDER BY 
  num_appointments DESC
LIMIT 1;
```

## 16. Revenue trend by month
- ✅ Rows Returned: 13

**SQL Query:**
```sql
SELECT 
  STRFTIME('%Y-%m', i.invoice_date) AS month,
  SUM(i.total_amount) AS revenue
FROM 
  invoices i
GROUP BY 
  STRFTIME('%Y-%m', i.invoice_date)
ORDER BY 
  month;
```

## 17. Average appointment duration by doctor
- ✅ Rows Returned: 15

**SQL Query:**
```sql
SELECT 
  d.name, 
  AVG(t.duration_minutes) AS average_duration
FROM 
  doctors d
  JOIN appointments a ON d.id = a.doctor_id
  JOIN treatments t ON a.id = t.appointment_id
GROUP BY 
  d.name
```

## 18. List patients with overdue invoices
- ✅ Rows Returned: 99

**SQL Query:**
```sql
SELECT p.id, p.first_name, p.last_name, i.invoice_date, i.total_amount, i.paid_amount
FROM patients p
JOIN invoices i ON p.id = i.patient_id
WHERE i.status = 'overdue' OR (i.total_amount - i.paid_amount) > 0;
```

## 19. Compare revenue between departments
- ✅ Rows Returned: 5

**SQL Query:**
```sql
SELECT 
  d.department, 
  SUM(t.cost) AS total_revenue
FROM 
  treatments t
  JOIN appointments a ON t.appointment_id = a.id
  JOIN doctors d ON a.doctor_id = d.id
GROUP BY 
  d.department
ORDER BY 
  total_revenue DESC;
```

## 20. Show patient registration trend by month
- ✅ Rows Returned: 56

**SQL Query:**
```sql
SELECT 
  STRFTIME('%Y-%m', registered_date) AS registration_month,
  COUNT(id) AS number_of_patients
FROM 
  patients
GROUP BY 
  STRFTIME('%Y-%m', registered_date)
ORDER BY 
  registration_month;
```

---
**Total:** 20
**Passed:** 20
**Failed:** 0
**Success Rate:** 100.0%
