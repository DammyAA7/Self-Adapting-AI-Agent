"""
Hospital Class
Main hospital system managing patients and records
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from .patient import Patient
from .medical_record import MedicalRecord
from .condition import Condition


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
        cutoff = datetime.now() - timedelta(days=days)
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
