def multiply(inputList):
    product = inputList[0]
    
    for i in range(1,len(inputList)):
        product = product*inputList[i]
    return product
