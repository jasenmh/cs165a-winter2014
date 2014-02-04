import heapq
import math
import sys
import timeit

##### class PriorityQueue #####

class PriorityQueue:
  def __init__(self):
    self._queue = []
    self._index = 0

  def push(self, item, priority):
    heapq.heappush(self._queue, (priority, self._index, item))
    self._index += 1

  def pop(self):
    if self._index == 0:
      return 0
    r = heapq.heappop(self._queue)[-1]
    self._index -= 1
    return r

##### class Anode #####

class Anode:
  def __init__(self):
    self.state = []
    self.dim = 0
    self.f = 0
    self.g = 99999
    self.lastmove = 'x'
    self.parent = 0
    self.next_node = 0

  def SetState(self, initState):
    self.state = initState
    self.dim = int(math.sqrt(len(initState)))

  def ManDistFromGoal(self):
    dist = 0
    for i in range(len(self.state)):
      if self.state[i] != i:
        tmpcell = self.state[i]
        if tmpcell == -1:
          tmpcell = 8
        sr = i / self.dim
        sc = i % self.dim
        dr = tmpcell / self.dim
        dc = tmpcell % self.dim

        dist += int(math.fabs(dc - sc) + math.fabs(dr - sr))

    return dist

  def GenerateMoves(self):
    moves = []
    xcell = self.state.index(-1)
    row = xcell / self.dim
    col = xcell % self.dim

    if row != 0:
      moves += ['u']
    if row != (self.dim - 1):
      moves += ['d']
    if col != 0:
      moves += ['l']
    if col != (self.dim - 1):
      moves += ['r']

    if self.lastmove == 'r' and 'l' in moves:
      moves.remove('l')
    if self.lastmove == 'l' and 'r' in moves:
      moves.remove('r')
    if self.lastmove == 'u' and 'd' in moves:
      moves.remove('d')
    if self.lastmove == 'd' and 'u' in moves:
      moves.remove('u')

    return moves

  def GenerateNextState(self):
    xidx = self.state.index(-1)
    swapidx = -1

    if self.lastmove == 'u':
      swapidx = xidx - self.dim
    elif self.lastmove == 'd':
      swapidx = xidx + self.dim
    elif self.lastmove == 'l':
      swapidx = xidx - 1
    else:
      swapidx = xidx + 1

    tmpcell = self.state[xidx]
    self.state[xidx] = self.state[swapidx]
    self.state[swapidx] = tmpcell

  def PrintMoves(self, terminate):
    if self.lastmove == 'x':  # root node
      return

    self.parent.PrintMoves(False)

    sys.stdout.write(self.lastmove)
    if terminate == True:
      sys.stdout.write('\n')

  def PrintState(self):
    for i in range(0, len(self.state), self.dim):
      #print "%d %d %d" % tuple(self.state[i:i+self.dim])
      print ' '.join(str(e) for e in self.state[i:i+self.dim])

  def ExportState(self):
    s = ''
    a = self.state[:]
    a = map(lambda x : x + 1, a)
    xloc = a.index(0)
    a = map(str, a)
    a[xloc] = 'X'
    for i in range(0, len(a), self.dim):
      #s = s + "%s %s %s\n" % tuple(a[i:i+self.dim])
      s = s + ' '.join(a[i:i+self.dim]) + '\n'

    #s = s[:-1]

    return s

##### Utility functions #####

def readInput():
  tmpState = []
  for line in sys.stdin:
    tmpState += line.split()

  retState = []
  for i in range(len(tmpState)):
    if tmpState[i] == 'X':
      retState.append(-1)
    else:
      retState.append(int(tmpState[i]) - 1)

  return retState

##### Main function #####

def Main():
  found = False
  q = PriorityQueue()

  initState = readInput()
  #printState(initState)

  # start timer
  start_time = timeit.default_timer()

  # wrap init state in a node, set to head, nnode
  nnode = Anode()
  nnode.SetState(initState)
  q.push(nnode, nnode.g)

  # is init state a solution?
  if nnode.ManDistFromGoal() == 0:
    found = True

  # A* loop
  while found == False:

    nnode = q.pop()
    if nnode == 0: # empty list
      break

    # generate valid moves from current state
    moves = nnode.GenerateMoves()

    # explore all moves
    for move in moves:

      # create copy slice of parent state
      childState = nnode.state[:]

      # wrap state and move in child class, set parent, f
      cnode = Anode()
      cnode.SetState(childState)
      cnode.lastmove = move
      cnode.parent = nnode
      cnode.f = nnode.f + 1

      # generate next state based on move
      cnode.GenerateNextState()

      # is new state solution?
      dist = cnode.ManDistFromGoal()
      cnode.g = cnode.f + dist
      if dist == 0:
        found = True
        nnode = cnode
        continue

      # insert new state into list
      q.push(cnode, cnode.g)

  # stop timer
  stop_time = timeit.default_timer()

  # print solution if found
  if found == True:
    nnode.PrintMoves(True)

  # print time
  tot_time = stop_time - start_time
  if tot_time< 1:
    print "%f seconds" % (tot_time)
  else:
    print "%d seconds" % (int(tot_time))

if __name__ == '__main__':
  Main()
