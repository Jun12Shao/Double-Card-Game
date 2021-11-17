# -*- coding:utf-8 -*-

"""
@author: Jun
@file: .py
@time: 2/21/20194:21 PM
"""


import numpy as np
import time
from decimal import Decimal

# Visualize the initial stage of the game
def Visulization(s):
    # Inputs: current stage of the game: s.
    # Actions: print out the stage (a 12*8 maatrix)
    table = np.zeros((13, 9), dtype='<U12')
    for i in range(12):
        table[i][0] = str(12 - i)
        for j in range(8):
            table[i][j + 1] = cells[s[i][j][0]]
    table[12][1:] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    # assume that your data rows are tuples
    template = "|{0:2}|{1:4}|{2:4}|{3:4}|{4:4}|{5:4}|{6:4}|{7:4}|{8:4}|"  # column widths: 2,3,3,3,3,3,3,3,3

    print('———————————————————————')
    for line in table:
        print(template.format(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8]))
        print('———————————————————————')
    return

def Rule_checker(s,p1,p2,step,r):
    # Inputs: current state s, command, step
    # Check the legibility of command. If illegible raise error.
    if not r:                                       # Move legibility check
        # Check legability of the move
        if p2[0]<0 or p2[1]>8:
            raise Exception("Illegible move. P2 Overbound!")
        if s[p1][0] != 0 or s[p2][0] != 0:          # Automatically check the legality of each move.
            raise Exception("Illegible move. Overlap existing positions!")
        if (p1[0] + 1 < 12 and s[p1[0] + 1, p1[1]][0] == 0) or (p2[1] - p1[1] == 1 and p2[0] + 1 < 12 and s[p2[0] + 1, p2[1]][0] == 0):
            raise Exception("Illegible move. Hanging over the empty cell!")
        return True

    else:                                           # Remove legibility check
        # Check legability of remove
        if p1 == p2 or p2[1] - p1[1] < 0 or p2[0] - p1[0] > 0:
            raise Exception("Wrong remove segments information.")
        if s[p1][1] == step - 1 or s[p2][1] == step - 1:
            raise Exception("Wrong remove. The card was placed just by the other player.")

        # segments retrieved should be from one card.
        if s[p1][1] != s[p2][1]:
            raise Exception("Wrong positions of removing card. Two segments are not from the same card.")

        # There must be a card in the desired position.
        if s[p1][0] == 0 or s[p2][0] == 0:
            raise Exception("There is no card in the desired position.")

        # after retrieving, the stage shopuld be legable.
        if p1[0] - p2[0] == 0:  # card removed is horizontal.
            if p1[0] > 0 and (
                    s[p1[0] - 1, p1[1]][0] != 0 or s[p2[0] - 1, p2[1]][0] != 0):  # there is a card above p1 0r p2
                raise Exception("Illegible remove. There are cards hanging above!")
        else:  # card removed is vertical.
            if p2[0] > 0 and s[p2[0] - 1, p2[1]][0] != 0:  # there is a card above p2
                raise Exception("Illegible remove. There are cards hanging above!")
        return True

def Move(s, m,step):
    # Inputs: Move indication m, current stage s.   Structure of m: [action,p1,p2]
    # Move a card to desired location
    # Returns: new stage after an action.
    a = m[0]  # get desired action of move, 1~8
    s[m[1]]= [A[a][0],step]
    s[m[2]] = [A[a][1],step]
    # Visulization(s)
    return s


def Remove(s, rm):
    # Inputs: Remove indication rm, current stage s. Structure of rm: [position 1, position 2]
    # Remove a card from a desired location
    # Returns: new stage after an action.
    s[rm[0]] = [0,0]
    s[rm[1]] = [0,0]
    return s

def Rev_translation(m):
    # translate the action of machine to human command

    if len(m)==3:
        p1=m[1]
        p2=m[2]
        new_m = str(0) + ' ' + str(m[0]) + ' ' + number2col[p1[1]] + ' ' + str(12 - p1[0])
    elif len(m)==5:
        p1 = m[0]
        p2 = m[1]
        p3 = m[3]
        p4=m[4]
        new_m = number2col[p1[1]] + ' ' + str(12 - p1[0]) + ' ' + number2col[p2[1]] + ' ' + str(12 - p2[0]) + ' ' + str(
            m[2]) + ' ' + number2col[p3[1]] + ' ' + str(12 - p3[0])
    return new_m

def Human_input(r=0):
    rm=[]
    if not r:
        command = input("Please input next move:")
        command = command.split()
        if len(command) != 4 or command[0] != '0':
            raise Exception("Wrong format of command: "
                            "The lenght of letters/numbers should be 4 and separared by space. "
                            "The first number should be 0"
                            "the second number(action) should be between 1 and 8"
                            "Such as: 0 5 A 2 or 0 8 A 11")
        else:
            a = dic_a[command[1]]
            c1 = dic_col[command[2]]
            r1 = dic_row[command[3]]
            p1 = (r1, c1)  # get the position in game board for the base point of our card.
            r2 = r1 + D[a % 2][0]
            c2 = c1 + D[a % 2][1]
            p2 = (r2, c2)  # get the position in game board for next segment of our card.
            m = [a, p1, p2]
    else:
        command = input("Please input next recycling move:")
        command = command.split()

        if len(command) != 7:
            raise Exception("Wrong format of command: "
                            "The lenght of letters/numbers should be 7 and separared by space. "
                            "the fifth number(action) should be between 1 and 8"
                            "Such as: F 2 F 3 3 A 2")
        c1 = dic_col[command[0]]
        r1 = dic_row[command[1]]
        p1 = (r1, c1)

        c2 = dic_col[command[2]]
        r2 = dic_row[command[3]]
        p2 = (r2, c2)

        a = dic_a[command[4]]
        c3 = dic_col[command[5]]
        r3 = dic_row[command[6]]
        p3 = (r3, c3)  # get the position in game board for the base point of our card.

        r4 = r3 + D[a % 2][0]
        c4 = c3 + D[a % 2][1]
        p4 = (r4, c4)  # get the position in game board for next segment of our card.
        rm = [p1, p2]
        m = [a, p3, p4]

    return rm,m

def get_winner(scores,step,c):
    k = 1
    if (c == 1 and step % 2 == 1) or (c == 0 and step % 2 == 0):
        for n in range(len(scores)):
            if (scores[n][0] == 4 or scores[n][1] == 4):
                winner='color'
                k = 0
                break
        if k:
            winner = 'dot'
    else:
        for n in range(len(scores)):
            if (scores[n][2] == 4 or scores[n][3] == 4):
                winner = 'dot'
                k = 0
                break
        if k:
            winner = 'color'
    return winner


def Calculate_scores(cell, score):
    # used to check four-consecutive-segment.
    if cell == 0:   # No empty space is allowed.
        score = [0, 0, 0, 0]
    elif cell == 1:
        score[0] += 1
        score[1] = 0
        score[2] += 1
        score[3] = 0
    elif cell == 2:
        score[0] += 1
        score[1] = 0
        score[2] = 0
        score[3] += 1
    elif cell == 3:
        score[0] = 0
        score[1] += 1
        score[2] += 1
        score[3] = 0
    elif cell == 4:
        score[0] = 0
        score[1] += 1
        score[2] = 0
        score[3] += 1
    return score

def Calculate_scores2(cell, score):
    # Used to check three-consecutive-segment or two-consecutive-segment
    if cell == 0:       # Empty space is allowed.
        score = score
    elif cell == 1:
        score[0] += 1
        score[1] = 0
        score[2] += 1
        score[3] = 0
    elif cell == 2:
        score[0] += 1
        score[1] = 0
        score[2] = 0
        score[3] += 1
    elif cell == 3:
        score[0] = 0
        score[1] += 1
        score[2] += 1
        score[3] = 0
    elif cell == 4:
        score[0] = 0
        score[1] += 1
        score[2] = 0
        score[3] += 1
    return score

def Terminal_checker(s,last_mv):
    # Inputs: Current stage s and last move .
    # Check if the stage is the terminal
    # Return the scoring boards
    terminal=0
    scores = []

    # check if there are four connections due to adding of p1 and p2.
    if len(last_mv)==5:
        # s_new=np.copy(s)
        # s_new=Remove(s_new,[last_mv[0],last_mv[1]])
        m=last_mv[3:]
    elif len(last_mv)==3:
        # s_new=s
        m=last_mv
    elif len(last_mv)==0:
        return terminal,scores


    for p in m[1:]:
        # Check the horizontal direction and see if there is a winner
        score = [0, 0, 0, 0]  # store the number of consecutive colors and dots [red,whites,dots,circles]
        r=p[0]
        for c in range(p[1]-3,p[1]+4,1):
            if c>=0 and c<8:
                cell = s[r][c][0]
                score=Calculate_scores(cell, score)
                if max(score) >= 4:
                    scores.append(score)
                    terminal=1
                    break

        # Check the vertical direction and see if there is a winner
        score = [0, 0, 0, 0]  # store the number of consecutive colors and dots [red,whites,dots,circles]
        c = p[1]
        for r in range(p[0], p[0] + 4, 1):
            if r < 12:
                cell = s[r][c][0]
                score = Calculate_scores(cell, score)
                if max(score) >= 4:
                    scores.append(score)
                    terminal=1
                    break

        # Check the left  diagonal(\) and see if there is a winner
        score = [0, 0, 0, 0]  # store the number of consecutive colors and dots [red,whites,dots,circles]
        r=p[0]
        c = p[1]
        for i in range(-3, 4, 1):
            r0=r+i
            c0=c+i
            if (r0>=0 and r0<12) and (c0>=0 and c0<8):
                cell = s[r0][c0][0]
                score = Calculate_scores(cell, score)
                if max(score) >= 4:
                    scores.append(score)
                    terminal=1
                    break

        # Check the right diagonal(/) and see if there is a winner
        score = [0, 0, 0, 0]  # store the number of consecutive colors and dots [red,whites,dots,circles]
        r = p[0]
        c = p[1]
        for i in range(-3, 4, 1):
            r0 = r - i
            c0 = c + i
            if (r0 >= 0 and r0 < 12) and (c0 >= 0 and c0 < 8):
                cell = s[r0][c0][0]
                score = Calculate_scores(cell, score)
                if max(score) >= 4:
                    scores.append(score)
                    terminal=1
                    break
    return terminal,scores

def Is_In(v_node,vs):
    belong=False
    for x in vs:
        i = 0
        if len(v_node)==len(x):
            for m in v_node:
                if m  in x:
                    i=1
                else:
                    i = 0
                    break
        if i:
            belong=True
            break
    return belong


def horizontal_detect(s,r,c,step,score_board):
    # calculate consecutive colors and dots
    score = [0, 0, 0, 0]  # store the number of consecutive colors and dots [red,whites,dots,circles]
    for k in range(3,-1,-1):
        if c-k<8:
            cell = s[r][c-k][0]
            score = Calculate_scores2(cell, score)
    for i in range(4):
        if score[i] == 2:  # it is possible for this line to combine 4 consecutive colors or dots
            score_board[i][0] += 1/2
        if score[i] == 3:
            score_board[i][1] += 1/2

    score = [0, 0, 0, 0]  # store the number of consecutive colors and dots [red,whites,dots,circles]
    for k in range(2, -2, -1):
        if c - k < 8:
            cell = s[r][c - k][0]
            score = Calculate_scores2(cell, score)
    for i in range(4):
        if score[i] == 2:  # it is possible for this line to combine 4 consecutive colors or dots
            score_board[i][0] += 1/2
        if score[i] == 3 :
            score_board[i][1] += 1/2

    score = [0, 0, 0, 0]  # store the number of consecutive colors and dots [red,whites,dots,circles]
    for k in range(3, -1, -1):
        if c + k < 8:
            cell = s[r][c + k][0]
            score = Calculate_scores2(cell, score)
    for i in range(4):
        if score[i] == 2:  # it is possible for this line to combine 4 consecutive colors or dots
            score_board[i][0] += 1/2
        if score[i] == 3:
            score_board[i][1] += 1/2

    score = [0, 0, 0, 0]  # store the number of consecutive colors and dots [red,whites,dots,circles]
    for k in range(2, -2, -1):
        if c + k < 8:
            cell = s[r][c + k][0]
            score = Calculate_scores2(cell, score)
    for i in range(4):
        if score[i] == 2:  # it is possible for this line to combine 4 consecutive colors or dots
            score_board[i][0] += 1/2
        if score[i] == 3:
            score_board[i][1] += 1/2
    return score_board

def vertical_detect(s,r,c,step,score_board):
    # calculate consecutive colors and dots
    score = [0, 0, 0, 0]  # store the number of consecutive colors and dots [red,whites,dots,circles]

    for r1 in range(r+4,r, -1):
        if r1 < 12:
            cell = s[r1][c][0]
            score = Calculate_scores2(cell, score)
            if (step > 24, r1 == r + 2 and s[r][c][1] != step - 1) or r1 == r+1:
                for i in range(4):
                    if score[i] == 2 and r >= 1:
                        score_board[i][0] += 1
                    if score[i] == 3 and r >= 0:
                        score_board[i][1] += 1

    return score_board

def left_diag_detect(s,r,c,step,score_board):
    # Check the left diagonal(/) and see if there is a winner
    score = [0, 0, 0, 0]  # store the number of consecutive colors and dots [red,whites,dots,circles]
    for k in range(3, 0, -1):
        r0 = r + k
        c0 = c - k
        if  r0 < 12 and c0 >= 0:
            cell = s[r0][c0][0]
            score = Calculate_scores2(cell, score)
    for i in range(4):
        if score[i] == 2:  # it is possible for this line to combine 4 consecutive colors or dots
            score_board[i][0] += 1
        if score[i] == 3:
            score_board[i][1] += 1

    return  score_board

def right_diag_detect(s,r,c,step,score_board):
    # Check the right diagonal(\) and see if there is a winner
    score = [0, 0, 0, 0]  # store the number of consecutive colors and dots [red,whites,dots,circles]
    for k in range(3, 0, -1):
        r0 = r + k
        c0 = c + k
        if  r0 < 12 and c0 < 8:
            cell = s[r0][c0][0]
            score = Calculate_scores2(cell, score)
            for i in range(4):
                if score[i] == 2:  # it is possible for this line to combine 4 consecutive colors or dots
                    score_board[i][0] += 1
                if score[i] == 3:
                    score_board[i][1] += 1

    return  score_board

def get_children(s,step,r=1,rm=[]):
    # Input： state of the game s ϵ S, depth of the game
    # Return : list of next states and last_move after a legal move
    # Notation: algorithm for forward moving and recycling moving is different
    s_next=[]

    if step<=24 or r==0:
        for c in range(8):
            for r in range(12):
                if s[r][c][0] ==0:
                    if r==11 or (r<=10 and s[r+1][c][0] != 0):
                        p1=(r,c)
                        for a in range(1,9):        # 8 kinds of cards
                            r2 = r + D[a % 2][0]
                            c2 = c + D[a % 2][1]
                            p2 = (r2, c2)           # get the position in game board for next segment of our card.
                            if len(rm)!=2 or p1!=rm[0] or p2!=rm[1]:
                                try:
                                    result=Rule_checker(s, p1, p2, step, r=0)
                                except:
                                    result=False
                                if result == True:
                                    if step<=24:
                                        m=[a,p1,p2]
                                    else:
                                        m=[rm[0],rm[1],a,p1,p2]
                                    s_next.append(m)

    elif step<=40 and r:                       # Remove cards from board
        visit_card=[step-1]
        for c in range(8):
            for r in range(12):
                if s[r][c][0] !=0:
                    if r==0 or s[r-1][c][0]==0:
                        card_number=s[r][c][1]
                        if card_number not in visit_card:
                            if r<11 and  s[r+1][c][1] == card_number:
                                p1=(r+1,c)
                                p2=(r,c)
                            if c<7 and s[r][c+1][1] == card_number:
                                p1=(r,c)
                                p2=(r,c+1)
                            # if c>0 and s[r][c-1][1] == card_number:
                            #     p1=(r,c-1)
                            #     p2=(r,c)
                            try:
                                result=Rule_checker(s, p1, p2, step, r=1)
                            except:
                                result=False
                            if result:
                                visit_card.append(card_number)
                                rm=[p1,p2]
                                s_rm=np.copy(s)
                                s_rm =Remove(s_rm,rm)
                                s_next+=get_children(s_rm,step,0,rm)

    return s_next

def get_children2(s, step, r=1, rm=[]):
    # Input： state of the game s ϵ S, depth of the game
    # Return : list of next states and last_move after a legal move
    # Notation: algorithm for forward moving and recycling moving is different
    s_next = []

    if step <= 24 or r == 0:
        for c in range(8):
            for r in range(12):
                if s[r][c][0] == 0:
                    if r == 11 or (r <= 10 and s[r + 1][c][0] != 0):
                        p1 = (r, c)
                        for a in range(1, 9):  # 8 kinds of cards
                            r2 = r + D[a % 2][0]
                            c2 = c + D[a % 2][1]
                            p2 = (r2, c2)  # get the position in game board for next segment of our card.
                            if len(rm) != 2 or p1 != rm[0] or p2 != rm[1]:
                                try:
                                    result = Rule_checker(s, p1, p2, step, r=0)
                                except:
                                    result = False
                                if result == True:
                                    if step <= 24:
                                        m = [a, p1, p2]
                                    else:
                                        m = [rm[0], rm[1], a, p1, p2]
                                    s_next.append([m,0,[]])


    elif step <= 40 and r:  # Remove cards from board
        visit_card = [step - 1]
        for c in range(8):
            for r in range(12):
                if s[r][c][0] != 0:
                    if r == 0 or s[r - 1][c][0] == 0:
                        card_number = s[r][c][1]
                        if card_number not in visit_card:
                            if r < 11 and s[r + 1][c][1] == card_number:
                                p1 = (r + 1, c)
                                p2 = (r, c)
                            if c < 7 and s[r][c + 1][1] == card_number:
                                p1=(r,c)
                                p2 = (r, c + 1)
                            # if c > 0 and s[r][c - 1][1] == card_number:
                            #     p1 = (r, c - 1)
                            #     p2 = (r, c)
                            try:
                                result = Rule_checker(s, p1, p2, step, r=1)
                            except:
                                result = False
                            if result:
                                visit_card.append(card_number)
                                rm = [p1, p2]
                                s_rm = np.copy(s)
                                s_rm = Remove(s_rm, rm)
                                s_next += get_children(s_rm, step, 0, rm)

    return s_next

def naive_heu(s,step):
    # Inputs: Current stage s, the border of the area covered by cards.
    # Calculate the heuristic function value.
    # Return the heuristic function value.
    #
    #  h(n) = "sum the coordinates of each white O"
    #"+ 3*(sum the coordinates of each white dot)"
    #"- 2*(sum the coordinates of each red dot)"
    #"- 1.5*(sum the coordinates of each red O)"

    # check each row and calculate the score
    score= [0,0, 0, 0, 0]  # store the number of cell  ['', 'r/d', 'r/o', 'w/d', 'w/o']

    for r in range(11,- 1, -1):
        for c in range(8):
            cell=s[r][c][0]
            score[cell]+=(11-r)*10+c
    return score[4]+3*score[3]-2*score[1]-1.5*score[2]


def h1(s,step):
    # h1 win over h2
    # Inputs: state of the game s ϵ S
    # without rule.
    # Search surface cells and calculate the number of three-continual colors, two continual colors and three-continual dots and two-continual dots
    # v(three-colors)=1; v(two-colors)=0.2;v(three-dots)=-1; v(two-dots)=-0.2;
    # h(s)=nb(three-colors)+0.2*nb(two-colors)-nb(three-dots)-0.2*nb(two-dots)
    # Reurn: heuristic function value of a state.

    score_board=np.zeros((4,2))
    # Initiate score board of size 4*2 with zero. [(nb_2reds,nb_3reds),(nb_2whites,nb_3whites),(nb_2dots,nb_3dots),(nb_2cricles,nb_3circles)]
    surface=np.array([[12,0],[12,1],[12,2],[12,3],[12,4],[12,5],[12,6],[12,7]])
    # if step<=24:
    # search vertically
    for c in range(8):
        for r in range(12):
            if s[r][c][0]!=0:                    # s[r][c] is the surface
                surface[c]=np.array([r,c])
                if r ==0 or s[r- 1][c][0] == 0: # and s[r-1][c] is empty
                # calculate consecutive colors and dots
                    score = [0, 0, 0, 0]  # store the number of consecutive colors and dots [red,whites,dots,circles]
                    for r1 in range(r + 3, r - 1, -1):
                        if r1 < 12:
                            cell = s[r1][c][0]
                            score = Calculate_scores2(cell, score)
                            if (step>24,r1==r+1 and s[r][c][1]!=step-1) or r1==r:
                                for i in range(4):
                                    if score[i] == 2 and r1 >= 2:  # it is possible for this line to combine 4 consecutive colors or dots
                                        score_board[i][0] += 1
                                    if score[i] == 3 and r1 >= 1:
                                        score_board[i][1] += 1

                    # Check the right  diagonal(\)
                    score = [0, 0, 0,0]  # store the number of consecutive colors and dots [red,whites,dots,circles]
                    for k in range(2, -3, -1):
                        r0 = r +k
                        c0 = c +k
                        if (r0 >= 0 and r0 < 12) and (c0 >= 0 and c0 < 8):
                            cell = s[r0][c0][0]
                            score = Calculate_scores2(cell, score)
                            if r0-1>0and c0-1 >0 and cell!=0 and s[r0-1][c0-1][0]==0 and k<=0:
                                for i in range(4):
                                    if score[i] == 2:  # it is possible for this line to combine 4 consecutive colors or dots
                                        score_board[i][0] += 1
                                    if score[i] == 3 :
                                        score_board[i][1] += 1

                    # Check the left diagonal(/) and see if there is a winner
                    score = [0, 0, 0, 0]  # store the number of consecutive colors and dots [red,whites,dots,circles]
                    for k in range(2, -3, 1):
                        r0 = r + k
                        c0 = c - k
                        if (r0 >= 0 and r0 < 12) and (c0 >= 0 and c0 < 8):
                            cell = s[r0][c0][0]
                            score = Calculate_scores2(cell, score)
                            if r0 -1 >= 0 and c0 +1 <8 and cell != 0 and s[r0 - 1][c0 + 1][0] == 0 and k<=0:
                                for i in range(4):
                                    if score[i] == 2:  # it is possible for this line to combine 4 consecutive colors or dots
                                        score_board[i][0] += 1
                                    if score[i] == 3:
                                        score_board[i][1] += 1
    # Check horizontally
    score = [0, 0, 0, 0]    # store the number of consecutive colors and dots [red,whites,dots,circles]
    for c in range(7):
        r1=surface[c][0]
        r2=surface[c+1][0]
        if r1<r2:
            if c > 0:
                for i in range(r1,r2):
                    if i<10 :
                        score_board = left_diag_detect(s, i, c+1, step, score_board)
                    score_board=horizontal_detect(s, i, c+1, step, score_board)
        elif r1>r2:
            if c < 6:
                for i in range(r1-1,r2,-1):
                    if i<10 :
                        score_board = right_diag_detect(s, i, c, step, score_board)
                    score_board=horizontal_detect(s, i, c, step, score_board)


    h=5*(score_board[0][1]+score_board[1][1])+0.2*(score_board[0][0]+score_board[1][0])-10*(score_board[2][1]+score_board[3][1])-0.2*(score_board[2][0]+score_board[3][0])

    h_min = 0
    if step > 24 and step <= 40:
        # zhaochu bianhua
        visit_card = [step - 1]
        for c in range(8):
            score_board2 = np.zeros((4, 2))
            r = surface[c][0]
            if r < 12:
                card_number = s[r][c][1]
                if card_number not in visit_card:
                    if r < 11 and s[r + 1][c][1] == card_number:  # vertical card
                        p1 = (r + 1, c)
                        p2 = (r, c)
                        v = 1
                    if c < 7 and s[r][c + 1][1] == card_number:  # horizontal card
                        p1 = (r, c)
                        p2 = (r, c + 1)
                        v = 0
                    try:
                        result = Rule_checker(s, p1, p2, step, r=1)
                    except:
                        result = False
                    if result:
                        visit_card.append(card_number)
                        rm = [p1, p2]
                        t = -1
                        for p in rm:
                            t += 1
                            # calculate consecutive colors and dots
                            score = [0, 0, 0,
                                     0]  # store the number of consecutive colors and dots [red,whites,dots,circles]
                            r0 = p[0]
                            c0 = p[1]
                            if v == 0 or t == 1:  # Check the vertical direction
                                for r1 in range(r0 + 3, r0, -1):
                                    if r1 < 12:
                                        cell = s[r1][c][0]
                                        score = Calculate_scores2(cell, score)
                                for i in range(4):
                                    if score[
                                        i] == 2 and r1 >= 2:  # it is possible for this line to combine 4 consecutive colors or dots
                                        score_board2[i][0] += 1
                                    if score[i] == 3 and r1 >= 1:
                                        score_board2[i][1] += 1

                            # Check the right  diagonal(\)
                            score = [0, 0, 0,0]  # store the number of consecutive colors and dots [red,whites,dots,circles]
                            for k in range(3, 0, -1):
                                r1 = r0 + k
                                c1 = c0 + k
                                if (r1 >= 0 and r1 < 12) and (c1 >= 0 and c1 < 8):
                                    cell = s[r1][c1][0]
                                    score = Calculate_scores2(cell, score)
                            for i in range(4):
                                if score[
                                    i] == 2:  # it is possible for this line to combine 4 consecutive colors or dots
                                    score_board2[i][0] += 1
                                if score[i] == 3:
                                    score_board2[i][1] += 1

                            # Check the left diagonal(/)
                            score = [0, 0, 0,
                                     0]  # store the number of consecutive colors and dots [red,whites,dots,circles]
                            for k in range(3, 0, 1):
                                r1 = r0 + k
                                c1 = c0 - k
                                if (r1 >= 0 and r1 < 12) and (c1 >= 0 and c1 < 8):
                                    cell = s[r1][c1][0]
                                    score = Calculate_scores2(cell, score)
                            for i in range(4):
                                if score[
                                    i] == 2:  # it is possible for this line to combine 4 consecutive colors or dots
                                    score_board[i][0] += 1
                                if score[i] == 3:
                                    score_board[i][1] += 1

                            # Check the horizontal direction
                            score = [0, 0, 0, 0]
                            if v == 0:
                                if t == 0:
                                    for i in range(3, 0, -1):
                                        c1 = c0 - i
                                        if c1 > 0:
                                            cell = s[r0][c1][0]
                                            score = Calculate_scores2(cell, score)
                                elif t == 1:
                                    for i in range(3, 0, -1):
                                        c1 = c0 - i
                                        if c1 > 0:
                                            cell = s[r0][c1][0]
                                            score = Calculate_scores2(cell, score)

                            elif v == 1:
                                score1 = np.array([0, 0, 0,
                                                   0])  # store the number of consecutive colors and dots [red,whites,dots,circles]
                                score2 = np.array([0, 0, 0,
                                                   0])  # store the number of consecutive colors and dots [red,whites,dots,circles]
                                for i in range(3, 0, -1):
                                    c1 = c0 - i
                                    if c1 > 0:
                                        cell = s[r][c1][0]
                                        score1 = Calculate_scores2(cell, score1)
                                for i in range(-3, 0, 1):
                                    c1 = c0 - i
                                    if c1 < 8:
                                        cell = s[r][c1][0]
                                        score2 = Calculate_scores2(cell, score2)
                                score = score1 + score2
                            for i in range(4):
                                if score[
                                    i] == 2:  # it is possible for this line to combine 4 consecutive colors or dots
                                    score_board2[i][0] += 1
                                if score[i] == 3:
                                    score_board2[i][1] += 1
                        h2 = 5 * (score_board2[0][1] + score_board2[1][1]) + 0.2 * (
                                score_board2[0][0] + score_board2[1][0]) - 10 * (
                                     score_board2[2][1] + score_board2[3][1]) - 0.2 * (
                                     score_board2[2][0] + score_board2[3][0])
                        if h2 < h_min:
                            h_min = h2
    return h + h_min




def h1_2(s,step):
    # Inputs: state of the game s ϵ S
    # Reurn: heuristic function value of a state.
    score_board = np.zeros((4, 2), dtype=int)
    c=0
    while c<8:
        go=False
        for r in range(11,-1,-1):
            if s[r][c][0]==0:
                score_board =vertical_detect(s,r,c,step,score_board)
                go=True
                break
        while go:
            if c+1>7: break
            if s[r][c+1][0]==0:                   # if can go to the right
                c+=1
                score_board=left_diag_detect(s,r,c,step,score_board)
                # if  c+1<8 and s[r][c+1][0]!=0:
                #     score_board=horizontal_detect(s,r,c,step,score_board,left=0)
                # if r+1<12 and c+1<8 and s[r+1][c+1][0]!=0:
                #     score_board =right_diag_detect(s,r,c,step,score_board)
                for r1 in range(r+1,12):                # if can go down
                    if s[r1][c][0] == 0:
                        score_board = horizontal_detect(s, r1, c, step, score_board)
                        score_board = left_diag_detect(s, r1,c, step, score_board)
                        # if  r1+1<12 and c+1<8 and s[r1+1][c+1][0]!=0:
                        #     score_board = right_diag_detect(s, r1, c, step, score_board)
                    else:
                        r=r1-1
                        score_board = vertical_detect(s, r,c, step, score_board)
                        break
                # score_board = left_diag_detect(s, r,0, step, score_board)
            else:
                if r-1>0:
                    r=r-1
                    score_board = horizontal_detect(s, r, c, step, score_board)
                    score_board = right_diag_detect(s, r, c, step, score_board)
                else:
                    break
        c=c+1
    h = (score_board[0][1] + score_board[1][1]) + 0.2 * (score_board[0][0] + score_board[1][0]) - (
            score_board[2][1] + score_board[3][1]) - 0.2 * (score_board[2][0] + score_board[3][0])
    return h

def h2(s, step, last_move):
    # calcaulate the relative change of heuristic value caused by last_move
    if len(last_move)==0:
        return 0
    score_board = np.zeros((4, 2))

    # check if there are four connections due to adding of p1 and p2.
    if len(last_move) == 5:
        rm= last_move[:2]
        m = last_move[2:]

        # calculate the change caused by removing
        # for p in last_move[:2]:

    elif len(last_move) == 3:
        m = last_move


    for p in m[1:]:
        # Check the vertical direction and see the change
        score = [0, 0, 0, 0]  # store the number of consecutive colors and dots [red,whites,dots,circles]
        c = p[1]
        if m[0]%2==1:

            for r in range(p[0]+3, p[0]-1, -1):
                if r < 12:
                    cell = s[r][c][0]
                    score = Calculate_scores2(cell, score)
                    if r==p[0]+1:
                        for i in range(4):
                            if score[i] == 2:  # it is possible for this line to combine 4 consecutive colors or dots
                                score_board[i][0] -= 1
                            if score[i] == 3:
                                score_board[i][1] -= 1
                    if r==p[0]:
                        for i in range(4):
                            if score[i] == 2:  # it is possible for this line to combine 4 consecutive colors or dots
                                score_board[i][0] += 1
                            if score[i] == 3:
                                score_board[i][1] += 1
        elif  p==m[2]:
            for r in range(p[0] + 4, p[0] - 1, -1):
                if r < 12:
                    cell = s[r][c][0]
                    score = Calculate_scores2(cell, score)
                    if r == p[0] + 2:
                        for i in range(4):
                            if score[i] == 2:  # it is possible for this line to combine 4 consecutive colors or dots
                                score_board[i][0] -= 1
                            if score[i] == 3:
                                score_board[i][1] -= 1
                    if r==p[0]:
                        for i in range(4):
                            if score[i] == 2:  # it is possible for this line to combine 4 consecutive colors or dots
                                score_board[i][0] += 1
                            if score[i] == 3:
                                score_board[i][1] += 1

        # Check the right diagonal(\) and see the change
        score1 = np.array([0, 0, 0, 0])  # store the number of consecutive colors and dots [red,whites,dots,circles]
        score2 = np.array([0, 0, 0, 0])  # store the number of consecutive colors and dots [red,whites,dots,circles]
        r = p[0]
        c = p[1]
        empt=0
        for i in range(3, 0, -1):
            r0 = r + i
            c0 = c + i
            if r0 < 12 and  c0 < 8:
                cell = s[r0][c0][0]
                if cell==0:
                    empt+=1
                else:
                    score1 = Calculate_scores2(cell, score1)
        for i in range(-3, 0, 1):
            r0 = r + i
            c0 = c + i
            if r0 >= 0 and c0 >= 0:
                cell = s[r0][c0][0]
                if cell == 0:
                    empt += 1
                else:
                    score2 = Calculate_scores2(cell, score2)
        score=score = score1+score2
        for i in range(4):
            if score[i] == 2:  # it is possible for this line to combine 4 consecutive colors or dots
                score_board[i][0] -= 1
            if score[i] >= 3:
                score_board[i][1] -= 1
        cell = s[r][c][0]
        score = Calculate_scores2(cell, score)

        for i in range(4):
            if score[i] == 2 and empt>1:  # it is possible for this line to combine 4 consecutive colors or dots
                score_board[i][0] += 1
            if score[i] >= 3 and empt>0 :
                score_board[i][1] += 1


        # Check the left diagonal(/) and see if there is a winner
        score1 = np.array([0, 0, 0, 0]) # store the number of consecutive colors and dots [red,whites,dots,circles]
        score2 = np.array([0, 0, 0, 0])  # store the number of consecutive colors and dots [red,whites,dots,circles]
        r = p[0]
        c = p[1]
        empt = 0
        for i in range(3, 0, -1):
            r0 = r + i
            c0 = c - i
            if r0 < 12 and c0 >0:
                cell = s[r0][c0][0]
                if cell == 0:
                    empt += 1
                else:
                    score1 = Calculate_scores2(cell, score1)
        for i in range(-3, 0, 1):
            r0 = r + i
            c0 = c - i
            if r0 >= 0 and c0<8:
                cell = s[r0][c0][0]
                if cell == 0:
                    empt += 1
                else:
                    score2 = Calculate_scores2(cell, score2)
        score = score1+score2
        for i in range(4):
            if score[i] == 2:  # it is possible for this line to combine 4 consecutive colors or dots
                score_board[i][0] -= 1
            if score[i] >= 3:
                score_board[i][1] -= 1
        cell = s[r][c][0]
        score = Calculate_scores2(cell, score)

        for i in range(4):
            if score[i] == 2 and empt > 1:  # it is possible for this line to combine 4 consecutive colors or dots
                score_board[i][0] += 1
            if score[i] >= 3 and empt > 0:
                score_board[i][1] += 1

        # Check the horizontal direction and see the change of consecutive cards
        score1 = np.array([0, 0, 0, 0])  # store the number of consecutive colors and dots [red,whites,dots,circles]
        score2 = np.array([0, 0, 0, 0])  # store the number of consecutive colors and dots [red,whites,dots,circles]
        r = p[0]
        c = p[1]
        empt = 0
        for i in range(3, 0, -1):
            c0 = c - i
            if  c0 > 0:
                cell = s[r][c0][0]
                if cell == 0:
                    empt += 1
                else:
                    score1 = Calculate_scores2(cell, score1)
        for i in range(-3, 0, 1):
            c0 = c - i
            if c0 < 8:
                cell = s[r][c0][0]
                if cell == 0:
                    empt += 1
                else:
                    score2 = Calculate_scores2(cell, score2)
        score = score1+score2
        for i in range(4):
            if score[i] == 2:  # it is possible for this line to combine 4 consecutive colors or dots
                score_board[i][0] -= 1
            if score[i] >= 3:
                score_board[i][1] -= 1
        cell = s[r][c][0]
        score = Calculate_scores2(cell, score)

        for i in range(4):
            if score[i] == 2 and empt > 1:  # it is possible for this line to combine 4 consecutive colors or dots
                score_board[i][0] += 1
            if score[i] >= 3 and empt > 0:
                score_board[i][1] += 1

    h = 5 * (score_board[0][1] + score_board[1][1]) + 0.2 * (score_board[0][0] + score_board[1][0]) - 10 * (
            score_board[2][1] + score_board[3][1]) - 0.2 * (score_board[2][0] + score_board[3][0])
    return  h


# Minimax + alpha-beata pruning search with heuristic
def Minimax_ab(s,depth,alpha,beta,maximizingPlayer,step,ab,trace,h,color,last_move=[]):
    # Inputs: state of the game s ϵ S, depth of the algorithm, alpha,beta and indicator for whose turn
    # Inputs: step,last_move, heuristic function and max_color
    # Actions: according to current stage, find out the 'optimal' action (position + placement)
    # Return: action to next step

    offspring = []
    terminal,scores=Terminal_checker(s,last_move)

    if depth == 0 or terminal or step>40:
        optimal_nodes=[last_move]
        if terminal:
            winner=get_winner(scores,step,color)
            if winner=='color':
                v=1e6
            else:
                v=-1e6
        else:
            v=h(s,step)
        return v,optimal_nodes,offspring

    children = get_children(s,step)                     # Data structure of children: [m1,m2,,,,mn]. m: next_move [a,p1,p2] or [p1,p2,a, p3,p4]

    if maximizingPlayer :
        v = -1e8
        for child in children:
            next_s=np.copy(s)
            if len(child)==3:
                next_s=Move(next_s,child,step)
            elif len(child)==5:
                next_s = Remove(next_s,child[0:2])
                next_s = Move(next_s, child[2:],step)

            v1,next_node,child_offspring=Minimax_ab(next_s,depth-1,alpha,beta,False,step+1,ab,trace,h,color,last_move=child)
            del next_s

            if trace:
                offspring+=[[v1,child,child_offspring]]

            if v1>v:
                v=v1
                optimal_nodes=[last_move]                   # optimal_nodes only record nodes of the optimal child
                optimal_nodes+=next_node

            if ab:
                alpha = max(alpha,v)
                if beta <= alpha:
                    break                   # beta pruning
        return  v,optimal_nodes,offspring


    else:
        v = 1e8
        for child in children:
            next_s = np.copy(s)
            if len(child) == 3:
                next_s = Move(next_s, child,step)
            elif len(child) == 5:
                next_s = Remove(next_s, child[0:2])
                next_s = Move(next_s, child[2:],step)

            v1, next_node,child_offspring = Minimax_ab(next_s,depth-1,alpha,beta,True,step+1,ab,trace,h,color,last_move=child)
            del next_s

            if trace:
                offspring+=[[v1,child,child_offspring]]

            if v1<v:
                v=v1
                optimal_nodes=[last_move]
                optimal_nodes+=next_node
            if ab:
                beta = min(beta,v)
                if beta <= alpha :
                    break                   #alpha pruning
        return v,optimal_nodes,offspring

# Minimax + alpha-beata pruning search with heuristic
def Minimax_ab2(s, depth, alpha, beta, maximizingPlayer, step, ab, trace, h, color, ph,last_move):
    # Inputs: state of the game s ϵ S, depth of the algorithm, alpha,beta and indicator for whose turn
    # Inputs: step,last_move, heuristic function and max_color
    # Actions: according to current stage, find out the 'optimal' action (position + placement)
    # Return: action to next step

    offspring = []
    terminal, scores = Terminal_checker(s, last_move)

    if depth == 0 or terminal or step >40:
        optimal_nodes = [last_move]
        if terminal:
            winner = get_winner(scores, step, color)
            if winner == 'color':
                v = 1e6
            else:
                v = -1e6
        else:
            v = h(s, step,last_move)
        return v, optimal_nodes, offspring


    children = get_children(s,step)  # Data structure of children: [[m1,0,[]],[m2,0,[]],,,,[mn,0,[]] ]. m: next_move [a,p1,p2] or [p1,p2,a, p3,p4]

    v0 = h(s, depth, last_move) + ph
    if maximizingPlayer:
        v = -1e8
        for child in children:
            m=child
            next_s = np.copy(s)
            if len(m) == 3:
                next_s = Move(next_s, m, step)
            elif len(m) == 5:
                next_s = Remove(next_s, m[0:2])
                next_s = Move(next_s, m[2:], step)

            v1, next_node, child_offspring = Minimax_ab2(next_s, depth - 1, alpha, beta, False, step + 1, ab, trace, h,
                                                        color, ph=v0,last_move=child)
            del next_s

            if trace:
                offspring += [[v1, m, child_offspring]]

            if v1 > v:
                v = v1
                optimal_nodes = [last_move]  # optimal_nodes only record nodes of the optimal child
                optimal_nodes += next_node

            # cost_tree[2][i]=subtree
            if ab:
                alpha = max(alpha, v)
                if beta <= alpha:
                    break  # beta pruning
            # i += 1
        return v, optimal_nodes, offspring

    else:
        v = 1e8
        for child in children:
            next_s = np.copy(s)
            m=child
            if len(m) == 3:
                next_s = Move(next_s, m, step)
            elif len(m) == 5:
                next_s = Remove(next_s, m[0:2])
                next_s = Move(next_s, m[2:], step)

            v1, next_node, child_offspring= Minimax_ab2(next_s, depth - 1, alpha, beta, True, step + 1, ab, trace, h,
                                                        color, ph=v0,last_move=child)
            del next_s

            if trace :
                offspring += [[v1, m, child_offspring]]
            if v1 < v:
                v = v1
                optimal_nodes = [last_move]
                optimal_nodes += next_node
            if ab:
                beta = min(beta, v)
                if beta <= alpha:
                    break  # alpha pruning

        return v, optimal_nodes, offspring


def Minimax_ab3(s,depth,alpha,beta,maximizingPlayer,step,ab,trace,h,color,last_move=[[]],vs=[]):
    # Inputs: state of the game s ϵ S, depth of the algorithm, alpha,beta and indicator for whose turn
    # Inputs: step,last_move, heuristic function and max_color
    # Actions: according to current stage, find out the 'optimal' action (position + placement)
    # Return: action to next step

    offspring = []
    terminal,scores=Terminal_checker(s,last_move[-1])

    if depth == 0 or terminal or step>40:
        optimal_nodes=[last_move[-1]]
        if terminal:
            winner=get_winner(scores,step,color)
            if winner=='color':
                v=1e6
            else:
                v=-1e6
        else:
            v=h(s,step)
        return v,optimal_nodes,offspring

    children = get_children(s,step)                     # Data structure of children: [m1,m2,,,,mn]. m: next_move [a,p1,p2] or [p1,p2,a, p3,p4]

    if maximizingPlayer :
        v = -1e8
        for child in children:
            next_s=np.copy(s)
            if len(child)==3:
                next_s=Move(next_s,child,step)
                v_node = last_move + [child]
            elif len(child)==5:
                next_s = Remove(next_s,child[0:2])
                next_s = Move(next_s, child[2:],step)
                v_node = last_move + [child[0:2],child[2:]]

            if not Is_In(v_node,vs):
                vs.append(v_node)
                v1,next_node,child_offspring=Minimax_ab3(next_s,depth-1,alpha,beta,False,step+1,ab,trace,h,color,last_move=v_node,vs=vs)

                del next_s

                if trace:
                    offspring+=[[v1,child,child_offspring]]

                if v1>v:
                    v=v1
                    optimal_nodes=[last_move[-1]]                   # optimal_nodes only record nodes of the optimal child
                    optimal_nodes+=next_node

                if ab:
                    alpha = max(alpha,v)
                    if beta <= alpha:
                        break                   # beta pruning
        return  v,optimal_nodes,offspring


    else:
        v = 1e8
        for child in children:
            next_s = np.copy(s)
            if len(child) == 3:
                next_s = Move(next_s, child,step)
                v_node = last_move + [child]
            elif len(child) == 5:
                next_s = Remove(next_s, child[0:2])
                next_s = Move(next_s, child[2:],step)
                v_node = last_move + [child[0:2], child[2:]]

            if not Is_In(v_node,vs):
                vs.append(v_node)
                v1, next_node,child_offspring = Minimax_ab3(next_s,depth-1,alpha,beta,True,step+1,ab,trace,h,color,last_move=v_node,vs=vs)
                del next_s

                if trace:
                    offspring+=[[v1,child,child_offspring]]

                if v1<v:
                    v=v1
                    optimal_nodes=[last_move[-1]]
                    optimal_nodes+=next_node
                if ab:
                    beta = min(beta,v)
                    if beta <= alpha :
                        break                   #alpha pruning
        return v,optimal_nodes,offspring



def Game_Frame(s):
    # ******************************** Flow Frame of the Game**********************************************************
    # automatic = int(input("If human-to-huam: input 0,else machine-to-human: input 1: "))
    print("In the machine-to-human mode.")
    automatic=1

    while True:
        firstplayer=input("AI palys as the 1th player or 2nd palyer?(1 or 2):")
        if firstplayer=='1':
            machine_first = 1
            break
        elif firstplayer== '2':
            machine_first=0
            break
        else:
            print("Wrong input,try again.Ipnut 1 or 2.")

    while True:
        print('Machine will adopt MiniMax search algorithm! ')
        ab=input("Activate alpha-beta or not.(activate: 1;not activate:0):")
        if ab=='1':
            ab = 1
            break
        elif ab== '0':
            ab=0
            break
        else:
            print("Wrong input,try again.Ipnut 0 or 1:")


    while True:
        tp = input("If open transposition input 1, otherwise 0: ")
        if tp == '1':
            tp = 1
            break
        elif tp == '0':
            tp = 0
            break
        else:
            print("Wrong input,try again.Ipnut 0 or 1:")

    while True:
        trace = input("Generate a trace of the minimax / alpha-beta or not.(yes: 1;not :0):")
        if trace == '1':
            trace = 1
            trace_file = input("Please input trace_file name(such as tracemm1.txt or traceab1.txt):")
            break
        elif trace == '0':
            trace = 0
            break
        else:
            print("Wrong input,try again.Ipnut 0 or 1:")

    while True:
        player=input("Input which role the first player wants to paly(color or dot?): ")
        if player.lower()=='color':
            print("Color first.")
            c=1
            break
        elif player.lower()=='dot':
            print("dot first.")
            c=0
            break
        else:
            print("Wrong input,try again.")

    if (machine_first and c) or not(machine_first or c):
        machine_max=1
    else:
        machine_max=0

    # Start the main for loop of our game
    times=[]
    numb=[]
    visited_state=[]
    for step in range(1,41):
        # if step==5:
        #     print('')
        print("step:",step)
        if step <= 24:                              # Period for regular moves
            while True:
                try:
                    if step % 2 == c:
                        print("It is color's turn.")
                    else:
                        print("It is dot/circle's turn.")

                    # if automatic:
                    if step % 2 == machine_first:

                        start = time.time()
                        if step<=2:
                            dep=2
                        elif step<=10:
                            dep=3
                        elif step<=21:
                            dep=4
                        else:
                            dep=5

                        # dep=2
                        if step<2:
                            lm=[]
                        else:
                            lm=m
                        if tp:
                            v1, optimal_path,offspring = Minimax_ab3(s, depth=dep, alpha=-1e8, beta=1e8, maximizingPlayer=machine_max,
                                                                step=step,ab = ab, trace=trace,color=c,h=h1,last_move=[lm])
                        else:
                            # v1, optimal_path, offspring = Minimax_ab(s, depth=dep, alpha=-1e8, beta=1e8,
                            #                                           maximizingPlayer=machine_max,
                            #                                           step=step, ab=ab, trace=trace, color=c, h=h1,
                            #                                           last_move=lm)
                            v1, optimal_path, offspring = Minimax_ab2(s, depth=dep, alpha=-1e8, beta=1e8,
                                                                 maximizingPlayer=machine_max,
                                                                 step=step, ab=ab, trace=trace,h=h2, color=c,ph=0,last_move=lm)

                        m= optimal_path[1]
                        print(Rev_translation(m))

                        if trace:
                            with open(trace_file,'a+') as file:
                                count=0
                                if dep==2:
                                    for x in offspring:
                                        count+=len(x[2])
                                elif dep==3:
                                    for x in offspring:
                                        if len(x[2]) > 0:
                                            for y in x[2]:
                                                count += len(y[2])
                                file.write(str(count)+'\n')
                                file.write(str(v1)+'\n\n')
                                for x in offspring:
                                    a = Decimal(str(x[0])).quantize(Decimal('0.0'))
                                    file.write(str(a) + '\n')
                                file.write('\n')
                            file.close()
                            numb.append(count)

                    else:
                        _, m = Human_input()

                        # start = time.time()
                        # if step<=2:
                        #     dep=2
                        # elif step<=16:
                        #     dep=3
                        # elif step<=22:
                        #     dep=4
                        # else:
                        #     dep=5
                        # # dep=2
                        #
                        #
                        # if step<2:
                        #     lm=[]
                        # else:
                        #     lm=m
                        # if tp:
                        #
                        #     v1, optimal_path, offspring = Minimax_ab3(s, depth=dep, alpha=-1e8, beta=1e8,
                        #                                              maximizingPlayer=not machine_max,
                        #                                              step=step, ab=ab, trace=trace, color=c, h=h1,last_move=[lm])
                        # else:
                        #     v1, optimal_path, offspring = Minimax_ab(s, depth=dep, alpha=-1e8, beta=1e8,
                        #                                              maximizingPlayer=machine_max,
                        #                                              step=step, ab=ab, trace=trace, color=c, h=h1,
                        #                                              last_move=lm)
                        # m = optimal_path[1]


                    # else:
                    #     _,m=Human_input()

                    Rule_checker(s,m[1],m[2],step,r=0)
                    s = Move(s, m,step)         # Move to the desired position
                    Visulization(s)
                    # if step % 2 == machine_first:
                    end=time.time()
                    print('time consume:',end-start)
                    times.append(end-start)

                except(Exception, IndexError, KeyError, ValueError) as e:
                    print(e)
                    if step%2==machine_first:
                        print("AI put an illigebal move. AI failed!!!  Game Over.")
                        # return
                    print("Please try again:")
                else:
                    break
            if step==24:
                print("End of regular move. Enter recycling moving stage!!!!")

        # Period for recycling moves
        else:
            while True:
                try:
                    if step % 2 == c:
                        print("It is color's turn.")
                    else:
                        print("It is dot/circle's turn.")
                    if not automatic:
                        rm,m=Human_input(r=1)
                    else:
                        if step%2==machine_first:
                            start=time.time()
                            if step==25:
                                lm=m
                            else:
                                lm=optimal_path[1][:]
                            if tp:
                                v1,optimal_path,offspring=Minimax_ab3(s, depth=dep, alpha=-1e8, beta=1e8, maximizingPlayer=machine_max,
                                                                    step=step,ab = ab, trace=trace,color=c,h=h1,last_move=[lm])
                            else:
                                v1, optimal_path, offspring = Minimax_ab2(s, depth=dep, alpha=-1e8, beta=1e8,
                                                                          maximizingPlayer=machine_max,
                                                                          step=step, ab=ab, trace=trace, color=c, h=h2,
                                                                          last_move=lm)
                            print(Rev_translation(optimal_path[1]))

                            rm = optimal_path[1][:2]
                            m = optimal_path[1][2:]

                            if trace:
                                with open(trace_file,'a+') as file:
                                    count=0
                                    if dep==2:
                                        for x in offspring:
                                            count+=len(x[2])
                                    elif dep==3:
                                        for x in offspring:
                                            if len(x[2]) > 0:
                                                for y in x[2]:
                                                    count+=len(y[2])

                                    file.write(str(count)+'\n')
                                    file.write(str(v1)+'\n\n')
                                    for x in offspring:
                                        a=Decimal(str(x[0])).quantize(Decimal('0.0'))
                                        file.write(str(a)+'\n')
                                    file.write('\n')
                                file.close()
                                numb.append(count)
                        else:
                            # rm, m = Human_input(r=1)
                            start = time.time()
                            if step==25:
                                lm=m
                            else:
                                lm=optimal_path[1][:]

                            if tp:
                                v1,optimal_path,offspring=Minimax_ab3(s, depth=dep, alpha=-1e8, beta=1e8, maximizingPlayer=machine_max,
                                                                    step=step,ab = ab, trace=trace,color=c,h=h1,last_move=[lm])
                            else:
                                v1, optimal_path, offspring = Minimax_ab(s, depth=dep, alpha=-1e8, beta=1e8,
                                                                          maximizingPlayer=machine_max,
                                                                          step=step, ab=ab, trace=trace, color=c, h=h1,
                                                                          last_move=lm)
                            rm = optimal_path[1][:2]
                            m = optimal_path[1][2:]
                    if rm[0]==m[1] and rm[1]==m[2]:
                        raise  Exception("Remove and move are in the same position!")

                    Rule_checker(s, rm[0], rm[1], step, r=1)
                    s1=np.copy(s)
                    s1 = Remove(s1, rm)
                    Rule_checker(s1, m[1], m[2], step, r=0)

                    s = Remove(s,rm)
                    s = Move(s, m,step)
                    Visulization(s)

                    # if step % 2 == machine_first:
                    end=time.time()
                    print('time consume:',end-start)
                    times.append(end-start)

                except(Exception, IndexError, KeyError, ValueError) as e:
                    if step%2==machine_first:
                        print("AI put an illigebal move. AI failed!!! Game Over.")
                        # return
                    print(e)
                    print("Please try again:")
                else:
                    break

        terminal,scores = Terminal_checker(s,m)

        if terminal == 1:
            winner=get_winner(scores,step,c)
            print("Congratalations! The winner is:",winner)
            for t in times:
                t = Decimal(str(t)).quantize(Decimal('0.00'))
            times = [float(Decimal(str(t)).quantize(Decimal('0.00'))) for t in times]
            print(times)
            print(numb)
            break  # break the 60 loops
    if terminal == 0:
        print("No winner, Draw")
        for t in times:
            t = Decimal(str(t)).quantize(Decimal('0.00'))
        times=[float(Decimal(str(t)).quantize(Decimal('0.00'))) for t in times]
        print(times)
        print(numb)
    return


if __name__ == '__main__':
    # ****************************Initialization************
    s = np.zeros((12, 8,2), dtype=int)
    # Initialize the stage function s, Each cell in the board contains [cell_state,step]

    cells = ['', 'r/d', 'r/o', 'w/d', 'w/o']
    # set of states for each cell on the board.  i.e cell_ss[1]: red and dot.

    A = [[], [1, 4], [4, 1], [4, 1], [1, 4], [2, 3], [3, 2], [3, 2], [2, 3]]
    # 8 actions, put responding number into the cell of the board. i.e action A[1]=[1,4], input 1 to target point, 4 on the right or top of the target point

    dic_col = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, "F": 5, 'G': 6, 'H': 7}
    number2col = ['A','B','C','D','E','F','G','H']
    dic_row = {'1': 11, '2': 10, '3': 9, '4': 8, '5': 7, '6': 6, '7': 5, '8': 4, '9': 3, '10': 2, '11': 1, '12': 0}
    dic_a = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8}

    D = [[-1, 0], [0, 1]]   # Direction of the card.
    #  D[1]: the next point is on the right, a horizontal card, which is corresponding to action A[i] with odd subscript.
    #  D[0]: the next point is on the top, a vertical card, which is corresponding to action A[i] with even subscript.
    Visulization(s)

    # Enter the Main Frame of game.*****************************
    Game_Frame(s)










