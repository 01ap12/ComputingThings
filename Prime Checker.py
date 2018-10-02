while True:
    number = int(input("What is your number? "))
    Prime = True
    for i in range(2,number):    
        if number % i == 0:
            Prime = False
    print("Is it prime? :",Prime,"\n")
