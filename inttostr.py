num = int(input("Enter a mumber from 1 to 10: "))
dict = {1:"One", 2:"Two", 3:"Three", 4:"Four", 5:"Five", 6:"Six",7:"Seven", 8:"Eight", 9:"Nine", 10:"Ten"}
if num in dict.keys():
    print("The number you entered is",dict[num],end=".")
else:
    print("Invalid input!")