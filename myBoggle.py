#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Boggle game
#  

from collections import defaultdict


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

import time #for timer
import sys #for kill

totalScores = 0

def printScore():
    print ("Time is over!!\n\nTotal Score is %d " % (totalScores))

def main():
    print("--- Boggle Game ---")
    root = myTrie()
    dictionary = ["test","hat","hit","bee"]
    for w in dictionary:
        root.add(w)
   
    import time
    timeout = time.time() + 10   # sec
    while time.time() < timeout:
        guessWord = input("Enter your word")
        print ("You entered %s",guessWord)
