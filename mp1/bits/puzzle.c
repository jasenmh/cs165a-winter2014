#include "puzzle.h"

int main(int argc, char *argv[])
{
  fringenode *f;

  f = create_node("12345678x", 3);

//  printf("fringenode is size %d\n", sizeof(fringenode));
//  printf("char is size %d\n", sizeof(char));
//  printf("short int is size %d\n", sizeof(short int));

  add_move(f, 'd');
  add_move(f, 'u');
  add_move(f, 'l');
  add_move(f, 'r');
  add_move(f, 'u');
  add_move(f, 'd');
  add_move(f, 'l');
  add_move(f, 'r');
  add_move(f, 'u');
  add_move(f, 'r');

  print_moves(f);

  return 0;
}

fringenode *create_node(char *istate, int dim)
{
  fringenode *newnode;
  int dimsqr = dim * dim;

  newnode = (fringenode *)malloc(sizeof(fringenode));
  newnode->moves = (char *)malloc(MOVEBLOCKSZ);
  newnode->state = (char *)malloc(dimsqr);

  bzero(newnode->moves, MOVEBLOCKSZ);
  newnode->movecount = 0;
  memcpy(newnode->state, istate, dimsqr);
  newnode->next_node = NULL;

if(PDEBUG) newnode->moves[0] = 0xFF;

if(PDEBUG) printf("create_node: moves size %d\n",
sizeof(newnode->moves));

  return newnode;
}

fringenode *copy_node(fringenode *orig, int dim)
{
  fringenode *newnode;
  int dimsqr = dim * dim;
  int blocks = (orig->movecount / MOVESPERBLOCK) + 1;

  newnode = (fringenode *)malloc(sizeof(fringenode));
  newnode->moves = (char *)malloc(blocks * MOVEBLOCKSZ);
  newnode->state = (char *)malloc(dimsqr);

  memcpy(newnode->moves, orig->moves, blocks);
  newnode->movecount = orig->movecount;
  memcpy(newnode->state, orig->state, dimsqr);
  newnode->next_node = orig->next_node;

  return newnode;
}

void add_move(fringenode *fn, char move)
{
  int moveidx;
  int haveblks = (fn->movecount / MOVESPERBLOCK) + 1;
  int needblks = ((fn->movecount + 1) / MOVESPERBLOCK) + 1;

  if(haveblks != needblks)
  {
    // TODO: allocate another block
    printf("ERROR: move block expansion not implemented\n");
  }

  moveidx = fn->movecount / MOVESPERBYTE;
  fn->moves[moveidx] = fn->moves[moveidx] << 2;

if(PDEBUG) printf("add_move: idx %d starts as %c\n", moveidx,
fn->moves[moveidx]);

  switch(move)
  {
    case 'u':
      fn->moves[moveidx] | UP;
      break;
    case 'd':
      fn->moves[moveidx] | DOWN;
      break;
    case 'l':
      fn->moves[moveidx] | LEFT;
      break;
    case 'r':
      fn->moves[moveidx] | RIGHT;
      break;
  }

if(PDEBUG) printf("add_move: idx %d starts as %c\n", moveidx,
fn->moves[moveidx]);

  fn->movecount++;
}

void print_moves(fringenode *fn)
{
  int move, moveidx;
  char curbyte;
  char curmove;

  for(move = 0; move < fn->movecount; ++move)
  {
    if(move % MOVESPERBYTE == 0)
    {
      moveidx = move / MOVESPERBLOCK;
      curbyte = fn->moves[moveidx];
    }

    curmove = curbyte & MOVEMASK;
    switch(curmove)
    {
      case UP:
        printf("u");
        break;
      case DOWN:
        printf("d");
        break;
      case LEFT:
        printf("l");
        break;
      case RIGHT:
        printf("r");
        break;
    }
  }

  printf("\n");
}

void update_state(char *state, int xloc, char move)
{

}
