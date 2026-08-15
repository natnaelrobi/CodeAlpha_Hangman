def power(base,exp):
    exp_power = base**exp
    return exp_power
inp = input("Enter the base and the exponent respectively separated by space: ")
inp_list = inp.split()
base = int(inp_list[0])
exp = int(inp_list[1])
ans = power(base,exp)
print("The answer for the power expression is:", ans)