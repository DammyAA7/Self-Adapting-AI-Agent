"""
Medical Record Class
Individual medical visit records with vital signs
"""

from datetime import datetime
from typing import Dict, List


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
