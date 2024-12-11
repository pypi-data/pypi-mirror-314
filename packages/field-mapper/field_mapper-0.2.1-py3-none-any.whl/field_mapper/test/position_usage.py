from field_mapper.mapper import FieldMapper

def validate_email(value: str) -> bool:
    """Custom validator for email format."""
    return "@" in value and "." in value

field_map = {
    "name": "full_name",
    "email": "contact_email",
    "phone": "mobile_number",
    "income": "monthly_income"
}
data = [
    {"name": "Alice",
     "email": ["alice@example.com", "alice2@example.com"],
     "phone": {"phone_one": '22222', "phone_two": "2332432"}, "income":[{"January":20000, "February":250000}]}
]

fields = {
    "name": {"type": str, "position": "name", "max_length": 50, "required_field": True, "required_value": True},
    "email": {"type": str, "position": "email[0]", "max_length": 100, "required_field": True, "required_value": True, "custom": validate_email},

}

mapper = FieldMapper(fields, field_map)
processed_data = mapper.process(data, skip_duplicate=True)
print("Output:", processed_data)
print("Error:",mapper.error)
