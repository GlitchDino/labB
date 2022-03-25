from collections import namedtuple
import argparse
import copy
import random
from hashlib import new
State = namedtuple('State',['position','player'])

class Queue:
    def __init__ (self):
        self._data = []
        self._size = 0
    def __len__(self):
        return self._size
    def is_empty(self):
        return self._size == 0
    def enqueue(self, item):
        self._size+=1
        self._data.append(item)
    def dequeue(self):
        self._size-=1
        return self._data.pop(0)
    def info(self):
        return self._data

class Node:
    def __init__(self,state):
        self.parent = None
        self.child = []
        self.action = None
        self.state = state
        self.utility = None
        self.depth = 0
        self.level = None

    def get_parent(self):
        return self.parent
    def get_child(self):
        return self.child
    def get_action(self):
        return self.action
    def get_state(self):
        return self.state
    def get_utility(self):
        return self.utility
    def get_depth(self):
        return self.depth
    def get_level(self):
        return self.level
    def set_parent(self,new_parent):
        self.parent = new_parent
    def set_action(self,new_action):
        self.action = new_action
    def increase_depth(self):
        self.depth += 1
    def set_child(self,list_kids):
        self.child=list_kids
    def set_utility(self, n):
        self.utility = n
    def set_level(self, new_level):
        self.level = new_level

Q = Queue()


class Game:
    def __init__(self):
        self.black_count = 0 
        self.white_count = 0
        self.turn = "white"

    def initial_state(self, rows,columns,pieces):
        Size = columns * (pieces)
        rest = (rows - pieces*2) * columns
        X = []
        X2 = []
        Spaces = []
        Spaces2 = []
        O = []
        O2 = []
        Board = []

        for i in range (Size):
            X.append('X')
            O.append('O')
        self.black_count=len(X)
        self.white_count=len(O)

        for i in range ((pieces)):
            X2.append(X[i*columns:(i+1) * columns])
            O2.append(O[i*columns:(i+1) * columns])
        for j in range (rest):
            Spaces.append('.')
        for i in range (rows - pieces*2):
            Spaces2.append(Spaces[i*columns:(i+1) * columns])
        for i in range(pieces):
            Board.append(X2[i])
        for i in range (rows - pieces*2):
            Board.append(Spaces2[i])
        for i in range(pieces):
            Board.append(O2[i])
        starting_state = State(Board,"W")
        return  starting_state

    def display_state(self, state):
        #return state[0]
        print("Number of black peices: "+str(self.black_count))
        print("Number of white peices: "+str(self.white_count))
        for line in state[0]:
            print(line)

    def white_pieces(self, state):
        white=[]
        black = []
        board = state[0]
        for rows in range (len(board)):
            for cols in range(len(board[0])):
                if board[rows][cols]== 'O':
                    piece = []
                    piece.append(rows)
                    piece.append(cols)
                    piece_tuple = tuple(piece)
                    white.append(piece_tuple)
        return white#list of tuple locations

    def black_pieces(self, state):
        black = []
        board = state[0]
        for rows in range (len(board)):
            for cols in range(len(board[0])):
                if board[rows][cols]== 'X':
                    piece = []
                    piece.append(rows)
                    piece.append(cols)
                    piece_tuple = tuple(piece)
                    black.append(piece_tuple)

        return black #list of tuple locations in the board
    """def move(self, start, finish):
        if self.turn=="white":
            Board"""
    def game_ending(self, state):
        count = 0
        Board = self.display_state(state)

        for i in range(len(state[0])):
            if "O" not in (state[0][i]):
                count+=1
        count = 0
        for i in range(len(state[0])):
            if "X" not in (state[0][i]):
                count+=1
        if count == len(state[0]):
            return True
        for j in range(len(state[0])):
            if Board[0][j-1] == 'O' or Board[(len(state[0])-1)][j-1] == 'X':
                return True

    def move_generator(self, state):
        black = self.black_pieces(state)
        white = self.white_pieces(state)
        actions = {}
        if self.game_ending(state)==True:
            return actions #"The game has ended no further moves to generate"
        if state[1]== "W":
            for pos in white:
                check = (pos[0]-1, pos[1])
                check_2 = pos[1]-1#out of bound to the left
                check_3 = pos[1]+1#out of bound to the right
                if check in black or check in white:
                    continue
                if check_2<0:
                    actions[pos]=[(pos[0]-1, pos[1]),(pos[0]-1, pos[1]+1)]
                elif check_3>=len(state[0]):
                    actions[pos]=[(pos[0]-1, pos[1]),(pos[0]-1, pos[1]-1)]
                else:
                    actions[pos]=[(pos[0]-1, pos[1]),(pos[0]-1, pos[1]-1),(pos[0]-1, pos[1]+1)]
        if state[1]== "B":
            for pos in black:
                check = (pos[0]+1, pos[1])
                check_2 = pos[1]-1#out of bound to the left
                check_3 = pos[1]+1#out of bound to the right
                if check in black or check in white:
                    continue
                if check_2<0:
                    actions[pos]=[(pos[0]+1, pos[1]),(pos[0]+1, pos[1]+1)]
                elif check_3>=len(state[0]):
                    actions[pos]=[(pos[0]+1, pos[1]),(pos[0]+1, pos[1]-1)]
                else:
                    actions[pos]=[(pos[0]+1, pos[1]),(pos[0]+1, pos[1]-1),(pos[0]+1, pos[1]+1)]
        return actions

    def transitional(self, state,piece,action):
        Board = copy.deepcopy(state[0])
        if Board[piece[0]][piece[1]] == 'X' and state[1] =='B': #if its blacks turn and peice is black
            if action[0] == piece[0]+1: #if move is in range for the peice
                if action[1] == piece[1]-1 or action[1] == piece[1]+1 or action[1] == piece[1]:
                    if  Board[action[0]][action[1]] == '.':
                        Board[action[0]][action[1]] = 'X'
                        Board[piece[0]][piece[1]] = '.'
                    elif  Board[action[0]][action[1]] == 'O':
                        Board[action[0]][action[1]] = 'X'
                        Board[piece[0]][piece[1]] = '.'
                        self.white_count-=1

                    else:
                        return 'spot taken'
            new_state = State(Board,"W")
            return new_state

        elif Board[piece[0]][piece[1]] == 'O' and state[1] == 'W':
            if action[0] == piece[0]-1:
                if action[1] == piece[1]-1 or action[1] == piece[1]+1 or action[1] == piece[1]:
                    if  Board[action[0]][action[1]] == '.':
                        Board[action[0]][action[1]] = 'O'
                        Board[piece[0]][piece[1]] = '.'
                    elif  Board[action[0]][action[1]] == 'X':
                        Board[action[0]][action[1]] = 'O'
                        Board[piece[0]][piece[1]] = '.'
                        self.black_count-=1
                    else:
                        return 'spot taken'
            new_state = State(Board,"B")
            return new_state

        return "wrong input"



    def create_tree(self, state, depth):
        curr_node = Node(state)
        Q.enqueue(curr_node)

        while Q.is_empty()==False:#game_ending(state)==False:
            curr_node = Q.dequeue()
    #         print("curr_node_state",curr_node.get_state())
            if curr_node.get_depth()==depth:#check if node expaned is at maximum depth
                if(curr_node.get_depth%2==0):
                    utility=self.white_count+random.random()
                    
                else:
                    utility=(0-self.black_count)+random.random()
                curr_node.set_utility(utility)
                continue
            possible_actions=self.move_generator(curr_node.get_state())
            all_keys = list(possible_actions.keys())
            child = []
            keys = 0
            while keys <len(all_keys):
                #child nodes depth is parents node +=1
                current_vals = list(possible_actions.values())#takes the amount of childs in the specific key
                n_kids = len(current_vals[keys])#how many kids are there for a specific key
                for i in range (n_kids):
                    new_state = self.transitional(curr_node.get_state(),all_keys[keys],current_vals[keys][i])
                    new_node = Node(new_state)#I need to feed a new state #the index of the children
                    new_node.set_parent(curr_node)
                    new_node.increase_depth()#one more than parent might have to change this
                    new_node.set_action(current_vals[keys][i])# new_node.set_action(node)####IMPORTANT FIGURE THIS OUT
                    child.append(new_node)
    #                 print("new node_state",new_node.get_state())
                    Q.enqueue(new_node)
                keys+=1
        return curr_node



def create_tree2(state, depth):
    curr_node = Node(state)
    Q.enqueue(curr_node)
#     keys = 0

    while Q.is_empty()==False:#game_ending(state)==False:
        curr_node = Q.dequeue()
        print("curr_node_state",curr_node.get_state())
        if curr_node.get_depth()==depth:#check if node expaned is at maximum depth
            #Calc unitility here
            continue
        possible_actions=move_generator(curr_node.get_state())
        all_keys = list(possible_actions.keys())
        child = []
        keys = 0
        while keys <len(all_keys):
            #child nodes depth is parents node +=1
            current_vals = list(possible_actions.values())#takes the amount of childs in the specific key
            n_kids = len(current_vals[keys])#how many kids are there for a specific key
            for i in range (n_kids):
                new_state = transitional(curr_node.get_state(),all_keys[keys],current_vals[keys][i])
                new_node = Node(new_state)#I need to feed a new state #the index of the children
                new_node.set_parent(curr_node)
                new_node.increase_depth()#one more than parent might have to change this
                child_depth=new_node.get_depth
                if(child_depth%2==0):
                    new_node.set_level("MAX")
                else:
                    new_node.set_level("MIN")
                new_node.set_action(current_vals[keys][i])# new_node.set_action(node)####IMPORTANT FIGURE THIS OUT
                child.append(new_node)
                print("new node_state",new_node.get_state())
                Q.enqueue(new_node)
            keys+=1














if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process file.')#Create argument paser object
    # parser.add_argument('m',help='teaseing')#Create first file argument
    args = parser.parse_args()
    game=Game()
   
    initial_state = game.initial_state(8,8,2)
    display = game.display_state(initial_state)
    tran = game.transitional(initial_state,(6,0),(5,0))
    tran2 = game.transitional(tran,(1,0),(2,0))
    tran3= game.transitional(tran2,(5,0), (4,0))
    tran4= game.transitional(tran3,(2,0), (3,0))
    tran5= game.transitional(tran4,(4,0), (3,0))
    #tran = game.transitional(tran,(5,1),(4,1))
    #tran = game.transitional(tran,(4,1),(3,1))
    print("Game after 1 move")
    game.display_state(tran)
    print("Game after 4 move")
    game.display_state(tran4)
    print("Game after 5 move")
    game.display_state(tran5)
    #print(display)
    """
    display = game.display_state(initial_state)
    move = game.move_generator(initial_state)
    print("Possible moves for player",move)

    termination = game.game_ending(initial_state)
    print(termination)
    ####### Test for game_ending
    l = initial_state[0][0]
    l.insert(0,'O')
    l.pop()
    initial_state[0][0]=l
    print(initial_state)

    termination = game.game_ending(initial_state)
    #create_tree(initial_state, 3)
    print(termination)
    """