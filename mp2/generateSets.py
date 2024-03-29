import sys
import random

if len(sys.argv) < 2:
  print "Usage: %s <percent to training> [percent spam to training]" % sys.argv[0]
  exit()

trainRatio = float(sys.argv[1]) / 100.0

if len(sys.argv) > 2:
  spamTrainRatio = float(sys.argv[2]) / 100.0
else:
  spamTrainRatio = 0.0  # split at same rate as trainRatio

tf = open("trainsms.txt", "w")
cf = open("classifysms.txt", "w")
random.seed()
count = 0

for line in sys.stdin:

  count = (count + 1) % 100
  if count == 0:
    sys.stdout.write(".")

  if len(line) < 3:
    continue

  words = line.split()

  if words[0] == "ham" or spamTrainRatio == 0:
    if random.random() < trainRatio:
      tf.write(line+"\n")
    else:
      wordLine = " ".join(words[1:])
      cf.write(wordLine+"\n")
      #cf.write(line+"\n")
  else: # sms is spam and we have a spamTrainRatio
    if random.random() < spamTrainRatio:
      tf.write(line+"\n")
    else:
      wordLine = " ".join(words[1:])
      cf.write(wordLine+"\n")
      #cf.write(line+"\n")

tf.close()
cf.close()

print "\nDone."
