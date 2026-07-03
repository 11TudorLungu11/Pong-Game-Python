import pygame
import sys
import time
import random


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(" Pong Game")


font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)


ball_speed = [5, 5]
paddle_speed = 6
ball_radius = 10
paddle_width = 10
paddle_height = 100
player1_score = 0
player2_score = 0


player1_pos = (10, SCREEN_HEIGHT // 2 - paddle_height // 2)
player2_pos = (SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2 - paddle_height // 2)
ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]


player1 = pygame.Rect(*player1_pos, paddle_width, paddle_height)
player2 = pygame.Rect(*player2_pos, paddle_width, paddle_height)
ball = pygame.Rect(ball_pos[0] - ball_radius, ball_pos[1] - ball_radius, ball_radius * 2, ball_radius * 2)


ball_color = WHITE



def get_random_color():
    return random.choice([(255, 0, 0), 
                          (0, 255, 0), 
                          (0, 0, 255), 
                          (255, 255, 0), 
                          (255, 0, 255), 
                          (0, 255, 255), 
                          (255, 192, 203), 
                          (255, 165, 0), 
                          (128, 0 ,128) 
                          ])



def show_menu():
    while True:
        screen.fill(BLACK)
        title = font.render(" A PONG GAME", True, WHITE)
        singleplayer = small_font.render(" Singleplayer", True, WHITE)
        multiplayer = small_font.render(" Multiplayer", True, WHITE)
        quit_game = small_font.render(" Quit", True, WHITE)

        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 4))
        screen.blit(singleplayer, (SCREEN_WIDTH // 2 - singleplayer.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(multiplayer, (SCREEN_WIDTH // 2 - multiplayer.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(quit_game, (SCREEN_WIDTH // 2 - quit_game.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "singleplayer"
                if event.key == pygame.K_2:
                    return "multiplayer"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def select_score():
    while True:
        screen.fill(BLACK)
        title = font.render("Select Winning Score", True, WHITE)
        short = small_font.render("Short (2 points)", True, WHITE)
        medium = small_font.render(" Medium (5 points)", True, WHITE)
        long = small_font.render(" Long (10 points) ", True, WHITE)

        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 4))
        screen.blit(short, (SCREEN_WIDTH // 2 - short.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(medium, (SCREEN_WIDTH // 2 - medium.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(long, (SCREEN_WIDTH // 2 - long.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 2
                if event.key == pygame.K_2:
                    return 5
                if event.key == pygame.K_3:
                    return 10
                

def show_victory_screen(winner):
    screen.fill(BLACK)

    
    try:
        victory_image = pygame.image.load("victory.png")
        victory_image = pygame.transform.scale(victory_image, (400, 300))
        screen.blit(victory_image, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 200))
    except:
        pass  

    victory_text = font.render(f"{winner} HAS WON", True, WHITE)
    screen.blit(victory_text, (SCREEN_WIDTH // 2 - victory_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    pygame.display.flip()
    time.sleep(3)  


def game_loop(mode, winning_score):
    global player1_score, player2_score, ball_speed, ball_color

    player1.y, player2.y = player1_pos[1], player2_pos[1]
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    ball_speed = [5, 5]

    clock = pygame.time.Clock()
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player1.top > 0:
            player1.y -= paddle_speed
        if keys[pygame.K_s] and player1.bottom < SCREEN_HEIGHT:
            player1.y += paddle_speed
        if mode == "multiplayer":
            if keys[pygame.K_UP] and player2.top > 0:
                player2.y -= paddle_speed
            if keys[pygame.K_DOWN] and player2.bottom < SCREEN_HEIGHT:
                player2.y += paddle_speed
        elif mode == "singleplayer":
            
            if player2.centery < ball.centery:
                player2.y += paddle_speed
            elif player2.centery > ball.centery:
                player2.y -= paddle_speed

        
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        
        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            ball_speed[1] = -ball_speed[1]

        
        if ball.colliderect(player1) or ball.colliderect(player2):
            ball_speed[0] = -ball_speed[0]
            ball_speed[0] *= 1.1  
            
            
            ball_color = get_random_color() 
            
            

       
        if ball.left <= 0:
            player2_score += 1
            ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            ball_speed = [5, 5]
            time.sleep(1)
        if ball.right >= SCREEN_WIDTH:
            player1_score += 1
            ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            ball_speed = [5, 5]
            time.sleep(1)

       
        
        
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, player1)
        pygame.draw.rect(screen, WHITE, player2)
        pygame.draw.ellipse(screen, ball_color, ball)
        pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

      
        if mode == "singleplayer":
            left_name = small_font.render("Player", True, WHITE)
            right_name = small_font.render("Computer", True, WHITE)
        else:  
            left_name = small_font.render("Player 1", True, WHITE)
            right_name = small_font.render("Player 2", True, WHITE)

        screen.blit(left_name, (50, 10))
        screen.blit(right_name, (SCREEN_WIDTH - right_name.get_width() - 50, 10))

        score_text = font.render(f"{player1_score} - {player2_score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 50))
        
         
        if player1_score >= winning_score:
            show_victory_screen("Player 1" if mode == "multiplayer" else "Player")
            return
        if player2_score >= winning_score:
            show_victory_screen("Player 2" if mode == "multiplayer" else "Computer")
            return

        pygame.display.flip()
        clock.tick(60)


while True:
    mode = show_menu()
    winning_score = select_score()
    player1_score = 0
    player2_score = 0
    game_loop(mode, winning_score)