def check_palindrome():
    val = input("Enter a value to check if its a palindrome or not: ")
    
    if val == val[::-1]:
        print(val, "is a Palindrome")
    else:
        print(val, "is not a Palindrome")
        
check_palindrome()