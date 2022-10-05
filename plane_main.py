import pygame
from plane_sprites import *

# 屏幕大小的常量
SCREEN_SIZE = pygame.Rect(0, 0, 480, 700)
# 刷新的帧率的常量
FRAME_PER_SEC = 60
# 创建敌机的定时常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 创建发射子弹的定时常量
HERO_FIRE_EVENT = pygame.USEREVENT + 1
# 英雄移动的速度
HERO_SPEED = 5
# 子弹发射的时间间隔
BULLET_TIME = 200
# 敌机生成的时间间隔
ENEMY_TIME = 500



class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self):
        print("游戏初始化")
        # 1、创建游戏的窗口
        self.screen = pygame.display.set_mode(SCREEN_SIZE.size)

        # 2、创建游戏的时钟
        self.clock = pygame.time.Clock()

        # 3、调用私有方法，完成精灵和精灵组的创建
        self.__create_sprites()

        # 4、设置定时器事件 - 创建敌机
        pygame.time.set_timer(CREATE_ENEMY_EVENT, ENEMY_TIME)
        pygame.time.set_timer(HERO_FIRE_EVENT, BULLET_TIME)

    def __create_sprites(self):
        
        # 创建背景精灵和精灵组
        bg1 = Background()
        bg2 = Background(True)
        self.back_group =  pygame.sprite.Group(bg1, bg2)

        # 创建敌机的精灵组
        self.enemy_group = pygame.sprite.Group()

        # 创建英雄的精灵及精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)


    def start_game(self):
        print("游戏开始")
        while True:
            # 1、设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            # 2、事件监听
            self.__event_handler()
            # 3、碰撞检测
            self.__check_collide()
            # 4、更新/绘制图样
            self.__update_sprites()
            # 5、更新显示
            pygame.display.update()

    def __event_handler(self):
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            
            if event.type == CREATE_ENEMY_EVENT:
                
                # 创建敌机精灵
                enemy = Enemy()

                # 添加到敌机精灵组中
                self.enemy_group.add(enemy)

            if event.type == HERO_FIRE_EVENT:
                
                print("发送子弹")
                self.hero.fire()
            
            # 读取玩家输入控制英雄移动
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_RIGHT]:
                self.hero.speed = HERO_SPEED
            elif keys_pressed[pygame.K_LEFT]:
                self.hero.speed = -HERO_SPEED
            else:
                self.hero.speed = 0
            
    def __check_collide(self):
        
        # 子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullet_group, self.enemy_group, True, True)
        
        # 敌机摧毁英雄
        ememies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)

        # 判断列表是否有内容
        if len(ememies) > 0:
            
            # 英雄牺牲
            self.hero.kill()
            # 游戏结束
            PlaneGame.__game_over()

    def __update_sprites(self):
        
        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullet_group.update()
        self.hero.bullet_group.draw(self.screen)

    @staticmethod
    def __game_over():

        print("游戏结束")
        pygame.quit()
        exit()


if __name__ == '__main__':

    # 创建游戏对象
    game = PlaneGame()

    # 启动游戏
    game.start_game()