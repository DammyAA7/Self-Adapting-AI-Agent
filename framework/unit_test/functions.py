from enum import Enum

class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


from dataset.patient_risk_analyzer.hospital import Hospital
from dataset.patient_risk_analyzer.patient import Patient
from dataset.patient_risk_analyzer.medical_record import MedicalRecord

def patient_risk_score(hospital, patient_id):
    """
    Calculates the risk score for a patient in the hospital system based on age, number of conditions,
    average severity, and recent abnormal vital signs.

    Args:
        hospital (Hospital): The hospital system instance.
        patient_id (str): The patient's unique ID.

    Returns:
        float: The patient's risk score (0.0 to 100.0), or 0.0/None if patient not found.
    """
    patient = hospital.get_patient(patient_id)
    if not patient:
        return 0.0

    age_score = (patient.age / 100.0) * 30

    total_conditions = patient.get_total_conditions()
    conditions_score = total_conditions * 5 * 0.25  # (n*5)*25/100 = n*5*0.25

    avg_severity = patient.get_average_severity()
    severity_score = avg_severity * 10 * 0.25

    recent_records = hospital.get_recent_records(patient_id, 90)
    abnormal_vitals_score = 0.0
    if any(r.has_abnormal_vitals() for r in recent_records):
        abnormal_vitals_score = 20.0

    total_score = age_score + conditions_score + severity_score + abnormal_vitals_score
    # Clamp between 0.0 and 100.0
    if total_score < 0.0:
        total_score = 0.0
    elif total_score > 100.0:
        total_score = 100.0

    return float(total_score)

