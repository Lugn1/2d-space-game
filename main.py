import pygame
import time
import random 
from enemies.enemy1 import Enemy
from bosses.boss1 import Boss
from player.player import Player

pygame.font.init()


WIDTH, HEIGHT = 1200, 800

clock = pygame.time.Clock()

PLAYER_WIDTH = 45
PLAYER_HEIGHT = 30
PLAYER_VELOCITY = 3

BULLET_VELOCITY = 5
BULLET_WIDTH = 20
BULLET_HEIGHT = 30
bullets = pygame.sprite.Group()

ENEMY_VELOCITY = 1
ENEMY1_WIDTH = 45
ENEMY1_HEIGHT = 30 
enemies = []

PROJECTILE_WIDTH = 6
PROJECTILE_HEIGHT = 12
PROJECTILE_VELOCITY = 1.5
projectiles = []
boss_projectiles = pygame.sprite.Group()



WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space game")

FONT = pygame.font.SysFont("comicsans", 30)


try:
    BG = pygame.image.load("./img/lvl1bg.jpg")
    BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
    playerShip = pygame.image.load("./sprites/playerShip.png")
    enemy1_img = pygame.image.load("./sprites/enemy1.png")
    enemy1_img = pygame.transform.scale(enemy1_img, (ENEMY1_WIDTH, ENEMY1_HEIGHT))
    player_bullet_image = pygame.image.load("./sprites/playerDefaultBullet.png")
    bullet_image = pygame.transform.rotate(player_bullet_image, 90)
    enemy1_projectile_img = pygame.image.load("./sprites/enemy1_projectile.png")
    enemy1_projectile_img = pygame.transform.rotate(enemy1_projectile_img, -90)
    enemy1_projectile_img = pygame.transform.scale(enemy1_projectile_img, (70, 70))
except Exception as e:
    print("Error loading image", e)

def draw(player, elapsed_time, projectiles, enemies, boss=None, fps=0):

    WIN.blit(BG, (0, 0))
    WIN.blit(player.image, player.rect)
    #pygame.draw.rect(WIN, "red", player, 2) 
    

    for enemy in enemies:
        WIN.blit(enemy1_img, (enemy.x, enemy.y))
        #pygame.draw.rect(WIN, "red", enemy, 2) 
    
    if boss:
        WIN.blit(boss.image, (boss.rect.x, boss.rect.y))
        #pygame.draw.rect(WIN, "red", boss, 2) 

    for bullet in bullets:
        bullet.draw(WIN)
       # pygame.draw.rect(WIN, "green", bullet, 2) 
    
    for projectile in projectiles:
        projectile.draw(WIN)
        #pygame.draw.rect(WIN, "red", projectile)

    for projectile in boss_projectiles:
        projectile.draw(WIN)

    
    time_text = FONT.render(F"Time: {round(elapsed_time)}", 1, "white")
    WIN.blit(time_text, (10, 10))

    fps_text = FONT.render(f"FPS: {int(fps)}", 1, (255, 255, 255))
    WIN.blit(fps_text, (10,  750))
    
    pygame.display.update()
    

def main():
    run = True

    player = Player(WIDTH/2 - 40, HEIGHT/2, playerShip, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_VELOCITY, HEIGHT, WIDTH, BULLET_VELOCITY, BULLET_WIDTH, BULLET_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    global bullet_image

    enemy_spawn_increment = 5000
    enemy_count = 0

    boss_fight = False
    boss_defeated = False
    boss = None
    
    hit = False
    game_won = False


    lost_text = FONT.render("Game Over!", 1, "white")
    win_text = FONT.render("YOU WON!", 1, "white")

    while run:
        TIMER = clock.tick(144)
        enemy_count += TIMER
        elapsed_time = time.time() - start_time
        fps = clock.get_fps()
        bullets.update()

        time_thresholds = [
            (10, 1350),
            (20, 1200),
            (30, 900),
            (40, 600),
            (50, 300),
            (60, 200),
            (70, 150),
            (80, 100),
            (90, 75),
            (100, 500000)
        ]

        if not game_won and enemy_count > enemy_spawn_increment:
            enemy_x_position = random.randint(0, WIDTH - PLAYER_WIDTH) 
            enemy = Enemy(enemy_x_position, -50, enemy1_img, enemy1_projectile_img, projectiles, ENEMY_VELOCITY)
            enemies.append(enemy)
            enemy_count = 0
            for time_threshold, spawn_increment in time_thresholds:
                if elapsed_time >= time_threshold:
                    enemy_spawn_increment = spawn_increment
                else:
                    break
        
        if elapsed_time >= 100 and not boss_fight:
            boss = Boss(WIDTH // 2, -100, "./sprites/boss1.png", boss_projectiles, HEIGHT) 
            boss_fight = True

        if boss_fight:
            boss.update()
            boss.draw(WIN)
    

        if boss and not boss.moving_in:
            boss.attack_timer += TIMER
            
            if boss.attack_timer > boss.attack_interval:
                    boss.attack(player)

            player_hit = boss.move_projectiles(PROJECTILE_VELOCITY, player)
            if player_hit:
                hit = True        
            
            for bullet in bullets:
                if bullet.rect.colliderect(boss.hitbox):
                    bullet.kill()
                    print("Bullet hit boss")
                    if boss.take_damage(10):
                        print("Boss defeated")
                        boss_defeated = True
                        boss_fight = False
                        boss = None
                        break
            if boss_defeated:
                game_won = True

        if game_won:
                for enemy in enemies[:]:
                    enemies.remove(enemy)
                WIN.blit(BG, (0, 0)) 
                WIN.blit(player.image, player.rect)  
                WIN.blit(win_text, (WIDTH/2 - win_text.get_width()/2, HEIGHT/2 - win_text.get_height()/2))
                pygame.display.update()
                pygame.time.delay(4000)     
                break     
               
        for enemy in enemies:
            enemy.move()
            enemy.shoot()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        player.move(keys)
        if (keys[pygame.K_SPACE] or keys[pygame.K_KP0]):
            player.shoot(bullets, bullet_image)       

        for bullet in bullets: 
            for enemy in enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    print("ENEMY HIT")
                    enemies.remove(enemy)
                    bullet.kill()
                    break

        for projectile in projectiles[:]:
            projectile.update()
            if projectile.rect.y > HEIGHT:
                projectiles.remove(projectile)
            elif projectile.rect.colliderect(player):
                projectiles.remove(projectile)
                hit = False # TODO swap to true 
                break    
        
        if hit:
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, projectiles, enemies, boss=boss, fps=fps)    

    pygame.quit()

if __name__ == "__main__":
    main()





