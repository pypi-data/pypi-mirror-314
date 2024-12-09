from field_mapper.mapper import FieldMapper

field_map = {
    "name": "full_name",
    "email": "contact_email",
    "phone": "mobile_number",
    "income": "monthly_income"
}
fields = {
    "name": {"type": str, "max_length": 50, "required_field": True, "required_value":True},
    "email": {"type": str, "max_length": 100, "required_field": True, "required_value":True},
    "phone": {"type": str, "max_length": 15, "required_field": False, "required_value":False},
    "income": {"type": int, "max_length": 15, "required_field": True, "required_value":False}
}
data = [
    {"name": "Charlie", "email": "charlie@example.com", "phone": "888888", "income":0},
    {"name": "Charlie", "email": "charlie@example.com", "phone": "444444", "income":0},
    {"name": "Charlie", "email": "charlie@example.com", "phone": "444444", "income":0}
]
mapper = FieldMapper(fields, field_map)
processed_data = mapper.process(data, skip_duplicate=True)
print("Output:", processed_data)
print("Error:",mapper.error)
