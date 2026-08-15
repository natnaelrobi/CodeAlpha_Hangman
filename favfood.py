fav_food=input("What are your favorite foods? Enter five separated by a comma: ")
fav = fav_food.split(",")
for i in range(5):
    fav.append(fav_food)
    print("Your favourite food",i+1, "is",fav[i])



