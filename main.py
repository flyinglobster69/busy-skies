import random
import time
import pygame

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
WIDTH = 1920
HEIGHT = 1080
TITLE = "Flight 16"


class Player(pygame.sprite.Sprite):
    """This class represents the aircraft on the left that the player controls"""

    def __init__(self):
        super().__init__()

        # Aircraft Image
        self.image = pygame.image.load('./assets/boeing777.png')
        # self.image = pygame.transform.scale(self.image, (128, 128))

        # Rect
        self.rect = self.image.get_rect()

        # Set vertical speed
        self.change_y = 0

    def update(self):
        """ Move the player aircraft up and down"""
        # Gravity
        self.calc_grav()

        # Move up/down
        self.rect.y += self.change_y

        # # Check and see if we hit anything in the vertical axis
        # block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        # for block in block_hit_list:
        #
        #     # Reset our position based on the top/bottom of the object.
        #     # TODO: Register crash
        #     if self.change_y > 0:
        #         self.rect.bottom = block.rect.top
        #     elif self.change_y < 0:
        #         self.rect.top = block.rect.bottom
        #
        #     # Stop our vertical movement
        #     self.change_y = 0

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35  # Strength of gravity

        # See if we are on the ground.
        if self.rect.y >= HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = HEIGHT - self.rect.height


class Traffic(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Traffic is generated randomly, with randomized aircraft types

        # Images list
        traffic_0 = pygame.image.load('./assets/aircanada.png')
        traffic_1 = pygame.image.load('./assets/british.png')
        traffic_2 = pygame.image.load('./assets/delta.png')
        traffic_3 = pygame.image.load('./assets/ryanair.png')
        traffic_4 = pygame.image.load('./assets/airfrance.png')
        # traffic_5 = pygame.image.load('./assets/')
        # traffic_6 = pygame.image.load('./assets/')
        traffic_list = [traffic_0,
                        traffic_1,
                        traffic_2,
                        traffic_3,
                        traffic_4,
                        # traffic_5,
                        # traffic_6
                        ]

        # Image
        self.image = traffic_list[random.randrange(0, traffic_list.__len__())]
        # self.image = pygame.transform.scale(self.image, (64, 64))

        # Rect
        self.rect = self.image.get_rect()
        self.rect.center = (self.rect.x, random_coords_planes())

    def update(self):
        """Planes will spawn outside the screen and float to the other side of the screen"""
        self.rect.y -= random.randrange(3, 9)


class Runway(pygame.sprite.Sprite):
    # Constructor
    def __init__(self):
        # Call superclass constructor
        super().__init__()

        # Image
        self.image = pygame.Surface([1000, 100])

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH, HEIGHT)


    def update(self):
        """Move the runway from the right to the left of the screen slowly"""
        self.rect.x -= 1


def random_coords_player():
    """Returns a random x, y coord between 50, HEIGHT"""
    return random.randrange(50, HEIGHT)


def random_coords_planes():
    """Returns a random x, y coord between WIDTH + 50, HEIGHT"""
    return random.randrange(0, HEIGHT)





def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    died = False
    traffic_count = 10
    health_points = 1
    game_font = pygame.font.SysFont('Calibri', 20)

    music = pygame.mixer.Sound('./assets/localelevator.mp3') # Kevin Macleod - Local Forecast - Elevator
    # collision_sound = pygame.mixer.Sound('./assets/')

    # Create sprite groups
    all_sprites_group = pygame.sprite.Group()
    traffic_sprites_group = pygame.sprite.Group()
    runway_sprites_group = pygame.sprite.Group()

    # Create treasure sprites
    for i in range(traffic_count):
        traffic = Traffic()
        all_sprites_group.add(traffic)
        traffic_sprites_group.add(traffic)

    # Create player sprite
    player = Player()
    all_sprites_group.add(player)

    # Start music
    music.play()

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # ----- LOGIC
        all_sprites_group.update()

        # Handle collision between player and traffic sprites
        # spritecollide(sprite, group, dokill, collided = None) -> sprite_list
        # Player aircraft collides with any aircraft
        collided_traffic = pygame.sprite.spritecollide(player, traffic_sprites_group, dokill=True, collided=None)

        if len(collided_traffic) > 0:
            # Some collision has happened
            died = True
            # collision_sound.play()
            death_msg = game_font.render("United 328 Heavy suffered a mid-air collision and crashed.", True, WHITE)

        # ----- RENDER
        screen.fill(SKY_BLUE)
        all_sprites_group.draw(screen)
        score = game_font.render(f"Time survived: {clock}", True, WHITE)
        screen.blit(score, (10, 10))
        health = game_font.render(f"Lives remaining: {health_points}", True, WHITE)
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

    print(f"Time survived: {clock}")
    pygame.quit()


if __name__ == "__main__":
    main()
