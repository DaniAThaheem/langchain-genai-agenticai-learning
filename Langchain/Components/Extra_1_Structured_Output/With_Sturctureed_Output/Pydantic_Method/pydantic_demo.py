from pydantic import BaseModel
from typing import Optional

class Person(BaseModel):
    name:str = "Dani"
    age: Optional[int] = None

student_name = {"name":"Danish", "age":32}
student = Person(**student_name)
print(student)
