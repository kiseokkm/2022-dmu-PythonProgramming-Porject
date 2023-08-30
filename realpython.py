from time import sleep
import pygame
import random
import os
import time

pygame.init() # pygame 진행시 초기화 꼭 해주기

screen_width = 480 #가로 크기
screen_height = 640 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

#배경음악
pygame.mixer.init()
pygame.mixer.music.load('musicc.ogg')
pygame.mixer.music.set_volume(0.40)
pygame.mixer.music.play(-3,0,0)

#화면 타이틀 설정
pygame.display.set_caption("장애물을 없애서 점수를 게임") #게임 이름

#FPS
clock = pygame.time.Clock()

# Font 정의
game_font = pygame.font.SysFont("malgungothicsemilight", 25)
notice_font = pygame.font.SysFont("malgungothicsemilight", 25)
quit_font = pygame.font.SysFont("malgungothicsemilight", 40)

total_time = 100 #게임 시간
start_ticks = pygame.time.get_ticks() #시작 시간


score = 0 #점수 초기화
scoreup1 = 10 #점수 올라가는 수
scoreup2 = 10#점수 올라가는 수
score_chk = False #장애물 제거시 추가점수
add_score = 0 # 추가점수
time_delay = 0
Stage = 1
#게임 종료 메시지
#Time Over (시간초과 실패)
#Mission Complete (성공)
#Game Over (캐릭터가 장애물에 맞음)

game_result = "Game Over" 

current_path = os.path.dirname(__file__) #현재 파일의 경로 반환
image_path = os.path.join(current_path, "images")
heartlife = pygame.image.load(os.path.join(image_path, "heartlife.png"))
heartlife_x_pos = random.randint(0, 480-100)
heartlife_y_pos = random.randint(0, 50)
heartlife_speed = 5
heartlife_respawn = 0
heartlife_chk = False
#폰트 정의
notice_font = pygame.font.SysFont("malgungothicsemilight", 12, True)

#하트 딜레이10초
def heartlife_timedelay():
    global heartlife_respawn
    if heartlife_respawn == 10: #10초
        heartlife_time = int((pygame.time.get_ticks() - heartlife_delay) / 1000)
        if heartlife_time == 10: #10초
            heartlife_respawn = 0



# 초기화
 #images 폴더 경로 반환

#배경
background = pygame.image.load(os.path.join(image_path, "background.png"))

#스테이지
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] #스테이지 위에 두기 위해

# 캐릭터
character = pygame.image.load(os.path.join(image_path, "character.png"))
character2 = pygame.image.load(os.path.join(image_path, "character2.png"))
character_size = character.get_rect().size #이미지의 크기를 구함
character_width = character_size[0] #가로 크기
character_height = character_size[1] #세로 크기
character_x_pos = (screen_width / 2) - (character_width / 2) #화면 가운데에 위치
character_y_pos = (screen_height - stage_height) - character_height #화면 맨아래에 위치

#시작 목숨 개수        
Life = 3
Life_chk = False

#이펙트 효과
effect = pygame.image.load(os.path.join(image_path, "effect.png"))
effect_size = effect.get_rect().size #이미지의 크기를 구함
effect_width = effect_size[0] #가로 크기
effect_height = effect_size[1] #세로 크기



#무기 제한 장애물
weapon_ben = pygame.image.load(os.path.join(image_path, "weapon_ben.png"))
weapon_ben_size = weapon_ben.get_rect().size
weapon_ben_width = weapon_ben_size[0]  #가로 크기
weapon_ben_height = weapon_ben_size[1] #세로 크기

weapon_ben_x_pos = random.randint(0, screen_width - weapon_ben_width)
weapon_ben_y_pos = random.randint(0, 50)
weapon_ben_speed = 12 #속도

#장애물
ddong = pygame.image.load(os.path.join(image_path, "snow.png"))
ddong2 = pygame.image.load(os.path.join(image_path, "ddong2.png"))
ddong3 = pygame.image.load(os.path.join(image_path, "ddong3.png"))

ddong_size = ddong.get_rect().size
ddong_width = ddong_size[0]  #가로 크기
ddong_height = ddong_size[1] #세로 크기

ddong_x_pos = random.randint(0, screen_width - ddong_width)
ddong2_x_pos = random.randint(0, screen_width - ddong_width)
ddong3_x_pos = random.randint(0, screen_width - ddong_width)

ddong_y_pos = random.randint(0, 50)
ddong2_y_pos = random.randint(0, 50)
ddong3_y_pos = random.randint(0, 50)
ddong_speed = 7 #장애물 속도

#무적 아이템
invincibility = pygame.image.load(os.path.join(image_path, "invincibility.png"))
invincibility_size = invincibility.get_rect().size
invincibility_width = invincibility_size[0] #가로 크기
invincibility_height = invincibility_size[1] #세로 크기
invincibility_x_pos = random.randint(0, screen_width - ddong_width)
invincibility_y_pos = random.randint(0, 50)
invincibility_speed = 12
invincibility_respawn = 0
invincibility_chk = False

#버튼 초기화
exit_img = pygame.image.load(os.path.join(image_path, "exit_btn.png"))

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

exit_button = Button(screen_width - 95, (screen_height - stage_height) -6, exit_img)

#이동 위치
character_to_x_LEFT = 0
character_to_x_RIGHT = 0

#캐릭터 이동 속도
character_speed = 0.4

#무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_delay = pygame.image.load(os.path.join(image_path, "weapon_delay.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]
#무기 인터벌
timedelay = 30
#무기 제한시간
weapon_respawn = 0
#무기 제한 텍스트
isTextView = False
#무기 리스트
weapons = []
#무기 이동 속도
weapon_speed = 10
#충돌 무기, 장애물 정보 저장 변수
weapon_to_remove = -1 #무기
#장애물
ddong_to_remove = -1
ddong2_to_remove = -1
ddong3_to_remove = -1

def STAGE2():
    global character_speed, ddong_speed, Stage
    Stage = 2
    character_speed = 0.8
    ddong_speed = 11

def STAGE3():
    global character_speed, ddong_speed, Stage
    Stage = 3
    character_speed = 0.9
    ddong_speed = 13

def startScreen():
    keyEnter = False
    while True:
        screen.fill((0,0,0))
        font = pygame.font.SysFont("malgungothicsemilight", 30)
        title = font.render("게임을 시작하려면 엔터키를",True,(255, 255, 255))
        screen.blit(title, (50, screen_height / 2 - ((screen_height / 2) / 2)))
        title = font.render("누르세요.",True,(255, 255, 255))
        screen.blit(title, (180, 220))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit(0)
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    keyEnter = True 
            elif event.type==pygame.KEYUP:
                if event.key==pygame.K_RETURN:
                    keyEnter = False 
        if keyEnter:
            break
startScreen()

#이벤트 루프
running = True #게임이 진행 중인지
while running:
    dt = clock.tick(60)
    heartlife_timedelay() #게임화면의 초당 프레임 수를 설정
    timedelay += 1
    if weapon_respawn == 5:
        isTextView = True
        respawn_time = int((pygame.time.get_ticks() - ben_ticks) / 1000)
        if respawn_time == 5:
            weapon_respawn = 0
            isTextView = False
    for event in pygame.event.get(): #어떤 이벤트가 발생
        if event.type == pygame.QUIT: #창이 닫힌 이벤트 발생
            running = False #게임종료
        if event.type == pygame.KEYDOWN: #키가 눌러졌는지 확인 
            if event.key == pygame.K_LEFT: #캐릭터 왼쪽
                character_to_x_LEFT -= character_speed
            elif event.key == pygame.K_RIGHT: #캐릭터 오른쪽
                character_to_x_RIGHT += character_speed
            elif event.key == pygame.K_SPACE:
                if weapon_respawn == 0:
                    weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                    weapon_y_pos = character_y_pos
                    if timedelay >= 30 or invincibility_chk:
                        timedelay = 0
                        weapons.append([weapon_x_pos, weapon_y_pos])
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                character_to_x_LEFT = 0
            elif event.key == pygame.K_RIGHT:
                character_to_x_RIGHT = 0

    character_x_pos += (character_to_x_LEFT + character_to_x_RIGHT) * dt

    #가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
        
    #충돌 처리를 위한 캐릭터 좌표 가져오기
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    #생명하트 아이템 좌표
    heartlife_rect = heartlife.get_rect()
    heartlife_rect.left = heartlife_x_pos
    heartlife_rect.top = heartlife_y_pos

    #생명하트 땅 충돌시 제거
    if heartlife_y_pos >= 640 -28: #해상도y-28
        heartlife_speed = random.randint(1, 3)
        heartlife_respawn = 10
        heartlife_delay = pygame.time.get_ticks()
        heartlife_x_pos = random.randint(0, 640) #0~해상도y까지 랜덤
        heartlife_y_pos = -1 #하트제거부분


    #생명하트 생명력 제한
    if heartlife_chk:
        L_time1 = int((pygame.time.get_ticks() - heartlife_ticks) / 100)
        if L_time1 == 1:
            if Life < 3: #생명력이 3이하면
                Life += 1 #생명+1
                heartlife_chk = False
        if L_time1 <= 5: #1초안됨
            screen.blit(notice_font.render("생명 +1",True, (255, 255, 255)), 
            (character_x_pos -3, character_y_pos -20))

    
    #무기를 위로 쏘기
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons]
    #천장에 닿은 무기 제거
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]

    #장애물 위치
    ddong_y_pos += ddong_speed
    ddong2_y_pos += ddong_speed
    ddong3_y_pos += ddong_speed
    weapon_ben_y_pos += weapon_ben_speed
    invincibility_y_pos += invincibility_speed

    if weapon_ben_y_pos > screen_height:
        weapon_ben_y_pos = 0
        weapon_ben_x_pos = random.randint(0, screen_width - weapon_ben_width)

    if invincibility_y_pos > screen_height:
        invincibility_y_pos = 0
        invincibility_x_pos = random.randint(0, screen_width - invincibility_width)

    if ddong_y_pos > screen_height:
        ddong_y_pos = 0
        ddong_x_pos = random.randint(0, screen_width - ddong_width)

    if ddong2_y_pos > screen_height:
        ddong2_y_pos = 0
        ddong2_x_pos = random.randint(0, screen_width - ddong_width)

    if ddong3_y_pos > screen_height:
        ddong3_y_pos = 0
        ddong3_x_pos = random.randint(0, screen_width - ddong_width)

    

    weapon_ben_rect = weapon_ben.get_rect()
    weapon_ben_rect.left = weapon_ben_x_pos
    weapon_ben_rect.top = weapon_ben_y_pos

    invincibility_rect = invincibility.get_rect()
    invincibility_rect.left = invincibility_x_pos
    invincibility_rect.top = invincibility_y_pos

    ddong_rect = ddong.get_rect()
    ddong_rect.left = ddong_x_pos
    ddong_rect.top = ddong_y_pos

    ddong2_rect = ddong2.get_rect()
    ddong2_rect.left = ddong2_x_pos
    ddong2_rect.top = ddong2_y_pos

    ddong3_rect = ddong3.get_rect()
    ddong3_rect.left = ddong3_x_pos
    ddong3_rect.top = ddong3_y_pos

    #생명하트 캐릭터 충돌시 제거
    if character_rect.colliderect(heartlife_rect): #캐릭터와 생명하트 충돌시
        heartlife_speed = random.randint(1, 3)
        heartlife_respawn = 10
        heartlife_delay = pygame.time.get_ticks()
        heartlife_x_pos = random.randint(0, 800)
        heartlife_y_pos = -1
        heartlife_ticks = pygame.time.get_ticks()
        heartlife_chk = True
        

    #무적 아이템 충돌 처리
    if character_rect.colliderect(invincibility_rect):
        invincibility_ticks = pygame.time.get_ticks()
        invincibility_chk = True

    #무적 상태가 아닐 시 작동
    if invincibility_chk == False:
        #무기 제한 장애물 충돌 처리
        if character_rect.colliderect(weapon_ben_rect):
            ben_ticks = pygame.time.get_ticks()
            weapon_respawn = 5

        #장애물1 충돌 처리
        if character_rect.colliderect(ddong_rect):          
            Life_ticks = pygame.time.get_ticks()
            Life_chk = True
            if Life == 0:
                running = False #게임 종료
                break
        #장애물2 충돌 처리
        if character_rect.colliderect(ddong2_rect):       
            Life_ticks = pygame.time.get_ticks()
            Life_chk = True
            if Life == 0:
                running = False #게임 종료
                break
        #장애물3 충돌 처리
        if character_rect.colliderect(ddong3_rect):  
            Life_ticks = pygame.time.get_ticks()
            Life_chk = True
            if Life == 0:
                running = False #게임 종료
                break

    #장애물과 무기 충돌 처리
    for weapon_idx, weapon_val in enumerate(weapons):
        weapon_x_pos = weapon_val[0]
        weapon_y_pos = weapon_val[1]
        #무기 rect 정보 업데이트
        weapon_rect = weapon.get_rect()
        weapon_rect.left = weapon_x_pos
        weapon_rect.top = weapon_y_pos
        #충돌 체크1
        if weapon_rect.colliderect(ddong_rect):
            weapon_to_remove = weapon_idx #무기 없애기 위한 값 설정
            ddong_to_remove = weapon_idx #장애물 없애기 위한 값 설정
            score_chk = True             #추가점수를 위한 값 설정
            break
        #충돌 체크2
        if weapon_rect.colliderect(ddong2_rect):
            weapon_to_remove = weapon_idx #무기 없애기 위한 값 설정
            ddong2_to_remove = weapon_idx #장애물 없애기 위한 값 설정
            score_chk = True              #추가점수를 위한 값 설정
            break
        #충돌 체크3
        if weapon_rect.colliderect(ddong3_rect):
            weapon_to_remove = weapon_idx #무기 없애기 위한 값 설정
            ddong3_to_remove = weapon_idx #장애물 없애기 위한 값 설정
            score_chk = True              #추가점수를 위한 값 설정
            break
    #장애물 제거1
    if ddong_to_remove > -1:
        ddong_y_pos = ddong_to_remove
        ddong_to_remove =- 1
    #장애물 제거2
    if ddong2_to_remove > -1:
        ddong2_y_pos = ddong2_to_remove
        ddong2_to_remove =- 1
    #장애물 제거3
    if ddong3_to_remove > -1:
        ddong3_y_pos = ddong3_to_remove
        ddong3_to_remove =- 1
    #무기 제거
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1
    #화면에 그리기
    screen.blit(background, (0, 0)) # 배경 그리기장전
    # 무기 그리기
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
    screen.blit(stage, (0, screen_height - stage_height)) #스테이지 그리기
    #screen.blit(character, (character_x_pos, character_y_pos)) #캐릭터 그리기
    screen.blit(ddong, (ddong_x_pos, ddong_y_pos)) #장애물 그리기
    screen.blit(ddong2, (ddong2_x_pos, ddong2_y_pos)) #장애물 그리기
    screen.blit(ddong3, (ddong3_x_pos, ddong3_y_pos)) #장애물 그리기
    screen.blit(weapon_ben, (weapon_ben_x_pos, weapon_ben_y_pos)) #무기 제한 장애물 그리기 
    screen.blit(invincibility, (invincibility_x_pos, invincibility_y_pos)) #무적 아이템 그리기
    #생명하트 아이템그리기
    if heartlife_respawn == 0: #10초에서 0초로 내려가는데 0초가될시
        heartlife_y_pos += heartlife_speed
        screen.blit(heartlife, (heartlife_x_pos, heartlife_y_pos))
    #무기 장전
    if timedelay <= 30: 
        weapon_y = -1
        screen.blit(weapon_delay, (screen_width - 60, weapon_y))
    else: 
        weapon_delay_y = -1
        screen.blit(weapon, (screen_width - 60, weapon_delay_y))
    #무적 아이템
    if invincibility_chk:
        r_time = int((pygame.time.get_ticks() - invincibility_ticks) / 1000)
        if r_time == 3:
            invincibility_chk = False
        screen.blit(character2, (character_x_pos, character_y_pos)) #무적 캐릭터 그리기
    else:
        screen.blit(character, (character_x_pos, character_y_pos)) #캐릭터 그리기
    #경과 시간 표시 100초>1초 (역순)
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 #플레이 시간을 초 단위로 표시 하기
    time_t = game_font.render("시간 : {}".format(int(total_time - elapsed_time)), True, (255, 255, 255)) #시간표시
    screen.blit(time_t, (10, 10))
    #목숨
    if Life_chk:
        L_time = int((pygame.time.get_ticks() - Life_ticks) / 100) 
        if L_time == 1: 
            Life -= 1
            Life_chk = False
        if L_time <= 3:
            screen.blit(effect, (character_x_pos, character_y_pos-20))
    screen.blit(game_font.render("목숨 : {}".format(Life), True, (255, 255, 255)), (10, 600))
    #점수 그리기
    if score_chk:
        add_score += 10 # 100점씩 점수추가
        score_chk = False
    score = int(((pygame.time.get_ticks() - start_ticks) / 1000) + add_score)
    score *= scoreup1
    score_t = game_font.render("점수 : {}".format(int(score)), True, (255, 255, 255)) #점수
    screen.blit(score_t, (300, 10))
    #난이도
    if score >= 3000:
        STAGE2()
    if score >= 6000:
        STAGE3()
    screen.blit(game_font.render("스테이지 : {}".format(Stage), True, (255, 255, 255)), (140, 10))
    #무기제한 텍스트 그리기
    if isTextView:
        ben = notice_font.render("{}초동안 무기사용이 금지됩니다.".format(weapon_respawn - respawn_time), True, (0, 0, 0))
        screen.blit(ben, (70 , 100))
    #만약 시간이 0 이하이면 게임 종료
    if total_time - elapsed_time <= 0:
        game_result = "Timer Over"
        running = False
    #종료 버튼
    if exit_button.draw(): #종료 버튼
        running = False
    pygame.display.update() #화면 그리기
#게임 오버 메시지
msg = quit_font.render(game_result, True, (255, 255, 255))
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)

pygame.display.update() #화면 그리기

#대기 시간
pygame.time.delay(4000) #4초동안 대기후 게임꺼짐          
# pygame 종료
pygame.quit()


