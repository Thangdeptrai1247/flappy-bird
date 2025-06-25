import pygame
import random
from remove_background_tool import remove_white_background

width,height =  1279,673
Ground_y = 450
pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Dinor Run')
clock = pygame.time.Clock()


#Lớp kủng long
class Player():
    def __init__(self, x, y, Ground_y):
        self.image = pygame.image.load('Duanluyentap/khunglong_cleaned.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100,100))
        self.image = pygame.transform.flip(self.image, True, False)
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(midbottom=(x + 40, Ground_y))
        mask_image = pygame.Surface((100, 100), pygame.SRCALPHA)
        reduced_image = pygame.transform.scale(self.image, (70, 90))  # giảm vùng va chạm
        mask_image.blit(reduced_image, ((100 - 70)//2, (100 - 90)//2))  # căn giữa
        self.mask = pygame.mask.from_surface(mask_image)
        self.velocity_y = 0
        self.is_jumping = False
        self.Ground_y = Ground_y
    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -15
            self.is_jumping = True
    def update(self):
        self.velocity_y += 1
        self.rect.y += self.velocity_y
        if self.rect.bottom >= self.Ground_y:
            self.rect.bottom = self.Ground_y
            self.is_jumping = False
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
#Xương rồng
class Obstacle:
    def __init__(self, ground_y):
        self.image = pygame.image.load('Duanluyentap/cactus_cleaned.png').convert_alpha()
        self.image.set_colorkey((255,255,255))
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(midbottom=(width + 20, ground_y))
        mask_image = pygame.Surface((100, 100), pygame.SRCALPHA)
        reduced_image = pygame.transform.scale(self.image, (60, 80))  # tùy chỉnh nhỏ lại
        mask_image.blit(reduced_image, ((100 - 60)//2, (100 - 80)//2))  # căn giữa
        self.mask = pygame.mask.from_surface(mask_image)
        self.passed = False
    def update(self):
        self.rect.x -= 8
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    def is_off_screen(self):
        return self.rect.right < 0
#Nền đất

#Điểm số
class Score:
    def __init__(self):
        self.value =  0
        self.font = pygame.font.SysFont('consolas', 30)
    def draw(self, screen):
        text = self.font.render(f'score:{self.value}', True, (0,0,0))
        screen.blit(text, (10,10))
#Lớp game hoạt động
class Game:
    def __init__(self):
        self.bg = pygame.image.load('Duanluyentap/background-pixel-art-game-interface-design-2d-design-blue-sky-white-clouds-green-grass_148553-732.jpg')
        self.bg = pygame.transform.scale(self.bg, (width, height))
        self.ground_y = 535
        self.player = Player(100, self.ground_y - 80, self.ground_y)
        self.score = Score()
        self.obstacles = []
        self.spawn_timer = 0
        self.running = True
    def reset(self):
        self.__init__()
    def spawn_obstacle(self):
        self.obstacles.append(Obstacle(self.ground_y))
    def draw(self, screen):
        screen.blit(self.bg, (0, 0))                                  
        for obs in self.obstacles:
            obs.draw(screen)
        self.player.draw(screen)
        self.score.draw(screen)
    def update(self):
        self.player.update()
        self.spawn_timer += 1
        if self.spawn_timer >= 90:
            self.spawn_obstacle()
            self.spawn_timer = 0
        for obs in self.obstacles:
            obs.update()
            print(f'[DEBUG] Player X:{self.player.rect.x}, Obstacle X:{obs.rect.centerx}, Passed: {obs.passed}')
            if not obs.passed  and obs.rect.centerx < self.player.rect.centerx:
                obs.passed = True
                self.score.value += 1
                print('[INFO] Đã cộng điểm')
        
            offset = (obs.rect.x - self.player.rect.x, obs.rect.y - self.player.rect.y)
            if self.player.mask.overlap(obs.mask, offset):
                print('[INFO] Va chạm xaayr ra')
                self.running =  False
        self.obstacles = [obs for obs in self.obstacles if not obs.is_off_screen()]            
     

#Hệ thống chạy chính
def main():
    game = Game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if game.running:
                    game.player.jump()
                else:
                    game.reset()

        if game.running:
            game.update()
            game.draw(screen)
        if not game.running:
            font = pygame.font.SysFont('consolas', 40)
            text = font.render('Game over, nhấn space để bắt đầu lại', True, (200,0,0))
            text_rect = text.get_rect(center = (width // 2, height //2))
            screen.blit(text, text_rect)
        
        pygame.display.update()
        clock.tick(60)
if __name__ == '__main__':
    main()
    
