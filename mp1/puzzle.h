#ifndef _PUZZLEH_
#define _PUZZLEH_

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define PDEBUG  1
#define MAXDIM  20

typedef struct fringenode_struct {  // 36 bytes, order matters (out of date)
  int *state;
  struct fringenode_struct *next_node;
  struct fringenode_struct *prev_node;
  short f;
  short g;  // g = f + h
  short childs;
  char lastmove;  // the move that got us to this state
int nodenum;  // for debug only
} fringenode;

fringenode *create_node(int *istate, int dim);
int read_state_from_stdin(int **state);
void print_moves(fringenode *endnode, int terminal);
void print_state(int *state, int dim);
void update_state(int *state, char move, int dim);
int h_man_dist(int *state, int dim);
void get_moves(char *moves, fringenode *fn, int dim);
void insert_node(fringenode *n, fringenode **h);
void print_list_order(fringenode *h, int count);

#endif
