import pygame
import time
import random 
from utils import resource_path
from bosses.boss import Boss
from player.player import Player
from movement_patterns.boss_patterns.horizontal_movement import HorizontalMovementPattern
from movement_patterns.enemy_patterns.horizontal_movement import EnemyHorizontalMovementPattern
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1600, 1000

PLAYER_WIDTH = 45
PLAYER_HEIGHT = 30
PLAYER_VELOCITY = 6

BULLET_VELOCITY = 8
BULLET_WIDTH = 20
BULLET_HEIGHT = 30

PROJECTILE_WIDTH = 6
PROJECTILE_HEIGHT = 12
PROJECTILE_VELOCITY = 2

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space game")
FONT = pygame.font.SysFont("comicsans", 30)



try:
    # backgrounds
    BG = pygame.image.load(resource_path("./img/lvl1bg.jpg"))
    BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

    # ships
    playerShip_path = resource_path("./sprites/playerShip.png") 
    playerShip = pygame.image.load(playerShip_path)
    enemy1_img = pygame.image.load(resource_path("./sprites/enemy1.png"))
    enemy1_img = pygame.transform.scale(enemy1_img, (45, 30))
    enemy2_img = pygame.image.load(resource_path("./sprites/enemy2.png"))
    enemy2_img = pygame.transform.scale(enemy2_img, (40, 25))
    #boss1_path = resource_path("./sprites/boss1.png")
    #boss1 = pygame.image.load(boss1_path)

    # player bullets
    player_bullet_image = pygame.image.load(resource_path("./sprites/playerDefaultBullet.png"))
    bullet_image = pygame.transform.rotate(player_bullet_image, 90)

    # enemy projectiles
    enemy1_projectile_img = pygame.image.load(resource_path("./sprites/enemy1_projectile.png"))
    enemy1_projectile_img = pygame.transform.scale(enemy1_projectile_img, (70, 70))
    enemy1_projectile_img = pygame.transform.rotate(enemy1_projectile_img, -90)

    enemy2_projectile_img = pygame.image.load(resource_path("./sprites/enemy2_projectile.png"))
    enemy2_projectile_img = pygame.transform.scale(enemy2_projectile_img, (65, 65))
    enemy2_projectile_img = pygame.transform.rotate(enemy2_projectile_img, -90)

    # boss1 projectiles
    boss1_projectile_img = pygame.image.load(resource_path("./sprites/enemy1_projectile.png"))
    boss1_projectile_img = pygame.transform.rotate(boss1_projectile_img, -90)

    # player lives
    full_heart_img = pygame.image.load(resource_path("./img/fullHeart.png"))
    full_heart = pygame.transform.scale(full_heart_img, (50, 40))
    empty_heart_img = pygame.image.load(resource_path("./img/emptyHeart.png"))
    full_heart = pygame.transform.scale(full_heart_img, (40, 30))
    empty_heart = pygame.transform.scale(empty_heart_img, (40, 30))
    
except Exception as e:
    print("Error loading image", e)



def draw_hearts(player, full_heart, empty_heart, start_x, start_y):
    for i in range(player.lives):
        heart_img = full_heart if i < player.current_hp else empty_heart
        WIN.blit(heart_img, (start_x, start_y - i * 25))

def draw(player, elapsed_time, projectiles, bullets, boss_projectiles, enemies,game_over, boss=None, fps=0):
    WIN.blit(BG, (0, 0))

    if not game_over:
        draw_hearts(player, full_heart, empty_heart, WIDTH - WIDTH + 10, HEIGHT - 70)
  
    player.draw_dash_tracker(WIN)
    player.draw(WIN)

    for enemy in enemies:
        enemy.draw(WIN)
    
    if boss:
        WIN.blit(boss.image, (boss.rect.x, boss.rect.y))
        #pygame.draw.rect(WIN, "red", boss, 2) 
        boss.draw_health_bar(WIN)

    for bullet in bullets:
        bullet.draw(WIN)
        #pygame.draw.rect(WIN, "green", bullet, 2) 
    
    for projectile in projectiles:
        projectile.draw(WIN)
        #pygame.draw.rect(WIN, "red", projectile)

    for projectile in boss_projectiles:
        projectile.draw(WIN)


    
    time_text = FONT.render(F"Time: {round(elapsed_time)}", 1, "white")
    WIN.blit(time_text, (10, 10))

    fps_small_font = pygame.font.Font(None, 32)
    fps_text = fps_small_font.render(f"{int(fps)}", 1, (255, 255, 255))
    WIN.blit(fps_text, (WIDTH - 40,  HEIGHT - 25))

    pygame.display.update()

def pause_menu(screen):
    paused = True
    clock = pygame.time.Clock()
    pause_options = ["Resume", "Restart Level", "Back to Menu", "Quit"]
    pointer_pos = 0
    
    font = pygame.font.SysFont("comicsans", 40)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    pointer_pos = (pointer_pos + 1) % len(pause_options)
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    pointer_pos = (pointer_pos - 1) % len(pause_options)
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if pointer_pos == 0:
                        return 'resume'
                    elif pointer_pos == 1:
                        return 'restart'
                    elif pointer_pos == 2:
                        return 'main_menu'
                    elif pointer_pos == 3:
                        pygame.quit()
                        return 'quit'
                        

        screen.fill((0, 0, 0))
        for index, option in enumerate(pause_options):
            if index == pointer_pos:
                label = font.render(f"> {option}", True, (255, 255, 255))
            else:
                label = font.render(option, True, (255, 255, 255))
            screen.blit(label, (100, 100 + 50 * index))

        pygame.display.update()
        clock.tick(60)

def game_loop():
    from enemies.enemy import Enemy
    run = True
    player = Player(WIDTH/2 - 40, HEIGHT/2, playerShip, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_VELOCITY, HEIGHT, WIDTH, BULLET_VELOCITY, BULLET_WIDTH, BULLET_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    global bullet_image
    # enemies spawn interval
    enemy_spawn_increment = 1500
    enemy2_spawn_increment = 7000 
    enemy2_last_spawn_time = 0
    enemy3_spawn_interval = 10000
    enemy3_last_spawn_time = 0
    
    enemy_count = 0
    boss_fight = False
    boss_defeated = False
    boss = None
    game_over = False
    game_won = False
    lost_text = FONT.render("Game Over!", 1, "white")
    # TODO add level complete sound
    win_text = FONT.render("YOU WON!", 1, "white")    
    # place holder sound for game_over
    game_over_mocking_laugh = pygame.mixer.Sound(resource_path("./sound_effects/mocking_laugh_1.wav"))
    # Refresh variables for restart-level
    enemies = []
    bullets = pygame.sprite.Group()
    boss_projectiles = pygame.sprite.Group()
    projectiles = []
   

    while run:
        TIMER = clock.tick(60)
        enemy_count += TIMER
        elapsed_time = time.time() - start_time
        fps = clock.get_fps()
        bullets.update()
        keys = pygame.key.get_pressed()
        

        time_thresholds = [
            (0, 1500),
            (10, 1350),
            (20, 100),
            (22, 1350),
            (30, 1000),
            (50, 40),
            (51, 800),
            (80, 30),
            (81, 700),
            (90, 30),
            (91, 50000000)
        ]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    action = pause_menu(WIN)
                    if action == 'quit':
                        return 'quit'
                    elif action == 'restart':
                        return game_loop()    
                    elif action == 'main_menu':
                        return main_menu(WIN)   

            # spawn enemy 1
            if not game_won and enemy_count > enemy_spawn_increment:
                enemy_x_position = random.randint(0, WIDTH - PLAYER_WIDTH) 
                # x, y, img, projectile_img, projectile_width, projectile_height, projectiles[], projectile_velocity, velocity, width, height, type, move_pattern 
                enemy = Enemy(enemy_x_position, -50, enemy1_img, enemy1_projectile_img, projectiles, 5, 2, 45, 30, "enemy1")
                enemies.append(enemy)
                enemy_count = 0
                for time_threshold, spawn_increment in time_thresholds:
                    if elapsed_time >= time_threshold:
                        enemy_spawn_increment = spawn_increment
                    else:
                      break

            #spawn enemy 2 (blue enemy)
            if elapsed_time > 9 and elapsed_time < 90:
                if(pygame.time.get_ticks() - enemy2_last_spawn_time) > enemy2_spawn_increment:
                    enemy2_x_pos = random.randint(0, WIDTH - PLAYER_WIDTH)
                     # x, y, img, projectile_img, projectile_width, projectile_height, projectiles[], projectile_velocity, velocity, width, height, type, move_pattern 
                    enemy2_pattern = EnemyHorizontalMovementPattern(WIDTH - WIDTH, WIDTH, 2, 200, True)
                    enemy2 = Enemy(enemy2_x_pos, -50, enemy2_img, enemy2_projectile_img, projectiles, 8, 3, 45, 25, "enemy2", enemy2_pattern)
                    enemies.append(enemy2)
                    enemy2_last_spawn_time = pygame.time.get_ticks()

            #spawn enemy 3 (zigzag enemy1)        
            current_time = pygame.time.get_ticks()
            if current_time - enemy3_last_spawn_time > enemy3_spawn_interval and elapsed_time < 90 and elapsed_time > 9:
                 #if(pygame.time.get_ticks() - enemy3_last_spawn_time) > enemy3_spawn_increment:
                    enemy3_x_pos = random.randint(0, WIDTH - PLAYER_WIDTH)
                     # x, y, img, projectile_img, projectile_width, projectile_height, projectiles[], projectile_velocity, velocity, width, height, type, move_pattern 
                    enemy3_pattern = EnemyHorizontalMovementPattern(WIDTH - WIDTH, WIDTH, 2, 120, True)
                    enemy3 = Enemy(enemy3_x_pos, -50, enemy1_img, enemy1_projectile_img, projectiles, 5, 3, 45, 25, "enemy3", enemy3_pattern)
                    enemies.append(enemy3)
                    enemy3_last_spawn_time = current_time

        
        # spawn boss
        if elapsed_time >= 100 and not boss_fight:
            boss_projectile_velocity = 3 
            horizontal_movement = HorizontalMovementPattern(left_limit = 100, right_limit = WIDTH - 100, velocity = 2, direction_interval = 120)
            boss_health = 120
            boss = Boss(WIDTH // 2, -100, boss1_projectile_img, boss_projectiles, WIDTH, HEIGHT, boss_projectile_velocity, horizontal_movement, boss_health) 
            boss_fight = True

        if boss_fight:
            boss.update()
            boss.draw(WIN)
    
        if boss and not boss.moving_in:
            boss.attack_timer += TIMER
            if boss.attack_timer > boss.attack_interval:
                    boss.attack(player)

            if boss.move_projectiles(PROJECTILE_VELOCITY, player):
                player_hit = player.is_hit() 
                game_over = player.current_hp <= 0 #False 
                    # TODO god-mode, for development 
                    #game_over = False      
                if game_over:
                    print("player killed by boss") 
                elif player_hit:
                    pass    

            for bullet in bullets:
                if bullet.rect.colliderect(boss.hitbox):
                    bullet.kill()
                    print("Bullet hit boss")
                    if boss.take_damage(5):
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
                if not player.game_over:
                        player.is_hit()
                        print("Player hit. Current HP:", player.current_hp)
                        if player.current_hp <= 0:
                            game_over = True
                        else:
                            projectiles.remove(projectile)    
                        
        draw(player, elapsed_time, projectiles, bullets, boss_projectiles, enemies, game_over, boss=boss, fps=fps)

        if game_over:
             pygame.display.update()
             game_over_mocking_laugh.play()
             WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
             pygame.display.update()
             pygame.time.delay(4000)
             return "game_over" # TODO go to game over

def select_level_menu(screen):
    selection = True
    clock = pygame.time.Clock()       
    level_options = ["Level 1", "Level 2", "Level 3", "Back"]
    pointer_pos = 0

    while selection:
        screen.fill((0,0,0))

        for index, option in enumerate(level_options):
            if index == pointer_pos:
                label = FONT.render(f"> {option}", True, (255, 255, 255))
            else:
                label = FONT.render(option, True, (255, 255, 255))
            screen.blit(label, (100, 100 + 50 * index))    

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        pointer_pos = (pointer_pos + 1) % len(level_options)
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        pointer_pos = (pointer_pos - 1) % len(level_options)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        selected_level = level_options[pointer_pos]
                        return selected_level

        pygame.display.update()
        clock.tick(60)

def main_menu(screen):
    menu = True
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("comicsans", 40)
    menu_options = ["Start Game", "Select level", "Options", "Exit"]
    pointer_pos = 0
    
    while menu:
        screen.fill((0, 0, 0,))
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            # Keyboard events
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    pointer_pos = (pointer_pos + 1) % len(menu_options)
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    pointer_pos = (pointer_pos - 1) % len(menu_options)
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if pointer_pos == 0:
                        return "start_game"
                        #menu = False
                    elif pointer_pos == 1:
                        return "select_level"    
                    elif pointer_pos == 2:
                        #return "options"
                        print("Options")
                    elif pointer_pos == 3:
                        return "quit"    
        # render menu options
        for index, option in enumerate(menu_options):
            if index == pointer_pos:
                label = font.render(f"> {option}", True, (255, 255, 255))
                screen.blit(label, (WIDTH / 2 - label.get_width() / 2, 200 + 60 * index))
            else:
                label = font.render(option, True, (255, 255, 255))
                screen.blit(label, (WIDTH / 2 - label.get_width() / 2, 200 + 60 * index))                   

        pygame.display.update()
        clock.tick(60)

def main():
    pygame.init()
    pygame.mouse.set_visible(False)
    running = True

    while running:
        action = main_menu(WIN)
        if action == "start_game":
            result = game_loop()
            if result == "quit":
                running = False
        elif action == 'select_level':
            selected_level = select_level_menu(WIN)
            if selected_level != "Back":
                print(f"Selected: {selected_level}")
            #level = level_selection_menu(WIN)        
        elif action == "quit":
            running = False    
    pygame.quit()

if __name__ == "__main__":
    main()









