CC = g++
INCLUDE_DIR = ./include
FLAGS = -c -I$(INCLUDE_DIR)

build:
	# g++ -c -I./include src/ml/*.cpp
	$(CC) $(FLAGS) src/utils/*.cpp 

test_array:
	$(CC) $(FLAGS) src/tests/test_array.cpp 
	$(CC) -o test_array *.o -lm
