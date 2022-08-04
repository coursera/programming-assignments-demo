# Tool macro
CC = gcc

# Settings
NAME = app

# Search path for header files (current directory)
CFLAGS = -I.

# Other compiler flags
CFLAGS += -Wall

# Names for our output object files
OBJS = main.o get-bit.o

# Default rule to make our application
.PHONY: all
all: testapp

# Compile library source code into object files
testapp:${OBJS}
	${CC} ${CFLAGS} -o $@ ${OBJS}

# Remove compiled objects
.PHONY: clean
clean:
	rm -r $(OBJS)