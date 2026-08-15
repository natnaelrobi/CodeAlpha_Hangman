class Numbers:
    def adding(self, a ,b=None):
        if b==None:
            print("The product of the number with itself is:", a**2)
        else:
            print("The product of the numbers is:", a*b)
nums1 = Numbers()
nums1.adding(23)
nums2 = Numbers()
nums2.adding(34,5)

