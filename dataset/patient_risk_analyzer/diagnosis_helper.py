"""
Diagnosis Helper
Assists with diagnostic decision support
"""
from typing import List, Dict, Set


class SymptomChecker:
    """Checks symptoms against known conditions"""

    SYMPTOM_DATABASE = {
        'Diabetes': {'thirst', 'frequent_urination', 'fatigue', 'blurred_vision'},
        'Hypertension': {'headache', 'dizziness', 'chest_pain', 'shortness_of_breath'},
        'Asthma': {'wheezing', 'coughing', 'shortness_of_breath', 'chest_tightness'},
        'Influenza': {'fever', 'cough', 'sore_throat', 'body_aches', 'fatigue'},
        'Migraine': {'headache', 'nausea', 'sensitivity_to_light', 'visual_disturbances'},
    }

    @staticmethod
    def match_symptoms(symptoms: Set[str]) -> List[tuple]:
        """Match symptoms to possible conditions with confidence scores"""
        matches = []
        for condition, condition_symptoms in SymptomChecker.SYMPTOM_DATABASE.items():
            overlap = symptoms.intersection(condition_symptoms)
            if overlap:
                confidence = len(overlap) / len(condition_symptoms)
                matches.append((condition, confidence, list(overlap)))

        return sorted(matches, key=lambda x: x[1], reverse=True)


class DiagnosticCriteria:
    """Diagnostic criteria for various conditions"""

    @staticmethod
    def check_diabetes_criteria(glucose_fasting: float, hba1c: float) -> str:
        """Check if patient meets diabetes diagnostic criteria"""
        if glucose_fasting >= 126 or hba1c >= 6.5:
            return 'diabetes'
        elif glucose_fasting >= 100 or hba1c >= 5.7:
            return 'prediabetes'
        return 'normal'

    @staticmethod
    def check_hypertension_stage(systolic: int, diastolic: int) -> str:
        """Determine hypertension stage"""
        if systolic >= 180 or diastolic >= 120:
            return 'hypertensive_crisis'
        elif systolic >= 140 or diastolic >= 90:
            return 'stage_2'
        elif systolic >= 130 or diastolic >= 80:
            return 'stage_1'
        elif systolic >= 120:
            return 'elevated'
        return 'normal'

    @staticmethod
    def assess_risk_factors(age: int, bmi: float, smoker: bool,
                           family_history: bool) -> int:
        """Calculate cardiovascular risk score"""
        score = 0
        if age > 65:
            score += 3
        elif age > 50:
            score += 2
        elif age > 40:
            score += 1

        if bmi > 30:
            score += 2
        elif bmi > 25:
            score += 1

        if smoker:
            score += 2
        if family_history:
            score += 1

        return score
