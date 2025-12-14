"""
Insurance Processor
Handles insurance verification and claims processing
"""
from typing import Dict, List, Optional


class InsurancePlan:
    """Represents an insurance plan"""
    def __init__(self, plan_id: str, provider: str, plan_type: str,
                 deductible: float, copay: float, coverage_percent: float):
        self.plan_id = plan_id
        self.provider = provider
        self.plan_type = plan_type  # HMO, PPO, etc.
        self.deductible = deductible
        self.copay = copay
        self.coverage_percent = coverage_percent


class InsuranceVerifier:
    """Verifies insurance coverage and eligibility"""

    @staticmethod
    def verify_coverage(plan: InsurancePlan, procedure_code: str) -> bool:
        """Verify if procedure is covered"""
        # Simplified verification
        covered_procedures = ['EXAM', 'LAB', 'XRAY', 'CONSULT']
        return any(code in procedure_code for code in covered_procedures)

    @staticmethod
    def calculate_patient_cost(plan: InsurancePlan, total_cost: float,
                              deductible_met: bool = False) -> Dict[str, float]:
        """Calculate patient's out-of-pocket cost"""
        if not deductible_met:
            if total_cost <= plan.deductible:
                return {
                    'patient_pays': total_cost,
                    'insurance_pays': 0.0,
                    'deductible_applied': total_cost
                }
            remaining = total_cost - plan.deductible
            insurance_portion = remaining * (plan.coverage_percent / 100)
            return {
                'patient_pays': plan.deductible + (remaining - insurance_portion) + plan.copay,
                'insurance_pays': insurance_portion,
                'deductible_applied': plan.deductible
            }
        else:
            insurance_portion = total_cost * (plan.coverage_percent / 100)
            return {
                'patient_pays': (total_cost - insurance_portion) + plan.copay,
                'insurance_pays': insurance_portion,
                'deductible_applied': 0.0
            }


class ClaimProcessor:
    """Processes insurance claims"""

    def __init__(self):
        self.claims: List[Dict] = []

    def submit_claim(self, patient_id: str, procedure_code: str,
                    amount: float, plan: InsurancePlan) -> str:
        """Submit an insurance claim"""
        claim_id = f"CLM-{len(self.claims) + 1:06d}"
        self.claims.append({
            'claim_id': claim_id,
            'patient_id': patient_id,
            'procedure_code': procedure_code,
            'amount': amount,
            'plan_id': plan.plan_id,
            'status': 'pending'
        })
        return claim_id
