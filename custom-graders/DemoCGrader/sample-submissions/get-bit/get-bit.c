#include "get-bit.h"

// Find the value (0 or 1) of the n-th bit in the provided byte
int getBit(unsigned char byte, unsigned char bit)
{
    int bit_val;
    
    // YOUR CODE HERE
    // ---
    bit_val = (byte >> bit) & 1;
    // ---

    return bit_val;
}