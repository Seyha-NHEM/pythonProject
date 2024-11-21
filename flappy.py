import pygame
from pygame.locals import *
import random

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flying Ghost')

# Define font
font = pygame.font.SysFont('Bauhaus 93', 60)
small_font = pygame.font.SysFont('Bauhaus 93', 40)

# Define colors
white = (255, 255, 255)

# Define game variables
ground_scroll = 0

flying = False
game_over = False
pipe_frequency = 900  # Reduced to spawn pipes more frequently (in milliseconds)
last_pipe = pygame.time.get_ticks() - pipe_frequency
start_time = 0  # Time when the game starts
survival_time = 0  # Survival time in seconds
lives = 2  # Starting lives
pipe_gap = 100  # The gap between pipes

# Load sounds
flap_sound = pygame.mixer.Sound('img/audio/flap.wav')
collision_sound = pygame.mixer.Sound('img/audio/collision.wav')
score_sound = pygame.mixer.Sound('img/audio/score.wav')

# Load background music
pygame.mixer.music.load('img/background.mp3')
pygame.mixer.music.play(-1)  # Play the music in a loop

# Load images
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')
button_img = pygame.image.load('img/restart.png')


# High score handling
def get_high_score():
    try:
        with open('high_score.txt', 'r') as file:
            return int(file.read())
    except:
        return 0


def update_high_score(new_score):
    high_score = get_high_score()
    if new_score > high_score:
        with open('high_score.txt', 'w') as file:
            file.write(str(new_score))
        return new_score
    return high_score


# Load high score
high_score = get_high_score()


# Function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game():
    global lives, start_time, survival_time
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    lives = 2  # Reset lives
    start_time = pygame.time.get_ticks()  # Record the new start time
    survival_time = 0  # Reset survival time
    return score


# Initialize sprite groups
pipe_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 7):
            img = pygame.image.load(f"img/bird{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        global flying

        # Control the bird's vertical position when the mouse is pressed
        if flying:
            if pygame.mouse.get_pressed()[0] == 1:  # Mouse is held down
                self.vel = -12  # Move the bird upward faster
            else:
                self.vel = 6  # Gravity effect when mouse is not pressed

            self.vel += 0.5  # Gravity effect
            if self.vel > 12:  # Maximum falling speed
                self.vel = 12
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if not game_over:
            self.counter += 1
            if self.counter > 3:  # Update every 3 ticks to speed up animation
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                self.image = self.images[self.index]

            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.frames = []
        for num in range(1, 8):  # Assuming you have 7 frames for animation
            self.frames.append(pygame.image.load(f"img/frame{num}.png"))
        self.index = 0
        self.counter = 0  # Frame counter for animation
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect()

        # Top or Bottom pipe position
        if position == 1:
            self.rect.bottomleft = [x, y - pipe_gap // 2]  # Adjust top pipe position
        elif position == -1:
            self.rect.topleft = [x, y + pipe_gap // 2]  # Adjust bottom pipe position

    def update(self):
        global scroll_speed
        # Move the pipe
        self.rect.x -= scroll_speed

        # Animate the frame
        self.counter += 1
        if self.counter > 5:  # Adjust for animation speed
            self.counter = 0
            self.index += 1
            if self.index >= len(self.frames):
                self.index = 0
            self.image = self.frames[self.index]

        # Remove the pipe if it goes off screen
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

run = True
while run:
    clock.tick(fps)
    screen.blit(bg, (0, 0))
    pipe_group.draw(screen)
    bird_group.draw(screen)
    bird_group.update()
    screen.blit(ground_img, (ground_scroll, 768))

    # Calculate and display survival time as the score
    if flying and not game_over:
        survival_time = (pygame.time.get_ticks() - start_time) // 1000
    draw_text(f"Sec: {survival_time} s", font, white, int(screen_width / 1.25), 20)
    draw_text(f"Lives: {lives}", font, white, 20, 20)
    # Update scroll speed based on survival time
    scroll_speed = 5 + (survival_time // 10)  # Increase speed by 1 every 10 seconds survived

    if flying and not game_over:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            # Randomly decide the pipe's position (top or bottom)
            pipe_position = random.choice([1, -1])  # 1 for top, -1 for bottom
            pipe_y = random.randint(150, screen_height - 150 - pipe_gap)  # Ensure a safe gap
            new_pipe = Pipe(screen_width, pipe_y, pipe_position)
            pipe_group.add(new_pipe)
            last_pipe = time_now

        pipe_group.update()

        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        if lives > 1:
            lives -= 1
            collision_sound.play()
            flappy.rect.x = 100
            flappy.rect.y = int(screen_height / 2)
            flying = False
        else:
            game_over = True
            flying = False
            high_score = update_high_score(survival_time)

    if flappy.rect.bottom >= 768:
        if lives > 1:
            lives -= 1
            flappy.rect.x = 100
            flappy.rect.y = int(screen_height / 2)
            flying = False
        else:
            game_over = True
            flying = False
            high_score = update_high_score(survival_time)

    if game_over:
        draw_text("Game Over!", font, white, screen_width // 2 - 100, screen_height // 2 - 100)
        draw_text(f"High Score: {high_score}", small_font, white, screen_width // 2 - 75, screen_height // 2 + 40)
        button.rect.y = screen_height // 2 - 40
        if button.draw():
            game_over = False
            survival_time = 0  # Reset survival time
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
            flying = True

    pygame.display.update()

pygame.quit()
