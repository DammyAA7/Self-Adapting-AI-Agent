from enum import Enum

class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


def patient_risk_score(hospital, patient_id):
    """Calculate patient risk score based on age, conditions, severity, and abnormal vitals."""
    patient = hospital.get_patient(patient_id)
    if patient is None:
        raise ValueError(f"Patient with ID {patient_id} not found")
    recent_records = hospital.get_recent_records(patient_id, 90)
    abnormal_flag = any(rec.has_abnormal_vitals() for rec in recent_records)
    age_score = patient.age / 100 * 30
    conditions_score = patient.get_total_conditions() * 5 * 0.25
    severity_score = patient.get_average_severity() * 10 * 0.25
    score = age_score + conditions_score + severity_score + (20 if abnormal_flag else 0)
    if score > 100:
        return 100.0
    if score < 0:
        return 0.0
    return float(score)
