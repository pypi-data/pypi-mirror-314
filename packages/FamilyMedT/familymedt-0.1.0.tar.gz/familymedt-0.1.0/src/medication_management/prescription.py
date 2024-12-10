# prescription.py
from datetime import datetime
from medication_management.medication import Medication

class PrescriptionMedication(Medication):
    def __init__(self, name, dosage, frequency, daily_dosage, stock, doctor_name, prescription_date, indication, warnings, expiration_date):
        super().__init__(name, dosage, frequency, daily_dosage, stock)
        self.doctor_name = doctor_name
        self.prescription_date = prescription_date
        self.indication = indication
        self.warnings = warnings
        self.expiration_date = expiration_date
        self._validate_dates()

    def _validate_dates(self):
        """验证日期格式"""
        try:
            datetime.strptime(self.prescription_date, "%Y-%m-%d")
            datetime.strptime(self.expiration_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Dates must be in YYYY-MM-DD format")

    def display_prescription_info(self):
        base_info = self.display_info()
        return f"{base_info}, Prescribed by: {self.doctor_name}, Prescription Date: {self.prescription_date}, "\
               f"Indication: {self.indication}, Warnings: {self.warnings}, Expiration Date: {self.expiration_date}"

    def is_expired(self):
        """检查药品是否过期"""
        try:
            current_date = datetime.now().date()
            expiry_date = datetime.strptime(self.expiration_date, "%Y-%m-%d").date()
            return current_date > expiry_date
        except ValueError:
            print("Error: Invalid date format")
            return True

    def to_dict(self):
        """将对象转为字典"""
        base_dict = super().to_dict()
        base_dict.update({
            "doctor_name": self.doctor_name,
            "prescription_date": self.prescription_date,
            "indication": self.indication,
            "warnings": self.warnings,
            "expiration_date": self.expiration_date
        })
        return base_dict
