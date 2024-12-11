from field_mapper.mapper import FieldMapper

def validate_email(value: str) -> bool:
    return "@" in value and "." in value
# To-DO Validate function not working properly

field_map = {
    "name": "full_name",
    "email[0]": "contact_email",
    "phone.phone_two": "mobile_number",
    "income[0].Jan": "monthly_income",
    "year_salary[].year": "salary"
}


data = [
    {
        "name": "Alice",
        "email": ["alice@example.com", "alice2@example.com"],
        "phone": {"phone_one": '22222', "phone_two": "2332432"},
        "income": [{"Jan": 2000, "Feb": 3000}],
        "year_salary": [
            {"year": "2020", "Jan": 2000, "Feb": 3000},
            {"year": "2021", "Jan": 2000, "Feb": 3000}
        ]
    }
]


fields = {
    "name": {"type": str, "position": "name", "max_length": 50, "required_field": True, "required_value": True},
    "email": {"type": list, "position": "email[0]", "max_length": 100, "required_field": True, "required_value": True},
    "phone": {"type": dict, "position": "phone.phone_two", "required_field": True, "required_value": True},
    "income": {"type": list, "position": "income[0].Jan", "required_field": True, "required_value": True},
    "year_salary": {"type": list, "position": "year_salary[].year", "required_field": True, "required_value": True}
}

mapper = FieldMapper(fields=fields, field_map=field_map)
processed_data = mapper.process(data, skip_duplicate=True)
print("Output:", processed_data)
print("Error:",mapper.error)

