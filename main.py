import pygame
import time
import random 
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
PLAYER_WIDTH = 45
PLAYER_HEIGHT = 20
PLAYER_VELOCITY = 5

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

FONT = pygame.font.SysFont("comicsans", 30)
PROJECTILE_WIDTH = 6
PROJECTILE_HEIGHT = 12
PROJECTILE_VELOCITY = 3

try:
    BG = pygame.image.load("./img/lvl1bg.jpg")
    BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
    playerShip = pygame.image.load("./sprites/playerShip.png")
except Exception as e:
    print("Error loading image", e)


def draw(player, elapsed_time, projectiles):
    WIN.blit(BG, (0, 0))
    
    time_text = FONT.render(F"Time: {round(elapsed_time)}", 1, "white")
    WIN.blit(time_text, (10, 10))

    WIN.blit(playerShip, (player.x, player.y))

    #pygame.draw.rect(WIN, "red", player, 2)
    

    for projectile in projectiles:
        pygame.draw.rect(WIN, "red", projectile)

    
    pygame.display.update()
    

def main():
    run = True

    player = pygame.Rect(WIDTH/2 - 40, HEIGHT/2, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    projectile_add_increment = 2000
    projectile_count = 0

    projectiles = []
    hit = False


    while run:
        projectile_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if projectile_count > projectile_add_increment:
            for _ in range(3):
                projectile_x = random.randint(0, WIDTH - PROJECTILE_WIDTH)
                projectile = pygame.Rect(projectile_x, -PROJECTILE_HEIGHT, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
                projectiles.append(projectile)

            projectile_add_increment = max(200, projectile_add_increment - 50)
            projectile_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            player.x = max(0, player.x - PLAYER_VELOCITY)      
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            player.x = min(WIDTH - player.width, player.x + PLAYER_VELOCITY)
        if (keys[pygame.K_w] or keys[pygame.K_UP]):
            player.y = max(0, player.y - PLAYER_VELOCITY) 
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]):
            player.y = min(HEIGHT - PLAYER_HEIGHT, player.y + PLAYER_VELOCITY)       

        for projectile in projectiles[:]:
            projectile.y += PROJECTILE_VELOCITY
            if projectile.y > HEIGHT:
                projectiles.remove(projectile)
            elif projectile.colliderect(player):
                projectiles.remove(projectile)
                hit = True
                break    
        
        if hit:
            lost_text = FONT.render("Game Over!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, projectiles)    

    pygame.quit()

if __name__ == "__main__":
    main()




