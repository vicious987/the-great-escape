#!python3
#pylint: disable=invalid-name, missing-docstring, trailing-whitespace, line-too-long, too-many-instance-attributes, too-few-public-methods, too-many-branches, pointless-string-statement,  unused-import, no-else-return
import sys
import math
from enum import Enum
from copy import copy
from operator import itemgetter
import numpy as np
# WHOLE MINMAX DEAL

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

def add_pair(a, b):
    return (a[0] + b[0], a[1] + b[1])

def diff_pair(a, b):
    return (a[0] - b[0], a[1] - b[1])

def pair_in_range(p, r):
    return p[0] in range(r) and p[1] in range(r)

def dir_to_str(cord):
    if cord == (-1, 0):
        return "UP"
    if cord == (1, 0):
        return "DOWN"
    if cord == (0, -1):
        return "LEFT"
    if cord == (0, 1):
        return "RIGHT"
    return "NOT A CORD"


# player data : {x, y,destination, walls left, is playing}
# walls data : {x, y}
class Finish_line(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

class State:
    def __init__(self, my_data, enemy_data, hw, vw):
        self.my_cord = my_data['cord']
        self.my_finish_line = my_data['finish_line']
        self.my_walls_left = my_data['walls_left']

        self.enemy_cord = enemy_data['cord']
        self.enemy_finish_line = enemy_data['finish_line']
        self.enemy_walls_left = enemy_data['walls_left']

        self.hwalls = hw
        self.vwalls = vw

    def update(self, my_data, enemy_data, hw, vw):
        self.my_cord = my_data['cord']
        self.my_walls_left = my_data['walls_left']

        self.enemy_cord = enemy_data['cord']
        self.enemy_walls_left = enemy_data['walls_left']

        self.hwalls = hw
        self.vwalls = vw

    #returns list of directions that move to into valid squares
    def valid_directions(self, cords):
        pm = []
        moved_up, moved_down = add_pair(cords, UP), add_pair(cords, DOWN)
        moved_left, moved_right = add_pair(cords, LEFT), add_pair(cords, RIGHT)

        if cords not in self.hwalls and moved_up[0] in range(9):
            pm.append(UP)
        if moved_down not in self.hwalls and moved_down[0] in range(9):
            pm.append(DOWN)
        if moved_right not in self.vwalls and moved_right[1] in range(9):
            pm.append(RIGHT)
        if cords not in self.vwalls and moved_left[1] in range(9):
            pm.append(LEFT)
        return pm

    #(int,int) -> list of (int,int)
    def neighbors(self, cords):
        return [add_pair(cords, d) for d in self.valid_directions(cords)]
        
    # (int,int), finish_line - > int, move_direction
    #calc distance from wall and give the best move
    def distance_from_fl(self, cord, vw_lst, hw_lst, finish_line):
        board = np.array([[100 for i in range(9)] for j in range(9)])
        if finish_line == Finish_line.LEFT:
            board[:, 0] = 0
            for c in range(9):
                for r in range(9):
                    for n in self.neighbors((r, c)):
                        n_x, n_y = n[0], n[1]
                        if board[r][c] + 1 < board[n_x][n_y]:
                            board[n_x][n_y] = board[r][c] + 1
        elif finish_line == Finish_line.RIGHT:
            board[:, 8] = 0
            for c in reversed(range(9)):
                for r in range(9):
                    for n in self.neighbors((r, c)):
                        n_x, n_y = n[0], n[1]
                        if board[r][c] + 1 < board[n_x][n_y]:
                            board[n_x][n_y] = board[r][c] + 1
        elif finish_line == Finish_line.UP:
            board[0] = 0
            for r in range(9):
                for c in range(9): 
                    for n in self.neighbors((r, c)):
                        n_x, n_y = n[0], n[1]
                        if board[r][c] + 1 < board[n_x][n_y]:
                            board[n_x][n_y] = board[r][c] + 1
        elif finish_line == Finish_line.DOWN:
            board[8] = 0
            for r in reversed(range(9)):
                for c in range(9):
                    for n in self.neighbors((r, c)):
                        n_x, n_y = n[0], n[1]
                        if board[r][c] + 1 < board[n_x][n_y]:
                            board[n_x][n_y] = board[r][c] + 1

        best_neighbor = min([(board[x[0]][x[1]], x) for x in self.neighbors(cord)], key=itemgetter(0))
        best_move = diff_pair(best_neighbor, cord)
        return board[cord[0]][cord[1]], best_move 

    #checks if wall can be placed in given cordinates
    # char, (int, int) -> bool
    def is_valid_wall(self, wall_type, wall_cords):
        wallp1 = wall_cords
        if wall_type == 'v':
            wallp2 = add_pair(wall_cords, DOWN)
            check_list = self.vwalls
        if wall_type == 'h':
            wallp2 = add_pair(wall_cords, RIGHT)
            check_list = self.hwalls 
        return pair_in_range(wallp1, 9) and pair_in_range(wallp2, 9) and wallp1 not in check_list and wallp2 not in check_list 

    
    #return list of valid walls adjecent to given cords
    def get_valid_walls(self, cord, wall_type):
        if wall_type == 'v':
            dir_ver = LEFT 
            dir_hor = DOWN
        elif wall_type == 'h':
            dir_ver = RIGHT
            dir_hor = UP
        pw = [cord, add_pair(cord, dir_hor), add_pair(cord, dir_ver), add_pair(cord, add_pair(dir_ver, dir_hor))]
        return [x for x in pw if self.is_valid_wall(wall_type, x)]

    #list of scores on cords with given walls
    # -> pair of list of (int, (int,int))
    def get_score_wall_list(self, cord, finline):
        v_list, h_list = [], []
        for wall in self.get_valid_walls(cord, 'v'):
            temp_vwalls = copy(self.vwalls)
            temp_vwalls.append(wall)
            v_list.append((self.distance_from_fl(cord, temp_vwalls, self.hwalls, finline), wall))
        for wall in self.get_valid_walls(cord, 'h'):
            temp_hwalls = copy(self.vwalls)
            temp_hwalls.append(wall)
            h_list.append((self.distance_from_fl(cord, self.vwalls, temp_hwalls, finline), wall))
        return v_list, h_list


    def choose_best_wall(self):
        verticals, horizontals = self.get_score_wall_list(self.enemy_cord, self.enemy_finish_line)
        best_ver, best_hor = max(verticals, key=itemgetter(0)), max(horizontals, key=itemgetter(0))
        if best_ver > best_hor:
            return ('v', best_ver[0], best_ver[1])
        else:
            return ('h', best_hor[0], best_hor[1])
        #if if there is no good wall, choose move on optimal path

    def make_move(self):
        my_dist, best_move = self.distance_from_fl(self.my_cord, self.hwalls, self.vwalls, self.my_finish_line) #me
        enemy_dist = self.distance_from_fl(self.enemy_cord, self.hwalls, self.vwalls, self.enemy_finish_line)[0] #enemy
        if my_dist < enemy_dist:
            return f"{dir_to_str(best_move)}"
        else:
            wall_type, _, wall_cord = self.choose_best_wall()
            w_x, w_y = wall_cord
            return f"{w_x} {w_y} {wall_type}"



""" less code, not checked 
    def finline_distance(self, player_cord, finish_line):
        board = np.array([[100 for i in range(9)] for j in range(9)])
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
