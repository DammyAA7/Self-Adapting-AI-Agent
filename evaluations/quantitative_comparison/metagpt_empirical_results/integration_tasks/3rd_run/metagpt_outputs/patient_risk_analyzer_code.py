def patient_risk_score(hospital, patient_id):
    """
    Calculate patient risk score based on age, conditions, severity, and recent abnormal vitals.
    Returns: float between 0.0 and 100.0
    """
    patient = hospital.get_patient(patient_id)
    if not patient:
        return 0.0

    # Age component
    age_score = (patient.age / 100) * 30

    # Condition count component
    total_conditions = patient.get_total_conditions()
    condition_score = total_conditions * 5 * 0.25

    # Average severity component
    avg_severity = patient.get_average_severity()
    severity_score = avg_severity * 10 * 0.25

    # Recent abnormal vitals component
    recent_records = hospital.get_recent_records(patient_id, 90)
    abnormal_vitals = any(r.has_abnormal_vitals() for r in recent_records)
    abnormal_vitals_score = 20 if abnormal_vitals else 0

    score = age_score + condition_score + severity_score + abnormal_vitals_score
    # Clamp score to [0.0, 100.0]
    return max(0.0, min(100.0, score))