# medication.py
class Medication:
    def __init__(self, name, dosage, frequency, daily_dosage, stock):
        self.name = name
        self.dosage = dosage
        self.frequency = frequency
        self.daily_dosage = daily_dosage
        self.stock = stock

    def calculate_days_left(self):
        """计算剩余天数"""
        if not isinstance(self.daily_dosage, int) or self.daily_dosage <= 0:
            raise ValueError("Daily dosage must be a positive integer.")
        return self.stock // self.daily_dosage  # 使用实际的 daily_dosage

    def display_info(self):
        return f"Medication: {self.name}, Dosage: {self.dosage}, Frequency: {self.frequency}, Daily Dosage: {self.daily_dosage}, Stock: {self.stock}"

    def update_stock(self, quantity):
        """更新库存"""
        if not isinstance(quantity, int):
            raise ValueError("Quantity must be an integer.")
        if self.stock + quantity < 0:
            print(f"Not enough stock to remove. Current stock: {self.stock}, Requested: {abs(quantity)}")
            return False
        self.stock += quantity
        return True

    def to_dict(self):
        """将对象转为字典"""
        return {
            "name": self.name,
            "dosage": self.dosage,
            "frequency": self.frequency,
            "daily_dosage": self.daily_dosage,
            "stock": self.stock
        }

    def __repr__(self):
        return f"Medication(name={self.name}, dosage={self.dosage}, frequency={self.frequency}, daily_dosage={self.daily_dosage}, stock={self.stock})"
