import pygame
import random

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Ustawienia gry
GRAVITY = 0.5
BIRD_JUMP = -10
PIPE_WIDTH = 80
PIPE_GAP = 150
PIPE_VELOCITY = 3

# Załadowanie obrazów
bird_img = pygame.Surface((40, 30))
bird_img.fill((255, 255, 0))

class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.img = bird_img

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def jump(self):
        self.velocity = BIRD_JUMP

class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - (self.height + PIPE_GAP))

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.top_rect)
        pygame.draw.rect(screen, (0, 255, 0), self.bottom_rect)

    def update(self):
        self.x -= PIPE_VELOCITY
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

def check_collision(bird, pipes):
    for pipe in pipes:
        if bird.img.get_rect(topleft=(bird.x, bird.y)).colliderect(pipe.top_rect) or bird.img.get_rect(topleft=(bird.x, bird.y)).colliderect(pipe.bottom_rect):
            return True
    if bird.y > SCREEN_HEIGHT or bird.y < 0:
        return True
    return False

def main():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    running = True

    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()

        bird.update()
        
        if pipes[-1].x < SCREEN_WIDTH - 200:
            pipes.append(Pipe())
        
        for pipe in pipes:
            pipe.update()

        if pipes[0].x < -PIPE_WIDTH:
            pipes.pop(0)
            score += 1

        if check_collision(bird, pipes):
            running = False

        screen.fill(WHITE)
        bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)
        pygame.display.flip()

    pygame.quit()
    print(f'Game Over! Your score: {score}')

if __name__ == "__main__":
    main()
