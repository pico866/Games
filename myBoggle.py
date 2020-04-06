#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Boggle game
#  
import threading
import time #for timer
import os #for exit
import random
from collections import defaultdict
#for nltk you need to install nltk (pip install --upgrade nltk)
import nltk
nltk.download('words')
from nltk.corpus import words
dictionary = words.words()

class myTrie(object):
	def __init__(self):
		self.children = defaultdict(myTrie)
		self.complete = False
		
	def add(self,s):
		if not s:
			self.complete = True
		else:
			self.children[s[0]].add(s[1:])
	
	def search(self,s,prefix=False):
		if not s:
			return prefix or self.complete
		else:
			if s[0] in self.children:
				return self.children[s[0]].search(s[1:],prefix)
			else:
				return False

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

	def setGrid(self):
		self.grid = [['N','N','O','E'],
                     ['E','S','M','A'],
                     ['E','A','C','R'],
                     ['D','O','T','A']]

dir = [(-1,-1),(0,-1),(1,-1),
	   (-1,0),	      (1,0),
	   (-1,1), (0,1), (1,1)]

def checkWord(grid,node,word):
    #print ("check if word is in grid: %s and also in the trie" % (word))
    if not word:
        return False

    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if dfs(grid,node,r,c,[],word,"",0) == True:
                #print("dfs returned True so exit now!!")
                return True
    return False

def dfs(grid,node,r,c,visited,word,currentStr,idx):
    
    if (r,c) in visited:
        return False
    letter = grid[r][c].lower()
    visited.append((r,c))
    if node.children[letter] is not None:
        #print("in the trie... %s"%(letter))
        if  idx>=0 and idx < len(word) and word[idx] == letter:
            currentStr = currentStr + letter
            #print("==dfs curStr=%s len=%d word=%s idx=%d letter=%s node.complete=%r" % (currentStr,len(currentStr),word,idx,letter,node.complete))
            if currentStr == word and node.complete == True:
                #print("returning true currentStr=%s complete=%r" % (currentStr,node.complete))
                return True
            for dr, dc in dir:
                nr, nc = r + dr, c + dc
                if isValid(grid,nr,nc):
                    if dfs(grid,node.children[letter],nr,nc,visited,word,currentStr,idx+1) == True:
                        return True
    if len(currentStr) > 0:#for backtrack reason
        idx = idx -1
        l = list(currentStr)#convert string to list to remove last char then change back to string
        l.pop() #remove last element in the list
        currentStr = "".join(l)#convert list to string
        visited.pop()

def isValid(grid,r,c):
    #print("r=%d c=%d" % (r,c))
    return r >= 0 and c >= 0 and r < len(grid) and c < len(grid[r])

totalScores = 0
wordSet = set([])
def printScore():
    print ("Current Score is %d" % (totalScores))
    print ("Current Words: %s" % (wordSet))
def printTotalScore():
    print ("\n=== Game is Over ===\nTotal Score is %d " % (totalScores))
    print ("Total Words: %s" % (wordSet))

def finish():
    printTotalScore()
    os._exit(0)

def main():
    print("--- Boggle Game ---")
    root = myTrie()
    
    for w in dictionary:
        root.add(w)
    
    board = myBoard()
    board.shuffle()
    #board.setGrid()#for test only
 
    global totalScores
    global wordSet

    threading.Timer(120, finish).start() #2 min timer
    
    while True:
        board.display()
        guessWord = input("Enter your word (to quit enter '1'):  ")
        if guessWord == '1':
            break
        print ("You entered %s",guessWord)
        #Test to see if guessWord is in Trie
        #if root.search(guessWord) == True:
        #    print("Fond in Trie")
        if checkWord(board.getGrid(),root,guessWord) == True:
            print("Fond your word!!")
            if guessWord in wordSet:
                print("Error: %s is a duplicate!" % (guessWord))
            else:
                wordSet.add(guessWord)
                totalScores = totalScores + len(guessWord)
            printScore()
        else:
            print("Error: Not valid word... Try again")
        
    printTotalScore()
      
if __name__ == "__main__":
    main()