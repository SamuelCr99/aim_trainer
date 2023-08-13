import pygame 
import math
import random
import time 
import pygame_widgets
from pygame_widgets.button import Button

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
WHITE = ((255, 255, 255))
RED = ((255, 0, 0))
BACKGROUND_C = ((0,76,130))
BLACK = (0,0,0)
GREEN = ((0, 255, 0))
ORANGE = ((255, 165, 0))

FPS = 60 # frames per second setting
fpsClock = pygame.time.Clock()

# Set values for gameplay
max_number_of_targets = 1
number_of_targets = 1
target_max_radius = 40
target_starting_radius = 1
change_speed = 0.25
expand_targets = True
main_menu_loop = True

class Target: 
    def __init__(self):
        self.x = random.randint(target_max_radius,WIDTH-target_max_radius)
        self.y = random.randint(target_max_radius,HEIGHT-target_max_radius)
        self.radius = target_starting_radius
        self.expanding = expand_targets
        self.alive_frames = 0
    
    def draw_target(self):
        pygame.draw.circle(WIN, RED, (self.x, self.y), self.radius)
        pygame.draw.circle(WIN, WHITE, (self.x, self.y), self.radius*0.75)
        pygame.draw.circle(WIN, RED, (self.x, self.y), self.radius*0.4)

    def handle_expansion(self):
        if self.expanding:
            # Function for handling the growing and shrinking of the target
            if self.expanding: 
                self.radius += change_speed
            else: 
                self.radius -= change_speed

            if self.radius >= target_max_radius:
                self.expanding = False

            if self.radius <= 0:
                return "Remove"
        else: 
            self.radius = target_max_radius
            self.alive_frames += 1
            if self.alive_frames == 60:
                return "Remove"


def clicked_circle(mouse_pos, target):
    if math.sqrt((mouse_pos[0] - target.x)**2 + (mouse_pos[1] - target.y)**2) < target.radius:
        return True

    return False

def create_targets(num):
    targets = []
    for _ in range(num):
        targets.append(Target())
    return targets

def set_easy():
    global main_menu_loop
    global max_number_of_targets
    global target_max_radius
    global change_speed

    main_menu_loop = False
    max_number_of_targets = 20
    target_max_radius = 50
    change_speed = 0.1




def set_medium():
    global main_menu_loop
    global max_number_of_targets
    global target_max_radius
    global change_speed

    main_menu_loop = False
    max_number_of_targets = 10
    target_max_radius = 40
    change_speed = 0.25


def set_hard():
    global main_menu_loop
    global max_number_of_targets
    global target_max_radius
    global change_speed

    main_menu_loop = False
    max_number_of_targets = 5
    target_max_radius = 20
    change_speed = 0.5

def menu(font):
    text = font.render("Select Difficulty", True, BLACK)
    text_rect = pygame.Rect(WIDTH/2 - 150, 200, 0, 0)
    WIN.blit(text, text_rect)
    Button(WIN, 50, 300, 200, 75, text="Easy", inactiveColour=GREEN, hoverColour=GREEN, onClick=lambda: set_easy())
    Button(WIN, 300, 300, 200, 75, text="Medium", inactiveColour=ORANGE, hoverColour=ORANGE, onClick=lambda: set_easy())
    Button(WIN, 550, 300, 200, 75, text="Hard", inactiveColour=RED, hoverColour=RED, onClick=lambda: set_easy())

    while main_menu_loop:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit()
        pygame_widgets.update(events)
        pygame.display.update()

def main():
    pygame.init()
    global number_of_targets
    font = pygame.font.SysFont('Monospace', 30)

    WIN.fill(BACKGROUND_C)
    menu(font)

    points = 0
    # Create all initial targets
    targets = create_targets(number_of_targets)
    tick = 0
    start_time = time.time()
    while(1): 
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN: 
                mouse_pos = pygame.mouse.get_pos()

                # Check if click has hit any of the targets
                for target in targets:
                    if clicked_circle(mouse_pos, target):
                        points += 1
                        targets.remove(target)
                

        while len(targets) < number_of_targets:
            targets.append(Target())

        WIN.fill(BACKGROUND_C)

        # Make target expand and shrink 
        for target in targets: 
            if target.handle_expansion() == "Remove":
                targets.remove(target)
            target.draw_target()

        # Draw score
        text = font.render(f'Score: {points}', True, BLACK)
        textRect = pygame.Rect(10, 0, 0, 0)
        WIN.blit(text, textRect)

        # Draw score
        time_left = 30 - int(time.time() - start_time)
        text = font.render(f'Time left: {time_left}', True, BLACK)
        textRect = pygame.Rect(550, 0, 0, 0)
        WIN.blit(text, textRect)

        if time_left <= 0: 
            print(f"Game over, your score was: {points}")
            break


        pygame.display.update()
        fpsClock.tick(FPS)
        tick += 1

        # Add 1 target per second, this to give game a short warm up
        if tick == FPS and len(targets) < max_number_of_targets: 
            tick = 0
            number_of_targets += 1
            



if __name__ == "__main__":
    main()