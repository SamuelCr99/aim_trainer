import pygame 
import math
import random

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
WHITE = ((255, 255, 255))
RED = ((255, 0, 0))
BLACK = ((0,76,130))

FPS = 60 # frames per second setting
fpsClock = pygame.time.Clock()

# Set values for gameplay
max_number_of_targets = 10
number_of_targets = 1
target_max_radius = 40
target_starting_radius = 1
change_speed = 0.25

class Target: 
    def __init__(self):
        self.x = random.randint(target_max_radius,WIDTH-target_max_radius)
        self.y = random.randint(target_max_radius,HEIGHT-target_max_radius)
        self.radius = target_starting_radius
        self.expanding = True
    
    def draw_target(self):
        pygame.draw.circle(WIN, RED, (self.x, self.y), self.radius)
        pygame.draw.circle(WIN, WHITE, (self.x, self.y), self.radius*0.75)
        pygame.draw.circle(WIN, RED, (self.x, self.y), self.radius*0.4)

    def handle_expansion(self):
        if self.expanding: 
            self.radius += change_speed
        else: 
            self.radius -= change_speed

        if self.radius >= target_max_radius:
            self.expanding = False

        if self.radius <= 0:
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


def main():
    global number_of_targets
    pygame.init()
    # Create all initial targets
    targets = create_targets(number_of_targets)
    tick = 0
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
                        # Remove the target
                        targets.remove(target)
                

        while len(targets) < number_of_targets:
            targets.append(Target())

        WIN.fill(BLACK)

        # Make target expand and shrink 
        for target in targets: 
            if target.handle_expansion() == "Remove":
                targets.remove(target)
            target.draw_target()

        pygame.display.update()
        fpsClock.tick(FPS)
        tick += 1

        # Add 1 target per second, this to give game a short warm up
        if tick == FPS and len(targets) < max_number_of_targets: 
            tick = 0
            number_of_targets += 1
            



if __name__ == "__main__":
    main()