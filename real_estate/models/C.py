class Property:
    def __init__(self, name, price, bedrooms):
        self.name = name
        self.price = price
        self.bedrooms = bedrooms

    def is_affordable(self, budget):
        """Check if within budget"""
        return self.price <= budget

    def return_bedrooms(self):
        """Return property bedrooms"""
        return f"{self.bedrooms}"

    def return_price(self):
        """Return property price"""
        return f"{self.price}"

    def return_name(self):
        """Return property name"""
        return f"{self.name}"

# Create properties
apt_a = Property("property  1", 1500, 2)
apt_b = Property("property  2", 2000, 3)
print("total prices", int(apt_a.return_price()) + int(apt_b.return_price())) # 2-bed at $1500/month

# print(apt_b.is_affordable(1800)) # False
# print(apt_a.is_affordable(1800)) # True


