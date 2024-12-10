# reminder.py
import pandas as pd
from pathlib import Path

class ReminderSystem:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        # 确保数据目录存在
        self.data_dir = self.base_dir / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.reminders_file = self.data_dir / "reminders.csv"

        # 使用成员名称区分提醒
        self.reminders = {}  # 结构：{ "member_name": {med_id: message, ...}, ... }
        self._load_reminders()

    def _load_reminders(self):
        """从CSV加载提醒数据"""
        if not self.reminders_file.exists():
            # 创建一个新的空提醒文件
            df = pd.DataFrame(columns=['member', 'med_id', 'message'])
            df.to_csv(self.reminders_file, index=False)
            return

        try:
            df = pd.read_csv(self.reminders_file)
            if not df.empty:
                for _, row in df.iterrows():
                    member = row['member']
                    med_id = int(row['med_id'])  # 确保med_id是整数
                    message = row['message']
                    if member not in self.reminders:
                        self.reminders[member] = {}
                    self.reminders[member][med_id] = message

        except Exception as e:
            print(f"Error loading reminders: {str(e)}")
            df = pd.DataFrame(columns=['member', 'med_id', 'message'])
            df.to_csv(self.reminders_file, index=False)

    def _save_reminders(self):
        """保存提醒数据到CSV"""
        try:
            data = []
            for member, member_reminders in self.reminders.items():
                for med_id, message in member_reminders.items():
                    data.append({
                        'member': member,
                        'med_id': med_id,
                        'message': message
                    })

            df = pd.DataFrame(data)
            df.to_csv(self.reminders_file, index=False)
            print("Reminders saved successfully")
        except Exception as e:
            print(f"Error saving reminders: {str(e)}")

    def set_reminder(self, member, med_id, message):
        """设置提醒"""
        if member not in self.reminders:
            self.reminders[member] = {}
        self.reminders[member][med_id] = message
        self._save_reminders()

    def clear_reminder(self, member, med_id):
        """清除特定成员的某个提醒"""
        if member in self.reminders and med_id in self.reminders[member]:
            del self.reminders[member][med_id]
            self._save_reminders()
            print(f"Cleared reminder for {member} - Medication ID {med_id}.")

    def check_alerts(self, member, low_stock_warnings):
        """检查并设置低库存警告"""
        if low_stock_warnings:
            for med_id, med_name, days_left in low_stock_warnings:
                message = f"Low stock alert for {med_name} (ID {med_id})! Only {days_left} days left."
                self.set_reminder(member, med_id, message)
                print(message)  # 添加即时打印提醒

    def list_reminders(self, member):
        """列出指定成员的提醒"""
        if member not in self.reminders or not self.reminders[member]:
            print(f"\nNo active reminders for {member}.")
            return

        print(f"\nActive reminders for {member}:")
        for med_id, message in self.reminders[member].items():
            print(f"ID: {med_id}, Message: {message}")

    def list_all_reminders(self):
        """列出所有成员的提醒"""
        if not any(reminders for reminders in self.reminders.values()):
            print("\nNo active reminders.")
            return

        print("\n=== Active Reminders for All Members ===")
        for member, member_reminders in self.reminders.items():
            if member_reminders:
                print(f"\nReminders for {member}:")
                for med_id, message in member_reminders.items():
                    print(f"ID: {med_id}, Message: {message}")

    def clear_all_reminders(self, member):
        """清除某成员的所有提醒"""
        if member in self.reminders:
            self.reminders[member] = {}
            self._save_reminders()
            print(f"All reminders cleared for {member}.")