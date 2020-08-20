
from random import *
reward = 0 
last_reward = 0
last_points = 0


def new_game(n):
    matrix = []

    for i in range(n):    #range(4) = 0,1,2,3
        matrix.append([0] * n)    #[0,0,0,0] n times
    return matrix


def add_two(mat):                            #choose a random point in matrix and check if not 0 add 2 to that point.
    a=randint(0,len(mat)-1)
    b=randint(0,len(mat)-1)
    while(mat[a][b]!=0):
        a=randint(0,len(mat)-1)
        b=randint(0,len(mat)-1)
    mat[a][b]=2
    return mat

def game_state(mat):
    for i in range(len(mat)):                      
        for j in range(len(mat[0])):               
            if mat[i][j]==2048:
                return 'win'
    for i in range(len(mat)-1): 
        for j in range(len(mat[0])-1): 
            if mat[i][j]==mat[i+1][j] or mat[i][j+1]==mat[i][j]:
                return 'not over'
    for i in range(len(mat)): 
        for j in range(len(mat[0])):
            if mat[i][j]==0:
                return 'not over'
    for k in range(len(mat)-1): 
        if mat[len(mat)-1][k]==mat[len(mat)-1][k+1]:
            return 'not over'
    for j in range(len(mat)-1): 
        if mat[j][len(mat)-1]==mat[j+1][len(mat)-1]:
            return 'not over'
    return 'lose'


def reverse(mat):
    new=[]
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):    
            new[i].append(mat[i][len(mat[0])-j-1])
    return new



def transpose(mat):
    new=[]
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    return new

def cover_up(mat):                                         #mat=[[0, 2, 2, 0], [4, 0, 8, 16], [16, 32, 4, 16], [8, 2, 0, 2]]
    new=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]          #new=[[2, 2, 0, 0], [4, 8, 16, 0], [16, 32, 4, 16], [8, 2, 2, 0]]
    done=False
    for i in range(4):
        count=0
        for j in range(4):
            if mat[i][j]!=0:
                new[i][count]=mat[i][j]
                if j!=count:
                    done=True
                count+=1           #count+=1 == ++count
    return (new,done)

def merge(mat):                                    #mat=[[0,2,2,0],[4,0,8,16],[16,32,4,16],[8,2,0,2]]
    done=False                                   #new=[[0, 4, 0, 0], [4, 0, 8, 16], [16, 32, 4, 16], [8, 2, 0, 2]]
    for i in range(4):
        for j in range(3):
            if mat[i][j]==mat[i][j+1] and mat[i][j]!=0:
                mat[i][j]*=2
                score(mat[i][j])
                mat[i][j+1]=0
                done=True        
    return (mat,done)


def up(game):
        global reward
        print(game)
        game=transpose(game)
        game,done=cover_up(game)
        temp=merge(game)
        game=temp[0]
        done=done or temp[1]
        game=cover_up(game)[0]
        game=transpose(game)
        #print(reward)
        point(reward)
        return (game,done)

def down(game):
        global reward
        print(game) 
        game=reverse(transpose(game))
        game,done=cover_up(game)
        temp=merge(game)
        game=temp[0]
        done=done or temp[1]
        game=cover_up(game)[0]
        game=transpose(reverse(game))
        #print(reward)
        point(reward)
        return (game,done)

def left(game):
        global reward
        print(game)
        game,done=cover_up(game)
        temp=merge(game)
        game=temp[0]
        done=done or temp[1]
        game=cover_up(game)[0]
        #print(reward)
        point(reward)
        
        return (game,done)

def right(game):
        global reward
        print(game)
        game=reverse(game)
        game,done=cover_up(game)
        temp=merge(game)
        game=temp[0]
        done=done or temp[1]
        game=cover_up(game)[0]
        game=reverse(game)
        #print(reward)
        point(reward)       
        return (game,done)

def score(points):
    global reward
    reward = reward + (points/2)
    return(reward)

def point(point1):
    global last_reward
    global last_points
    last_points = point1 - last_reward
    last_reward = reward
    return(last_points)

def last_rew():
	return(last_points)