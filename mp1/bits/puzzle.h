#ifndef _PUZZLEH_
#define _PUZZLEH_

#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#define PDEBUG 1

#define MOVEBLOCKSZ 32 // 32 bytes, 2 bits per move, 128 moves
#define MOVESPERBLOCK 128
#define MOVESPERBYTE  4
/*
const char UP = 0;    // 00000000
const char DOWN = 1;  // 00000001
const char LEFT = 2;  // 00000010
const char RIGHT = 3; // 00000011
*/
#define UP 0x0 // 00000000
#define DOWN 0x1  // 00000001
#define LEFT 0x2  // 00000010
#define RIGHT 0x3 // 00000011

const char MOVEMASK = 3;

typedef struct fringenode_struct {  // 32 bytes
  char *moves;
  int movecount;
  char *state;
  struct fringenode_struct *next_node;
} fringenode;

fringenode *create_node(char *istate, int dim);
fringenode *copy_node(fringenode *orig, int dim);
void add_move(fringenode *fn, char move);
void print_moves(fringenode *fn);
void update_state(char *state, int xloc, char move);

#endif
