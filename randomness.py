
import sys
import pygame
import math
import time
import random

length = 200

if __name__ == '__main__':
    pygame.init()
    # Create the window, saving it to a variable.
    surface = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Random starting position generator")

    surface.fill((255, 255, 255))
    pygame.display.update()

    while True:
        time.sleep(0.05)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    while True:
                        theta1 = random.uniform(0, 360)
                        theta2 = random.uniform(0, 360)

                        pos = [pygame.Vector2(0, 0) for _ in range(3)]

                        pos[1].from_polar((length, theta1))
                        pos[1] += pos[0]
                        pos[2].from_polar((length, theta2))
                        pos[2] += pos[1]

                        if pos[2].x >= 0 and random.uniform(-2 * length, 2 * length) > pos[2].y:
                            offset = pygame.Vector2(surface.get_width() / 2, surface.get_height() / 2)

                            for i, _ in enumerate(pos):
                                pos[i] += offset

                            surface.fill((255, 255, 255))
                            pygame.draw.line(surface, color=(0, 0, 0), start_pos=pos[0], end_pos=pos[1], width=2)
                            pygame.draw.line(surface, color=(0, 0, 0), start_pos=pos[1], end_pos=pos[2], width=2)
                            # pygame.draw.circle(surface, (255, 0, 0), pos[0], 4)
                            # pygame.draw.circle(surface, (255, 0, 0), pos[1], 7)
                            pygame.draw.circle(surface, (255, 0, 0), pos[2], 10)
                            pygame.display.update()
                            break