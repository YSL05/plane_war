from os import kill
import random
import pygame

# 屏幕大小的常量
SCREEN_SIZE = pygame.Rect(0, 0, 480, 700)

class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏 精灵"""

    def __init__(self, image_name, speed = 1):
        
        # 调用父类的方法
        super().__init__()

        # 定义对象的属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed
    
    def update(self):
        
        # 在屏幕的垂直方向上移动
        self.rect.y = self.rect.y + self.speed

class Background(GameSprite):
    """游戏背景精灵"""

    def __init__(self, is_alt = False):
        
        super().__init__("./images/background.png")

        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        
        # 1、调用父类方法
        super().update()

        # 2、判断是否移出屏幕
        if self.rect.y >= SCREEN_SIZE.height:
            self.rect.y = -self.rect.height

class Enemy(GameSprite):
    """敌机精灵"""

    def __init__(self):
        
        # 调用父类方法 
        super().__init__("./images/enemy1.png")
        # 指定敌机初始速度
        self.speed = random.randint(1,3)
        # 指定敌机初始位置
        self.rect.bottom = 0
        self.rect.x = random.randint(0, SCREEN_SIZE.width - self.rect.width)
    def update(self):
        
        # 调用父类方法
        super().update()

        # 判断是否飞出屏幕
        if self.rect.y >= SCREEN_SIZE.height:
            
            # 销毁精灵
            self.kill()

class Hero(GameSprite):
    """英雄精灵"""

    def __init__(self):

        # 调用父类方法，设置图片和速度
        super().__init__("./images/me1.png", 0)

        # 设置初始位置
        self.rect.centerx = SCREEN_SIZE.centerx
        self.rect.bottom = SCREEN_SIZE.bottom - 120

        # 初始化子弹属性
        self.bullet_group = pygame.sprite.Group()

    def update(self):
        
        # 英雄在水平方向上移动
        temp_position = self.rect.x + self.speed
        if temp_position < 0:
            self.rect.x = self.rect.x
        elif temp_position > SCREEN_SIZE.width - self.rect.width:
            self.rect.x = self.rect.x
        else:
            self.rect.x = temp_position
    
    def fire(self):
        bullet = Bullet()

        bullet.rect.bottom = self.rect.y - 5
        bullet.rect.centerx = self.rect.centerx

        self.bullet_group.add(bullet)

class Bullet(GameSprite):
    """子弹精灵"""

    def __init__(self):
        super().__init__("./images/bullet1.png", -2)
    
    def update(self):

        # 调用父类方法沿垂直方向飞行
        super().update()

        # 如果超出屏幕删除子弹精灵
        if self.rect.y <= -self.rect.height:
            self.kill()
    
    def __del__(self):
        print("子弹被销毁")

