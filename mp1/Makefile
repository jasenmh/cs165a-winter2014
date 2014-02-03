all: puzzle

puzzle: puzzle.c puzzle.h
	gcc -o puzzle puzzle.c -lm -Wall

puzzle-debug: puzzle.c puzzle.h
	gcc -o puzzle puzzle.c -lm -Wall -g

clean:
	rm puzzle
