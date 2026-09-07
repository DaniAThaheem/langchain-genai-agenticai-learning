from typing import TypedDict

class Person(TypedDict):
    name: str
    age: int

user_dict : Person = {"name": "Danish", "age": 22}

print(user_dict)