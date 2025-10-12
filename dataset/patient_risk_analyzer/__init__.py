"""
Patient Risk Analyzer Package
Healthcare domain codebase for self-evolution testing
"""

# Core classes
from .condition import *
from .patient import *
from .medical_record import *
from .hospital import *

# Helper utilities
from .medication_manager import *
from .vital_signs_analyzer import *
from .appointment_scheduler import *
from .insurance_processor import *
from .lab_results import *
from .diagnosis_helper import *
from .treatment_plan import *

# Explicit exports
__all__ = [
    # Core classes
    'Condition', 'Patient', 'MedicalRecord', 'Hospital', 'create_sample_hospital',
    # Medication management
    'Medication', 'DrugInteractionChecker', 'DosageCalculator',
    # Vital signs
    'VitalSignsTrends', 'HeartRateMonitor',
    # Appointments
    'Appointment', 'AppointmentScheduler',
    # Insurance
    'InsurancePlan', 'InsuranceVerifier', 'ClaimProcessor',
    # Lab results
    'LabTest', 'LabResultsManager',
    # Diagnosis
    'SymptomChecker', 'DiagnosticCriteria',
    # Treatment
    'TreatmentPlan', 'CareProtocol',
]
