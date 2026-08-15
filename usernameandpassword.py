user_name = input("Enter your username: ")
password = int(input("Enter your password: "))
if user_name == "username@gmail.com" and password == 8765421:
    print("You are successfully logged in!")
elif user_name == "username@gmail.com" and password != 8765421:
    print("Incorrect password!")
elif user_name != "username@gmail.com" and password == 8765421:
    print("Incorrect username!")
else:
    print("Incorrect username and password!")
