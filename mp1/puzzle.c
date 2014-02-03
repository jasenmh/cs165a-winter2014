#include <math.h>
#include "puzzle.h"

int nodenum = 0;

int main(int argc, char *argv[])
{
  fringenode *head = NULL;
  fringenode *tmpnode;
  fringenode *nnode;
  int dim;
  int dimsqr;
  time_t start_time, end_time;
  int *istate = NULL;
  int found = 0;
  char *moves;
  int dist;
  int i;

  // read input state
  dim = read_state_from_stdin(&istate);
  if(dim == 0)
  {
    printf("Error: invalid input\n");
    return 0;
  }

if(PDEBUG) { printf("*after read\n"); print_state(istate, dim); printf("\n"); }

  // initialize head and state dimension
  dimsqr = dim * dim;
  head = create_node(istate, dim);
  nnode = head;

  moves = (char *)malloc(4 * sizeof(char));

  // time it!
  start_time = time(NULL);

  // is initial state a solution?
  dist = h_man_dist(nnode->state, dim);
  if(dist == 0)
  {
if(PDEBUG) printf("- init state is goal state\n");
    found = 1;
  }

  // A* for the solution
  while(!found)
  {
    if(head == NULL)  // empty list
    {
if(PDEBUG) printf("- head of list is empty at start\n");
      break;
    }

    nnode = head;
    // get possible moves from current state
    get_moves(moves, nnode, dim);

    // explore all moves
    i = 0;
    while(i < 4 && moves[i] != 'x')
    {
if(nodenum > 10) exit(0);
      // copy parent state to istate
      memcpy(istate, nnode->state, dimsqr * sizeof(int));

      // generate child state
      update_state(istate, moves[i], dim);

      // create child node and link with parent (prev_node)
      tmpnode = create_node(istate, dim);
      tmpnode->prev_node = nnode;
      tmpnode->f = nnode->f + 1;
      nnode->childs += 1;
if(PDEBUG) printf("- parent now has %d childs\n", nnode->childs);
if(PDEBUG) { printf("*in while child create\n"); print_state(tmpnode->state, dim); }

      // generate dist and goal check
      dist = h_man_dist(istate, dim);
      tmpnode->g = tmpnode->f + dist;
      if(dist == 0)
      {
        found = 1;
        continue;
      }

      // insert child into list (next_node)
      insert_node(tmpnode, &head);
if(PDEBUG) print_list_order(head, 2);

      ++i;
    }

  }

  end_time = time(NULL);

  if(found)
  {
    print_moves(nnode, 1);
  }
  printf("%d seconds\n", end_time - start_time);

  return 0;
}

/*
 * create a new node using an initial state
 */
fringenode *create_node(int *istate, int dim)
{
  int dimsqr = dim * dim;
  fringenode *nnode;

  nnode = (fringenode *)malloc(sizeof(fringenode));
  nnode->state = (int *)malloc(dimsqr * sizeof(int));
  memcpy(nnode->state, istate, dimsqr * sizeof(int));

  nnode->next_node = NULL;
  nnode->prev_node = NULL;
  nnode->f = 0;
  nnode->g = dimsqr;  // an arbitrary big number
  nnode->childs = 0;
  nnode->lastmove = 'x';  // x in initial state

nnode->nodenum = nodenum++;

  return nnode;
}

/*
 * fill the passed in state buffer with the initial state
 */
int read_state_from_stdin(int **state)
{
  int readdim = MAXDIM * 10;
  int instate[MAXDIM * MAXDIM];
  char userin[readdim];
  char *nexttok;
  int ldim = 0;
  int done = 0;
  int *lstate;

  while(!done)
  {
    if(fgets(userin, readdim, stdin) == NULL) // EOF
    {
      done = 1;
      continue;
    }

    userin[strlen(userin) - 1] = '\0';  // trim for strcmp

    nexttok = strtok(userin, " ");
    while(nexttok != NULL)
    {
      if(strcmp(nexttok, "X") != 0)
        // decrement number so it matches state index
        instate[ldim++] = atoi(nexttok) - 1;
      else
        instate[ldim++] = -1;

      nexttok = strtok(NULL, " ");
    }
  }

if(PDEBUG) printf("read: %d, dim: %d\n", ldim,
(int)sqrt(ldim));

  lstate = (int *)malloc(sizeof(int) * ldim);
  memcpy(lstate, instate, sizeof(int) * ldim);
  *state = lstate;

if(PDEBUG) printf(" state: %s, dim: %d\n",
(state == NULL) ? "NULL" : "NOT NULL", (int)sqrt(ldim));

  return (int)sqrt(ldim);
}

/*
 * recurisvely print out moves needed to get to node
 */
void print_moves(fringenode *fn, int terminal)
{
  if(fn->prev_node != NULL)
  {
    print_moves(fn->prev_node, 0);
  }

  if(fn->lastmove != 'x') // don't print init state move
    printf("%c", fn->lastmove);

  if(terminal)
    printf("\n");

}

/*
 * print an nxn grid of the state
 */
void print_state(int *state, int dim)
{
  int i;
  int dimsqr = dim * dim;

  for(i = 0; i < dimsqr; ++i)
  {
    if(state[i] == -1)
      printf("X ");
    else
      printf("%d ", state[i] + 1);

    if((i + 1) % 3 == 0)
      printf("\n");
  }

}

/*
 * change the state based on the given move
 */
void update_state(int *state, char move, int dim)
{
  int tmpidx, tmpcell, xcell;

  // find location of empty space (-1)
  xcell = 0;
  while(state[xcell] != -1)
    ++xcell;

  // find cell to switch
  switch(move)
  {
    case 'u':
      tmpidx = xcell - dim;
      break;
    case 'd':
      tmpidx = xcell + dim;
      break;
    case 'l':
      tmpidx = xcell - 1;
      break;
    case 'r':
      tmpidx = xcell + 1;
      break;
    default:
      printf("Error: unknown move in update_state\n");
  }

  // switch cells
  tmpcell = state[tmpidx];
  state[tmpidx] = state[xcell];
  state[xcell] = tmpcell;

}

/*
 * Manhatten distance heuristic function
 */
int h_man_dist(int *state, int dim)
{
  int dist = 0;
  int sr, sc, dr, dc; // source/dest row/col
  int tmpcell;
  int i;
  int dimsqr = dim * dim;

  for(i = 0; i < dimsqr; ++i)
  {
    if(i != state[i]) // cell out of place, get distance
    {
      tmpcell = state[i];
      if(tmpcell == -1)
        tmpcell = 8;

      sr = i / dim;
      sc = i % dim;
      dr = tmpcell / dim;
      dc = tmpcell % dim;

      if((dc = dc - sc) < 0)
        dc = dc * -1;
      if((dr = dr - sr) < 0)
        dr = dr * -1;
      
      dist += (dc + dr);
    }
  }

  return dist;
}

/*
 * determine all legal moves of node's state
 */
void get_moves(char *moves, fringenode *fn, int dim)
{
  int row, col, i;
/*
  for(i = 0; i < 4; ++i)
  {
    moves[i] = 'x';
  }
*/
  for(row = 0; row < 4; ++row)
  {
    for(col = 0; col < 4; ++col)
    {
      i = (row * dim) + col;
      if(fn->state[i] == -1)
        break;
    }

    if(fn->state[i] == -1)
      break;
  }

  i = 0;
  if(row != 0 && fn->lastmove != 'd')
  {
    moves[i++] = 'u';
if(PDEBUG) printf("- get_moves adding 'u'\n");
  }
  if(row != dim - 1 && fn->lastmove != 'u')
  {
    moves[i++] = 'd';
if(PDEBUG) printf("- get_moves adding 'd'\n");
  }
  if(col != 0 && fn->lastmove != 'r')
  {
    moves[i++] = 'l';
if(PDEBUG) printf("- get_moves adding 'l'\n");
  }
  if(col != dim - 1 && fn->lastmove != 'l')
  {
    moves[i++] = 'r';
if(PDEBUG) printf("- get_moves adding 'r'\n");
  }

  if(i < 4)
    moves[i] = 'x';

}

/* 
 * insert n node starting at h based on g value
 */
void insert_node(fringenode *n, fringenode **h)
{
  fringenode *tn; // test (next) node
  fringenode *cn = *h; // current node
int testcnt = 0;
if(PDEBUG) printf("-insert_node inserting node %d\n", n->nodenum);

  if(n->g < (*h)->g) // new node is better than head node
  {
    n->next_node = *h;
    *h = n;

if(PDEBUG) printf("-insert_node: new(%d) better than head(%d)\n",n->g,(*h)->g);
    return;
  }

  while(cn->next_node != NULL)
  {
testcnt++;
    tn = cn->next_node;
    if(n->g < tn->g)  // place new node before next node
      n->next_node = tn;
      tn->next_node = n;

if(PDEBUG) printf("-insert_node: new(%d) better than %d(%d)\n",n->g,testcnt,cn->g);
      return;
  }

  // place new node at the end
if(PDEBUG) printf("-insert_node: inserting at end\n");
  cn->next_node = n;

}

void print_list_order(fringenode *h, int count)
{
  int i = 0;
  fringenode *cn = h;

  printf("-list order: ");
  while(i < count && cn != NULL)
  {
    printf("%d ", cn->nodenum);
    cn = cn->next_node;
  }

  printf("\n");
}
