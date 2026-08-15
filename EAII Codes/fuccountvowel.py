def count_vowels(text):
    vowels = ['a', 'e', 'i', 'o', 'u']
    count = 0
    for i in text.lower():
        if i in vowels:
            count += 1
        else:
            continue
    return count
text = input("Enter a string: ")
count = count_vowels(text)
print("The number of vowels in the text is",count)
