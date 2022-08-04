#include "power.h"

// Raise a to the power of b (positive integers only)
int power(int a, int b)
{
    int p;

    // YOUR CODE HERE
    // ---
    p = 1;
    for (int i = 0; i < b; i++)
    {
        p *= a;
    }
    // ---

    return p;
}