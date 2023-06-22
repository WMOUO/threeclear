import pygame,os,random

#變數
fps = 60
w = 1260
h = 960
pressed = False
checked = False

#圖片
bg_png = pygame.image.load(os.path.join('picture','background.png'))
fire_png = pygame.image.load(os.path.join('picture','fire.png'))
water_png = pygame.image.load(os.path.join('picture','water.png'))
wind_png = pygame.image.load(os.path.join('picture','wind.png'))
img = [fire_png,water_png,wind_png]

#
pygame.init()
window = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()
pygame.display.set_caption("三消遊戲")
white = [255,255,255]

#生成
def map_clear():
    global map
    map = [[0 for _ in range(10)]for _ in range(10)]

def move_clear():
    global move
    move = []
    return

def exp_clear():
    global exp
    exp = []
    return

#圖片顯示
def map_able():
    window.blit(bg_png,[0,0])
    for i in range(10):
        for u in range(10):
            window.blit(img[map[i][u]],[u*90+30,i*90+30])#pygame x,y須注意與陣列不同

#圖片生成
def gamemap():
    for i in range(10):
        for u in range(10):
            if map[i][u] == 0:
                while True:
                    r_num = random.randint(0,2)
                    if i >= 2 and u >= 2:
                        if (map[i-1][u] != r_num or map[i-2][u] != r_num) and (map[i][u-1] != r_num or map[i][u-2] != r_num):
                            break
                    elif i >= 2 :
                        if map[i-1][u] != r_num or map[i-2][u] != r_num:
                            break
                    elif u >= 2 :
                        if map[i][u-1] != r_num or map[i][u-2] != r_num:
                            break
                    else:
                        break
                map[i][u] = r_num
    map_able()
    return

#紀錄座標
def map_move(x,y):
    move.append([(y-30)//90,(x-30)//90])
    return

#物品移動
def element_move():
    if (move[0][0] == move[1][0] or move[0][1] == move[1][1]) and (move[0][0] != move[1][0] or move[0][1] != move[1][1]):
        map[move[0][0]][move[0][1]],map[move[1][0]][move[1][1]] = map[move[1][0]][move[1][1]],map[move[0][0]][move[0][1]]
        move[0],move[1] = move[1],move[0]
    else:
        print("con't move")
        print(move)
    return

#檢查是否有連續
def check():
    for i in range(2,10):
        for u in range(2,10):
            if i >= 2:
                if map[i][u] == map[i-1][u]== map[i-2][u]:
                    if(i,u) not in exp:
                        exp.append((i,u))
                    if(i-1,u) not in exp:
                        exp.append((i-1,u))
                    if(i-2,u) not in exp:
                        exp.append((i-2,u))
            if u >= 2:
                if map[i][u] == map[i][u-1]== map[i][u-2]:
                    if(i,u) not in exp:
                        exp.append((i,u))
                    if(i,u-1) not in exp:
                        exp.append((i,u-1))
                    if(i,u-2) not in exp:
                        exp.append((i,u-2))
    if len(exp) == 0:
        element_move()
        map_able()
    return

#將連續方塊消失
def explosion():
    for i in exp:
        map[i[0]][i[1]] = 0
        return

#降落
def down():
    for i in range(9,-1,-1):
        for u in range(10):
            if map[i][u] == 0:
                map[i][u] = map[i-1][u]
                map[i-1][u] = 0
                return
                

#主體
map_clear()
move_clear()
exp_clear()
gamemap()
while True:
    mouse_x,mouse_y = pygame.mouse.get_pos()
    mouse_leftpressed = pygame.mouse.get_pressed()
    if checked == True:
        check()
        move_clear()
        explosion()
        down()
        gamemap()
        exp_clear()
        checked = False
    for event in pygame.event.get():
        if mouse_leftpressed[0] == True:
            map_move(mouse_x,mouse_y)
            if pressed == False:
                pressed = True
            else:
                element_move()
                map_able()
                checked = True
                pressed = False
        if event.type == pygame.QUIT:
            pygame.quit()
    clock.tick(fps)
    pygame.display.update()
