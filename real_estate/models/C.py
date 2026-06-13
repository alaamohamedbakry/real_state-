from datetime import date

# Part 1: Variables & Types
# -------------------------
# Variables store values. Each value has a type, such as string, integer, boolean, or None.
property_name = "Downtown Apartment A"    # string text
property_price = 1500                     # integer number
is_available = True                       # boolean value: True or False
bedrooms = 2                              # integer for number of bedrooms
tenant_name = None                        # None represents no value yet

# Part 2: Data Structures
# ----------------------
# Lists store ordered collections of values. We can access items by index.
prices = [1500, 2000, 1800, 2200]

# Dictionaries store key-value pairs. Keys are used to look up values.
property_data = {
    "name": "Downtown Apartment A",
    "price": 1500,
    "bedrooms": 2,
    "is_available": True,
}

# Part 5: Functions
# -----------------
# Functions are reusable blocks of code. They take inputs, run code, and return outputs.

def calculate_property_total(rent, maintenance, utilities):
    """Calculate the total monthly cost of a property."""
    return rent + maintenance + utilities


def is_property_available(property_record, today_date):
    """Return True if the property is available and the lease end date has passed."""
    if property_record["available"] and property_record["lease_end_date"] < today_date:
        return True
    return False

# Part 6: Classes
# ---------------
# Classes are blueprints for creating objects with shared behavior.
class Property:
    def __init__(self, name, price, bedrooms):
        # The __init__ method sets up a new object with its own data.
        self.name = name
        self.price = price
        self.bedrooms = bedrooms

    def is_affordable(self, budget):
        """Return True if this property is within the given budget."""
        return self.price <= budget

    def monthly_cost(self):
        """Return the monthly cost of this property."""
        return self.price

    def description(self):
        """Return a short description of the property."""
        return f"{self.bedrooms}-bed at ${self.price}/month"

class Tenant:
    def __init__(self, id,name):
        self.id = id
        self.name = name
 
class Contract:
    def __init__(self,property_obj , tenant_obj):
        self.property = property_obj
        self.tenant = tenant_obj
        
# Part 7: Inheritance
# -------------------
# Inheritance lets a class reuse methods and data from a parent class.
class ApartmentProperty(Property):
    """ApartmentProperty inherits from Property and adds specific behavior."""

    def __init__(self, name, price, bedrooms):
        # Call the parent class initializer to set basic fields.
        super().__init__(name, price, bedrooms)

    def description(self):
        """Override the description method to add apartment-specific text."""
        return f"{self.bedrooms}-bed apartment"


if __name__ == "__main__":
    # Part 1 runtime examples
    print(property_name)
    print(property_price)
    print(type(property_name), type(property_price), type(is_available), type(bedrooms), type(tenant_name))
    print()

    # Part 2 runtime examples
    print(prices[0])  # first item in a list
    print(prices[1])  # second item in a list
    prices.append(1900)  # add a new value to the end of the list
    print(prices)

    print(property_data["name"])   # look up a dictionary value by key
    print(property_data["price"])
    property_data["price"] = 1600  # update an existing dictionary value
    print(property_data)
    print()

    # Part 3: Conditions
    budget = 1800
    if property_price <= budget:
        print("You can afford it")
    else:
        print("Too expensive")

    price = 1500
    if bedrooms >= 2 and price <= 2000:
        print("Good deal for 2-bedroom")
    elif bedrooms == 1:
        print("Studio or 1-bedroom")
    else:
        print("Check other properties")
    print()

    # Part 4: Loops
    properties = [
        {"name": "Apt A", "price": 1500, "available": True},
        {"name": "Apt B", "price": 2000, "available": False},
        {"name": "Apt C", "price": 1800, "available": True},
    ]

    # Loop through each property in the list
    for property_item in properties:
        if property_item["available"]:
            print(f"{property_item['name']} is available for ${property_item['price']}")
    print()

    # Use a loop and condition to calculate a total
    total_rent = 0
    for property_item in properties:
        if property_item["available"] == False:
            total_rent += property_item["price"]
    print(f"Total rent from occupied units: ${total_rent}")
    print()

    # Part 5: Function usage
    property1_total = calculate_property_total(1500, 50, 30)
    property2_total = calculate_property_total(2000, 75, 40)
    print(property1_total)  # 1580
    print(property2_total)  # 2115
    print()

    today = "2024-06-01"
    apt = {"available": True, "lease_end_date": "2024-05-01"}
    if is_property_available(apt, today):
        print("Available for booking")
    else:
        print("Not available yet")
    print()

    # Part 6: Classes usage
    apt_a = Property("Downtown Apt A", 1500, 2)
    apt_b = Property("Downtown Apt B", 2000, 3)
    print(apt_a.description())
    print(apt_b.is_affordable(1800))
    print(apt_a.is_affordable(1800))
    print()
    tenant_1 = Tenant(1, "alaa")
    for prop in properties:
      if prop["price"] == 1500:
        contract = Contract(prop, tenant_1)

        print(
            f"{tenant_1.name} rented {prop['name']}"
        )

    # Part 7: Inheritance usage
    apt_inherited = ApartmentProperty("Downtown", 1500, 2)
    print(apt_inherited.monthly_cost())
    print(apt_inherited.description())
    print()

    # Part 8: Dictionaries as simple object records
    property_record = {
        "id": 1,
        "name": "Downtown Apt",
        "price": 1500,
        "bedrooms": 2,
    }
    print(property_record["name"])        # access value by key
    property_record["tenant"] = "Ahmed"  # add a new key/value pair
    property_record["price"] = 1600          # update an existing value
    print(property_record)

    # pip install flake8, pylint, black, isort for code quality and formatting checks
    # pylint -E /home/odoo/workspace/Odoo_17/my_adds/real_estate_project/real_estate/models/C.py



