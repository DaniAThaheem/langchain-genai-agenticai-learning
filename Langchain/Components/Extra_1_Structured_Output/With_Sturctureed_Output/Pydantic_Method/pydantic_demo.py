from pydantic import BaseModel

class Person(BaseModel):
    name:str

student_name = {"name":"Danish"}
student = Person(**student_name)
print(student)
