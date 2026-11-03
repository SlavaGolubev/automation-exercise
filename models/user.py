import random
from typing import Optional

from faker import Faker
from pydantic import BaseModel


class RegistrationData(BaseModel):
    name: str
    email: str
    password: str
    birth_day: str
    birth_month: str
    birth_year: str
    newsletter: bool
    offersletter: bool
    first_name: str
    last_name: str
    company: str
    address1: str
    address2: Optional[str] = None
    country: str
    city: str
    state: str
    zipcode: str
    mobile_number: str
    title: str

    @classmethod
    def generate_data(cls):

        fake = Faker()
        reg_data = dict()

        reg_data['title'] = random.choice(["Mr.", "Mrs", "Miss"])
        reg_data['name'] = fake.first_name_male() if reg_data['title'] == "Mr." else fake.first_name_female()
        reg_data['email'] = fake.email()
        reg_data['password'] = fake.password()
        reg_data['birth_day'] = str(random.choice(range(1, 32)))
        reg_data['birth_month'] = random.choice(["January", "February", "March", "April", "May", "June",
                                           "July", "August", "September", "October", "November", "December"])
        reg_data['birth_year'] = str(random.choice(range(1900, 2022)))
        reg_data['newsletter'] = random.choice([True, False])
        reg_data['offersletter'] = random.choice([True, False])
        reg_data['first_name'] = reg_data['name']
        reg_data['last_name'] = fake.last_name_male() if reg_data['title'] == "Mr." else fake.last_name_female()
        reg_data['company'] = fake.company()
        reg_data['address1'] = fake.address()
        reg_data['address2'] = random.choice([fake.address(), None])
        reg_data['country'] = random.choice(
            ["India", "United States", "Canada", "Australia", "Israel", "New Zealand", "Singapore", ])
        reg_data['state'] = fake.state()
        reg_data['city'] = fake.city()
        reg_data['zipcode'] = fake.zipcode()
        reg_data['mobile_number'] = fake.phone_number()
        return cls(**reg_data)






