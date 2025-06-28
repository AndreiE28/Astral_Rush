import pygame
from sys import exit
import random

#collision check function
def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

#initializing pygame
pygame.init()
pygame.mixer.init()

#setting up the window
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
pygame.display.set_caption("Astral Rush")
background = pygame.image.load("Assets\Images\Background.png").convert()
background = pygame.transform.scale(background, (screen_width, screen_height))

#game icon
icon = pygame.image.load("Assets/Images/icon.png")
pygame.display.set_icon(icon)

#setting up sound
pygame.mixer.music.load("Assets\Audio\DEAF KEV - Invincible ｜ Glitch Hop ｜ NCS - Copyright Free Music.mp3") 
volume = 0.5
pygame.mixer.music.set_volume(volume)  
pygame.mixer.music.play(-1) 
laser_sound = pygame.mixer.Sound("Assets\Audio\Laser.mp3")
explosion_sound = pygame.mixer.Sound("Assets\Audio\Explosion.mp3")

#setting the frame rate variable
clock = pygame.time.Clock()

#player settings
player_width = 100
player_height = 120
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height
player_speed = 10

#player2 settings
player2_width = 100
player2_height = 120
player2_x = screen_width // 2 - player2_width // 2
player2_y = 0
player2_speed = 10

#bullet settings
bullet_width = 5
bullet_height = 10
bullet_speed = 10
bullets = []

#enemy bullet settings
enemy_bullet_width = 5
enemy_bullet_height = 10
enemy_bullet_speed = 7
enemy_bullets = []

#enemy settings
enemy_width = 100
enemy_height = 120
enemy_speed = 3
enemies = []

#enemy spawn
enemy_timer = 0
enemy_spawn_time = 2000

#enemy shoot
enemy_shoot_time = 1500

#explosion animation
explosions = []
explosion_frames = [
    pygame.image.load("Assets\Images\explosion_animation1.png").convert_alpha(),
    pygame.image.load("Assets\Images\explosion_animation2.png").convert_alpha(),
    pygame.image.load("Assets\Images\explosion_animation3.png").convert_alpha(),
    pygame.image.load("Assets\Images\explosion_animation4.png").convert_alpha(),
    pygame.image.load("Assets\Images\explosion_animation5.png").convert_alpha(),
    pygame.image.load("Assets\Images\explosion_animation6.png").convert_alpha(),
]

#explosion class
class Explosion:

    def __init__(self, x, y):
        self.frames = explosion_frames
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = pygame.time.get_ticks()
        self.frame_rate = 50  
        self.finished = False

    def update(self):
        if pygame.time.get_ticks() - self.timer > self.frame_rate:
            self.index += 1
            self.timer = pygame.time.get_ticks()
            if self.index >= len(self.frames):
                self.finished = True
            else:
                self.image = self.frames[self.index]

    def draw(self, screen):
        if not self.finished:
            screen.blit(self.image, self.rect)

#load high score function
def load_high_score(filename="highscore.txt"):
    try:
        with open(filename, "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

#save high score function
def save_high_score(score, filename="highscore.txt"):
    with open(filename, "w") as file:
        file.write(str(score))

#button class
class Button:

    def __init__(self, text, font, x, y, padding=20, text_color=(255, 255, 255), bg_color=(0, 0, 0), hover_color=(150, 150, 150)):
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.padding = padding

        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.rect = self.text_surface.get_rect(center=(x, y))
        self.rect.inflate_ip(padding, padding)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        pygame.draw.rect(screen, self.hover_color if is_hovered else self.bg_color, self.rect, border_radius=8)
        screen.blit(self.text_surface, self.text_surface.get_rect(center=self.rect.center))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

font_path = 'Assets\Fonts\ARCADECLASSIC.TTF'
symbols_font_path = 'Assets\Fonts\ArcadeAlternate.ttf'
symbols_font = pygame.font.Font(symbols_font_path, size=36)
symbols_font_72 = pygame.font.Font(symbols_font_path, size=72)
my_font_subtext = pygame.font.Font(font_path, size=36)
my_font_text = pygame.font.Font(font_path, size=72)

game_over = False
game_over_2p = False

menu = True
controls = False
settings = False
volume_menu = False

lives = 3
lives_p2 = 3
score = 0
level = 1 
high_score = load_high_score()


paused = False
mute = False

pre_volume = volume

player_image_rect = pygame.Rect(player_x, player_y, player_width, player_height)
player2_image_rect = pygame.Rect(player2_x, player2_y, player2_width, player2_height)

shoot_time = 0
shoot_time_p2 = 0
shoot_cooldown = 300


two_player_game = False

#main loop
while True:

    events = pygame.event.get()

    #menu 
    if menu and not controls and not settings:

        button_start = Button("START", my_font_subtext, screen_width // 2, screen_height // 2)  
        button_2pGame = Button("2    PLAYER    GAME", my_font_subtext, screen_width // 2, screen_height // 2 + 60) 
        button_settings = Button("SETTINGS", my_font_subtext, screen_width // 2, screen_height // 2 + 120) 
        button_quit = Button("QUIT", my_font_subtext, screen_width // 2, screen_height // 2 + 180) 

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if button_start.is_clicked(event):
                menu = False
                game_over = False
                paused = False
                player_x = screen_width // 2 - player_width // 2
                player_y = screen_height - player_height
                bullets = []
                enemies = []
                explosions = []
                lives = 3
                score = 0
                level = 1

            elif button_quit.is_clicked(event):
                pygame.quit()
                exit()
            
            elif button_settings.is_clicked(event):
                settings = True
                menu = False
                controls = False
                volume_menu = False

            elif button_2pGame.is_clicked(event):
                two_player_game = True
                menu = False
                game_over_2p = False
                paused = False
                player_x = screen_width // 2 - player_width // 2
                player_y = screen_height - player_height
                player2_x = screen_width // 2 - player2_width // 2
                player2_y = 0
                bullets = []
                enemy_bullets = []
                explosions = []
                lives = 3
                lives_p2 = 3
                paused = False
        
        screen.blit(background, (0, 0))

        font = my_font_subtext
    
        text = my_font_text.render("ASTRAL    RUSH", True, (255, 255, 255))
        screen.blit(text, (screen_width //2 - text.get_width()//2, screen.get_height()//2 - 120))

        button_start.draw(screen)
        button_2pGame.draw(screen)
        button_settings.draw(screen)
        button_quit.draw(screen)

        pygame.display.flip()
    
    #settings menu
    elif settings and not menu and not controls and not volume_menu:

        button_controls = Button("CONTROLS", my_font_subtext, screen_width // 2, screen_height // 2 + 20)
        button_volume = Button("Volume", my_font_subtext, screen_width // 2, screen_height // 2 + 80)
        button_menu_settings = Button("Back    to    menu", my_font_subtext, screen_width // 2, screen_height // 2 + 160)

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if button_controls.is_clicked(event) and settings and not paused:
                volume_menu = False
                controls = True
                settings = False
               
            elif button_volume.is_clicked(event) and settings and not paused:
                volume_menu = True
                controls = False
                settings = False

            elif button_menu_settings.is_clicked(event):
                menu = True
                controls = False
                settings = False
                volume_menu = False

        screen.blit(background, (0, 0))
        text = my_font_text.render("Settings", True, (255, 255, 255))
        screen.blit(text, (screen_width//2 - text.get_width()//2, screen.get_height()//2 - 100))

        button_controls.draw(screen)
        button_volume.draw(screen)
        button_menu_settings.draw(screen)

        pygame.display.flip()

    #controls menu
    elif controls and not volume_menu:

        screen.blit(background, (0, 0))
        text = symbols_font_72.render("Controls", True, (255, 255, 255))
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - 160))
        
        button_back_settings = Button("Back    to    Settings", symbols_font, screen_width // 2, screen_height // 2 + 260)

        for event in events:
            if button_back_settings.is_clicked(event) and (volume_menu or controls) and not menu:
                controls = False
                volume_menu = False
                settings = True

        subtext = symbols_font.render("PLAYER    1", True, (255, 255, 255))
        screen.blit(subtext, (screen_width // 2 - 150 - subtext.get_width()//2, screen_height//2 - 60))

        subtext1 = symbols_font.render("LEFT:      A", True, (255, 255, 255))
        screen.blit(subtext1, (screen_width // 2 - 250, screen_height//2 - 30))

        subtext2 = symbols_font.render("RIGHT:    D", True, (255, 255, 255))
        screen.blit(subtext2, (screen_width // 2 - 250, screen.get_height()//2 + 10))

        subtext3 = symbols_font.render("UP:          W", True, (255, 255, 255))
        screen.blit(subtext3, (screen_width // 2 - 250, screen.get_height()//2 + 50))

        subtext4 = symbols_font.render("DOWN:     S", True, (255, 255, 255))
        screen.blit(subtext4, (screen_width // 2 - 250, screen.get_height()//2 + 90))

        subtext5 = symbols_font.render("SHOOT:    SPACE", True, (255, 255, 255))
        screen.blit(subtext5, (screen_width // 2 - 250, screen.get_height()//2 + 130))

        subtext6 = symbols_font.render("PAUSE:    P", True, (255, 255, 255))
        screen.blit(subtext6, (screen_width // 2 - 250, screen.get_height()//2 + 170))

        subtext7 = symbols_font.render("PLAYER    2", True, (255, 255, 255))
        screen.blit(subtext7, (screen_width // 2 + 150 - subtext.get_width()//2, screen_height//2 - 60))

        subtext8 = symbols_font.render("LEFT:    LEFT    ARROW", True, (255, 255, 255))
        screen.blit(subtext8, (screen_width // 2 + 50, screen_height//2 - 30))

        subtext9 = symbols_font.render("RIGHT:    RIGHT    ARROW", True, (255, 255, 255))
        screen.blit(subtext9, (screen_width // 2 + 50, screen.get_height()//2 + 10))

        subtext10 = symbols_font.render("UP:    UP    ARROW", True, (255, 255, 255))
        screen.blit(subtext10, (screen_width // 2 + 50, screen.get_height()//2 + 50))

        subtext11 = symbols_font.render("DOWN:    DOWN    ARROW", True, (255, 255, 255))
        screen.blit(subtext11, (screen_width // 2 + 50, screen.get_height()//2 + 90))

        subtext12 = symbols_font.render("SHOOT:    ENTER", True, (255, 255, 255))
        screen.blit(subtext12, (screen_width // 2 + 50, screen.get_height()//2 + 130))

        subtext13 = symbols_font.render("PAUSE:    P", True, (255, 255, 255))
        screen.blit(subtext13, (screen_width // 2 + 50, screen.get_height()//2 + 170))

        button_back_settings.draw(screen)

        pygame.display.flip()                 

    #volume menu      
    elif volume_menu:
        
        screen.blit(background, (0, 0))

        button_back_settings = Button("Back    to    Settings", symbols_font, screen_width // 2, screen_height // 2 + 200)
        button_volume_up = Button("+", symbols_font, screen_width // 2 + 200 // 2 + 150, screen_height // 2 + 10)
        button_volume_down = Button("-", symbols_font, screen_width // 2 + 200 // 2 + 110, screen_height // 2 + 10)
        button_volume_up_10 = Button("+10", symbols_font, screen_width // 2 + 200 // 2 + 220, screen_height // 2 + 10)
        button_volume_down_10 = Button("-10", symbols_font, screen_width // 2 + 200 // 2 + 50, screen_height // 2 + 10)
        button_mute = Button("Mute", symbols_font,screen_width // 2, screen_height // 2 + 130)

        for event in events:
            if button_back_settings.is_clicked(event) and (volume_menu or controls) and not menu:
                controls = False
                volume_menu = False
                settings = True
            
            elif button_volume_up.is_clicked(event) and volume_menu:
                mute = False
                volume = round(min(volume + 0.01, 1.0), 2)
                pygame.mixer.music.set_volume(volume)

            elif button_volume_up_10.is_clicked(event) and volume_menu:
                mute = False
                volume = round(min(volume + 0.1, 1.0), 2)
                pygame.mixer.music.set_volume(volume)

            elif button_volume_down.is_clicked(event) and volume_menu:
                mute = False
                volume = round(max(volume - 0.01, 0.0), 2)
                pygame.mixer.music.set_volume(volume)

            elif button_volume_down_10.is_clicked(event) and volume_menu:
                mute = False
                volume = round(max(volume - 0.1, 0.0), 2)
                pygame.mixer.music.set_volume(volume)

            elif button_mute.is_clicked(event) and volume_menu:
                if not mute:
                    pre_volume = volume
                    pygame.mixer.music.set_volume(0)
                                    
                else:
                    volume = pre_volume
                    pygame.mixer.music.set_volume(volume)

                mute = not mute

        text = my_font_text.render("Volume", True, (255, 255, 255))
        screen.blit(text, (screen_width//2 - text.get_width()//2, screen.get_height()//2 - 120))
        
        button_volume_up.draw(screen)
        button_volume_down.draw(screen)
        button_volume_up_10.draw(screen)
        button_volume_down_10.draw(screen)
        button_mute.draw(screen)

        # Volume slider
        slider_width = 200
        slider_height = 10
        slider_x = screen_width // 2 - slider_width // 2
        slider_y = screen_height // 2 + 10
        pygame.draw.rect(screen, (100, 100, 100), (slider_x, slider_y, slider_width, slider_height), border_radius=5)

        # Volume level indicator
        filled_width = int(slider_width * volume)
        pygame.draw.rect(screen, (0, 200, 0), (slider_x, slider_y, filled_width, slider_height), border_radius=5)

        # Volume percentage text
        volume_text = symbols_font.render(f"{round(volume*100)}%", True, (255, 255, 255))
        screen.blit(volume_text, (screen_width // 2 - volume_text.get_width() // 2, slider_y - 40))

        button_back_settings.draw(screen)

        pygame.display.flip()

    #game
    elif not paused:
        current_time = pygame.time.get_ticks()
        if not game_over and not two_player_game:
            button_pause = Button("||", my_font_subtext, screen_width - 30, 30)

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused

                    if event.key == pygame.K_SPACE  or event.key == pygame.K_RETURN and not paused and not menu and not controls:
                        if shoot_cooldown + shoot_time < current_time:   
                            laser_sound.play()        
                            bullet_x = player_x + player_width // 2 + 9
                            bullet_y = player_y  
                            bullet = pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height)     
                            bullets.append(bullet)
                            shoot_time = current_time
                if button_pause.is_clicked(event):
                    paused = not paused
                        
            #player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player_x -= player_speed
                if player_x < -player_width // 2:
                    player_x = screen_width + player_width // 2
            player_image_rect.x = player_x
            player_image_rect.y = player_y

            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player_x += player_speed
                if player_x > screen_width + player_width // 2:
                    player_x = -player_width // 2

            if keys[pygame.K_w] or keys[pygame.K_UP] and player_y > 0:
                player_y -= player_speed

            if keys[pygame.K_s] or keys[pygame.K_DOWN] and player_y < screen_height - player_height:
                player_y += player_speed

            if player_y < 0:
                player_y = 0

            elif player_y > screen_height - player_height:
                player_y = screen_height - player_height
            
            #bullet position update
            for bullet in bullets:
                bullet.y -= bullet_speed

            #enemy bullet position update
            for enemy_bullet in enemy_bullets:
                enemy_bullet.y += bullet_speed

            #remove bullets out of screen
            bullets = [bullet for bullet in bullets if bullet.top > 0]
            enemy_bullets = [enemy_bullet for enemy_bullet in enemy_bullets if enemy_bullet.top < screen_height]

            #enemy spawn and position
            current_time = pygame.time.get_ticks()
            if current_time - enemy_timer > enemy_spawn_time:
                enemy_x = random.randint(0, screen_width - enemy_width)
                enemy_y = -enemy_height
                enemies.append({
                "rect": pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height),
                "spawn_time": current_time
                })
                enemy_timer = current_time

            for enemy in enemies:
                enemy["rect"].y += enemy_speed

            #remove enemies off screen
            for enemy in enemies[:]:
                if enemy["rect"].top >= screen_height:
                    if score > 0:
                        score -= 50

            enemies = [enemy for enemy in enemies if enemy["rect"].y < screen_height]

            #setting up the background
            screen.blit(background, (0, 0))
            button_pause.draw(screen)

            #drawing the enemies
            enemy_image = pygame.image.load("Assets\Images\enemy.png").convert_alpha()
            for enemy in enemies:
                enemy_rect = enemy_image.get_rect(topleft=(enemy["rect"].x, enemy["rect"].y))
                screen.blit(enemy_image, enemy_rect)
            
                #creating and drawing the enemy projectiles
                if current_time - enemy["spawn_time"] > enemy_shoot_time:
                    enemy_bullet = pygame.Rect(
                        enemy["rect"].centerx - enemy_bullet_width // 2,
                        enemy["rect"].bottom,
                        enemy_bullet_width,
                        enemy_bullet_height
                    )
                    enemy_bullets.append(enemy_bullet)
                    laser_sound.play()
                    enemy["spawn_time"] = current_time

            #drawing player projectiles
            for bullet in bullets:
                bullet_image = pygame.transform.scale_by((pygame.image.load("Assets\Images\laser_blue.png")), 1.0)
                bullet_image_rect = bullet_image.get_rect(center=(bullet.x, bullet.y))  # Use bullet position
                screen.blit(bullet_image, bullet_image_rect)

            for enemy_bullet in enemy_bullets:
                enemy_bullet_image = pygame.transform.scale_by((pygame.image.load("Assets\Images\laser_red.png")), 1.0)
                enemy_bullet_image_rect = enemy_bullet_image.get_rect(center=(enemy_bullet.x, enemy_bullet.y))
                screen.blit(enemy_bullet_image, enemy_bullet_image_rect)

            #drawing the player
            player_image = pygame.image.load("Assets\Images\player.png").convert_alpha()
            screen.blit(player_image, player_image_rect)

            #drawing the explosion animation
            for explosion in explosions[:]:
                explosion.update()
                explosion.draw(screen)
                if explosion.finished:
                    explosions.remove(explosion)
            
            #drawing the lives on the screen
            life_image = pygame.image.load("Assets\Images\gas.png").convert_alpha()
            if lives == 3:
                life_image_rect = life_image.get_rect(topleft=(0, 0))
                screen.blit(life_image, life_image_rect)
                life_image_rect = life_image.get_rect(topleft=(50, 0))
                screen.blit(life_image, life_image_rect)
                life_image_rect = life_image.get_rect(topleft=(100, 0))
                screen.blit(life_image, life_image_rect)

            if lives == 2:
                life_image_rect = life_image.get_rect(topleft=(0, 0))
                screen.blit(life_image, life_image_rect)
                life_image_rect = life_image.get_rect(topleft=(50, 0))
                screen.blit(life_image, life_image_rect)

            if lives == 1:
                life_image_rect = life_image.get_rect(topleft=(0, 0))
                screen.blit(life_image, life_image_rect)

            #showing the score
            font = my_font_subtext
            score_text = font.render(f"Score    {score}", True, (255, 255, 255))
            screen.blit(score_text, (screen_width - score_text.get_width() - 80, 10))

            for bullet in bullets[:]:
                for enemy in enemies[:]:
                    if check_collision(bullet, enemy["rect"]):
                        explosions.append(Explosion(enemy["rect"].x + enemy["rect"].width // 2, enemy["rect"].y + enemy["rect"].height // 2))
                        explosion_sound.play()
                        bullets.remove(bullet)
                        enemies.remove(enemy)   
                        score += 100 
                        if score > high_score:  
                            high_score = score
                            save_high_score(high_score)
                        break

            for enemy_bullet in enemy_bullets[:]:   
                if check_collision(enemy_bullet, player_image_rect):    
                    explosion_sound.play()
                    explosions.append(Explosion(player_image_rect.x + player_image_rect.width // 2, player_image_rect.y + player_image_rect.height // 2))
                    enemy_bullets.remove(enemy_bullet)
                    lives -= 1  
                    if lives > 0:
                        score = (level-1)*1000  #the score goes down to the previous level
                    break

            for enemy in enemies[:]:
                if check_collision(enemy["rect"],player_image_rect): 
                    explosion_sound.play()
                    explosions.append(Explosion(enemy["rect"].x + enemy["rect"].width // 2, enemy["rect"].y + enemy["rect"].height // 2))
                    enemies.remove(enemy)
                    lives -= 1  
                    if lives > 0:
                        score = (level-1)*1000  #the score goes down to the previous level
                    break

            for bullet in bullets[:]:
                for enemy_bullet in enemy_bullets[:]:
                    if check_collision(bullet, enemy_bullet):   
                        explosion_sound.play()
                        explosions.append(Explosion(enemy_bullet.x + bullet_width // 2, enemy_bullet.y + bullet_height // 2))
                        bullets.remove(bullet)  
                        enemy_bullets.remove(enemy_bullet)

            #next level check
            if score == level*1000 and level < 11:  #check if the score gets over the previous threshold with a thousand points
                level += 1
                enemy_speed += level-1
                if enemy_spawn_time >= 500:
                    enemy_spawn_time -= 100
                if level >= 5:
                    enemy_shoot_time = 1000

            #show level
            font = my_font_subtext
            level_text = font.render(f"LEVEL {level}", True, (255, 255, 255))
            screen.blit(level_text, (screen_width - level_text.get_width() - 300, 10))

            #game over check
            if not lives:
                game_over = True
                two_player_game = False
                game_over_2p = False

            clock.tick(60)

            pygame.display.flip()

        elif not game_over_2p and two_player_game and not paused:
            button_pause = Button("||", my_font_subtext, screen_width - 30, 30)

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused

                    if event.key == pygame.K_SPACE and not paused and not game_over_2p and not menu and not controls:
                        if shoot_cooldown + shoot_time < current_time:   
                            laser_sound.play()        
                            bullet_x = player_x + player_width // 2 + 9
                            bullet_y = player_y 
                            bullet = pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height)     
                            bullets.append(bullet)
                            shoot_time = current_time
                    if event.key == pygame.K_RETURN and not paused and not game_over_2p and not menu and not controls:
                        if shoot_cooldown + shoot_time_p2 < current_time:   
                            laser_sound.play()        
                            enemy_bullet_x = player2_image_rect.centerx - enemy_bullet_width // 2
                            enemy_bullet_y = player2_image_rect.bottom  
                            enemy_bullet = pygame.Rect(enemy_bullet_x, enemy_bullet_y, enemy_bullet_width, enemy_bullet_height)     
                            enemy_bullets.append(enemy_bullet)
                            shoot_time_p2 = current_time

                if button_pause.is_clicked(event):
                    paused = not paused

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                player_x -= player_speed
                if player_x < -player_width // 2:
                    player_x = screen_width + player_width // 2
            player_image_rect.x = player_x
            player_image_rect.y = player_y

            if keys[pygame.K_d]:
                player_x += player_speed
                if player_x > screen_width + player_width // 2:
                    player_x = -player_width // 2

            if keys[pygame.K_w] and player_y > 0:
                player_y -= player_speed

            if keys[pygame.K_s] and player_y < screen_height - player_height:
                player_y += player_speed

            if player_y < 0:
                player_y = 0

            elif player_y < screen_height // 2:
                player_y = screen_height // 2

            if keys[pygame.K_LEFT]:
                player2_x -= player_speed
                if player2_x < -player2_width // 2:
                    player2_x = screen_width + player2_width // 2
            player2_image_rect.x = player2_x
            player2_image_rect.y = player2_y

            if keys[pygame.K_RIGHT]:
                player2_x += player_speed
                if player2_x > screen_width + player2_width // 2:
                    player2_x = -player2_width // 2

            if keys[pygame.K_UP] and player2_y > 0:
                player2_y -= player_speed

            if keys[pygame.K_DOWN] and player2_y < screen_height - player2_height:
                player2_y += player_speed

            if player2_y < 0:
                player2_y = 0

            elif player2_y > screen_height // 2 - player2_height:
                player2_y = screen_height // 2 - player2_height

            #bullet position update
            for bullet in bullets:
                bullet.y -= bullet_speed

            #enemy bullet position update
            for enemy_bullet in enemy_bullets:
                enemy_bullet.y += bullet_speed

            #remove bullets out of screen
            bullets = [bullet for bullet in bullets if bullet.top > 0]
            enemy_bullets = [enemy_bullet for enemy_bullet in enemy_bullets if enemy_bullet.top < screen_height]

            #screen fill
            screen.blit(background, (0, 0))
            button_pause.draw(screen)

            #draw bullet
            for bullet in bullets:
                bullet_image = pygame.transform.scale_by((pygame.image.load("Assets\Images\laser_blue.png")), 1.0)
                bullet_image_rect = bullet_image.get_rect(center=(bullet.x, bullet.y))  # Use bullet position
                screen.blit(bullet_image, bullet_image_rect)

            for enemy_bullet in enemy_bullets:
                enemy_bullet_image = pygame.transform.scale_by((pygame.image.load("Assets\Images\laser_red.png")), 1.0)
                enemy_bullet_image_rect = enemy_bullet_image.get_rect(center=(enemy_bullet.x, enemy_bullet.y))
                screen.blit(enemy_bullet_image, enemy_bullet_image_rect)

            #player draw
            player_image = pygame.image.load("Assets\Images\player.png").convert_alpha()
            screen.blit(player_image, player_image_rect)

            #plyer 2 draw
            player2_image = pygame.image.load("Assets\Images\enemy.png").convert_alpha()
            screen.blit(player2_image, player2_image_rect)

            #explosion draw
            for explosion in explosions[:]:
                explosion.update()
                explosion.draw(screen)
                if explosion.finished:
                    explosions.remove(explosion)
            
            #show lives
            life_image = pygame.image.load("Assets\Images\gas.png").convert_alpha()
            if lives_p2 == 3:
                life_image_rect = life_image.get_rect(topleft=(0, 0))
                screen.blit(life_image, life_image_rect)
                life_image_rect = life_image.get_rect(topleft=(50, 0))
                screen.blit(life_image, life_image_rect)
                life_image_rect = life_image.get_rect(topleft=(100, 0))
                screen.blit(life_image, life_image_rect)
            if lives_p2 == 2:
                life_image_rect = life_image.get_rect(topleft=(0, 0))
                screen.blit(life_image, life_image_rect)
                life_image_rect = life_image.get_rect(topleft=(50, 0))
                screen.blit(life_image, life_image_rect)
            if lives_p2 == 1:
                life_image_rect = life_image.get_rect(topleft=(0, 0))
                screen.blit(life_image, life_image_rect)

            if lives == 3:
                screen.blit(life_image, (0, screen_height - 80))
                screen.blit(life_image, (50, screen_height - 80))
                screen.blit(life_image, (100, screen_height - 80))
            if lives == 2:
                screen.blit(life_image, (0, screen_height - 80))
                screen.blit(life_image, (50, screen_height - 80))
            if lives == 1:
                screen.blit(life_image, (100, screen_height - 80))

            #collision check
            for bullet in bullets[:]:
                if check_collision(bullet, player_image_rect):
                    explosions.append(Explosion(player2_image_rect.x + player2_image_rect.width // 2, player2_image_rect.y + player2_image_rect.height // 2))
                    explosion_sound.play()
                    bullets.remove(bullet)
                    lives_p2 -= 1
                    break

            for enemy_bullet in enemy_bullets[:]:
                if check_collision(enemy_bullet, player_image_rect):
                    explosion_sound.play()
                    explosions.append(Explosion(player_image_rect.x + player_image_rect.width // 2, player_image_rect.y + player_image_rect.height // 2))
                    enemy_bullets.remove(enemy_bullet)
                    lives -= 1
                    break

            for bullet in bullets[:]:
                for enemy_bullet in enemy_bullets[:]:
                    if check_collision(bullet, enemy_bullet):
                        explosion_sound.play()
                        explosions.append(Explosion(enemy_bullet.x + bullet_width // 2, enemy_bullet.y + bullet_height // 2))
                        bullets.remove(bullet)
                        enemy_bullets.remove(enemy_bullet)
            for bullet in bullets[:]:
                if check_collision(bullet, player2_image_rect):
                    explosion_sound.play()
                    explosions.append(Explosion(player2_image_rect.x + player2_image_rect.width // 2, player2_image_rect.y + player2_image_rect.height // 2))
                    bullets.remove(bullet)
                    lives_p2 -= 1
                    break

            if not lives or not lives_p2:
                    game_over_2p = True
                    game_over = False

            clock.tick(60)

            pygame.display.flip()

        elif game_over_2p and two_player_game:
            #game over  2p screen
            button_restart = Button("Restart", my_font_subtext, screen_width // 2, screen_height // 2)
            button_quit = Button("QUIT", my_font_subtext, screen_width // 2, screen_height // 2 + 180)
            button_menu = Button("Back    to    menu", my_font_subtext, screen_width // 2, screen_height // 2 + 80)

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                if button_restart.is_clicked(event) and game_over_2p and not paused:
                    two_player_game = True
                    menu = False
                    game_over_2p = False
                    paused = False
                    player_x = screen_width // 2 - player_width // 2
                    player_y = screen_height - player_height
                    player2_x = screen_width // 2 - player2_width // 2
                    player2_y = 0
                    bullets = []
                    enemy_bullets = []
                    explosions = []
                    lives = 3
                    lives_p2 = 3
                
                elif button_menu.is_clicked(event):
                    menu = True
                    controls = False
                    game_over = False
                    settings = False
                    volume_menu = False

                elif button_quit.is_clicked(event) and not settings and not volume_menu and not controls:
                    pygame.quit()
                    exit()

            screen.blit(background, (0, 0))

            if not lives == 0:
                text = my_font_text.render("PLAYER    1    WINS!", True, (255, 0, 0))
                screen.blit(text, (screen_width//2 - text.get_width()//2, screen.get_height()//2 - 200))
            else:
                text = my_font_text.render("PLAYER    2    WINS!", True, (255, 0, 0))
                screen.blit(text, (screen_width//2 - text.get_width()//2, screen.get_height()//2 - 200))

            button_restart.draw(screen)
            button_menu.draw(screen)
            button_quit.draw(screen)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                two_player_game = True
                menu = False
                game_over_2p = False
                paused = False
                player_x = screen_width // 2 - player_width // 2
                player_y = screen_height - player_height
                player2_x = screen_width // 2 - player2_width // 2
                player2_y = 0
                bullets = []
                enemy_bullets = []
                explosions = []
                lives = 3
                lives_p2 = 3

            if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                pygame.quit()
                exit()

            if keys[pygame.K_m]:
                game_over_2p = False
                game = False
                menu = True

            #window update
            pygame.display.flip()
            
            #cap for the fps
            clock.tick(60)

        elif game_over:
            #game over screen
            button_restart = Button("Restart", my_font_subtext, screen_width // 2, screen_height // 2)
            button_quit = Button("QUIT", my_font_subtext, screen_width // 2, screen_height // 2 + 180)
            button_menu = Button("Back    to    menu", my_font_subtext, screen_width // 2, screen_height // 2 + 80)

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                if button_restart.is_clicked(event) and game_over and not paused:
                    menu = False
                    game_over = False
                    player_x = screen_width // 2 - player_width // 2
                    player_y = screen_height - player_height
                    explosions = []
                    bullets = []
                    enemies = []
                    lives = 3
                    score = 0
                    level = 1
                
                elif button_menu.is_clicked(event):
                    menu = True
                    controls = False
                    game_over = False
                    settings = False
                    volume_menu = False
                    two_player_game = False

                elif button_quit.is_clicked(event) and not settings and not volume_menu and not controls:
                    pygame.quit()
                    exit()

            screen.blit(background, (0, 0))

            text = my_font_text.render("GAME    OVER!", True, (255, 0, 0))
            screen.blit(text, (screen_width//2 - text.get_width()//2, screen.get_height()//2 - 200))

            font = my_font_subtext
            score_text = font.render(f"Score    {score}", True, (255, 255, 255))
            screen.blit(score_text, (screen_width//2 - score_text.get_width()//2, screen.get_height()//2 - 125))

            font = my_font_subtext
            high_score_text = font.render(f"High    Score    {high_score}", True, (255, 255, 255))
            screen.blit(high_score_text, (screen_width//2 - high_score_text.get_width()//2, screen.get_height()//2 - 85))

            button_restart.draw(screen)
            button_menu.draw(screen)
            button_quit.draw(screen)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                game_over = False
                player_x = screen_width // 2 - player_width // 2
                player_y = screen_height - player_height
                bullets = []
                enemies = []
                explosions = []
                lives = 3
                score = 0
                level = 1

            if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                pygame.quit()
                exit()

            if keys[pygame.K_m]:
                game_over = False
                game = False
                menu = True

            pygame.display.flip()
            
            #cap for the fps
            clock.tick(60)

    else:
        #pause screen
        button_continue = Button("Continue", my_font_subtext, screen_width // 2, screen_height // 2 + 60)
        button_menu = Button("Back    to    menu", my_font_subtext, screen_width // 2, screen_height // 2 + 120)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

            elif button_menu.is_clicked(event):
                menu = True
                controls = False
                game_over = False
                settings = False
                volume_menu = False

            elif button_quit.is_clicked(event) and not settings and not volume_menu and not controls:
                pygame.quit()
                exit()

        pause_font = my_font_text
        pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
        screen.blit(pause_text, (screen_width // 2 - pause_text.get_width() // 2, screen_height // 2 - pause_text.get_height() // 2))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                pygame.quit()
                exit()
        
        button_continue.draw(screen)
        button_menu.draw(screen)
        button_quit.draw(screen)

        for event in events:
            if button_menu.is_clicked(event):
                menu = True
                paused = False
                controls = False
                game_over = False
                settings = False
                volume_menu = False
            if button_quit.is_clicked(event):
                pygame.quit()
                exit()
            if button_continue.is_clicked(event):
                paused = not paused

        pygame.display.flip()
            
        #cap for the fps
        clock.tick(60)
    
