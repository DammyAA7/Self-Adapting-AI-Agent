"""
Appointment Scheduler
Manages patient appointments and scheduling
"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class Appointment:
    """Represents a medical appointment"""
    def __init__(self, patient_id: str, doctor: str, date_time: str,
                 duration_minutes: int, appointment_type: str):
        self.patient_id = patient_id
        self.doctor = doctor
        self.date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M")
        self.duration_minutes = duration_minutes
        self.appointment_type = appointment_type
        self.status = 'scheduled'

    def get_end_time(self) -> datetime:
        """Get appointment end time"""
        return self.date_time + timedelta(minutes=self.duration_minutes)


class AppointmentScheduler:
    """Schedules and manages appointments"""

    def __init__(self):
        self.appointments: List[Appointment] = []

    def add_appointment(self, appointment: Appointment) -> bool:
        """Add new appointment if no conflicts"""
        if self.has_conflict(appointment):
            return False
        self.appointments.append(appointment)
        return True

    def has_conflict(self, new_appt: Appointment) -> bool:
        """Check if appointment conflicts with existing ones"""
        for appt in self.appointments:
            if appt.doctor != new_appt.doctor:
                continue
            if appt.status == 'cancelled':
                continue

            # Check time overlap
            if (new_appt.date_time < appt.get_end_time() and
                new_appt.get_end_time() > appt.date_time):
                return True
        return False

    def get_patient_appointments(self, patient_id: str) -> List[Appointment]:
        """Get all appointments for a patient"""
        return [a for a in self.appointments if a.patient_id == patient_id]

    def get_doctor_schedule(self, doctor: str, date: str) -> List[Appointment]:
        """Get doctor's schedule for a specific date"""
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
        return [a for a in self.appointments
                if a.doctor == doctor and a.date_time.date() == target_date]
