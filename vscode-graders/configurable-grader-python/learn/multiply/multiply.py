def multiply(inputList):

    # Correct solution
    product = inputList[0]
    for i in range(1,len(inputList)):
        product = product*inputList[i]

    # Optional wrong solution below - uncomment if you'd like example of
    # elaborate feedback when testing with this template
    
    # product = inputList[0]
    
    return product
