import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 288
screen_height = 512
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird AI")

# Game assets
bird_images = [pygame.image.load('assets/bird-upflap.png').convert_alpha(),
               pygame.image.load('assets/bird-midflap.png').convert_alpha(),
               pygame.image.load('assets/bird-downflap.png').convert_alpha()]
pipe_image = pygame.image.load('assets/pipe.png').convert_alpha()
background_image = pygame.image.load('assets/background-day.png').convert()
ground_image = pygame.image.load('assets/base.png').convert()

# Game variables
gravity = 1
bird_movement = 0
pipe_gap = 150
pipe_frequency = 1500  # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
font = pygame.font.Font(None, 36)

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = bird_images
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += gravity
        self.rect.centery += self.velocity
        self.flap()

    def flap(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.velocity = -10

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, top):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.flip(pipe_image, False, top)
        self.rect = self.image.get_rect(midleft=(x, y))
        self.top_pipe = top
        self.passed = False

    def update(self, speed):
        self.rect.x -= speed

def create_pipe():
    random_pipe_pos = random.choice([200, 300, 400])
    bottom_pipe = Pipe(screen_width + 100, random_pipe_pos, False)
    top_pipe = Pipe(screen_width + 100, random_pipe_pos - pipe_gap, True)
    return bottom_pipe, top_pipe

bird_group = pygame.sprite.GroupSingle()
bird = Bird(50, screen_height // 2)
bird_group.add(bird)

pipe_group = pygame.sprite.Group()

game_over = False
game_speed = 2

def draw_floor():
    screen.blit(ground_image, (ground_scroll, 450))
    screen.blit(ground_image, (ground_scroll + 288, 450))

ground_scroll = 0

def display_score(score):
    score_surface = font.render(str(int(score)), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(screen_width // 2, 50))
    screen.blit(score_surface, score_rect)

def check_collision(bird_group, pipe_group):
    if bird_group.sprite.rect.top <= 0 or bird_group.sprite.rect.bottom >= 450:
        return True
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False):
        return True
    return False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_group.sprite.flap()
            if event.key == pygame.K_SPACE and game_over:
                game_over = False
                pipe_group.empty()
                bird_group.sprite.rect.center = (50, screen_height // 2)
                bird_group.sprite.velocity = 0
                score = 0
                last_pipe = pygame.time.get_ticks() - pipe_frequency

    screen.blit(background_image, (0, 0))
    pipe_group.draw(screen)
    bird_group.draw(screen)
    draw_floor()
    display_score(score)

    if not game_over:
        ground_scroll -= game_speed
        if abs(ground_scroll) > 288:
            ground_scroll = 0

        if pygame.time.get_ticks() - last_pipe > pipe_frequency:
            bottom_pipe, top_pipe = create_pipe()
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            last_pipe = pygame.time.get_ticks()

        pipe_group.update(game_speed)

        for pipe in pipe_group:
            if pipe.rect.right < bird_group.sprite.rect.left and not pipe.passed:
                score += 0.5
                pipe.passed = True
            if pipe.rect.left < -50:
                pipe.kill()

        game_over = check_collision(bird_group, pipe_group)
        bird_group.update()
    else:
        game_speed = 0
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(game_over_text, game_over_rect)
        restart_text = font.render("Press Space to Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        screen.blit(restart_text, restart_rect)

    pygame.display.update()

pygame.quit()
