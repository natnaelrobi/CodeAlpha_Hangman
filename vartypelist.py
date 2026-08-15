char = [
    ("String", "Hello World"),
    ("Integer", 12),
    ("Float", 3.14),
    ("Bollean", True)
]
for name, value in char:
    print(f"{name}: {type(value)}")