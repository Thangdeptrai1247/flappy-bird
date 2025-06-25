# flappy-bird

import pygame
import random
import os

pygame.init()
#chim
screen = pygame.display.set_mode((420,650))
pygame.display.set_caption("game4")
icon = pygame.image.load('FileGame/assets/yellowbird-upflap.png')
pygame.display.set_icon(icon)
class Bird():
    def __init__(self,image_path,pos):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image,(34,24))
        self.rect = self.image.get_rect(center=pos)
        self.velocity=0
        self.gravity=0.25
        
    def flap(self):
        self.velocity=-6.5
    def update(self, floor_y ):
        self.velocity += self.gravity
        self.rect.centery += self.velocity
        if self.rect.top <= 0:
            self.rect.top=0
            self.velocity = 0
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    def reset(self,pos):
        self.rect.center = pos
        self.velocity = 0
    def get_rect(self):
        return self.rect
class Game():
    #Diem khi choi
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.score = 0
        self.hscored = self.load_highscore()
        self.font = pygame.font.Font(None,30)
        self.background = pygame.image.load('FileGame/assets/background-night.png')
        self.background = pygame.transform.scale(self.background, (420, 650))
    def load_highscore(self):
            if os.path.exists('highscore.txt'):
                try:
                    with open('highscore.txt','r') as f:
                        return int(f.read())
                except:
                    return 0
            return 0
    def save_highscore(self):
        with open('highscore.txt','w') as f:
                f.write(str(int(self.hscored)))
    def draw_score(self):
        score_surf = self.font.render(f'score:{int(self.score)}',True,(255,255,255))
        score_rect = score_surf.get_rect(center=(200,30))
        self.screen.blit(score_surf,score_rect)     
            #Diem cao nhat
        hscore_surf = self.font.render(f'High score:{int(self.hscored)}',True,(255,255,255))
        hscore_rect = hscore_surf.get_rect(center=(200,80))
        self.screen.blit(hscore_surf,hscore_rect)
class Floor:
    def __init__(self, image_path, y_pos, speed):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image =pygame.transform.scale(self.image,(420,112))
        self.y = y_pos
        self.x =0
        self.speed = speed
    def update(self):
        self.x -= self.speed
        if self.x <= -420:
            self.x = 0
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        surface.blit(self.image, (self.x + 420, self.y))
class Pipe:
    def __init__(self,x, gap_y, gap_size, pipe_img, pipe_img_flipped):
        self.gap_size = gap_size
        self.pipe_img = pipe_img
        self.pipe_img_flipped =  pipe_img_flipped
        self.speed = 2        
        self.top = pipe_img_flipped.get_rect(midbottom=(x, gap_y - gap_size // 2))
        self.bottom = pipe_img.get_rect(midtop=(x, gap_y + gap_size // 2))
        self.passed = False
    def update(self, speed):
        self.top.centerx -= speed
        self.bottom.centerx -= speed
    def draw(self,surface, pipe_img, pipe_img_flipped):
        surface.blit(pipe_img_flipped, self.top)
        surface.blit(pipe_img, self.bottom)
    def is_off_screen(self):
        return self.top.right < 0 
    def check_collision(self, bird_rect):
        return bird_rect.colliderect(self.top) or bird_rect.colliderect(self.bottom)
class PipeManager:
    def __init__(self, pipe_img,pipe_img_flipped, gap_size, speed):
        self.pipes = []#danh sách các ống nước
        self.pipe_img = pipe_img
        self.pipe_img_flipped = pipe_img_flipped
        self.gap_size = gap_size
        self.speed = speed
    def spawn_pipe(self):
        gap_y = random.randint(150, 300)
        new_pipe = Pipe(450, gap_y, self.gap_size, self.pipe_img,self.pipe_img_flipped)
        self.pipes.append(new_pipe)
    def update(self):
        for pipe in self.pipes:
            pipe.update(self.speed)
        self.pipes =  [ pipe for pipe in self.pipes if not  pipe.is_off_screen()]
    def draw(self, surface):
        for pipe in self.pipes:
            pipe.draw(surface, self.pipe_img, self.pipe_img_flipped)
    def check_collision(self, bird_rect):
        for pipe in self.pipes:
            if pipe.check_collision(bird_rect):
                return True
        return False
    def check_passed_pipes(self, bird_rect, on_score_callback):
        for pipe in self.pipes:
            if not pipe.passed and pipe.top.right < bird_rect.left:
                pipe.passed = True
                on_score_callback()
class GameController():
    def __init__(self):
        self.bird = Bird('FileGame/assets/yellowbird-upflap.png', (212,325))
        self.floor = Floor('FileGame/assets/floor.png', 538, 2)
        pipe_img = pygame.image.load('FileGame/assets/pipe-green.png')
        pipe_img = pygame.transform.scale(pipe_img, (60, 400))
        pipe_img_flipped = pygame.transform.flip(pipe_img, False, True) 
        self.pipe_manager = PipeManager(pipe_img, pipe_img_flipped, 150, 2)
        self.game = Game(screen)
        self.running = True
        self.playing =  True
        self.waiting_to_start = True
        self.background = pygame.image.load('FileGame/assets/background-night.png')
        self.background = pygame.transform.scale(self.background, (420,650))
        self.game_started = False
    def run(self):
        SPAWN_PIPE = pygame.USEREVENT
        pygame.time.set_timer(SPAWN_PIPE, 1500)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        if not self.playing:
                            self.bird.reset((212,325))
                            self.pipe_manager.pipes.clear()
                            self.game.score = 0
                            self.playing =  True
                            self.game_started = True
                        elif not self.game_started:
                            self.game_started = True
                        else:
                            self.bird.flap()
                            wing_sound.play()
                elif event.type == SPAWN_PIPE and self.playing:
                    self.pipe_manager.spawn_pipe()
            screen.blit(self.background, (0,0))

            if self.waiting_to_start:
                self.bird.draw(screen)
                self.pipe_manager.draw(screen)
                self.floor.draw(screen)
                self.game.draw_score()
                message_img = pygame.image.load('FileGame/assets/message.png')
                message_rect = message_img.get_rect(center=(210, 300))
                screen.blit(message_img, message_rect)

            if self.playing:
                if self.game_started:
                    self.bird.update(self.floor.y)
                    self.floor.update()
                    self.pipe_manager.update()
                bird_rect = self.bird.get_rect()
                if self.pipe_manager.check_collision(bird_rect) or self.bird.get_rect().bottom >= self.floor.y:
                    self.playing= False
                    hit_sound.play()

                    if self.game.score > self.game.hscored:
                        self.game.hscored = self.game.score
                        self.game.save_highscore()
                self.pipe_manager.check_passed_pipes(self.bird.get_rect(), lambda:( point_sound.play(), setattr(self.game, 'score', self.game.score + 1)))
            screen.blit(self.background,(0,0))
            self.bird.draw(screen)
            self.pipe_manager.draw(screen)
            self.floor.draw(screen)
            self.game.draw_score()
            
            if not self.playing:
               
                message_img = pygame.image.load('FileGame/assets/message.png')
                message_rect = message_img.get_rect(center=(210, 300))
                screen.blit(message_img, message_rect)

            pygame.display.update()
            self.game.clock.tick(60)

#Âm thanh
wing_sound =  pygame.mixer.Sound('FileGame/sound/sfx_wing.wav')
hit_sound =  pygame.mixer.Sound('FileGame/sound/sfx_hit.wav')
point_sound =  pygame.mixer.Sound('FileGame/sound/sfx_point.wav')

if __name__ == '__main__':

    game  = GameController()
    game.run()
    pygame.quit() 


Đây là tựa game do tôi tạo ra, có sự hỗ trợ của AI, dù là người mới nhưng tôi mong người sẽ ủng hộ dự án này! có ý kiến thì hãy đóng góp(Use traslate google)
