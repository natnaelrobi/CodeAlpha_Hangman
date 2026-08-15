class Animal:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def show(self):
        print("Name:",self.name, "Age:",self.age)
    def make_sound(self):
        print("Some generic animal sound")
class Dog(Animal):
    def make_sound(self):
        print("Woff! Woff!")
ani1= Animal("Jack",17)
ani1.show()
ani1.make_sound()
ani2 = Dog("Bob",12)
ani2.show()
ani2.make_sound()