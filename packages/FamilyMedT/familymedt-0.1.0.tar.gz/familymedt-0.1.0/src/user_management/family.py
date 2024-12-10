# family.py
import pandas as pd
from pathlib import Path
from medication_management.inventory import InventoryManagement

class FamilyManagement:
    def __init__(self, base_dir, reminder_system):
        self.base_dir = base_dir
        self.reminder_system = reminder_system
        # 确保数据目录存在
        self.data_dir = self.base_dir / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.members_file = self.data_dir / "members.csv"
        self.members = {}
        self.current_member = None
        self._load_members()

    def _load_members(self):
        """从CSV加载成员数据"""
        if not self.members_file.exists():
            df = pd.DataFrame(columns=['name'])
            df.to_csv(self.members_file, index=False)
            return

        try:
            df = pd.read_csv(self.members_file)
            if not df.empty:
                for _, row in df.iterrows():
                    self.members[row['name']] = InventoryManagement(
                        row['name'], self.base_dir, self.reminder_system
                    )
        except Exception as e:
            print(f"Error loading members: {str(e)}")
            df = pd.DataFrame(columns=['name'])
            df.to_csv(self.members_file, index=False)

    def save_all_data(self):
        """保存所有数据"""
        try:
            df = pd.DataFrame({'name': list(self.members.keys())})
            df.to_csv(self.members_file, index=False)

            for member_name, inventory in self.members.items():
                inventory._save_inventory()

            print("All data saved successfully")
            return True
        except Exception as e:
            print(f"Error saving data: {str(e)}")
            return False

    def add_member(self, name):
        """添加新成员"""
        if not name:
            raise ValueError("Name cannot be empty")

        if name in self.members:
            print(f"Member {name} already exists.")
            return False

        self.members[name] = InventoryManagement(name, self.base_dir, self.reminder_system)
        self.save_all_data()
        print(f"Family member '{name}' added successfully.")
        return True

    def switch_member(self, name):
        """切换当前成员"""
        if name in self.members:
            self.current_member = name
            print(f"Switched to family member: {name}")
            
            # 切换成员时检查低库存情况
            inventory_manager = self.get_current_member_inventory()
            if inventory_manager:
                low_stock_warnings = inventory_manager.check_low_stock()
                if low_stock_warnings:
                    self.reminder_system.check_alerts(name, low_stock_warnings)
            return True
            
        print(f"Family member '{name}' not found.")
        return False

    def list_members(self):
        """列出所有成员"""
        if not self.members:
            print("No family members registered.")
            return

        print("\nRegistered family members:")
        for name in self.members:
            if name == self.current_member:
                print(f"- {name} (current)")
            else:
                print(f"- {name}")

    def delete_member(self, name):
        """删除家庭成员"""
        if name not in self.members:
            print(f"Family member '{name}' not found.")
            return False

        inventory = self.members[name]
        if hasattr(inventory, 'inventory_file') and inventory.inventory_file.exists():
            inventory.inventory_file.unlink()

        if hasattr(inventory, 'history_file') and inventory.history_file.exists():
            inventory.history_file.unlink()

        del self.members[name]
        if self.current_member == name:
            self.current_member = None
            
        # 删除成员时清除所有提醒
        self.reminder_system.clear_all_reminders(name)
        
        self.save_all_data()
        print(f"Family member '{name}' and associated data deleted successfully.")
        return True

    def get_current_member_inventory(self):
        """获取当前成员的库存管理器"""
        if not self.current_member:
            print("No family member selected.")
            return None
        return self.members[self.current_member]

    def get_all_low_stock(self):
        """获取所有成员的低库存警告"""
        low_stock_warnings = []
        for member_name, inventory in self.members.items():
            low_stock_meds = inventory.check_low_stock()
            for med_id, med_name, days_left in low_stock_meds:
                low_stock_warnings.append((member_name, med_id, med_name, days_left))
        return low_stock_warnings