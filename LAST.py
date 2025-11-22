class Person:
       """Person 基类：姓名、年龄、性别"""
       def __init__(self, name: str, age: int, gender: str):
                self.name = name
                self.age = age
                self.gender = gender
       def person_info(self):    
            print(f"[Person] 姓名：{self.name} | 年龄：{self.age} | 性别：{self.gender}")
class Student(Person):
       def __init__(self, name: str, age: int, gender: str, college: str, clazz: str):
                super().__init__(name, age, gender)
                self.college = college
                self.clazz = clazz
       def person_info(self):
             super().person_info()  
             print(f"[Student] 学院：{self.college} | 班级：{self.clazz}")
       def __str__(self):
          return (f"Student(name={self.name}, age={self.age}, gender={self.gender}, "
                  f"college={self.college}, class={self.clazz})")
if __name__ == "__main__":
       stu = Student("liangaoyan", 20, "nan", "dianziyuxinxixuebu", "XX2404")
       stu.person_info() 
       print(stu)  
