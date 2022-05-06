import random
import time
import pygame

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
WIDTH = 1280
HEIGHT = 720
TITLE = "Flight 16"


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Aircraft Image
        self.image = pygame.image.load('./assets/boeing777.png')
        self.image = pygame.transform.scale(self.image, (128, 128))

        # Rect
        self.rect = self.image.get_rect()

    def update(self):
        """The plane has a fixed X position and a variable Y position where it can move up and down"""

        self.rect.center = pygame.mouse.get_pos()


class Traffic(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Traffic is generated randomly, with randomized aircraft types

        # Images list
        traffic_0 = pygame.image.load('./assets/')
        traffic_1 = pygame.image.load('./assets/')
        traffic_2 = pygame.image.load('./assets/')
        traffic_3 = pygame.image.load('./assets/')
        traffic_4 = pygame.image.load('./assets/')
        traffic_5 = pygame.image.load('./assets/')
        traffic_6 = pygame.image.load('./assets/')
        traffic_list = [traffic_0,
                        traffic_1,
                        traffic_2,
                        traffic_3,
                        traffic_4,
                        traffic_5,
                        traffic_6]

        # Image
        self.image = random.randrange(0, traffic_list.__len__())
        # self.image = pygame.transform.scale(self.image, (64, 64))

        # Rect
        self.rect = self.image.get_rect()
        self.rect.center = random_coords()


class Runway(pygame.sprite.Sprite):
    # Constructor
    def __init__(self):
        # Call superclass constructor
        super().__init__()

        # Image
        self.image = pygame.image.load('./assets/')
        self.image = pygame.transform.scale(self.image, (64, 64))

        self.rect = self.image.get_rect()
        self.rect.center = random_coords()

        self.xv = 3
        self.yv = 3

    def update(self):
        """Change the x coordinate based on the xv"""
        self.rect.x += self.xv
        """Change the y coordinate based on the yv"""
        self.rect.y += self.yv

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.xv *= -1
        if self.rect.left < 0:
            self.rect.left = 0
            self.xv *= -1
        if self.rect.top < 0:
            self.rect.top = 0
            self.yv *= -1
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.yv *= -1


def random_coords():
    """Returns a random x, y coord between 0, HEIGHT"""
    return random.randrange(0, HEIGHT)


def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # Remove cursor
    pygame.mouse.set_visible(False)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    died = False
    traffic_count = 10
    health_points = 1
    game_font = pygame.font.SysFont('Calibri', 20)

    eng_sound = pygame.mixer.Sound('./assets/')
    radio = pygame.mixer.Sound('./assets/')

    # Create sprite groups
    all_sprites_group = pygame.sprite.Group()
    traffic_sprites_group = pygame.sprite.Group()
    runway_sprites_group = pygame.sprite.Group()

    # Create treasure sprites
    for i in range(traffic_count):
        traffic = Traffic()
        all_sprites_group.add(traffic)
        traffic_sprites_group.add(traffic)


    # for i in range(primo_count):
    #     primo = Primogem()
    #     all_sprites_group.add(primo)
    #     treasure_sprites_group.add(primo)

    # Create player sprite
    player = Player()
    all_sprites_group.add(player)

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # ----- LOGIC
        all_sprites_group.update()

        # Handle collision between player and treasure sprites
        # spritecollide(sprite, group, dokill, collided = None) -> sprite_list
        # Zhongli collides with any Treasure Sprite
        collided_treasure = pygame.sprite.spritecollide(player, treasure_sprites_group, dokill=True, collided=None)

        if len(collided_treasure) > 0:
            # Some collision has happened
            treasure_sound.play()

        # Iterate through all collided treasure
        for treasure in collided_treasure:
            print(f"x: {treasure.rect.x}, y: {treasure.rect.y}")

            mora = Mora()
            all_sprites_group.add(mora)
            treasure_sprites_group.add(mora)
            mora_collected += 1

        # Collided enemy
        collided_enemy = pygame.sprite.spritecollide(player, enemy_sprites_group, dokill=False, collided=None)

        if len(collided_enemy) > 0:
            # Some collision has happened
            health_points -= 1
            if health_points < 1:
                died = True
                death_sound.play()
                death_msg = death_font.render("I WILL HAVE ORDER", True, WHITE)
            else:
                pass
            # death_msg = death_font.render("I WILL HAVE ORDER", True, WHITE)
            # screen.blit(death_msg, (WIDTH/2, HEIGHT/2))


        # ----- RENDER
        screen.fill(BLACK)
        all_sprites_group.draw(screen)
        score = score_font.render(f"Mora Collected: {mora_collected}", True, WHITE)
        screen.blit(score, (10, 10))
        health = health_font.render(f"Health Remanining: {health_points}", True, WHITE)
        screen.blit(health, (10, 30))

        if died:
            screen.blit(death_msg, (300, HEIGHT/2))
            pygame.display.flip()
            pygame.time.wait(5000)
            done = True
        else:
            pass

        # ----- UPDATE DISPLAY
        pygame.display.flip()
        clock.tick(60)

    print(f"Mora: {mora_collected}")
    pygame.quit()


if __name__ == "__main__":
    main()
