import asyncio
import pygame

# Init
pygame.init()
# Import randint
from random import randint

# Make display surface
W = 600
H = 300
display_surface = pygame.display.set_mode((W, H))
pygame.display.set_caption("10-Collision detection, at 60 fps")


async def main():
    # Lag en klokke
    clock = pygame.time.Clock()
    # Keep it running
    running = True
    speed = 5
    coins = 0

    # Load images
    player_surface = pygame.image.load("dragon_right.png")
    player_rect = player_surface.get_rect()
    # Place player bottom center
    player_rect.centerx = 300
    player_rect.bottom = 300
    # Player positions
    player_x = 300
    player_y = 300

    # The coin
    coin_surface = pygame.image.load("coin.png")
    coin_rect = coin_surface.get_rect()
    # Place coin in middle of screen
    coin_x = 300
    coin_y = 150
    coin_rect.centerx = coin_x
    coin_rect.centery = coin_y

    # Fetch sound
    sound1 = pygame.mixer.Sound("sound_1.ogg")

    # Text for points
    system_font = pygame.font.Font('AttackGraffiti.ttf', 32)  # En systemfont
    system_text = system_font.render("Dragons rule!", True, "Green", "darkslategrey")
    sys_text_rect = system_text.get_rect()  # Rektanglet
    sys_text_rect.center = (150, 20)  # Plassering, her sentrert på skjermen

    # Loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Metoden er annerledes, fordi det å holde inne en tast er ikke en event.
        # Derfor må vi sjekke om en tast blir holdt inne utenfor event-for loopen over

        # Get a list of all of the keys that are currently pressed down
        keys = pygame.key.get_pressed()
        # print(keys)  # Printer en nokså uoversiktlig liste, men de som har 1 eller True er trykket

        # Vi kan sjekke om bestemte knapper er holdt inne slik:
        if keys[pygame.K_LEFT]:  # Sjekker om pil venstre er holdt inne
            player_x -= speed  # uten delay går dette fryktelig fort
        if keys[pygame.K_RIGHT]:
            player_x += speed
        if keys[pygame.K_UP]:
            player_y -= speed
        if keys[pygame.K_DOWN]:
            player_y += speed

        # Don't go offscreen
        if player_x < player_rect.width // 2:
            player_x = player_rect.width // 2
        if player_x > 600 - player_rect.width // 2:
            player_x = 600 - player_rect.width // 2
        if player_y < player_rect.height:
            player_y = player_rect.height
        if player_y > 300:
            player_y = 300

        # Rensk skjermen
        display_surface.fill('Black')

        # Change player position
        player_rect.centerx = player_x
        player_rect.bottom = player_y

        # Check for collision
        if player_rect.colliderect(coin_rect):
            sound1.play()
            coins += 1
            # print("You're hitting the coin, Dragon!")
            coin_x = randint(coin_rect.width // 2, 600 - coin_rect.width)
            coin_y = randint(coin_rect.height // 2, 300 - coin_rect.height)
            # Update coin position
            coin_rect.centerx = coin_x
            coin_rect.centery = coin_y
            # Small delay
            pygame.time.delay(17)

        # Blit text
        display_surface.blit(system_text, sys_text_rect)
        # make the coin-points show
        coin_text = system_font.render("Points: " + str(coins), True, "Yellow")
        coin_text_rect = coin_text.get_rect()  # Rektanglet
        coin_text_rect.center = (450, 20)  # Plassering, her sentrert på skjermen
        # Blit points
        display_surface.blit(coin_text, coin_text_rect)

        # Draw rectangles around coin and dragon
        """
        pygame.draw.rect(display_surface, "Yellow", coin_rect, 1)
        pygame.draw.rect(display_surface, "Green", player_rect, 1)
        """

        # Blit coin
        display_surface.blit(coin_surface, coin_rect)

        # Blit player to screen
        display_surface.blit(player_surface, player_rect)

        # Oppdater skjermen
        pygame.display.flip()
        await asyncio.sleep(0)  # Must always be there, and always 0
        # Sett fps
        clock.tick(60)  # 60 fps, løkka tar minimum 1/60 sekund


    pygame.quit()


asyncio.run(main())
