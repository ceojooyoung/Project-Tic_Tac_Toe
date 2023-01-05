import random
game_board: str = '_'*9
AI = True
HUMAN =  False

AI_MARK = 'X'
HUMAN_MARK = 'O'

def main():
    player:bool = AI
    if random.randint(0,1):
        player = HUMAN
        print("You First\n")
    else : print("AI First\n")
    while find_empty(game_board) and not is_end(game_board):
        if player == AI :
            position, _ = minimax(game_board, 9, AI)
            place(position, AI_MARK)
            player = HUMAN
        else:
            position = input_num()
            place(position, HUMAN_MARK)
            player = AI
        draw()
    ending()

def find_empty(board: str) -> tuple[int,]:
    return tuple(x for x, cell in enumerate(board) if cell == '_')

def is_end(board: str) -> bool:
    return is_win(board, AI_MARK) or is_win(board, HUMAN_MARK)

def is_win(board, player):
    for (x,y,z) in ((0,1,2,),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)):
        if board[x] == board[y] == board[z]:
            if board[x]==player : return True
    return False

def minimax(board:str, depth: int, max_player: bool) -> tuple:
    position = -1
    if depth == 0 or not find_empty(board) or is_end(board):
        return -1, evaluate(board)
    if max_player == AI :
        value = float('-inf')
        for each in find_empty(board):
            _, score = minimax(board[:each]+AI_MARK+board[each+1:],depth-1,HUMAN)
            if score > value:
                value = score
                position = each
            if score == 1: break
    else :
        value = float('inf')
        for each in find_empty(board):
            _, score = minimax(board[:each]+HUMAN_MARK+board[each+1:], depth-1,AI)
            if score < value:
                value = score
                position = each
            if score == -1: break
    return position, value

def evaluate(board: str) -> int:
    if is_win(board, AI_MARK): score = 1
    elif is_win(board, HUMAN_MARK): score = -1
    else: score = 0
    return score

def place(x: int, player: str) -> bool:
    if is_valid(x):
        global game_board
        game_board = game_board[:x]+player+game_board[x+1:]
        return True
    return False

def is_valid(x:int)->bool : return x in find_empty(game_board)

def input_num()->int:
    num= -1
    while num not in find_empty(game_board):
        input_str=''
        while not input_str.isdecimal():
            input_str=input('\n1~9? : ')
        num = int(input_str) -1
    return num

def draw(): print(f'\n{game_board[6:]} 789\n{game_board[3:6]} 456\n{game_board[:3]} 123')

def ending():
    if is_win(game_board, AI_MARK): print('AI Win')
    elif is_win(game_board, HUMAN_MARK): print('HUMAN Win')
    else : print('Tie')

if __name__ == '__main__': main()
