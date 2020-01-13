# This function takes a numeric input and returns the negative of this number.

def flipSign(input):
    product = input*(-1)
    return product

# MAIN -------------------------------------------------------------------------
def main(input):
    output = flipSign(input)
    return output

if __name__ == '__main__':
    main(input)
