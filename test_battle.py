#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Timer Setup
from func_timeout import func_set_timeout
from random import randint
import random
import time
import func_timeout
import json

# need to use deepcopy for multi-dim list
import copy

# import every team's scoring function here
# from team1 import ... as AI_Score_Red_Side
# from team2 import ... as AI_Score_Yellow_Side
# ...
# after server move forward then modify this

# Global Variables Declaration Here

# red side and yellow side declaration
global_red_side = 0
global_yellow_side = 1

# board connection declaration
# Notice: Because the Board index start from 1, here the connection
#         list, index 0 will leave space.
global_board_connection = [[],
                           [2, 3, 4],
                           [1, 4, 5],
                           [1, 4, 7],
                           [1, 2, 3, 6],
                           [2, 8, 9],
                           [4, 10, 11, 12],
                           [3, 13, 14],
                           [5, 9, 15],
                           [5, 8, 10, 15],
                           [6, 9, 11, 16],
                           [6, 10, 12, 16],
                           [6, 11, 13, 16],
                           [7, 12, 14, 17],
                           [7, 13, 17],
                           [8, 9, 19],
                           [10, 11, 12, 18],
                           [13, 14, 20],
                           [16, 19, 20, 21],
                           [15, 18, 21],
                           [17, 18, 21],
                           [18, 19, 20]]

# chess position declaration
# If the chess got eaten, will turn to 0
global_chess_position = [[1, 2, 3, 4, 5, 7],
                         [15, 17, 18, 19, 20, 21]]

# remain chess number declaration
global_remain_chess = [6, 6]

# trash move number declaration, if this number over 20, then game auto ends for even
global_trash_move = 0

# Save in Json Array
json_array = """{"teamRed": "", "teamYellow": "", "process": [], "totalSteps": 0, "win": ""}"""
array = json.loads(json_array)
process = {"step": 0, "moving": "", "movingBoardIndex": 0, "movingTo": 0, "kill": []}


# Test the variables declare properly
# print ("global red side", global_red_side)
# print ("global yellow side", global_yellow_side)
# print ("global board connection", global_board_connection)
# print ("check board connection for index 0", global_board_connection[0])
# print ("board connection for index 12", global_board_connection[12])
# print ("global chess position", global_chess_position)
# print ("global remain chess", global_remain_chess)


# In[2]:


# Define the functions that later will need
# This block will define the functions students can use
# Because we use Chinese to name those functions in App Inventor,
# need to be careful when transition
# Neighbor function
def Neighbor(pos):
    return global_board_connection[pos]


# Exist_Chess function
def Exist_Chess(pos):
    result = 0
    if pos in global_chess_position[global_red_side]:
        result = global_red_side
    elif pos in global_chess_position[global_yellow_side]:
        result = global_yellow_side
    return result


# Group function
def Group(pos, player, group):
    group.append(pos)
    for neighbor in Neighbor(pos):
        if (neighbor in global_chess_position[player]) and not (neighbor in group):
            for member in Group(neighbor, player, group):
                if not (member in group):
                    group.append(member)
    return group


def fun_Group(pos):
    group = []
    if pos in global_chess_position[global_yellow_side]:
        group = Group(pos, global_yellow_side, group)
    elif global_chess_position[global_red_side]:
        group = Group(pos, global_red_side, group)

    return group


# Get_Group function, this function will check the "pos" chess is
# red side or yellow side or neither of them, then call group
# function next.
def Get_Group(pos):
    group = []
    player = Exist_Chess(pos)
    if player != 0:
        Group(pos, player, group)
    return group


# Alive function
# Notice this function originally not able to let students use, but
# after consideration decide to let student use this function.
# Because we can confirm there is not any same color chesses connected
# with the "group", so just check have space or not.
def Alive(board, group):
    alive = False
    for member in group:
        for neighbor in Neighbor(member):
            if not ((neighbor in board[global_red_side]) or (neighbor in board[global_yellow_side])):
                alive = True
                break
        if alive:
            break
    return alive


def fun_Alive(group):
    return Alive(global_chess_position, group)


# In[3]:


# This block will define the functions students cannot use
# Move_Chess definition
def Move_Chess(player, index, position):
    global global_chess_position
    if (player == global_red_side):
        print('Red side move:', global_chess_position[player][index], 'to', position)
    else:
        print('Yellow side move:', global_chess_position[player][index], 'to', position)
    global_chess_position[player][index] = position
    return


# Chess_Eliminate definition
def Chess_Eliminate(player):
    global global_remain_chess
    global global_chess_position
    global process
    process['kill'] = []
    eliminate = False
    chess_search = [0, 0, 0, 0, 0, 0]
    for i in range(6):
        if global_chess_position[player][i] == 0:
            chess_search[i] = 1
    for chess in global_chess_position[player]:
        if chess != 0 and chess_search[(global_chess_position[player]).index(chess)] == 0:
            group = Group(chess, player, [])
            for member in group:
                chess_search[(global_chess_position[player]).index(member)] = 1
            if not Alive(global_chess_position, group):
                eliminate = True
                global_remain_chess[player] = global_remain_chess[player] - len(group)
                for member in group:
                    global_chess_position[player][(global_chess_position[player]).index(member)] = 0
                    if player == global_red_side:
                        print('Red Side Chess at position', member, 'has got eaten.')
                    else:
                        print('Yellow Side Chess at position', member, 'has got eaten.')
                    process['kill'].append(member)
    return eliminate


# Winner definition
def Winner():
    winner = -1
    if global_remain_chess[global_red_side] < 3:
        winner = global_yellow_side
    elif global_remain_chess[global_yellow_side] < 3:
        winner = global_red_side
    return winner


# Update_Condition definition
def Update_Condition(player, index, position):
    global global_trash_move
    Move_Chess(player, index, position)
    eliminate = False
    if player == global_red_side:
        eliminate = Chess_Eliminate(global_yellow_side)
    else:
        eliminate = Chess_Eliminate(global_red_side)
    if eliminate:
        global_trash_move = 0
    else:
        global_trash_move = global_trash_move + 1
    return


# In[4]:


# This block will define AI_Play and Scoring Functions for both teams
# AI_Score_Red_Side definition

def AI_Score_Red_Side(board):
    score = 0
    red_player = 0
    yellow_player = 1

    C0C1 = None
    C2C3 = None
    C4C5 = None

    for C0C1 in board[yellow_player]:
        if C0C1 != 0:
            for C2C3 in Neighbor(C0C1):
                if Exist_Chess(C2C3) == 0:
                    score = (score + 20)
                elif Exist_Chess(C2C3) == 2:
                    score = (score + 15)
                else:
                    score = (score - 20)
    return score


def AI_Score_Yellow_Side(board):
    score = 0
    red_player = 1
    yellow_player = 0

    C0C1 = None
    C2C3 = None
    C4C5 = None

    for C0C1 in board[yellow_player]:
        if C0C1 != 0:
            for C2C3 in Neighbor(C0C1):
                if Exist_Chess(C2C3) == 0:
                    score = (score + 20)
                elif Exist_Chess(C2C3) == 2:
                    score = (score + 15)
                else:
                    score = (score - 20)
    return score


# AI_Score_Random definition, use for testing, on yellow side, use for test timer too
def AI_Score_Random(board):
    timer = randint(0, 2)
    print('yellow side timer:', timer)
    time.sleep(timer)
    return 100


# AI_Score_SmartRandom definition, use for testing, on red side
def AI_Score_SmartRandom_Red(board):
    score = 0
    player = global_yellow_side  # Opponent Color
    chess_search = [0, 0, 0, 0, 0, 0]
    for i in range(6):
        if board[player][i] == 0:
            chess_search[i] = 1
    for chess in board[player]:
        if chess != 0 and chess_search[(board[player]).index(chess)] == 0:
            group = Group(chess, player, [])
            for member in group:
                chess_search[(board[player]).index(member)] = 1
            if not Alive(board, group):
                score = score + len(group)
                for member in group:
                    board[player][(board[player]).index(member)] = 0
    return score


# AI_Score_SmartRandom definition, use for testing, on yellow side
def AI_Score_SmartRandom_Yellow(board):
    score = 0
    player = global_red_side  # Opponent Color
    chess_search = [0, 0, 0, 0, 0, 0]
    for i in range(6):
        if board[player][i] == 0:
            chess_search[i] = 1
    for chess in board[player]:
        if chess != 0 and chess_search[(board[player]).index(chess)] == 0:
            group = Group(chess, player, [])
            for member in group:
                chess_search[(board[player]).index(member)] = 1
            if not Alive(board, group):
                score = score + len(group)
                for member in group:
                    board[player][(board[player]).index(member)] = 0
    return score


# AI_Play definition
@func_set_timeout(1000)
def AI_Play(player):
    chess_search = []
    chess_index = randint(0, 5)
    best_choice = 0
    move_position = 0
    max_score = -9999
    global process
    global array
    while len(chess_search) < 6:
        if not chess_index in chess_search:
            chess_search.append(chess_index)
            if global_chess_position[player][chess_index] != 0:
                connection = Neighbor(global_chess_position[player][chess_index])
                connection_search = []
                score = 0
                move = connection[randint(0, len(connection) - 1)]
                while len(connection_search) < len(connection):
                    if not move in connection_search:
                        connection_search.append(move)
                        if not ((move in global_chess_position[global_red_side]) or (
                                move in global_chess_position[global_yellow_side])):
                            expected_board = copy.deepcopy(global_chess_position)
                            expected_board[player][chess_index] = move
                            if player == global_red_side:
                                score = AI_Score_Red_Side(expected_board)
                                # score = AI_Score_SmartRandom_Red (expected_board) # Use for test timer
                                # score = Red_Side(expected_board)
                            else:
                                score = AI_Score_Yellow_Side(expected_board)
                                # score = AI_Score_SmartRandom_Yellow(expected_board) # Use for test timer
                                # score = AI_Score_Random(expected_board)
                                # score = Yellow_Side(expected_board)
                            if score > max_score:
                                best_choice = chess_index
                                move_position = move
                                max_score = score
                                # print(best_choice, move_position, max_score)
                    move = connection[randint(0, len(connection) - 1)]
        chess_index = randint(0, 5)
    Update_Condition(player, best_choice, move_position)
    process['step'] = process['step'] + 1
    array['totalSteps'] = array['totalSteps'] + 1
    if player == global_red_side:
        process['moving'] = "Red"
    else:
        process['moving'] = "Yellow"
    process['movingBoardIndex'] = global_chess_position[player][best_choice]
    process['movingTo'] = move_position
    print('Now:', global_chess_position)
    return


# In[5]:


# This block will define main function
def main():
    winner = -1
    now_turn = global_red_side
    global array
    print('Start:', global_chess_position)
    try:
        while winner == -1:
            AI_Play(now_turn)
            winner = Winner()
            if now_turn == global_red_side:
                now_turn = global_yellow_side
            else:
                now_turn = global_red_side
            if global_trash_move == 200:
                print("連續空步已達200步！")
                if global_remain_chess[global_red_side] > global_remain_chess[global_yellow_side]:
                    winner = global_red_side
                    print("紅方剩子較多")
                elif global_remain_chess[global_red_side] < global_remain_chess[global_yellow_side]:
                    winner = global_yellow_side
                    print("黃方剩子較多")
                break

    except func_timeout.exceptions.FunctionTimedOut:
        if now_turn == global_red_side:
            print("紅方超時，判輸")
            winner = global_yellow_side
        else:
            print("黃方超時，判輸")
            winner = global_red_side

    finally:

        if winner == global_red_side:
            print("紅方獲勝！")
            array['win'] = "Red"
        elif winner == global_yellow_side:
            print("黃方獲勝！")
            array['win'] = "Yellow"
        else:
            print("雙方和局")
            array['win'] = "Even"
        json_file = json.dumps(array, indent=4)
        file = open('BattleReport/Report.json', "w")
        file.write(json_file)
        file.close()
    return


main()




