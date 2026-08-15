class Animal:
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def show(self):
        print("Name:",self.name, "Age:",self.age)
    def sound(self):
        print("Some generic animal sound")
class Dog(Animal):
    def sound(self):
        print("Woff! Woff!")
class Cat(Animal):
    def sound(self):
        print("Meaw Meaw")
ani1 = Dog("Bob",12)
ani2 = Cat("Tom",10)
ani1.show()

ani1.sound()
ani2.show()
ani2.sound()
