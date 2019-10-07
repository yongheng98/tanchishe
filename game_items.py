import pygame
import random
BACKGROUND_COLOR=(232,232,232)
SCORE_TEXT_COLOR=(192,192,192)
TIP_TEXT_COLOR=(64,64,64)
SCREEN_RECT=pygame.Rect(0,0,640,480)
CELL_SIZE=20
FOOD_UPDATE_EVENT=pygame.USEREVENT
SNAEK_UPDATE_EVENT=pygame.USEREVENT+1
class Label(object):
    def __init__(self,size=48,is_score=True):
        self.font=pygame.font.SysFont("simhei",size)
        self.is_score=is_score
    def draw(self,window,text):
        color=SCORE_TEXT_COLOR if self.is_score else TIP_TEXT_COLOR
        text_surface=self.font.render(text,True,color)
        text_rect=text_surface.get_rect()
        window_rect=window.get_rect()
        if self.is_score:
            text_rect.bottomleft=window_rect.bottomleft
        else:
            text_rect.center=window_rect.center

        # text_rect.bottomleft=window_rect.bottomleft
        # text_rect.y=window_rect.height-text_rect.height
        # print(text_rect)
        window.blit(text_surface,text_rect)
class Food(object):
    def __init__(self):
        self.color=(255,0,0)
        self.score=10
        self.rect=pygame.Rect(0,0,CELL_SIZE,CELL_SIZE)
        self.random_rect()
    def draw(self,window):
        if self.rect.w<CELL_SIZE:
            self.rect.inflate_ip(2,2)
        pygame.draw.ellipse(window,self.color,self.rect)

    def random_rect(self):
        col=SCREEN_RECT.w/CELL_SIZE-1
        row=SCREEN_RECT.h/CELL_SIZE-1
        x=random.randint(0,col)*CELL_SIZE
        y=random.randint(0,row)*CELL_SIZE
        self.rect=pygame.Rect(x,y,CELL_SIZE,CELL_SIZE)
        pygame.time.set_timer(FOOD_UPDATE_EVENT,30000)
class Snake(object):
    def __init__(self):
        self.dir=pygame.K_RIGHT
        self.score=0
        self.time_interval=500
        self.color=(64,64,64)
        self.body_list=[]
        self.reset_snake()
    def reset_snake(self):
        self.dir=pygame.K_RIGHT
        self.score=0
        self.time_interval=500
        self.body_list.clear()
        for i in range(3):
            self.add_node()
    def add_node(self):
        if self.body_list:
            head=self.body_list[0].copy()
        else:
            head=pygame.Rect(-CELL_SIZE,0,CELL_SIZE,CELL_SIZE)
        if self.dir==pygame.K_RIGHT:
            head.x+=CELL_SIZE
        elif self.dir==pygame.K_LEFT:
            head.x-=CELL_SIZE
        elif self.dir==pygame.K_UP:
            head.y-=CELL_SIZE
        elif self.dir==pygame.K_DOWN:
            head.y+=CELL_SIZE
        self.body_list.insert(0,head)
        pygame.time.set_timer(SNAEK_UPDATE_EVENT,self.time_interval)
    def draw(self,window):
        for idx,rect in enumerate(self.body_list):
            pygame.draw.rect(window,self.color,rect.inflate(-2,-2),idx==0)
    def update(self):
        body_list_copy=self.body_list.copy()
        self.add_node()
        self.body_list.pop()
        if self.is_dead():
            self.body_list=body_list_copy
            return False
        return True

    def change_dir(self,to_dir):
        hor_dirs=(pygame.K_RIGHT,pygame.K_LEFT)
        ver_dirs=(pygame.K_UP,pygame.K_DOWN)
        if ((self.dir in hor_dirs and to_dir not in hor_dirs)or(self.dir in ver_dirs and to_dir not in ver_dirs)):
            self.dir=to_dir
    def has_eat(self,food):
        if self.body_list[0].contains(food.rect):
            self.score+=food.score
            if self.time_interval>100:
                self.time_interval-=50
            self.add_node()
            return True
        return False
    def is_dead(self):
        head=self.body_list[0]
        if not SCREEN_RECT.contains(head):
            return True
        for body in self.body_list[1:]:
            if head.contains(body):
                return True
        return False







