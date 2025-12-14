"""
Medication Manager
Handles drug prescriptions, interactions, and dosage calculations
"""
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class Medication:
    """Represents a medication"""
    def __init__(self, name: str, dosage: str, frequency: str, category: str):
        self.name = name
        self.dosage = dosage
        self.frequency = frequency
        self.category = category


class DrugInteractionChecker:
    """Checks for potential drug interactions"""

    # Known drug interactions (simplified for demo)
    INTERACTIONS = {
        ('Warfarin', 'Aspirin'): 'severe',
        ('Metformin', 'Alcohol'): 'moderate',
        ('Lisinopril', 'Potassium'): 'moderate',
        ('Simvastatin', 'Grapefruit'): 'severe',
    }

    @staticmethod
    def check_interaction(drug1: str, drug2: str) -> Optional[str]:
        """Check for interaction between two drugs"""
        key1 = (drug1, drug2)
        key2 = (drug2, drug1)
        return DrugInteractionChecker.INTERACTIONS.get(key1) or DrugInteractionChecker.INTERACTIONS.get(key2)

    @staticmethod
    def check_multiple(medications: List[str]) -> List[Tuple[str, str, str]]:
        """Check interactions across multiple medications"""
        interactions = []
        for i in range(len(medications)):
            for j in range(i + 1, len(medications)):
                severity = DrugInteractionChecker.check_interaction(medications[i], medications[j])
                if severity:
                    interactions.append((medications[i], medications[j], severity))
        return interactions


class DosageCalculator:
    """Calculates medication dosages based on patient parameters"""

    @staticmethod
    def calculate_by_weight(base_dose_mg: float, patient_weight_kg: float,
                          max_dose_mg: float = None) -> float:
        """Calculate dose based on patient weight"""
        calculated_dose = base_dose_mg * patient_weight_kg
        if max_dose_mg and calculated_dose > max_dose_mg:
            return max_dose_mg
        return calculated_dose

    @staticmethod
    def calculate_by_age(adult_dose_mg: float, patient_age: int) -> float:
        """Calculate pediatric dose using Young's formula"""
        if patient_age >= 18:
            return adult_dose_mg
        return (patient_age / (patient_age + 12)) * adult_dose_mg

    @staticmethod
    def adjust_for_renal_function(dose_mg: float, gfr: float) -> float:
        """Adjust dose based on kidney function (GFR)"""
        if gfr >= 60:
            return dose_mg  # Normal kidney function
        elif gfr >= 30:
            return dose_mg * 0.75  # Mild impairment
        elif gfr >= 15:
            return dose_mg * 0.50  # Moderate impairment
        else:
            return dose_mg * 0.25  # Severe impairment
