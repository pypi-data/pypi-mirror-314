# inventory.py
import os
import pandas as pd
from pathlib import Path
from medication_management.medication import Medication
from medication_management.prescription import PrescriptionMedication

class InventoryManagement:
    def __init__(self, member_name, base_dir, reminder_system=None):
        self.member_name = member_name
        self.base_dir = Path(base_dir)
        self.reminder_system = reminder_system
        
        # 确保数据目录存在
        self.data_dir = self.base_dir / "data"
        self.data_dir.mkdir(exist_ok=True)
        
        self.inventory_file = self.data_dir / f"{member_name}_inventory.csv"
        self.history_file = self.data_dir / f"{member_name}_history.csv"

        self.medications = {}
        self.next_med_id = 1
        self._load_inventory()

    def _load_inventory(self):
        """从CSV加载库存数据"""
        if not self.inventory_file.exists():
            self._create_empty_inventory()
            return

        try:
            df = pd.read_csv(self.inventory_file)
            if df.empty:
                self._create_empty_inventory()
                return

            for _, row in df.iterrows():
                try:
                    if row['is_prescription']:
                        med = PrescriptionMedication(
                            name=row['name'],
                            dosage=row['dosage'],
                            frequency=row['frequency'],
                            daily_dosage=row['daily_dosage'],
                            stock=row['stock'],
                            doctor_name=row['doctor_name'],
                            prescription_date=row['prescription_date'],
                            indication=row['indication'],
                            warnings=row['warnings'],
                            expiration_date=row['expiration_date']
                        )
                    else:
                        med = Medication(
                            name=row['name'],
                            dosage=row['dosage'],
                            frequency=row['frequency'],
                            daily_dosage=row['daily_dosage'],
                            stock=row['stock']
                        )
                    self.medications[int(row['med_id'])] = med
                except Exception as e:
                    print(f"Error loading medication: {str(e)}")
                    continue

            if not df.empty:
                self.next_med_id = df['med_id'].max() + 1

        except Exception as e:
            print(f"Error loading inventory: {str(e)}")
            self._create_empty_inventory()

    def _create_empty_inventory(self):
        """创建空的库存文件"""
        columns = [
            'med_id', 'name', 'dosage', 'frequency', 'daily_dosage',
            'stock', 'is_prescription', 'doctor_name', 'prescription_date',
            'indication', 'warnings', 'expiration_date'
        ]
        df = pd.DataFrame(columns=columns)
        df.to_csv(self.inventory_file, index=False)

    def _save_inventory(self):
        """保存库存数据到CSV"""
        try:
            data = []
            for med_id, med in self.medications.items():
                med_data = med.to_dict()
                med_data['med_id'] = med_id
                med_data['is_prescription'] = isinstance(med, PrescriptionMedication)
                data.append(med_data)

            if not data:
                return

            df = pd.DataFrame(data)
            df.to_csv(self.inventory_file, index=False)
            print(f"Inventory for {self.member_name} saved successfully.")

        except Exception as e:
            print(f"Error saving inventory: {str(e)}")

    def add_medication(self, medication):
        """添加新药物"""
        med_id = self.next_med_id
        self.medications[med_id] = medication
        self.next_med_id += 1

        self._save_inventory()
        print(f"Added medication {medication.name} with ID {med_id}")
        
        # 添加药物时检查库存并设置提醒
        try:
            days_left = medication.calculate_days_left()
            if days_left <= 3 and self.reminder_system:
                self.reminder_system.set_reminder(
                    self.member_name,
                    med_id,
                    f"Low stock alert for {medication.name} (ID {med_id})! Only {days_left} days left."
                )
        except Exception as e:
            print(f"Error checking stock for new medication: {str(e)}")
        
        return med_id

    def update_stock(self, med_id, quantity):
        """更新库存"""
        if med_id not in self.medications:
            print(f"Medication ID {med_id} not found.")
            return False

        medication = self.medications[med_id]
        if medication.update_stock(quantity):
            self._save_inventory()
            print(f"Updated stock for {medication.name} (ID {med_id}) by {quantity}")

            # 检查更新后的库存状态并设置提醒
            try:
                days_left = medication.calculate_days_left()
                if days_left <= 3 and self.reminder_system:
                    self.reminder_system.set_reminder(
                        self.member_name,
                        med_id,
                        f"Low stock alert for {medication.name} (ID {med_id})! Only {days_left} days left."
                    )
                elif days_left > 3 and self.reminder_system:
                    self.reminder_system.clear_reminder(self.member_name, med_id)
            except Exception as e:
                print(f"Error checking stock after update: {str(e)}")

            return True

        print(f"Failed to update stock for {medication.name} (ID {med_id})")
        return False

    def delete_medication(self, med_id):
        """删除药物"""
        if med_id not in self.medications:
            print(f"Medication ID {med_id} not found.")
            return False

        deleted_med = self.medications.pop(med_id)
        self._save_inventory()

        if self.reminder_system:
            self.reminder_system.clear_reminder(self.member_name, med_id)

        print(f"Medication '{deleted_med.name}' (ID {med_id}) deleted successfully.")
        return True

    def check_low_stock(self):
        """检查低库存药物"""
        low_stock = []
        for med_id, medication in self.medications.items():
            try:
                days_left = medication.calculate_days_left()
                if days_left <= 3:
                    low_stock.append((med_id, medication.name, days_left))
                    # 检查时同时设置提醒
                    if self.reminder_system:
                        self.reminder_system.set_reminder(
                            self.member_name,
                            med_id,
                            f"Low stock alert for {medication.name} (ID {med_id})! Only {days_left} days left."
                        )
            except Exception as e:
                print(f"Error checking stock for medication {med_id}: {str(e)}")
                continue

        return low_stock

    def generate_stock_report(self):
        """生成库存报告"""
        if not self.medications:
            print(f"No medications found for {self.member_name}.")
            return

        print(f"\nStock Report for {self.member_name}:")
        print(f"{'ID':<5} {'Name':<20} {'Stock':<10} {'Days Left':<10}")
        print("-" * 50)

        for med_id, medication in self.medications.items():
            days_left = medication.calculate_days_left() or "N/A"
            print(f"{med_id:<5} {medication.name:<20} {medication.stock:<10} {days_left:<10}")

    def generate_prescription_report(self):
        """生成处方药报告"""
        prescriptions = self.list_prescription_medications()
        if not prescriptions:
            print(f"No prescription medications found for {self.member_name}.")
            return

        print(f"\nPrescription Report for {self.member_name}:")
        print(f"{'ID':<5} {'Name':<20} {'Doctor':<15} {'Date':<12} {'Expiration':<12}")
        print("-" * 80)

        for med in prescriptions:
            print(f"{med['id']:<5} {med['name']:<20} {med['doctor']:<15} {med['date']:<12} {med['expiration_date']:<12}")

    def list_prescription_medications(self):
        """列出所有处方药"""
        prescriptions = [
            {
                "id": med_id,
                "name": med.name,
                "doctor": getattr(med, 'doctor_name', 'N/A'),
                "date": getattr(med, 'prescription_date', 'N/A'),
                "indication": getattr(med, 'indication', 'N/A'),
                "warnings": getattr(med, 'warnings', 'N/A'),
                "expiration_date": getattr(med, 'expiration_date', 'N/A')
            }
            for med_id, med in self.medications.items()
            if isinstance(med, PrescriptionMedication)
        ]
        return prescriptions
