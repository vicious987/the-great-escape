import sys
import math
import enum
import numpy as np

def add_pair(a, b):
    return (a[0] + b[0], a[1] + b[1])

def pair_in_range(p, r):
    return p[0] in range(r) and p[1] in range(r)
UP_WALL, LEFT_WALL = 0
RIGHT_WALL, DOWN_WALL = 8
POTENTIAL_MOVES = [(1,0),(-1,0),(0,1),(0,-1)]
UP =(1,0)
DOWN =(-1,0)
LEFT = (0,-1)
RIGHT = (0,1)

# player data : {x, y,destination, walls left, is playing}
# walls data : {x, y}
class State:

    def __init__(self, pd1, pd2, wd):
        self.player_1_data, self.player_2_data = pd1, pd2
        self.h_walls, self.v_walls = hw, vw


    # (int, int) -> list of pair
    # return list of every unobstructed square pos for given square position




    def passable_directions(cords):
        pm = []
        moved_up, moved_down = add_pair(cords, UP), add_pair(cords, DOWN)
        moved_left, moved_right = add_pair(cords, LEFT), add_pair(cords, RIGHT)

        if not hwall_on(cords) and moved_up[0] in range(9):
            pm.append(UP)
        if not hwall_on(moved_down) and moved_down[0] in range(9):
            pm.append(DOWN)
        if not vwall_on(moved_right) and moved_right[1] in range(9):
            pm.append(RIGHT)
        if not vwall_on(cords) and moved_left[1] in range(9):
            pm.append(LEFT)
        return pm

    def neighbors(cords):
        

    # (int, int), (int, int) -> move
    def move_direction(start_cord, end_cord):
        pass

    # (int,int), finish_line - > int, move_direction
    #calc distance from wall and give the best move
    def shortest_path(self, player_cord, finish_line):

        board = np.array([[100 for i in range(9)] for j in range(9)])
        if finish_line == Edge.left:
            board[:,0] = 0
            for c in range(9):
                for r in range(9):
                    for n in neighbors(r,c):
                        n_x, n_y = n[0], n[1]
                        if board[r][c] + 1 < board[n_x][n_y]:
                            board[n_x][n_y] = board[r][c] + 1
        elif finish_line == Edge.right:
            board[:,8] = 0
            for c in reversed(range(9)):
                for r in range(9):
                    for n in neighbors(r,c):
                        n_x, n_y = n[0], n[1]
                        if board[r][c] + 1 < board[n_x][n_y]:
                            board[n_x][n_y] = board[r][c] + 1
        elif finish_line == Edge.up:
            board[0] = 0
            for r in range(9):
                for c in range(9):
                    for n in neighbors(r,c):
                        n_x, n_y = n[0], n[1]
                        if board[r][c] + 1 < board[n_x][n_y]:
                            board[n_x][n_y] = board[r][c] + 1
        elif finish_line == Edge.down:
            board[8] = 0
            for r in reversed(range(9)):
                for c in range(9):
                    for n in neighbors(r,c):
                        n_x, n_y = n[0], n[1]
                        if board[r][c] + 1 < board[n_x][n_y]:
                            board[n_x][n_y] = board[r][c] + 1

        #min  by score [(board[n[0]][n[1]], n) for n in neighbors(player_cord)]
        #return sc, move_direction(player_cord, move_cord)




""" less code, not checked 
        board_range = range(9)
        if finish_line == Edge.right or finish_line == Edge.down:
            board_range = reversed(board_range)
        for c in board_range:
            for r in range(9):
                if finish_line == Edge.down or finish_line == Edge.up:
                    r, c = c, r
                    for n in neighbors(r,c):
                        n_x, n_y = n[0], n[1]
                        if reachable((r,c),n) and board[r][c] + 1 < board[n_x][n_y]:
                            board[n_x][n_y] = board[r][c] + 1
                else:
                    for n in neighbors(r,c):
                        n_x, n_y = n[0], n[1]
                        if reachable((r,c),n) and board[r][c] + 1 < board[n_x][n_y]:
                            board[n_x][n_y] = board[r][c] + 1
"""




# w: width of the board
# h: height of the board
# player_count: number of players (2 or 3)
# my_id: id of my player (0 = 1st player, 1 = 2nd player, ...)
w, h, player_count, my_id = [int(i) for i in input().split()]

# game loop
while True:
    for i in range(player_count):
        # x: x-coordinate of the player
        # y: y-coordinate of the player
        # walls_left: number of walls available for the player
        x, y, walls_left = [int(j) for j in input().split()]
    wall_count = int(input())  # number of walls on the board
    for i in range(wall_count):
        # wall_x: x-coordinate of the wall
        # wall_y: y-coordinate of the wall
        # wall_orientation: wall orientation ('H' or 'V')
        wall_x, wall_y, wall_orientation = input().split()
        wall_x = int(wall_x)
        wall_y = int(wall_y)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)


    # action: LEFT, RIGHT, UP, DOWN or "putX putY putOrientation" to place a wall
    print("RIGHT")
