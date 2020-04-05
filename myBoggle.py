#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Boggle game
#  

from collections import defaultdict
#import nltk
#nltk.download('words')

class myTrie(object):
	def __init__(self):
		self.children = defaultdict(myTrie)
		self.complete = False
		
	def add(self,s):
		if not s:
			self.complete = True
		else:
			self.children[s[0]].add(s[1:])
	
	def check(self,s,prefix=False):
		if not s:
			return prefix or self.complete
		else:
			if s[0] in self.children:
				return self.children[s[0]].check(s[1:],prefix)
			else:
				return False

import random

class myBoard(object):
	def __init__(self):
		self.row = 4
		self.col = 4
		self.grid = []
		#Used international configuration for 16 diece (French version: https://fr.wikipedia.org/wiki/Boggle )
		self.config = [
		['E','T','U','K','N','O'],
		['E','V','G','T','I','N'],
		['D','E','C','A','M','P'],
		['I','E','L','R','U','W'],
		['E','H','I','F','S','E'],
		['R','E','C','A','L','S'], 
		['E','N','T','D','O','S'],
		['O','F','X','R','I','A'],
		['N','A','V','E','D','Z'],
		['E','I','O','A','T','A'],
		['G','L','E','N','Y','U'],
		['B','M','A','Q','J','O'],
		['T','L','I','B','R','A'],
		['S','P','U','L','T','E'],
		['A','I','M','S','O','R'],
		['E','N','H','R','I','S']]
		
	def shuffle(self):
		randrow = random.sample(range(15),4)
		for r in range(0,self.row):
			self.grid.append([])
			randcol = random.sample(range(5),4)
			for c in range(0,self.col):
				#print ("randrow[%d]=%d" % (r,randrow[r]))
				randletter = self.config[randrow[r]][randcol[c]]
				self.grid[r].append(randletter)
	
	def display(self):
		from pprint import pprint #to print row by row
		pprint(self.grid)
		
	def getGrid(self):
		return self.grid



import time #for timer
import sys #for kill
from nltk.corpus import words
dictionary = words.words()

totalScores = 0

def printScore():
    print ("Time is over!!\n\nTotal Score is %d " % (totalScores))

def main():
    print("--- Boggle Game ---")
    root = myTrie()
    
    for w in dictionary:
        root.add(w)
    
    board = myBoard()
    board.shuffle()
    board.display()

    import time
    timeout = time.time() + 20   # sec
    while time.time() < timeout:
        guessWord = input("Enter your word:  ")
        print ("You entered %s",guessWord)
        if guessWord in dictionary:
            print("BINGO!!")
        else:
            print("NOT!!!")

    printScore()
      
if __name__ == "__main__":
    main()