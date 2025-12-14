
def patient_risk_score(hospital, patient_id):
    '''
    Create a function called patient_risk_score that takes a Hospital object and patient_id. Calculate risk score using formula: (patient.age / 100 * 30) + (patient.get_total_conditions() * 5 * 25/100) + (patient.get_average_severity() * 10 * 25/100) + (20 if recent records have abnormal vitals else 0). Use hospital.get_patient(patient_id) and hospital.get_recent_records(patient_id, 90). Returns: float between 0.0 and 100.0.
    '''
    # 1. Get patient object
    patient = hospital.get_patient(patient_id)
    if patient is None:
        return 0.0

    # 2. Basic scores
    age_score = (patient.age / 100.0) * 30

    total_conditions = patient.get_total_conditions()
    cond_score = total_conditions * 5 * 0.25  # 25/100

    avg_severity = patient.get_average_severity()
    sev_score = avg_severity * 10 * 0.25      # 25/100

    # 3. Recent records and abnormal vitals
    recent_records = hospital.get_recent_records(patient_id, 90)
    abnormal_vitals = any(
        r.has_abnormal_vitals() for r in recent_records
    )
    abnormal_score = 20 if abnormal_vitals else 0

    # 4. Sum for final score (max is 100 by formula)
    score = age_score + cond_score + sev_score + abnormal_score

    # 5. Clamp if needed to 100.0 (optional, per doc no need, but safe in case input weirdness)
    if score > 100.0:
        score = 100.0
    if score < 0.0:
        score = 0.0

    return float(score)



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
