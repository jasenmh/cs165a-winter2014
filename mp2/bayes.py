import string
import sys
import math

VERBOSE = True
WEIGHTWORDS = True
DIGITCOUNT = True

##### class ClassModel #####

class ClassModel:
  def __init__(self):
    self.wordList = {}
    self.wordTotal = 0
    self.spamWords = 0
    self.hamWords = 0
    self.smsTotal = 0
    self.smsSpam = 0
    self.smsHam = 0
    self.pSpam = 0.0
    self.pHam = 0.0
    self.spamDigits = 0 # avg num digits in spam messages
    self.hamDigits = 0 # avg num digits in ham messages

  def wordInClass(self, word, c):
    #self.wordTotal += 1

    # add word to list if new
    if word not in self.wordList:
      self.wordTotal += 1
      wi = WordInfo()
      self.wordList[word] = wi

    # increment classification
    if c == 'ham':
      self.wordList[word].incrementHam()
      self.incrHamWords()
    else:
      self.wordList[word].incrementSpam()
      self.incrHamWords()

  def incrSmsSpam(self):
    self.smsTotal += 1
    self.smsSpam += 1

  def incrSmsHam(self):
    self.smsTotal += 1
    self.smsHam += 1

  def incrSpamWords(self):
    self.spamWords += 1

  def incrHamWords(self):
    self.hamWords += 1

  def probWord(self, word):
    # if word is not in training data, return 1s which will not affect P()
    if word not in self.wordList:
      #return (1, 1)
      return (0, 0) # adding logs, not multiplying Ps

    fspam = float(self.wordList[word].inSpam)
    fham = float(self.wordList[word].inHam)

    printf "%f / %f, %f : %f / %f, %f" % (0, 0, 0, 0, 0, 0)
#(fspam + 1, self.spamWords + self.wordTotal, math.log((fspam + 1) / (self.spamWords + self.wordTotal)), fham + 1, self.hamWords + self.wordTotal, math.log((fham + 1) / (self.hamWords + self.wordTotal))

    return ( math.log((fspam + 1) / (self.spamWords + self.wordTotal)), math.log((fham + 1) / (self.hamWords + self.wordTotal)) ) # smoothed, guard against 0s
    #return ( fspam/self.spamWords, fham/self.hamWords )
    #return ( fspam/self.smsSpam, fham/self.smsHam )

  def trainModel(self, trainList):
    count = 0

    # count occurrences of words in each class
    for line in trainList:
      count = (count + 1) % 100
      if VERBOSE and count == 0:
        sys.stdout.write(".")
      words = line.split()
      smsClass = words[0]
      wordList = words[1:]

      if smsClass == 'ham':
        self.incrSmsHam()
      else:
        self.incrSmsSpam()

      for word in wordList:
        self.wordInClass(word, smsClass)

      # count digits in message
      messList = list(line)
      messList = filter(lambda x: x in '1234567890', messList)
      digits = len(messList)
      if smsClass == 'ham':
        self.hamDigits += 1
      else:
        self.spamDigits += 1

    # calculate p(C=ci)
    self.pSpam = float(self.smsSpam) / self.smsTotal
    self.pHam = float(self.smsHam) / self.smsTotal

    # calc digit averages
    self.hamDigits = float(self.hamDigits) / self.smsHam
    self.spamDigits = float(self.spamDigits) / self.smsSpam

  def classify(self, classList, withCheck):
    classedSms = 0
    correctSms = 0
    pf = open("predictions.txt", "w")
    count = 0
    # classify each SMS and write class to file
    for sms in classList:
      count = (count + 1) % 100
      if VERBOSE and count == 0:
        sys.stdout.write(".")
      classedSms += 1
      words = sms.split()
      if withCheck:
        knownClass = words[0]
        predClass = self.classifySms(words[1:])
        if knownClass == predClass:
          correctSms += 1
      else:
        predClass = self.classifySms(words)

      pf.write("%s\n" % (predClass))

    pf.close()
    acc = float(correctSms) / classedSms

    return acc

  def classifySms(self, smsList):
    #probs = [1.0, 1.0]  # spam, ham
    probs = [0.0, 0.0] # adding log(P), start at 0

    for word in smsList:
      wProbs = self.probWord(word)
      if wProbs[0] != 0:
        probs[0] += wProbs[0]
      if wProbs[1] != 0:
        probs[1] += wProbs[1]

    print "words: %f %f" % (probs[0], probs[1])

    # consider digit in message
    messList = list("".join(smsList))
    messList = filter(lambda x: x in '1234567890', messList)
    digits = len(messList)
    if digits > 0:
      probs[0] += self.spamDigits
      probs[1] += self.hamDigits
      print "digits: %f %f" % (probs[0], probs[1])

    probs[0] += self.pSpam
    probs[1] += self.pHam
    print "class: %f %f" % (probs[0], probs[1])

    if probs[0] > probs[1]:
      return 'spam'
    else:
      return 'ham'

##### class WordInfo #####

class WordInfo:
  def __init__(self):
    self.inSpam = 0
    self.inHam = 0

  def incrementSpam(self):
    self.inSpam += 1

  def incrementHam(self):
    self.inHam += 1

##### Utility functions #####

table = string.maketrans("", "")

def removePunctuation(s):
  return s.translate(table, string.punctuation)

def readDataFromFile(fn):
  inFile = open(fn, "r")
  count = 0
  inList = []

  for line in inFile:
    count = (count + 1) % 100
    if VERBOSE and count == 0:
      sys.stdout.write(".")

    if len(line) > 3:
      inList += [ removePunctuation(line) ]

  return inList

##### Main function #####

def Main():

  # correct arguments?
  if len(sys.argv) < 3:
    print "Usage: %s <train file> <test file>" % sys.argv[0]
    exit()

  # setup files
  trainFile = sys.argv[1]
  testFile = sys.argv[2]

  # using test files generated by me?
  checkAcc = False
  if len(sys.argv) > 3:
    if sys.argv[3] == '-t': # using my test files with labels, check accuracy
      checkAcc = True
    else:
      checkAcc = False

  # read in the training data
  if VERBOSE:
    sys.stdout.write("Reading training file %s" % (trainFile))
  trainList = readDataFromFile(trainFile)
  if VERBOSE:
    print ".\nRead %d training messages" % (len(trainList))

  cm = ClassModel()

  # train the model
  if VERBOSE:
    sys.stdout.write("Training model")
  cm.trainModel(trainList)
  if VERBOSE:
    print "."

  # read in the test data
  if VERBOSE:
    sys.stdout.write("Reading test file %s" % (testFile))
  testList = readDataFromFile(testFile)
  if VERBOSE:
    print ".\nRead %d test messages" % (len(testList))

  # test data classification
  if VERBOSE:
    sys.stdout.write("Classifying SMS")
  accuracy = cm.classify(testList, checkAcc)
  if VERBOSE:
    print "."

  # report accuracy
  if VERBOSE:
    print "Classification accuracy: %f" % accuracy


if __name__ == '__main__':
  Main()
