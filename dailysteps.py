daily_steps = input("ENter your daily steps for the past seven days separated by space: ")
steps_list = daily_steps.split()
total_steps = 0
for steps in steps_list:
    total_steps += float(steps)
average = total_steps/ len(steps_list)
print("Averge:", average)
if total_steps < 100:
    print("You have made too few steps")
elif 100<total_steps<500:
    print("You have made enough steps")
else:
    print("You have made too many steps")