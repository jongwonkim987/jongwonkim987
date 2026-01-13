class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def info(self):
        return f'강아지 이름: {self.name}, 나이: {self.age}살'