
n = int(input("Enter any natural number: "))

if n < 0:
    print ("wrong input. Please enter a positive number.")

else:
    sum = 0
    while (n > 0):
        sum +=n
        n = n - 1
    print ("The sum of the natural numbers is: ", sum)