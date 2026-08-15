expense_dict = {}
num = int(input("How many expenses do you want to enter?"))
for i in range(num):
    expense = input("Enter your expense {i}: ".format(i=i+1))
    expense_price = int(input("Enter the expense {i} price: ".format(i=i+1)))
    expense_dict[expense] = expense_price
print(expense_dict)
total_expense = sum(expense_dict.values())

if total_expense > 500:
    print("You have made the most expense")
elif 100< total_expense < 500:
    print("You have made the medium expense")
else:
    print("You have made the least expense")