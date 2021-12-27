import pygame


def main():
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    start_created_map = True
    cheak = pygame.image.load('texture/tanks/PNG/Tracks/Track_1_A.png')
    screen.fill((250, 250, 250))
    while start_created_map:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.blit(cheak, (0, 0))
        pygame.display.update()



main()