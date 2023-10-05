import pygame
import time
import random 
from enemies.enemy_1 import Enemy

pygame.font.init()

WIDTH, HEIGHT = 1000, 800
PLAYER_WIDTH = 45
PLAYER_HEIGHT = 30
PLAYER_VELOCITY = 7
BULLET_VELOCITY = 9
BULLET_WIDTH = 6
BULLET_HEIGHT = 12
bullets = []

ENEMY_VELOCITY = 2
ENEMY1_WIDTH = 45
ENEMY1_HEIGHT = 30 
enemies = []
PROJECTILE_WIDTH = 6
PROJECTILE_HEIGHT = 12
PROJECTILE_VELOCITY = 4
projectiles = []

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

FONT = pygame.font.SysFont("comicsans", 30)


try:
    BG = pygame.image.load("./img/lvl1bg.jpg")
    BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
    playerShip = pygame.image.load("./sprites/playerShip.png")
    enemy1 = pygame.image.load("./sprites/enemy1.png")
    enemy1 = pygame.transform.scale(enemy1, (ENEMY1_WIDTH, ENEMY1_HEIGHT))
    print("enemy1 transformed")
    
except Exception as e:
    print("Error loading image", e)

def shoot(x, y):
    bullet = pygame.Rect(x, y - BULLET_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT)
    bullets.append(bullet)

def draw(player, elapsed_time, projectiles, enemies):
    WIN.blit(BG, (0, 0))
    
    time_text = FONT.render(F"Time: {round(elapsed_time)}", 1, "white")
    WIN.blit(time_text, (10, 10))

    WIN.blit(playerShip, (player.x, player.y))

    #pygame.draw.rect(WIN, "red", player, 2)
    


    for enemy in enemies:
        WIN.blit(enemy1, (enemy.x, enemy.y))
    
    for bullet in bullets:
        pygame.draw.rect(WIN, "green", bullet)

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

    enemy_spawn_increment = 1500
    enemy_count = 0
    

    hit = False
    spacebar_held = False
    can_shoot = True

    while run:
        enemy_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        time_thresholds = [
            (10, 1400),
            (20, 1200),
            (30, 900),
            (40, 600),
            (50, 300),
        ]

        if enemy_count > enemy_spawn_increment:
            enemy_x_position = random.randint(0, WIDTH - PLAYER_WIDTH) 
            enemy = Enemy(enemy_x_position, -50, enemy1, projectiles, ENEMY_VELOCITY)
            enemies.append(enemy)
            enemy_count = 0
            for time_threshold, spawn_increment in time_thresholds:
                if elapsed_time >= time_threshold:
                    enemy_spawn_increment = spawn_increment
                else:
                    break

            if elapsed_time >= 60:        
                win_text = FONT.render("YOU WON!", 1, "white")
                WIN.blit(win_text, (WIDTH/2 - win_text.get_width()/2, HEIGHT/2 - win_text.get_height()/2))
                pygame.display.update()
                pygame.time.delay(4000)     
                break       
                            # TODO: Make the game continue until all enemies have left the screen then win_text
                            
            
               

        for enemy in enemies:
            enemy.move()
            enemy.shoot()
 

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
        if (keys[pygame.K_SPACE]):
            if not spacebar_held and can_shoot:
                shoot(player.x + PLAYER_WIDTH/2 - BULLET_WIDTH/2, player.y)  
                can_shoot = False
            spacebar_held = True
        else:
            spacebar_held = False
            can_shoot = True        

        for bullet in bullets[:]:
            bullet.y -= BULLET_VELOCITY

        for bullet in bullets[:]:    
            for enemy in enemies[:]:
                if bullet.colliderect(enemy.rect):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    break

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

        draw(player, elapsed_time, projectiles, enemies)    

    pygame.quit()

if __name__ == "__main__":
    main()




