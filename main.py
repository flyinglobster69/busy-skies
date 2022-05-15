import random
import time
import pygame

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 69)
RED = (255, 0, 0)
SKY_BLUE = (69, 165, 228)

# --- Objects drawn on standard 1440p (2K) resolution ---
WIDTH = 2560
HEIGHT = 1440

# Images list
# Airliners PNG images individually adjusted to be proportionally accurate
traffic_0 = pygame.image.load('./assets/aircanada.png')
traffic_1 = pygame.image.load('./assets/british.png')
traffic_2 = pygame.image.load('./assets/delta.png')
traffic_3 = pygame.image.load('./assets/lufthansa.png')
traffic_4 = pygame.image.load('./assets/airfrance.png')
traffic_5 = pygame.image.load('./assets/united.png')
traffic_6 = pygame.image.load('./assets/ryanair.png')
traffic_7 = pygame.image.load('./assets/etihad.png')
traffic_8 = pygame.image.load('./assets/spirit.png')
traffic_list = [traffic_0,
                traffic_1,
                traffic_2,
                traffic_3,
                traffic_4,
                traffic_5,
                traffic_6,
                traffic_7,
                traffic_8
                ]

TITLE = "Busy Skies"


class Player(pygame.sprite.Sprite):
    """This class represents the aircraft on the left that the player controls"""

    def __init__(self):
        super().__init__()

        # Random Player Aircraft Image
        self.image = traffic_list[random.randrange(0, traffic_list.__len__())]

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

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .10  # Strength of gravity

        # See if we are on the ground.
        if self.rect.y >= HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = HEIGHT - self.rect.height

        # See if we are at the top of the screen
        if self.rect.y <= 0 + self.rect.height and self.change_y <= 0:
            self.change_y = 0
            self.rect.y = 0 + self.rect.height

    def gain_altitude(self):
        self.change_y -= 3


class Traffic(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Traffic is generated randomly, with randomized aircraft types

        # Random Image
        self.image = traffic_list[random.randrange(0, traffic_list.__len__())]

        # Rect
        self.rect = self.image.get_rect()
        self.rect.center = (random_coords_planes())

    def update(self):
        """Planes will spawn outside the screen and float to the other side of the screen"""
        self.rect.x -= random.randrange(3, 9)

        # When the Traffic reaches the left side of the screen, respawn it on the right
        if self.rect.x < -500:
            self.rect.center = random_coords_planes()


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
    """Returns WIDTH and y coord between 0, HEIGHT"""
    return random.randrange(WIDTH, WIDTH * 3), random.randrange(0, HEIGHT)


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
    traffic_count = 16
    game_font = pygame.font.SysFont('Calibri', 40)
    death_font = pygame.font.SysFont('Calibri', 80)

    music = pygame.mixer.Sound('./assets/localelevator.mp3')
        # Local Forecast - Elevator Kevin MacLeod (incompetech.com)
        # Licensed under Creative Commons: By Attribution 3.0 License
        # http://creativecommons.org/licenses/by/3.0/
    death_sound = pygame.mixer.Sound('./assets/deathsound.mp3')
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

            # Keyboard controls
            if event.type == pygame.KEYDOWN:
                player.gain_altitude()

        # ----- LOGIC
        all_sprites_group.update()

        # Update vertical speed
        vertical_speed = (player.change_y * -1) * 1000

        # Handle collision between player and traffic sprites
        # spritecollide(sprite, group, dokill, collided = None) -> sprite_list
        # Player aircraft collides with any aircraft
        collided_traffic = pygame.sprite.spritecollide(player, traffic_sprites_group, dokill=True, collided=None)

        if len(collided_traffic) > 0:
            # Some collision has happened
            died = True
            music.stop()
            death_sound.play()
            death_msg = death_font.render("You crashed into another airplane and died :(", True, WHITE)

        # ----- RENDER
        screen.fill(SKY_BLUE)
        all_sprites_group.draw(screen)

        # Time survived
        instructions = game_font.render(
            "Press any key to increase the rate of climb and counter the effect of gravity.",
            True, BLACK)
        screen.blit(instructions, (10, 10))

        # Caution hitbox
        health = game_font.render("Caution Wake Turbulence (hitbox).", True, GREEN)
        screen.blit(health, (10, 50))

        # Player vertical speed
        vs = game_font.render(f"Vertical speed: {vertical_speed} feet per minute", True, WHITE)
        screen.blit(vs, (10, 90))

        # Vertical speed WARNING
        if vertical_speed > 4000:
            warning = game_font.render("Caution Vertical Speed", True, RED)
            screen.blit(warning, (10, 130))
        elif vertical_speed < -4000:
            warning = game_font.render("Caution Vertical Speed", True, RED)
            screen.blit(warning, (10, 130))

        # Called when died = True
        if died:
            screen.blit(death_msg, (300, HEIGHT / 2))
            pygame.display.flip()
            pygame.time.wait(5000)
            done = True
        else:
            pass

        # ----- UPDATE DISPLAY
        pygame.display.flip()
        clock.tick(69)  # nice

    pygame.quit()


if __name__ == "__main__":
    main()
