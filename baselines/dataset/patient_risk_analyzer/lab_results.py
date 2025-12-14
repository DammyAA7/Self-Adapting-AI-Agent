"""
Lab Results Manager
Handles laboratory test results and reference ranges
"""
from typing import Dict, List, Optional
from datetime import datetime


class LabTest:
    """Represents a lab test result"""
    def __init__(self, test_name: str, value: float, unit: str,
                 reference_min: float, reference_max: float, date: str):
        self.test_name = test_name
        self.value = value
        self.unit = unit
        self.reference_min = reference_min
        self.reference_max = reference_max
        self.date = datetime.strptime(date, "%Y-%m-%d")

    def is_normal(self) -> bool:
        """Check if result is within normal range"""
        return self.reference_min <= self.value <= self.reference_max

    def get_status(self) -> str:
        """Get status: normal, high, low, critical"""
        if self.value < self.reference_min:
            if self.value < self.reference_min * 0.7:
                return 'critical_low'
            return 'low'
        elif self.value > self.reference_max:
            if self.value > self.reference_max * 1.3:
                return 'critical_high'
            return 'high'
        return 'normal'


class LabResultsManager:
    """Manages lab test results for patients"""

    # Common lab test reference ranges
    REFERENCE_RANGES = {
        'glucose': (70, 100, 'mg/dL'),
        'cholesterol': (0, 200, 'mg/dL'),
        'hemoglobin': (13.5, 17.5, 'g/dL'),
        'white_blood_cells': (4.5, 11.0, 'K/uL'),
        'creatinine': (0.7, 1.3, 'mg/dL'),
    }

    def __init__(self):
        self.results: Dict[str, List[LabTest]] = {}

    def add_result(self, patient_id: str, test: LabTest):
        """Add lab result for a patient"""
        if patient_id not in self.results:
            self.results[patient_id] = []
        self.results[patient_id].append(test)

    def get_patient_results(self, patient_id: str) -> List[LabTest]:
        """Get all lab results for a patient"""
        return self.results.get(patient_id, [])

    def get_abnormal_results(self, patient_id: str) -> List[LabTest]:
        """Get only abnormal results"""
        results = self.get_patient_results(patient_id)
        return [r for r in results if not r.is_normal()]

    def get_critical_results(self, patient_id: str) -> List[LabTest]:
        """Get critical results requiring immediate attention"""
        results = self.get_patient_results(patient_id)
        return [r for r in results if 'critical' in r.get_status()]
