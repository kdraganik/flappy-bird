import pygame
import random

WHITE = (255, 255, 255)

FPS = 30
WIDTH = 400
HEIGHT = 600
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
GRAVITY = .5
JUMP = -5

class Bird:
    def __init__(self, x=50):
        self.width = BIRD_WIDTH
        self.height = BIRD_HEIGHT
        self.x = x
        self.y = HEIGHT // 2
        self.velocity = 0
        self.images = [pygame.image.load("assets/yellowbird-downflap.png"), pygame.image.load("assets/yellowbird-midflap.png"), pygame.image.load("assets/yellowbird-upflap.png")]
        self.imageIdx = 0
        self.wingAudio = "assets/wing.wav"

    
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def render(self, screen, timmer):
        rect = self.images[0].get_rect()
        rect.x = self.x
        rect.y = self.y
        if timmer % 2 == 0:
            self.imageIdx = (self.imageIdx + 1) % 3
        screen.blit(self.images[self.imageIdx], rect)
        

    def jump(self):
        self.velocity = JUMP

class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.y_offset = random.randint(0, 200)
        self.speed = 5
        self.imageBottom = pygame.image.load("assets/pipe-green.png")
        self.imageTop = pygame.transform.flip(pygame.image.load("assets/pipe-green.png"), False, True)
        self.past = False

    def update(self):
        self.x -= self.speed

    def render(self, screen):
        rect = self.imageTop.get_rect()
        rect.x = self.x
        rect.y = self.y_offset - 200
        screen.blit(self.imageTop, rect)
        rect = self.imageBottom.get_rect()
        rect.x = self.x
        rect.y = self.y_offset + 250
        screen.blit(self.imageBottom, rect)

    def is_colliding(self, bird):
        image_rect = self.imageBottom.get_rect()
        pipe_width = image_rect.width
        pipe_height = image_rect.height
        upper_limit = self.y_offset - 200 + pipe_height
        lower_limit = self.y_offset + 250
        return (((bird.x + bird.width) >= self.x and 
                bird.x <= self.x + pipe_width) and
                (bird.y <= upper_limit or
                bird.y + bird.height >= lower_limit))

    def is_off_screen(self):
        return self.x < -50
    
    def is_past(self, bird):
        if not self.past:
            image_rect = self.imageBottom.get_rect()
            pipe_width = image_rect.width
            if bird.x > self.x + pipe_width:
                self.past = True
                return True
        return False

class Ground:
    def __init__(self):
        self.x = 0
        self.y = HEIGHT - 100
        self.image = pygame.transform.scale(pygame.image.load("assets/base.png"), (WIDTH, 100))
    
    def render(self, screen):
        rect = self.image.get_rect()
        rect.x = self.x
        rect.y = self.y
        screen.blit(self.image, rect)

    def is_colliding(self, bird):
        return (bird.y + bird.height) > self.y

class Game:
    def __init__(self):
        self.running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.bg_image = pygame.transform.scale(pygame.image.load("assets/background-day.png"), (WIDTH, HEIGHT))
        self.bird = Bird()
        self.ground = Ground()
        self.pipes = []
        self.timmer = 50
        self.points = 0
        self.audioMixer = pygame.mixer.music
        pygame.display.set_caption("Flappy Bird")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird.jump()
                    self.audioMixer.load(self.bird.wingAudio)
                    self.audioMixer.play()

    def update_game(self):
        if self.timmer == 0:
            self.pipes.append(Pipe())
            self.timmer = 50
        self.timmer -= 1
        self.bird.update()
        for i in range(len(self.pipes) - 1):
            self.pipes[i].update()
            if self.pipes[i].is_off_screen():
                self.pipes.pop(i)
            if self.pipes[i].is_past(self.bird):
                self.points+=1
                print(self.points)


    def render_game(self):
        rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.screen.blit(self.bg_image, rect)
        self.bird.render(self.screen, self.timmer)
        for pipe in self.pipes:
            pipe.render(self.screen)
        self.ground.render(self.screen)
        font = pygame.font.SysFont(None, 24)
        img = font.render(str(self.points), True, (255, 0, 0))
        self.screen.blit(img, (WIDTH / 2, 20))
        pygame.display.flip()

    def handle_game_over(self):
        if self.bird.y < 0:
            self.running = False

        if self.ground.is_colliding(self.bird):
            self.running = False

        for pipe in self.pipes:
            if pipe.is_colliding(self.bird):
                self.running = False

    def run(self):
        while self.running:
            self.clock.tick(FPS)
                
            self.handle_events()
            self.update_game()
            self.render_game()
            self.handle_game_over()

        pygame.quit()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()