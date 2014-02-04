import random
from puzzle import Anode

MAXDIM = 13
MAXMOVES = 21
MAXITERS = 5

griddim = 3
while griddim < MAXDIM:

#  print "Grid size %d" % (griddim)
  movecnt = 5
  while movecnt < MAXMOVES:

#    print " Move count %d" % (movecnt)
    iters = 0
    while iters < MAXITERS:
#      print "  Iteration %d" % (iters)
      state = range(griddim*griddim)
      state[(griddim*griddim)-1] = -1
      nn = Anode()
      nn.SetState(state)
      i = 0
      sol = []

      while i < movecnt:
#        nn.PrintState()
        moves = nn.GenerateMoves()

#        print "Valid moves: %s" % (''.join(moves))

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

    movecnt = movecnt * 2

  griddim += 2

print "Done."
