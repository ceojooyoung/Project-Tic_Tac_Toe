import pygame
import random
import os
from os import path

pygame.init()

#변수 설정 및 초기화
#색
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

#폰트
font=pygame.font.SysFont("arial", 50, True, False)
font2=pygame.font.SysFont("arial", 20, True, False)

#UI 크기
CELL_SIZE = 200
UI_SIZE = 100
SCREEN_WIDTH = 3*CELL_SIZE
SCREEN_HEIGHT = 3*CELL_SIZE+UI_SIZE

#파이게임 설정
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Death of TTT")
clock = pygame.time.Clock()
event = pygame.event.poll()
done=False

# assets 경로 설정
current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')

# 사운드
shoot_sound = pygame.mixer.Sound(path.join(assets_path, 'pew.mp3'))
power_sound = pygame.mixer.Sound(path.join(assets_path, 'pow5.mp3'))
burst_sound = pygame.mixer.Sound(path.join(assets_path, '폭팔음 깔끔.mp3'))
shortscream = pygame.mixer.Sound(path.join(assets_path, 'shortscream.mp3'))
bell = pygame.mixer.Sound(path.join(assets_path, 'bell.mp3'))
woo = pygame.mixer.Sound(path.join(assets_path, '야유.mp3'))
pygame.mixer.music.load(path.join(assets_path, 'bgm.mp3'))
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops=-1)

#게임변수
PLAYAI = False
playing=False
gameover = False
L=[[0,0,0],[0,0,0],[0,0,0]]
AWIN=False
BWIN=False
TIE=False
TurnA = True
TurnB = False
First=None
fired = False

#승패 판정 함수
# A승 1 / B승 2 / 비김 3 / 진행 중 0 
def who_win(L) : 
    over = 0
    for i in range(1,3) :
        for j in range(3):
            if (L[j][0]==i and L[j][1]==i) and L[j][2]==i : 
                over = i
                break
            elif (L[0][j]==i and L[1][j]==i) and L[2][j]==i : 
                over = i
                break
        if over > 0 : break
        if (L[0][0]==i and L[1][1]==i) and L[2][2]==i : 
            over = i
            break
        if (L[2][0]==i and L[1][1]==i) and L[0][2]==i : 
            over = i
            break
    if not over :
        tie = 3
        for i in range(3) :
            for j in range(3) :
                if L[i][j]==0 :
                    tie=0
                    break
            if tie==0 : break
        over = tie
    return over

#게임이 끝날 수 있는 상황인지 판정
def crisis(l, p) :
    L=[0]
    for i in range(3) : L+=l[i]
    if L[5]==p :
        for i in range(1,10):
            if i==5 : continue
            elif L[i]==p :
                return 10-i
    elif L[1]==p:
        if L[4]==p : return 7
        elif L[7]==p : return 4
        elif L[9]==p : return 5
        elif L[2]==p : return 3
        elif L[3]==p : return 2
    elif (L[2]==p and L[3]==p) or (L[4]==p and L[7]==p) : return 1
    elif L[3]==p :
        if L[6]==p : return 9
        elif L[9]==p : return 6
    elif (L[4]==p and L[6]==p) or (L[2]==p and L[8]==p) : return 5
    elif (L[6]==p and L[9]==p) or (L[7]==p and L[8]==p) : return 9
    elif L[8]==p and L[9]==p : return 7
    elif (L[7]==p and L[9]==p) : return 8
    return 0

#게임이 끝날 상황만 아니면 무작위
def Strategy_A(L, p) :
    a = crisis(L,p)-1
    b = crisis(L, 3-p)-1
    if a>=0 and not L[a//3][a%3] : L[a//3][a%3]=p
    elif b>=0 and not L[b//3][b%3] : L[b//3][b%3]=p
    else :
        temp=[]
        for i in range(9) :
            if L[i//3][i%3] ==0 : temp.append(i)
        if temp == [] : return
        if len(temp)==1 : L[temp[0]//3][temp[0]%3]=p 
        else : L[temp[random.randint(0,len(temp)-1)]//3][temp[random.randint(0,len(temp)-1)]%3]=p

# 게임 반복 구간
while not done:
    # 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:

            #플레이타입이 정해지지 않은 처음 클릭
            if not playing :
                bell.play()
                x, y = event.pos[0], event.pos[1]
                if y < UI_SIZE+1.5*CELL_SIZE : PLAYAI = True                
                playing = True
                if PLAYAI :
                    First = True
                    if random.randint(0,1) : First = False
                    if not First :
                            power_sound.play()
                            Strategy_A(L,1)
                            TurnA, TurnB = TurnB, TurnA
            #플레이타입 결정 이후
            elif playing :
                #게임 종료 시엔 눌러서 새로 시작하기
                if gameover :
                        gameover = False
                        fired = False
                        L=[[0,0,0],[0,0,0],[0,0,0]]
                        if TIE : woo.play()
                        elif PLAYAI :
                            if First :
                                if AWIN : burst_sound.play()
                                elif BWIN : shortscream.play()
                            elif not First :
                                if AWIN : shortscream.play()
                                elif BWIN : burst_sound.play()
                        elif not TIE : shortscream.play()
                        AWIN=False                    
                        BWIN=False
                        TIE=False
                        TurnA = True
                        TurnB = False
                        if PLAYAI :
                            First = True
                            if random.randint(0,1) : First = False
                            if not First :
                                Strategy_A(L,1)
                                TurnA, TurnB = TurnB, TurnA
                                
                #인간과 플레이 도중 클릭
                elif not PLAYAI :
                    x, y = event.pos[0] // CELL_SIZE, (event.pos[1]-UI_SIZE) // CELL_SIZE
                    if TurnA and not L[x][y]:
                        L[x][y]=1                            
                        TurnA, TurnB = TurnB, TurnA
                        if who_win(L)==1 or who_win(L)==2 : shoot_sound.play()
                        else : power_sound.play()
                    elif TurnB and not L[x][y]:
                        L[x][y]=2
                        TurnA, TurnB = TurnB, TurnA
                        if who_win(L)==1 or who_win(L)==2 : shoot_sound.play()
                        else : power_sound.play()
                #AI와 플레이 도중 클릭
                else :
                    x, y = event.pos[0] // CELL_SIZE, (event.pos[1]-UI_SIZE) // CELL_SIZE
                    if First :
                        if TurnA and not L[x][y]:
                            L[x][y]=1
                            TurnA, TurnB = TurnB, TurnA
                            if who_win(L)==1 or who_win(L)==2 : shoot_sound.play()
                            else : power_sound.play()
                        if TurnB :
                            Strategy_A(L,2)
                            TurnA, TurnB = TurnB, TurnA
                            if who_win(L)==1 or who_win(L)==2 : shoot_sound.play()
                            else : power_sound.play()
                    if First == False :
                        if TurnB and not L[x][y]:
                            L[x][y]=2
                            TurnA, TurnB = TurnB, TurnA
                            if who_win(L)==1 or who_win(L)==2 : shoot_sound.play()
                            else : power_sound.play()
                        if TurnA :
                            Strategy_A(L,1)
                            TurnA, TurnB = TurnB, TurnA
                            if who_win(L)==1 or who_win(L)==2 : shoot_sound.play()
                            else : power_sound.play()
                        
    flag = who_win(L)   
    if flag == 1 :
        AWIN = True
        gameover = True
    elif flag == 2 :
        BWIN = True
        gameover = True
    elif flag == 3 :
        TIE = True
        gameover = True

    #UI
    #제목
    screen.blit(font.render("Tic Tac Toe", True, BLACK), [190, 20])
    #게임판
    if playing == True :
        for x in range(3):
            for y in range(3):
                pygame.draw.rect(screen, BLACK, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE+UI_SIZE, CELL_SIZE, CELL_SIZE), 1)
                if L[x][y] == 1 : 
                    pygame.draw.circle(screen, GREEN, [(x+0.5)*CELL_SIZE,(y+0.5)*CELL_SIZE+UI_SIZE], 0.4*CELL_SIZE, 0)                        
                    pygame.draw.circle(screen, WHITE, [(x+0.5)*CELL_SIZE,(y+0.5)*CELL_SIZE+UI_SIZE], 0.3*CELL_SIZE, 0)                    
                elif L[x][y] == 2 :
                    pygame.draw.line(screen, RED, [int((x+0.8)*CELL_SIZE),int((y+0.1)*CELL_SIZE)+UI_SIZE], [int((x+0.2)*CELL_SIZE),int((y+0.9)*CELL_SIZE)+UI_SIZE], int(0.15*CELL_SIZE))
                    pygame.draw.line(screen, RED, [int((x+0.2)*CELL_SIZE),int((y+0.1)*CELL_SIZE)+UI_SIZE], [int((x+0.8)*CELL_SIZE),int((y+0.9)*CELL_SIZE)+UI_SIZE], int(0.15*CELL_SIZE))
    #AI 대전 시 순서 표시
        if PLAYAI :
            if First :  screen.blit(font2.render("You First", True, BLACK, WHITE), [SCREEN_WIDTH-100, 40])
            else : screen.blit(font2.render("You Second", True, BLACK, WHITE), [SCREEN_WIDTH-100, 40])
    #인간 대전 시 결과창
        if gameover :
            if not PLAYAI :
                screen.blit(font.render("Game Over!", True, BLACK, WHITE), [SCREEN_WIDTH//2-120, SCREEN_HEIGHT//2-140])
                screen.blit(font.render("Click to Play Again", True, BLACK, WHITE), [SCREEN_WIDTH//2-170, SCREEN_HEIGHT//2-20])
                if AWIN : screen.blit(font.render("A Win!", True, GREEN, WHITE), [SCREEN_WIDTH//2-60, SCREEN_HEIGHT//2-80])
                elif BWIN : screen.blit(font.render("B win!", True, RED, WHITE), [SCREEN_WIDTH//2-60, SCREEN_HEIGHT//2-80])
                elif TIE : screen.blit(font.render("Tie!", True, BLUE, WHITE),  [SCREEN_WIDTH//2-30, SCREEN_HEIGHT//2-80])
    #AI 대전 시 결과창
            elif PLAYAI :
                screen.blit(font.render("Game Over!", True, BLACK, WHITE), [SCREEN_WIDTH//2-120, SCREEN_HEIGHT//2-140])
                screen.blit(font.render("Click to Play Again", True, BLACK, WHITE), [SCREEN_WIDTH//2-170, SCREEN_HEIGHT//2-20])
                if First :
                    if AWIN : screen.blit(font.render("You Win!", True, GREEN, WHITE), [SCREEN_WIDTH//2-80, SCREEN_HEIGHT//2-80])
                    elif BWIN : screen.blit(font.render("You Lose!", True, RED, WHITE), [SCREEN_WIDTH//2-90, SCREEN_HEIGHT//2-80])
                    elif TIE : screen.blit(font.render("Tie!", True, BLUE, WHITE),  [SCREEN_WIDTH//2-30, SCREEN_HEIGHT//2-80])
                else :
                    if AWIN : screen.blit(font.render("You Lose!", True, GREEN, WHITE), [SCREEN_WIDTH//2-90, SCREEN_HEIGHT//2-80])
                    elif BWIN : screen.blit(font.render("You win!", True, RED, WHITE), [SCREEN_WIDTH//2-80, SCREEN_HEIGHT//2-80])
                    elif TIE : screen.blit(font.render("Tie!", True, BLUE, WHITE),  [SCREEN_WIDTH//2-30, SCREEN_HEIGHT//2-80])
    #게임 모드 선택
    else : 
        screen.blit(font.render("Play with AI", True, RED),  [SCREEN_WIDTH//2-120, SCREEN_HEIGHT//2-140])
        screen.blit(font.render("Play with Human", True, BLUE),  [SCREEN_WIDTH//2-160, SCREEN_HEIGHT//2+170])
        pygame.draw.line(screen, BLACK, [0, UI_SIZE], [SCREEN_WIDTH, UI_SIZE], 1)
        pygame.draw.line(screen, BLACK, [0, UI_SIZE+1.5*CELL_SIZE], [SCREEN_WIDTH, UI_SIZE+1.5*CELL_SIZE], 1)
        
    pygame.display.update()
    screen.fill(WHITE)
    clock.tick(60)

pygame.quit() 
