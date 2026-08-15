name = input("Enter your name: ")
sent = input("Enter a sentence with your name in it: ")
sent = sent.lower()
words = sent.split()
if name.lower() in words:
    print("Your name is in the sentence!")
else:
    print("Your name is not in the sentence!")
