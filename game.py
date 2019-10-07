import pygame
from game_items import *
class Game(object):
    def __init__(self):
        self.main_window=pygame.display.set_mode((640,480))
        pygame.display.set_caption("贪吃蛇")
        # self.score=0
        self.score_label=Label()
        self.tip_label=Label(24,False)
        self.is_game_over=False
        self.is_pause=False
        self.food=Food()
        self.snake=Snake()
        # print(self.snake.body_list)
    def reset_game(self):
        self.is_game_over=False
        self.is_pause=False
        self.food.random_rect()
        self.snake.reset_snake()



    def start(self):
        clock=pygame.time.Clock()
        while(True):
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    return
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        return
                    elif event.key==pygame.K_SPACE:
                        if self.is_game_over:
                            self.reset_game()
                        else:
                            self.is_pause=not self.is_pause
                if not self.is_pause and not self.is_game_over:
                    if event.type == FOOD_UPDATE_EVENT:
                        self.food.random_rect()
                    if event.type==SNAEK_UPDATE_EVENT:
                        self.is_game_over=not self.snake.update()
                        # self.snake.update()

                    if event.type==pygame.KEYDOWN:
                        if event.key in(pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN):
                            self.snake.change_dir(event.key)


            self.main_window.fill(BACKGROUND_COLOR)
            if self.is_game_over:
                self.tip_label.draw(self.main_window,"游戏结束，按空格键开始新游戏......")
            elif self.is_pause:
                self.tip_label.draw(self.main_window,"游戏暂停，按空格键继续......")
            else:
                if self.snake.has_eat(self.food):
                    self.food.random_rect()
                    # self.snake.score += 1

            self.score_label.draw(self.main_window,"得分：%d"%self.snake.score)
            self.food.draw(self.main_window)
            self.snake.draw(self.main_window)
            pygame.display.update()
            clock.tick(60)
    def reset_geme(self):
        self.is_game_over=False
        self.is_pause=False
        self.score=0
        self.food.random_rect()




if (__name__ =="__main__"):
    pygame.init()
    Game()
    Game().start()
    pygame.quit()
