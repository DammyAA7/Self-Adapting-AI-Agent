"""
Medical Patient Records System
Healthcare domain codebase for self-evolution testing
"""

from datetime import datetime
from typing import List, Dict, Optional


class Condition:
    """Represents a medical condition"""
    def __init__(self, name: str, severity: int, diagnosed_date: str):
        self.name = name
        self.severity = severity  # 1-10 scale
        self.diagnosed_date = datetime.strptime(diagnosed_date, "%Y-%m-%d")

    def __repr__(self):
        return f"Condition({self.name}, severity={self.severity})"


class Patient:
    """Patient information and medical history"""
    def __init__(self, id: str, name: str, age: int, blood_type: str):
        self.id = id
        self.name = name
        self.age = age
        self.blood_type = blood_type
        self.conditions: List[Condition] = []

    def add_condition(self, condition: Condition):
        """Add a medical condition to patient record"""
        self.conditions.append(condition)

    def get_total_conditions(self) -> int:
        """Get count of all conditions"""
        return len(self.conditions)

    def get_average_severity(self) -> float:
        """Calculate average severity of all conditions"""
        if not self.conditions:
            return 0.0
        return sum(c.severity for c in self.conditions) / len(self.conditions)

    def __repr__(self):
        return f"Patient({self.id}, {self.name}, age={self.age})"


class MedicalRecord:
    """Individual medical visit record"""
    def __init__(self, patient_id: str, visit_date: str, vitals: Dict[str, float],
                 medications: List[str]):
        self.patient_id = patient_id
        self.visit_date = datetime.strptime(visit_date, "%Y-%m-%d")
        self.vitals = vitals  # {'bp_systolic': 120, 'bp_diastolic': 80, 'heart_rate': 72, 'temp': 98.6}
        self.medications = medications

    def has_abnormal_vitals(self) -> bool:
        """Check if any vital signs are outside normal ranges"""
        if self.vitals.get('bp_systolic', 0) > 140 or self.vitals.get('bp_systolic', 0) < 90:
            return True
        if self.vitals.get('heart_rate', 0) > 100 or self.vitals.get('heart_rate', 0) < 60:
            return True
        if self.vitals.get('temp', 0) > 100.4 or self.vitals.get('temp', 0) < 97:
            return True
        return False

    def __repr__(self):
        return f"MedicalRecord({self.patient_id}, {self.visit_date.date()})"


class Hospital:
    """Main hospital system managing patients and records"""
    def __init__(self):
        self.patients: Dict[str, Patient] = {}
        self.records: List[MedicalRecord] = []

    def add_patient(self, patient: Patient):
        """Register a new patient"""
        self.patients[patient.id] = patient

    def add_record(self, record: MedicalRecord):
        """Add a medical visit record"""
        self.records.append(record)

    def get_patient(self, patient_id: str) -> Optional[Patient]:
        """Retrieve patient by ID"""
        return self.patients.get(patient_id)

    def get_records_by_patient(self, patient_id: str) -> List[MedicalRecord]:
        """Get all medical records for a patient"""
        return [r for r in self.records if r.patient_id == patient_id]

    def get_recent_records(self, patient_id: str, days: int = 90) -> List[MedicalRecord]:
        """Get recent medical records within specified days"""
        cutoff = datetime.now()
        from datetime import timedelta
        cutoff = cutoff - timedelta(days=days)
        return [r for r in self.records
                if r.patient_id == patient_id and r.visit_date >= cutoff]

    def get_all_patients(self) -> List[Patient]:
        """Get all registered patients"""
        return list(self.patients.values())

    def __repr__(self):
        return f"Hospital({len(self.patients)} patients, {len(self.records)} records)"


# Sample data for testing
def create_sample_hospital():
    """Create sample hospital with test data"""
    hospital = Hospital()

    # Patient 1: High risk
    p1 = Patient("P001", "John Doe", 65, "O+")
    p1.add_condition(Condition("Diabetes", 7, "2020-05-15"))
    p1.add_condition(Condition("Hypertension", 8, "2019-03-10"))
    p1.add_condition(Condition("High Cholesterol", 6, "2021-01-20"))
    hospital.add_patient(p1)

    r1 = MedicalRecord("P001", "2025-09-01",
                       {'bp_systolic': 145, 'bp_diastolic': 95, 'heart_rate': 88, 'temp': 98.6},
                       ["Metformin", "Lisinopril", "Atorvastatin"])
    hospital.add_record(r1)

    # Patient 2: Medium risk
    p2 = Patient("P002", "Jane Smith", 45, "A+")
    p2.add_condition(Condition("Asthma", 4, "2018-07-12"))
    hospital.add_patient(p2)

    r2 = MedicalRecord("P002", "2025-09-15",
                       {'bp_systolic': 118, 'bp_diastolic': 78, 'heart_rate': 72, 'temp': 98.2},
                       ["Albuterol"])
    hospital.add_record(r2)

    # Patient 3: Low risk
    p3 = Patient("P003", "Bob Johnson", 28, "B+")
    hospital.add_patient(p3)

    r3 = MedicalRecord("P003", "2025-10-01",
                       {'bp_systolic': 115, 'bp_diastolic': 75, 'heart_rate': 68, 'temp': 98.4},
                       [])
    hospital.add_record(r3)

    return hospital


if __name__ == "__main__":
    hospital = create_sample_hospital()
    print(hospital)
    print(f"\nPatients: {[p.name for p in hospital.get_all_patients()]}")
    print(f"P001 conditions: {hospital.get_patient('P001').conditions}")
    print(f"P001 avg severity: {hospital.get_patient('P001').get_average_severity()}")
    print(f"P001 recent records: {hospital.get_recent_records('P001', 90)}")
