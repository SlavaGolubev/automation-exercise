from models.user import RegistrationData


def generate_user_data():
    reg_data_obj = RegistrationData.generate_data()
    reg_data = {
        "name": reg_data_obj.name,
        "email": reg_data_obj.email,
        "password": reg_data_obj.password,
        "title": reg_data_obj.title.strip('.'),
        "birth_date": reg_data_obj.birth_day,
        "birth_month": reg_data_obj.birth_month,
        "birth_year": reg_data_obj.birth_year,
        "firstname": reg_data_obj.first_name,
        "lastname": reg_data_obj.last_name,
        "company": reg_data_obj.company,
        "address1": reg_data_obj.address1,
        "address2": reg_data_obj.address2,
        "country": reg_data_obj.country,
        "zipcode": reg_data_obj.zipcode,
        "state": reg_data_obj.state,
        "city": reg_data_obj.city,
        "mobile_number": reg_data_obj.mobile_number,
    }
    return reg_data_obj, reg_data
