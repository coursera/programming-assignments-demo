#include <stdio.h>

// Include the user's submission
#include "get-bit.h"

// Define the number of tests to run
#define NUM_TEST_CASES 5

int main() {

    int ans;

    // Define the test cases
    const unsigned char inputs[NUM_TEST_CASES][2] = { {0, 5},
                                            {255, 0},
                                            {0xAE, 4},
                                            {0xAE, 5},
                                            {15, 3}};
    const unsigned char outputs[NUM_TEST_CASES] = {0, 1, 0, 1, 1};

    // Store which answers were correct
    float scores[NUM_TEST_CASES];

    // Run the tests, giving a 100% score to each correct answer
    for (int i = 0; i < NUM_TEST_CASES; i++) 
    {
        ans = getBit(inputs[i][0], inputs[i][1]);
        if (ans == outputs[i])
        {
            scores[i] = 1.0;
        }
        else
        {
            scores[i] = 0.0;
        }
    }

    // Print out the test results in JSON format
    printf("{\"scores\":[");
    for (int i = 0; i < NUM_TEST_CASES; i++)
    {
        printf("%f", scores[i]);
        if (i < NUM_TEST_CASES - 1)
        {
            printf(",");
        }
    }
    printf("]}\r\n");
    
    return 0;
}