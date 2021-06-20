import numpy as np
from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
from puzzleDetect import *
from cam import *
from treeSearch import *
from mlModel import Model
import os

puzzle = get_puzzle_info()
puzzle, solution = A_search(Puzzle(8), puzzle)

PATH = 'puzzle.txt'
s = str(puzzle) + '\n' + str(solution)

with open(PATH, mode='w') as f:
	f.write(s)

# not recommened but works
os.system('python3 showSolution.py')