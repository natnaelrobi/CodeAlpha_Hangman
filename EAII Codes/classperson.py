class Person:
    def __init__(self,name,age):
        self.__name =name
        self.__age=age
    def show(self):
        print("Name:",self.__name,"Age:",self.__age)
    '''def get_name(self):
        return self.__name
    def get_age(self):
        return self.__age
    def set_name(self,name):
        self.__name=name
    def set_age(self,age):
        self.__age=age'''
per1= Person("Abebe",25)
per2= Person("Henok",35)
per1.show()
per2.show()
'''per1.get_name()
per2.get_age()
per1.set_name("Nahom")
per2.set_age(32)
print("The new name of person 1 is",per1.get_name())
print("The new age of person 2 is",per2.get_age())'''