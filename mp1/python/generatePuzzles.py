import random
from puzzle import Anode

MAXDIM = 5
MAXMOVES = 4
MAXITERS = 1

griddim = 4
while griddim < MAXDIM:

  movecnt = 3
  while movecnt < MAXMOVES:

    iters = 0
    while iters < MAXITERS:
      
      state = range(griddim*griddim)
      state[(griddim*griddim)-1] = -1
      nn = Anode()
      nn.SetState(state)
      i = 0
      sol = []

      while i < movecnt:

        moves = nn.GenerateMoves()

        if len(moves) == 0:
          continue
        move = random.choice(moves)
        nn.lastmove = move
        sol.append(move)
        nn.GenerateNextState()
        i += 1

      gfile = open("test-sz%d-mv%d-%d.txt" % (griddim, i, iters), "w")
      sfile = open("solu-sz%d-mv%d-%d.txt" % (griddim, i, iters), "w")
      gfile.write(nn.ExportState())
      sfile.write(''.join(sol))
      gfile.close()
      sfile.close()
      iters += 1

    #movecnt = movecnt * 2
    movecnt += 1

  griddim += 2

print "Done."
