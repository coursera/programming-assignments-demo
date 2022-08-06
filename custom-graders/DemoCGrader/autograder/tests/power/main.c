#include <stdio.h>

// Include the user's submission
#include "power.h"

// Define the number of tests to run
#define NUM_TEST_CASES 5

int main() {

    int ans;

    // Define the test cases
    const int inputs[NUM_TEST_CASES][2] = { {0, 0},
                                            {10, 0},
                                            {1, 2},
                                            {3, 3},
                                            {3, 10}};
    const int outputs[NUM_TEST_CASES] = {1, 1, 1, 27, 59049};

    // Store which answers were correct
    float scores[NUM_TEST_CASES];

    // Run the tests, giving a 100% score to each correct answer
    for (int i = 0; i < NUM_TEST_CASES; i++) 
    {
        ans = power(inputs[i][0], inputs[i][1]);
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