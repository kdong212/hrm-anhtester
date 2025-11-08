# warehouse_data.py
import random
from faker import Faker

fake = Faker()

class WarehouseData:
    def __init__(self, location_option=None, country_name=None):
        self.name = f"WH_{fake.company()}_{fake.random_int(min=1000, max=9999)}"
        self.contact_number = fake.phone_number()
        # 'Yes' cho Pickup, 'No' cho Drop Off. Điều chỉnh nếu logic thực tế khác.
        self.location = location_option if location_option is not None else random.choice(["Yes", "No"])
        self.country = country_name # Sẽ được gán sau khi lấy từ dropdown
        self.address = fake.street_address()
        self.address2 = fake.secondary_address() 
        self.city = fake.city()
        self.state = fake.state() 
        self.postal_code = fake.postcode()