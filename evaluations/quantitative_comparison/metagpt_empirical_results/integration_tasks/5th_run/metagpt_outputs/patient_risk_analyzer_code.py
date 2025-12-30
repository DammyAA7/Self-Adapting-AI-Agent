def patient_risk_score(hospital, patient_id):
    """
    Calculate patient risk score based on age, conditions, severity, and recent abnormal vitals.
    Returns float between 0.0 and 100.0
    """
    patient = hospital.get_patient(patient_id)
    if patient is None:
        return 0.0
    
    age_score = (patient.age / 100) * 30
    condition_score = patient.get_total_conditions() * 5 * 0.25
    severity_score = patient.get_average_severity() * 10 * 0.25
    
    recent_records = hospital.get_recent_records(patient_id, 90)
    abnormal_vitals = any(r.has_abnormal_vitals() for r in recent_records)
    abnormal_score = 20 if abnormal_vitals else 0
    
    total_score = age_score + condition_score + severity_score + abnormal_score
    return min(max(total_score, 0.0), 100.0)