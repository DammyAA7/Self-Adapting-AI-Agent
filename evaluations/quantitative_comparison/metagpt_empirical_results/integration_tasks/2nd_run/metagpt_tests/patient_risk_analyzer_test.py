# Add project root to path for imports
import sys
sys.path.insert(0, '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent')

# Generated code by MetaGPT
def patient_risk_score(hospital, patient_id):
    """
    Calculate patient risk score based on age, conditions, severity, and recent abnormal vitals.
    Returns a float between 0.0 and 100.0.
    """
    patient = hospital.get_patient(patient_id)
    if not patient:
        return 0.0

    # Age component
    age_score = (patient.age / 100) * 30

    # Conditions count component
    total_conditions = patient.get_total_conditions()
    conditions_score = total_conditions * 5 * 0.25

    # Average severity component
    avg_severity = patient.get_average_severity()
    severity_score = avg_severity * 10 * 0.25

    # Recent abnormal vitals component
    recent_records = hospital.get_recent_records(patient_id, 90)
    abnormal_vitals = any(r.has_abnormal_vitals() for r in recent_records)
    abnormal_vitals_score = 20 if abnormal_vitals else 0

    # Total risk score
    score = age_score + conditions_score + severity_score + abnormal_vitals_score

    # Clamp to [0.0, 100.0]
    return max(0.0, min(100.0, score))

# Ground-truth test from problem.json

from dataset.patient_risk_analyzer.hospital import Hospital, create_sample_hospital
from dataset.patient_risk_analyzer.patient import Patient
from dataset.patient_risk_analyzer.condition import Condition
from dataset.patient_risk_analyzer.medical_record import MedicalRecord

hospital = create_sample_hospital()

# Test P001 - High risk: age=65, conditions=3, avg_severity=7.0, abnormal_vitals=True
# Expected: (65/100*30) + (3*5*0.25) + (7*10*0.25) + 20 = 19.5 + 3.75 + 17.5 + 20 = 60.75
score_p001 = patient_risk_score(hospital, 'P001')
assert isinstance(score_p001, float)
assert abs(score_p001 - 60.75) < 0.1

# Test P002 - Medium risk: age=45, conditions=1, severity=4, no abnormal
# Expected: (45/100*30) + (1*5*0.25) + (4*10*0.25) + 0 = 13.5 + 1.25 + 10.0 + 0 = 24.75
score_p002 = patient_risk_score(hospital, 'P002')
assert isinstance(score_p002, float)
assert abs(score_p002 - 24.75) < 0.1

# Test P003 - Low risk: age=28, no conditions, no abnormal
# Expected: (28/100*30) + 0 + 0 + 0 = 8.4
score_p003 = patient_risk_score(hospital, 'P003')
assert isinstance(score_p003, float)
assert abs(score_p003 - 8.4) < 0.1

print('Patient Risk Analyzer tests passed')

