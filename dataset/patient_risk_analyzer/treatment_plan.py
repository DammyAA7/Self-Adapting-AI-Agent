"""
Treatment Plan Manager
Manages patient treatment plans and care protocols
"""
from typing import List, Dict, Optional
from datetime import datetime


class TreatmentPlan:
    """Represents a treatment plan"""
    def __init__(self, patient_id: str, diagnosis: str, plan_type: str):
        self.patient_id = patient_id
        self.diagnosis = diagnosis
        self.plan_type = plan_type
        self.medications: List[str] = []
        self.procedures: List[str] = []
        self.goals: List[str] = []
        self.created_date = datetime.now()

    def add_medication(self, medication: str):
        """Add medication to treatment plan"""
        if medication not in self.medications:
            self.medications.append(medication)

    def add_procedure(self, procedure: str):
        """Add procedure to treatment plan"""
        if procedure not in self.procedures:
            self.procedures.append(procedure)

    def add_goal(self, goal: str):
        """Add treatment goal"""
        if goal not in self.goals:
            self.goals.append(goal)


class CareProtocol:
    """Standard care protocols for common conditions"""

    PROTOCOLS = {
        'Diabetes': {
            'monitoring': ['Blood glucose daily', 'HbA1c quarterly'],
            'medications': ['Metformin', 'Insulin'],
            'lifestyle': ['Diet modification', 'Regular exercise'],
            'followup_weeks': 12
        },
        'Hypertension': {
            'monitoring': ['BP twice daily', 'Heart rate'],
            'medications': ['ACE inhibitor', 'Diuretic'],
            'lifestyle': ['Low sodium diet', 'Stress management'],
            'followup_weeks': 8
        },
        'Asthma': {
            'monitoring': ['Peak flow daily', 'Symptom diary'],
            'medications': ['Inhaled corticosteroid', 'Rescue inhaler'],
            'lifestyle': ['Avoid triggers', 'Environmental control'],
            'followup_weeks': 6
        }
    }

    @staticmethod
    def get_protocol(condition: str) -> Optional[Dict]:
        """Get standard care protocol for a condition"""
        return CareProtocol.PROTOCOLS.get(condition)

    @staticmethod
    def create_treatment_plan(patient_id: str, condition: str) -> Optional[TreatmentPlan]:
        """Create treatment plan from protocol"""
        protocol = CareProtocol.get_protocol(condition)
        if not protocol:
            return None

        plan = TreatmentPlan(patient_id, condition, 'standard')
        for med in protocol['medications']:
            plan.add_medication(med)
        for goal in protocol['lifestyle']:
            plan.add_goal(goal)
        return plan
