from field_mapper.mapper import FieldMapper

field_map = {
    "name": "full_name",
    "email": "contact_email",
    "phone": "mobile_number",
    "income": "monthly_income"
}
fields = {
    "name": {"type": str, "max_length": 50, "required_field": True, "required_value":True},
    "email": {"type": list, "max_length": 100, "required_field": True, "required_value":True},
    "phone": {"type": dict, "max_length": 15, "required_field": False, "required_value":False},
    "income": {"type": list, "max_length": 15, "required_field": True, "required_value":False}
}

data = [
    {"name": "Alice", "email": ["alice@example.com", "alice2@example.com"],
     "phone": {"phone_one": '22222', "phone_two": "2332432"},
     "income": [{"January": 20000, "February": 250000}]},
    {"name": "Alice", "email": ["alice@example.com", "alice2@example.com"],
     "phone": {"phone_one": '22222', "phone_two": "2332432"},
     "income": [{"January": 20000, "February": 250000}]}
]

mapper = FieldMapper(fields, field_map)
processed_data = mapper.process(data, skip_duplicate=True)
print("Output:", processed_data)
print("Error:",mapper.error)
