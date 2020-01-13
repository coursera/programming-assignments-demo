def multiply(inputList):
    product = inputList[0]
    
    for i in range(1,len(inputList)):
        product = product*inputList[i]
    return product

# MAIN -------------------------------------------------------------------------
def main(input):
    output = multiply(input)
    return output

if __name__ == '__main__':
    main(input)
