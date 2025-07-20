# Pygame stuff
import pygame
from pygame.locals import *

# Object interactions
from Ball import Ball
from collision import check_collision, spacial_partitioned_collisions

# Misc stuff
import time
import random
import sys

# Main
if __name__ == '__main__':
    BALL_RADIUS = 5 
    NUM_BALLS = 200 
    WINDOW_SIZE = (1000, 1000)
    BACKGROUND_COLOR = (0,0,0)
    TARGET_FPS = 100

    # Setup the pygame window
    pygame.init()
    screen = pygame.display.set_mode(
        WINDOW_SIZE,
        flags=pygame.RESIZABLE
    )
    screen.fill(BACKGROUND_COLOR)
    pygame.display.set_caption("Object Interaction Simulation")

    # TODO: make balls more generic for future objects
    balls = []
    # Create some balls
    for i in range(NUM_BALLS):
        balls.append(Ball(
            surface    = pygame.display.get_surface(),
            color      = pygame.Color(
                random.randint(50, 255),
                random.randint(50, 255),
                random.randint(50, 255)
            ),
            center     = (random.randint(0, WINDOW_SIZE[0]), random.randint(0, WINDOW_SIZE[1])),
            init_x_vel = [random.randint(5, 50), random.choice([-1, 1])],
            init_y_vel = [random.randint(5, 50), random.choice([-1, 1])],
            radius     = BALL_RADIUS
            )
        )

    if len(sys.argv) > 1:
        if sys.argv[1] == '--fbf':
            # Set frame-by-frame simulation by pressing right
            mode = 'fbf'
    else:
        # let it run
        mode = None

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if mode == None:
            # Sets to a target FPS
            dt = clock.tick(TARGET_FPS) / 1000
            screen.fill(BACKGROUND_COLOR)
            # check_collision(balls)
            spacial_partitioned_collisions(balls)
            for idx, ball in enumerate(balls):
                ball.move()
                # print(f"Position of ball {idx}: ({ball.get_x_pos()}, {ball.get_y_pos()})")
                # print(f"Velocity of ball {idx}: ({ball.get_x_vel()}, {ball.get_y_vel()})")


        elif mode == 'fbf':
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:            # Press right arrow key to go to next "frame"
                    screen.fill(BACKGROUND_COLOR)
                    # check_collision(balls)
                    spacial_partitioned_collisions(balls)
                    for idx, ball in enumerate(balls):
                        ball.move()
                        # print(f"Position of ball {idx}: ({ball.get_x_pos()}, {ball.get_y_pos()})")
                        # print(f"Velocity of ball {idx}: ({ball.get_x_vel()}, {ball.get_y_vel()})")
                    time.sleep(0.1)                 # Wait some time so the downpress doesn't loop multiple frames

    pygame.quit

