'''
Debra,YaYa,Beena,Gracie G8, Computer Science
The Final Project:
This program is a game that uses mouse to
control the Spaceship and avoiding the stars to win
'''

import pygame # helps us make games 
import time # helps us keep track of time 
import random # helps make random numbers 
pygame.font.init() # lets us use text in the game 

# size of the game window in pixels
WIDTH, HEIGHT = 1000, 800

# Create the game window 
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption( "Space Dodge" )

# size of the player's spaceship 
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

# load background image and make the size fit the screen 
BG = pygame.transform.scale(pygame.image.load("StarWar.PNG"), (WIDTH, HEIGHT))
SPACESHIP = pygame.transform.scale(pygame.image.load("spaceship.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))

PLAYER_VEL = 5 # how fast the player moves 

STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3 # how fast the stars fall

# font and size for the text 
FONT = pygame.font.SysFont("comicsans", 30)

# function to draw everything on the screen 
def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    # the time survived at the top left corner
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    # draw the spaceship
    WIN.blit(SPACESHIP, (player.x, player.y))

    # draw all the stars ( white rectangles )
    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()

# the main part of the game 
def main():
    run = True

    # create player rectangle near the bottom of the screen 
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT,
                        PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    # how often new stars are genarated 
    star_add_increment = 2000
    star_count = 0

    # list to store all the stars
    stars = []

    # if the plater has been hit by a star
    hit = False
    
    while run:
        # update the time and how long the player has lasted 
        star_count += clock.tick(60)  # 60 frames per second 
        elapsed_time = time.time() - start_time
        # add new stars every few seconds 
        if star_count > star_add_increment:
            for _ in range(3):   # add 3 stars at a time 
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            # make the game harder over time ( stars come more often )
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        # check if the player wants to stop the game 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False # stop the game
                break
        
        # check what keys are pressed 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL # move left 
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL # move right 

        # move the stars and check for collisions 
        for star in stars[:]:
            star.y += STAR_VEL # move the star down 
            if star.y > HEIGHT:
                stars.remove(star) # remove star when it goes off the screen 
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star) # remove star if it hits the player 
                hit = True # mark that the player was hit 
                break # exit the loop 

        # If the player was hit, show "You Lost!" and end the game
        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000) # wait 4 seconds before closing 
            break

        # draw everythingon the screen 
        draw(player, elapsed_time, stars)

    pygame.quit() # close the game when done 

# makes sure the game starts when we run the file 
if __name__ == "__main__":  
    main()  


   