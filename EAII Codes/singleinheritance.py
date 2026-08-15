#Single Inheritance
class Parent:
    def show(self):
        print("This is from parent class")
class Child(Parent):
    def show_child(self):
        print("This is from child class")
        print("\n")
chi1 = Child()
chi1.show()
chi1.show_child()

#Multiple Inheritance
class Internet:
    def show(self):
        print("This is from the Internet")
class Book:
    def show_book(self):
        print("This is from the book")
class Answer(Internet, Book):
    def show_ans(self):
        print("This is from the answer")
        print("\n")
ans1= Answer()
ans1.show()
ans1.show_book()
ans1.show_ans()

#Multi-level Inheritance
class Animal:
    def show(self):
        print("This is from the animal class")
class Mammal(Animal):
    def show_mammal(self):
        print("This is from the mammal class")
class Dog(Mammal):
    def show_dog(self):
        print("This is from the dog class")
        print("\n")
dog1 = Dog()
dog1.show()
dog1.show_mammal()
dog1.show_dog()

#Hierarchical Inheritance
class Vehicle:
    def show(self):
        print("This is from the vehicle")
class AirPlane(Vehicle):
    def show_air(self):
        print("This is from the airplane")
class Ship(Vehicle):
    def show_ship(self):
        print("This is from the ship")
        print("\n")
air1 =AirPlane()
ship1 = Ship()
air1.show()
air1.show_air()
ship1.show()
ship1.show_ship()

#Hybrid Inheritance (Combination of the above)
class Internet1:
    def show1(self):
        print("This is from the Internet1")
class Articles(Internet1):
    def show_arc(self):
        print("This is from the articles")
class PDFs(Internet1):
    def show_pdfs(self):
        print("This is from the PDFs")
class Answer1(Articles,PDFs):
    def show_ans1(self):
        print("This is from the answer1")
ans2 = Answer1()
ans2.show1()
ans2.show_arc()
ans2.show_pdfs()
ans2.show_ans1()
