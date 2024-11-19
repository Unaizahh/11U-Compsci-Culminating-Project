# Grade 10 Computer Science Culminating
# Unaizah Qutub
# Mr. Riverso
# January 22nd, 2024
# Title: The Quest of the Knight
# This is a hybrid maze and platformer game about a knight on a quest toe save his sister from an evil wizard. There are mutltiple levels for the player to go through.
# As they complete the various levels, the story progresses. Will the knight be successful in rescuing his sister and defeating the evil wizard? Play and find out. 

import pgzrun
import pygame
import os
from pgzhelper import *
import random

WIDTH = 1200
HEIGHT = 700

# Window Settings
os.environ['SDL_VIDEO_CENTERED'] = '1' #Forces window to be centered on screen.

# Initialize primary Actors
player = Actor('dungeon_0097')
player.scale = 3
player.pos = (30, 670)
player.dy = 0
player.isJumping = False  # controls player jumping
player.cycle = ['dungeon_0097', 'dungeon_0096']
player.images = player.cycle
player.fps = 2
player.score = 0
player.lives = 0

player.name = 'Lancelot'

# Highscore default value
highscore = 0

life = Actor('dungeon_0098') # Life symbol (the amount drawn is the number of lives)


    # flying friend
buddy = Actor('fly')
buddy.cycle = ['fly', 'fly_dead', 'fly_fly']
buddy.images = buddy.cycle
buddy.fps = 10


# Initialize Global Variables
scene = 'None'
sceneType = 'None' #Can control elements for BOTH maze levels at once 
background = None
level = 8
losing_game = False

# Initialize Secondary Actors (interactive elements: levers, moving platforms, etc...)

    # Platform Elements (buttons, levers, etc...)

platforms = [] # platform elements (to jump on: platforms, trampoline, ramps)
platformTiles = [] # platform elements (cannot jump on: railings, decor, mobs, end point, etc...)

lever1 = Actor('underground_laserswitchredoff')
platformTiles.append(lever1)

lever2 = Actor('underground_laserswitchyellowoff')
platformTiles.append(lever1)

lever3 = Actor('underground_laserswitchgreenoff')
platformTiles.append(lever3)

lever4 = Actor('underground_laserswitchgreenoff')
platformTiles.append(lever4)

ghostButton = Actor('dungeon_0108')
platformTiles.append(ghostButton)

rocks = [Actor('underground_dirtcaverocklarge'), Actor('underground_dirtcaverocklarge'), Actor('underground_dirtcaverocklarge')]

sliding_platform =  Actor('underground_stonecavespiketop')
platforms.append(sliding_platform)

descending_platform = Actor('underground_metalhalf')
platforms.append(descending_platform)

secret_ghost = Actor('dungeon_0121')
platformTiles.append(secret_ghost)

playerSword  = Actor('underground_swordbronze1') # used by player to kill enemies
playerSword.cycle = ['underground_swordbronze1', 'underground_swordbronze2', 'underground_swordbronze3', 'underground_swordbronze4']
playerSword.images = playerSword.cycle
playerSword.fps = 6

    #trampoline
trampoline = Actor('underground_laserupshoot') 
platforms.append(trampoline)

    # sword (end point for platform level)
sword = Actor('underground_swordgold4')
platformTiles.append(sword)
        
    # Flying friend
platformTiles.append(buddy)


# Maze level
mazeTiles = [] # maze (both) elements: power ups, decor, end point, etc...

maze1_grid = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
              [1,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
              [0,0,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,0],
              [0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,0,1,0],
              [0,0,0,1,0,0,0,1,0,1,0,1,0,1,0,1,0,0,1,0],
              [1,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,1,1,1,0],
              [1,1,0,0,0,0,0,1,0,1,2,1,0,1,0,0,0,0,0,0],
              [1,1,1,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,1,1],
              [1,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
              [1,1,0,1,0,1,0,1,1,1,0,1,1,1,1,2,0,0,1,0],
              [1,1,0,1,0,1,0,1,1,1,0,1,1,1,1,1,0,0,1,0],
              [1,1,2,1,0,0,0,0,0,0,0,1,1,1,1,1,0,0,1,0]
              ]
              
maze2_grid = [[4,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3],
              [4,1,2,2,2,3,0,0,0,0,0,0,0,0,4,4,4,4,4,0,1],
              [4,2,0,1,4,3,0,1,3,0,1,2,4,0,0,0,0,1,1,0,1],
              [4,0,0,0,0,0,0,1,2,2,2,2,2,2,3,0,0,0,0,0,1],
              [4,0,1,2,5,3,0,1,0,0,0,0,0,1,2,4,2,2,5,0,1],
              [4,0,1,2,2,3,0,0,0,0,0,5,2,2,2,3,0,1,2,2,3],
              [4,0,0,0,1,2,2,2,3,0,1,3,0,0,0,0,0,0,1,2,3],
              [4,0,4,0,0,0,2,0,0,0,0,1,3,0,1,2,3,0,0,0,1],
              [4,0,4,0,1,2,3,0,0,0,0,0,2,0,0,0,4,4,4,0,0],
              [4,0,4,0,0,0,5,0,1,2,3,0,1,2,4,0,1,2,2,2,3],
              [1,2,2,2,3,0,5,0,2,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,1,2,2,2,2,2,2,3,0,1,2,2,3,0,1],
              [1,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,3],
              ]

mazes_grid = [] # the grid that will be used during each maze level

mazes = [] # List for mazes to be drawn

sword = Actor('underground_swordsilver') # endpoint for maze levels
sword.scale = 0.5
mazeTiles.append(sword)

chest = Actor('dungeon_0091')
mazeTiles.append(chest) # player will gain an achievement if they get to this chest during the first maze level

# Losing screen
losing_screen = Actor('losing_screen')
losing_screen.pos = (WIDTH/2, HEIGHT/2)
losingscreencover = Actor('losingscreen_cover') # covers part of the screen I don't want, but allows me to keep the images shape
losingscreencover.pos = (598, 275)
losing_background = Actor('losinggame_background') # Losing screen background (makes it black)

# Invisible button to restart game after losing
yesButton = Actor('town_0000')
yesButton.scale = 2.75
yesButton.pos = (565,455)

# invisble button to quit game after losing
noButton = Actor('town_0000')
noButton.pos = (650, 455)

# Button that can be clicked on during the menu (intro) screen to start a new game
newGame =  Actor('intro_button')
newGame.scale = 0.9
newGame.pos = (599,584)

# Button that can be clicked on during the menu (intro) screen to continue an old game
loadGame = Actor('intro_button')
loadGame.scale = 0.9
loadGame.pos = (600,522)

level_warning = False # Allows message to appear if player tries to load a game, but there's no old game progrss

# Will allow badges to be drawn if achievment is reached by player
achievement1 = False
achievement2 = False

# Story scenes (and introduction) lists of phrases
story_scene1_words = ['You are starting the game, press the C key to continue.', 'One fateful afternoon, a knight and his sister who is a princess, were out on a stroll...',
                      'However, the knight noticed something amiss and when he turned around, he could not see his sister!',
                      'He started searching for his sister, until he heard a screen, and caught a glimpse of her being taken away!!!',
                      'The kidnapper seems to be a wizard...',
                      'Now you must chase after them and save the princess!',
                      'But be aware of the obstacles and enemies ahead, make sure to not touch any mysterious mushrooms',
                      'Good luck! (press the A, D, W, and S keys to move around, click the mouse to attack)'
                        ] # dialoge text in a list to click  through and clear when need
story_scene2_words = ['Knight: Hey you! Stop right there!', 'Knight: Where is my sister?!', 'Wizard: Mwahaha',
                      'Mysterious Creature: Hey! Do you need help?', 'Knight: Huh... Who are you?',
                      'Buddy: You can call me Buddy and I want to help',
                      "Buddy: I'm tired of the evil wizard evilness!", 'Wizard: Tsk. Annoying pest!',
                      "Buddy: He's gonna jump down, get ready to jump on platforms!", '(Press spacebar to jump', 'Knight: After him!!'] #dialoge text in a list to click  through and clear when need
story_scene3_words = ['Knight: Phew we made it out', 'Buddy: Yes, thank you for clearing the monsters',
                      'Buddy: Now my friends can be free of the evil wizard!', 'Knight: Oh your welcome, shall we go in the dungeon?',
                      'Buddy: No.', 'Knight: Why not?', 'Buddy: It is too scary and I have to go help my friends right now.',
                      'Knight: Oh ok, I must hurry inside though...', 'Buddy: You are very brave, good luck in getting your sister back!'] #dialoge text in a list to click  through and clear when need
story_scene4_words = ['Sister are you there?', 'Oh no...', 'I was too late...', 'I will get revenge!!'] # dialoge text in a list to click  through and clear when need
wordCounter = 0 # keeps track of what phrases are being said

story_scene_images = [] # List to make sure that actors appear during story scenes and disappear after

enemies = [] # List to store aliens
shooterEnemies = [] # List of enemies that can shoot at player
enemyBullet = None # bullet shot at player by enemies

powerups = []


# Functions


#Function to choose random enemy to shoot at player
def enemy_shoot():
      
    global enemyBullet, shooterEnemies, player
    
    if sceneType != 'None': # Only happening during game levls
        
        if len(enemies) > 0:
            for enemy in enemies:
                shooterEnemies.append(enemy)

                   
            shooterEnemy = random.choice(shooterEnemies)
            
            if shooterEnemy != None:
                enemyBullet = Actor('underground_laser', shooterEnemy.pos)
                enemyBullet.angle = enemyBullet.direction_to(player)
                enemyBullet.scale = 0.5
    
    clock.schedule(enemy_shoot, 10)

  
    
# Function to create enemies at specific positions (made in groups of 5)
def create_enemies(pos1, pos2, pos3, pos4, pos5):
    
    # Enemy 1
    enemy1 = Actor('bee')
    enemy1.pos = pos1
    
    # Enemy animation
    enemy1.cycle = ['bee', 'bee_fly']
    enemy1.images = enemy1.cycle
    enemy1.fps = 3
    
    # Enemy points and lives depending on level
    if scene == 'maze_level1':
        enemy1.points = 20
        enemy1.lives = 1 
    elif scene == 'platform_level':
        enemy1.points = 25
        enemy1.lives = 2
    elif scene == 'maze_level2':
        enemy1.points = 30
        enemy1.lives = 3 
        
    enemies.append(enemy1) # Added to list


    # Enemy 2
    if sceneType == 'maze':
        enemy2 = Actor('slimegreen')
    elif sceneType == 'platform':
        enemy2 = Actor('slimeblue')   # Changes enemy image depending on game level
    
    enemy2.pos = pos2
    
    # Enemy animation  
    if sceneType == 'maze':
        enemy2.cycle = ['slimegreen', 'slimegreen_walk', 'slimegreen_squashed']
    elif sceneType == 'platform':
        enemy2.cycle = ['slimeblue', 'slimeblue_blue', 'slimeblue_squashed'] # Changes enemy animation depending on game level
    
    enemy2.images = enemy2.cycle
    enemy2.fps = 3

    
    # Enemy points and lives depending on level
    if scene == 'maze_level1':
        enemy2.points = 10
        enemy2.lives = 1
    elif scene == 'platform_level':
        enemy2.points = 15
        enemy2.lives = 2
    elif scene == 'maze_level2':
        enemy2.points = 20
        enemy2.lives = 3
        
    enemies.append(enemy2) # Added to list
        

    # Enemy 3
    enemy3 = Actor('snake')
    enemy3.pos = pos3
    
    # Enemy animation
    enemy3.cycle = ['snake', 'snake_walk']
    enemy3.images = enemy3.cycle
    enemy3.fps = 2

    # Enemy points and lives depending on level
    if scene == 'maze_level1':
        enemy3.points = 5
        enemy3.lives = 1
    elif scene == 'platform_level':
        enemy3.points = 10
        enemy3.lives = 2
    elif scene == 'maze_level2':
        enemy3.points = 15
        enemy3.lives = 3
        
    enemies.append(enemy3) # Added to list


    # Enemy 4
    enemy4 = Actor('spinner')
    enemy4.pos = pos4
    
    # Enemy animation
    enemy4.cycle = ['spinner', 'spinner_spin']
    enemy4.images = enemy4.cycle
    enemy4.fps = 2
    
    # Enemy points and lives depending on level
    if scene == 'maze_level1':
        enemy4.points = 10
        enemy4.lives = 1
    elif scene == 'platform_level':
        enemy4.points = 15
        enemy4.lives = 2
    elif scene == 'maze_level2':
        enemy4.points = 20
        enemy4.lives = 3
        
    enemies.append(enemy4) # Added to list
    
    # Enemy 5
    enemy5 = Actor('barnacle')
    enemy5.pos = pos5
    
    # Emnemy animation
    enemy5.cycle = ['barnacle', 'barnacle_bite']
    enemy5.images = enemy5.cycle
    enemy5.fps = 3
    
    # Enemy points and lives depending on level
    if scene == 'maze_level1':
        enemy5.points = 50
        enemy5.lives = 1
    elif scene == 'platform_level':
        enemy5.points = 20
        enemy5.lives = 2
    elif scene == 'maze_level2':
        enemy5.points = 25
        enemy5.lives = 3
        
    enemies.append(enemy5) # Added to list
            
    return enemy1, enemy2, enemy3, enemy4, enemy5

# Create the maze walls from the maze grid depending on maze level
def create_maze():

    if scene == 'maze_level1':
        for y in range(12):
            for x in range(20):
                tile_type = mazes_grid[y][x]
                if tile_type == 0:
                    ground = Actor('town_0025')
                    ground.scale = 3
                    ground.x = x*62
                    ground.y = y*62
                    mazeTiles.append(ground) # In list to be drawn and treated as a wall
                elif tile_type == 1:
                    wall = Actor('treewall')
                    wall.scale = 2
                    wall.x = x*62
                    wall.y = y*62
                    mazes.append(wall) # In list to be drawn and treated as a wall
                elif tile_type == 2:
                    mushroom = Actor('town_0029')
                    mushroom.scale = 2
                    mushroom.x = x*62
                    mushroom.y = y*62
                    mazeTiles.append(mushroom) # In list to be drawn
                    
                
    if scene == 'maze_level2':
        for y in range(13):
            for x in range(21):
                tile_type = mazes_grid[y][x]
                if tile_type == 1:
                    wallLeft = Actor('town_0099')
                    wallLeft.scale = 3.7
                    wallLeft.x = x*60 
                    wallLeft.y = y*60 
                    mazes.append(wallLeft) # In list to be drawn and treated as a wall          
                elif tile_type == 2:
                    wallMid = Actor('town_0100')
                    wallMid.scale = 3.7
                    wallMid.x = x*60
                    wallMid.y = y*60
                    mazes.append(wallMid) # In list to be drawn and treated as a wall
                elif tile_type == 3:
                    wallRight = Actor('town_0101')
                    wallRight.scale = 3.7
                    wallRight.x = x*60
                    wallRight.y = y*60
                    mazes.append(wallRight) # In list to be drawn and treated as a wall
                elif tile_type == 4:
                    brick = Actor('dungeon_0019')
                    brick.scale = 3.7
                    brick.x = x*60
                    brick.y = y*60
                    mazes.append(brick)
                elif tile_type == 5:
                    spider = Actor('dungeon_0122')
                    spider.scale = 3.7
                    spider.x = x*60
                    spider.y = y*60
                    mazeTiles.append(spider)                    



    # Funtion to create platforms (that the player can and can't jump on) with any type of tiles and length
def create_platform(leftI, rightI, middleI, pos, length, is_platform): 
    
    if sceneType == 'platform':
        # Create the left-most piece of the platform
        left = Actor(leftI)
        left.scale = 0.5
        left.pos = pos
        
        # Create specific amount of middle tiles depending on the length
        for i in range(1, length-1):
            middle = Actor(middleI)
            middle.scale = 0.5
            middle.y = left.y
            middle.x = left.x + (i*35)
            # Append to specific lists for interactablility 
            if is_platform == True:
                platforms.append(middle)
            else:
                platformTiles.append(middle)
        
        # Create the right-most piece of the platforms
        right = Actor(rightI)
        right.scale = 0.5
        right.y = left.y
        right.x = left.x + ((length-1)*35)
        
        # Append to specific list for interactablility 
        if is_platform == True:
            platforms.append(left)
            platforms.append(right)
        else:
            platformTiles.append(left)
            platformTiles.append(left)
        
    return left
    return right
    return middle

# Function to create power up at any location
def create_powerup(pos):
    
    powerup = Actor('dungeon_0116')
    powerup.scale = 3
    powerup.pos = pos
    
    powerups.append(powerup)
    

    # Function to load the levels of the game
def load_level(levels):
    
    global level, scene, background, platforms, platformTiles, buddy, trampoline, player, key, mazeTiles, sword, lever1, lever2, lever3,lever4, rocks, ghostButton, sliding_platform, descending_platform, losing_background, playerSword, sceneType, mazes, mazes_grid, maze1_grid, maze2_grid, unlock, story_scene1_words, chest, powerups, song
    
    background = None
    player.pos = (50, 655) # resets player position
    
    # Reset platform elements
    platformTiles.clear()
    platforms.clear()
    
    # Reset maze elements
    mazeTiles.clear()
    mazes.clear()
    
    # Reset enemies
    enemies.clear()
    shooterEnemies.clear()
    
    # Reset story scene images
    story_scene_images.clear()
    
    # Reset powerups
    powerups.clear()
    
    # Reset level_warning
    level_warning = False
    
    
    if levels == 1:
        level = 1
        scene = 'story_scene1'
        background = 'losinggame_background'
        player.pos = (-100, -100) #removes player from the screen
        sceneType = 'None'



    elif levels == 2:
        level = 2
        player.pos = (44, 169)
        player.lives = 5
        scene = 'maze_level1'
        background = 'maze1_background'
        sceneType = 'maze'
        
        mazes_grid = maze1_grid # this level's walls will be drawn
        
        # Plays song
        music.play('worldmap_theme')

        # Creates the maze layout on maze level
        create_maze()
        
        # Creates Powerups at random locations on the ground                        
        valid = False
              
        while valid == False:
                
            powerup_x = random.randint(0, 19)
            powerup_y = random.randint(0, 11)
                
            if mazes_grid[powerup_y][powerup_x] == 0:
                    
                temp_pos = (powerup_x*62, powerup_y*62)
                    
                create_powerup(temp_pos)
                    
                if len(powerups) == 5: # Stops generating powerups until 5 are made
                    valid = True
                
        
        # Actors
        
        sword = Actor('underground_swordsilver')
        sword.pos = (1173, 672)
        mazeTiles.append(sword)
        
        chest = Actor('dungeon_0091')
        chest.pos = (992,248)
        chest.scale = 2
        mazeTiles.append(chest)
        
            # Enemies
        create_enemies((743,61), (491,499), (989,184), (372,162), (992, 497))
        create_enemies((248,648), (621,621), (1171,497), (124,499), (744, 189))
        
    elif levels == 3:
        level = 3
        background = 'story_scene1_background'
        scene = 'story_scene2'
        sceneType = 'None'
        
        # Actors
        player.pos = (220, 590) # changes player position on screen
        player.scale = 4

        wizard = Actor('dungeon_0084')
        wizard.scale = 5
        wizard.flip_x = True
        wizard.pos = (840,570)
        story_scene_images.append(wizard)

    elif levels == 4:
        level = 4
        player.lives = 4
        scene = 'platform_level'
        background = 'platform_background2'
        sceneType = 'platform'
        
        # Song
        music.play('boss_theme')
        
        # Creates Powerups at random locations                        
        valid = False
              
        while valid == False:
                
            powerup_x = random.randint(200, 1000)
            powerup_y = random.randint(100, 600)
                                    
            temp_pos = (powerup_x, powerup_y)
                    
            create_powerup(temp_pos)
                    
            if len(powerups) == 4: # Stops generating powerups until 4 are made
                valid = True              
        
        # Player sword  (changing type)     
        playerSword.image = 'underground_swordsilver1'
        playerSword.cycle = ['underground_swordsilver1', 'underground_swordsilver2', 'underground_swordsilver3', 'underground_swordsilver4']
        playerSword.images = playerSword.cycle
        playerSword.fps = 6
        
        # platforms
        create_platform('underground_dirtcaveleft', 'underground_dirtcaveright', 'underground_dirtcavemiddle', (15, 690), 10, True)
        create_platform('underground_dirtcaveleft', 'underground_dirtcaveright', 'underground_dirtcavemiddle', (1000, 580), 7, True)
        create_platform('underground_metalcliffleft', 'underground_metalcliffright', 'underground_metalcenterwarning', (5, 440), 24, True)
        create_platform('underground_beamboltsnarrow', 'underground_beamboltsnarrow', 'underground_beamboltsnarrow', (450, 410), 1, True)      
        create_platform('underground_metalhalfleft', 'underground_metalhalfright', 'underground_metalhalfmid', (150, 275), 4, True)
        create_platform('underground_metalcliffleft', 'underground_metalcliffright', 'underground_metalcentersticker', (440, 225), 10, True)
        create_platform('underground_stonecaveleft', 'underground_stonecaveright', 'underground_stonecavemiddle', (940, 190), 7, True)
        create_platform('underground_metalplatformwirealt', 'underground_metalplatformwirealt', 'underground_metalplatformwirealt', (WIDTH/2, 50), 2, True)
        
        # lever 1 platforms
        
        rocks = [Actor('underground_dirtcaverocklarge'), Actor('underground_dirtcaverocklarge'), Actor('underground_dirtcaverocklarge')]
      
        # lever 2 platform
        sliding_platform =  Actor('underground_stonecavespiketop')
        sliding_platform.pos = (780, 455)
        platforms.append(sliding_platform)
        
        #lever 3 and lever 4 platform
        
        descending_platform = Actor('underground_metalhalf')
        descending_platform.pos = (819, -10)
        platforms.append(descending_platform)
        

        # decor
        create_platform('underground_umbrellaopen', 'underground_umbrellaopen', 'underground_umbrellaopen', (60, 657), 1, False)
        create_platform('underground_beamholes', 'underground_beamholes', 'underground_beamholes', (440, 190), 11, False)

        
        # Actors
        
            #trampoline
        trampoline = Actor('underground_laserupshoot') 
        trampoline.pos = (50,400)
        trampoline.scale = 0.7
        platforms.append(trampoline)

            # sword(end point)
        sword = Actor('underground_swordgold')
        sword.pos = (617, 20)
        sword.scale = 0.5
        platformTiles.append(sword)
        
            #levers
        lever1 = Actor('underground_laserswitchredoff')
        lever1.scale = 0.5
        lever1.pos = (240, 655)
        platformTiles.append(lever1)

        lever2 = Actor('underground_laserswitchyellowoff')
        lever2.scale = 0.5
        lever2.pos = (1050, 545)
        platformTiles.append(lever2)
        
        lever3 = Actor('underground_laserswitchgreenoff')
        platformTiles.append(lever3)
        lever3.scale = 0.5
        lever3.pos = (1180, 300)
        lever3.angle = 90
        
        lever4 = Actor('underground_laserswitchgreenoff')
        lever4.scale = 0.5
        lever4.pos = (1000, 155)
        platformTiles.append(lever4)
        
        ghostButton = Actor('dungeon_0108')
        ghostButton.scale = 2
        ghostButton.pos =(1195, 650)
        ghostButton.angle = 15
        platformTiles.append(ghostButton)


            # flying friend
        buddy = Actor('fly')
        buddy.cycle = ['fly', 'fly_dead', 'fly_fly']
        buddy.images = buddy.cycle
        buddy.fps = 10
        platformTiles.append(buddy)
            
            # Enemies
        create_enemies((400, 89), (593,406), (212,410), (171,643), (1121,143))     
        create_enemies((870, 69), (1155,546), (357,410), (260,230), (603,178))     
        create_enemies((980,333), (730,190), (458,190), (703, 395), (514,395)) 


    elif levels == 5:
        level = 5
        background = 'story_scene3_image'
        scene = 'story_scene3'
        sceneType = 'None'
        
        # Actor
        player.pos = (610, 608)
        player.scale = 4
        player.flip_x = True
        
        buddy.pos = (524,558)
        story_scene_images.append(buddy)
        
    
    elif levels == 6:
        level = 6
        player.lives = 3
        background = 'maze2background'
        scene = 'maze_level2'
        sceneType = 'maze'
        
        mazes_grid = maze2_grid # this level's walls will be drawn
        
        # Song
        music.play('desert_theme')
    
        #creates the maze layout on maze level
        create_maze()
        
        # Creates Powerups at random locations on the ground                        
        valid = False
           
        while valid == False:
                
            powerup_x = random.randint(0, 20)
            powerup_y = random.randint(0, 12)
                
            if mazes_grid[powerup_y][powerup_x] == 0:
                    
                temp_pos = (powerup_x*60, powerup_y*60)
                    
                create_powerup(temp_pos)
                    
                if len(powerups) == 3: # Stops generating powerups until 3 are made
                    valid = True
        
        # Player sword (changing type)
        playerSword.image = 'underground_swordgold1'
        playerSword.cycle = ['underground_swordgold1', 'underground_swordgold2', 'underground_swordgold3', 'underground_swordgold4']
        playerSword.images = playerSword.cycle
        playerSword.fps = 6
        
        # Actors
        
        # Key to reveal exit door
        unlock = Actor('town_0117') 
        unlock.pos = (1140, 665)
        unlock.scale = 2
        mazeTiles.append(unlock)
        
            # Enemies (bees are removed from the screen)
        create_enemies((1300,-10), (360,122), (783,425), (276,422), (957, 182))
        create_enemies((1300,-10), (298,541), (902,604), (961, 358), (541,480)) 
        create_enemies((1300,-10), (60,550), (902,604), (961, 358), (541,480)) 
        create_enemies((1300,-10), (540,602), (1164,481), (779,60), (417,600))

    
    elif levels == 7:
        level = 7 
        background = 'story_scene4_image'
        scene = 'story_scene4'
        sceneType = 'None'
       
        # Actors
        player.pos = (925, 650) #removes player from the screen
        player.scale = 4
        player.flip_x = True
        
    elif levels == 8:
        
        background = 'menu_screen'
        scene = 'intro'
        player.pos = (-100, -100) #removes player from the screen
        sceneType = 'None'



    # Function for the interactive elements of the platform level
def platform_level_elements(rocks):
    
    if losing_game == False:
        
        # Lever 1
        if player.colliderect(lever1) and lever1.image == 'underground_laserswitchredoff':
            lever1.image = 'underground_laserswitchredon'
            for i in range(4):
                for rock in rocks:
                    rock.scale = 0.8
                    rock.x = i*170
                    rock.y = i*-25 + 750
                    platforms.append(rock)
                    i += 1
        
        # Lever 2
        if player.colliderect(lever2):
            
            # change lever image 
            lever2.image = 'underground_laserswitchyellowon'
            lever2.scale = 0.5
            
            # moves platform forward until it reaches a certain point
            if sliding_platform.x <= 1000:
                sliding_platform.x += 0.5
                    
        elif not player.colliderect(lever2):
            
            # change levr image
            if lever2.image == 'underground_laserswitchyellowon':
                lever2.image = 'underground_laserswitchyellowoff'
                lever2.scale = 0.5
            
            #moves platform back until it reaches a certain point
                
            if sliding_platform.x >= 780:
                sliding_platform.x -= 0.5
        
        # Lever 3 and 4
        if player.colliderect(lever4) and buddy.colliderect(lever3):
            
            # change lever images
            lever4.image = 'underground_laserswitchgreenon'
            lever4.scale = 0.5
            lever3.image = 'underground_laserswitchgreenon'
            lever3.scale = 0.5
            
            # fix platform scale
            descending_platform.scale = 0.5
            
            # moving platform down until it reachers a certain point            
            if descending_platform.y <= 115:
                descending_platform.y += 1
        else:
            # change lever images
            lever4.image = 'underground_laserswitchgreenoff'
            lever4.scale = 0.5
            lever3.image = 'underground_laserswitchgreenoff'
            lever3.scale = 0.5

        
def on_key_down(key):
    
    global level, scene, phrase, losing_game, wordCounter, story_scene1_words
        
    # transition from story scenes to next game level (exiting story scenes)
        
    if scene == 'story_scene1':
           
        if key == keys.C:

            wordCounter += 1 # goes through dialouge list index for story scenes
            
            if wordCounter == len(story_scene1_words):
                wordCounter = 0
                level = 2
                load_level(2)
       
    elif scene == 'story_scene2':
        
        if key == keys.C:

            wordCounter += 1 # goes through dialouge list index for story scenes         
            
            if wordCounter == len(story_scene2_words):
                wordCounter = 0
                level = 4
                load_level(4)
                                               
    elif scene == 'story_scene3':
    
        if key == keys.C:

            wordCounter += 1 # goes through dialouge list index for story scenes         
            
            if wordCounter == len(story_scene3_words):
                wordCounter = 0           
                level = 6
                load_level(6)
                
    elif scene == 'story_scene4':
        
        if key == keys.C:

            wordCounter += 1 # goes through dialouge list index for story scenes
        
            # Plays door opening sound in the beginning of the scene
            if wordCounter == 1:
                sounds.story_scene4_opening.play()
            
            if wordCounter == len(story_scene4_words):
                
                sounds.story_scene4_ending.play() # Ending game sound
                
                # Goes back to menu screen
                wordCounter = 0           
                level = 8
                load_level(8) 

        
    # allows character to jump on swordpress
    if scene == 'platform_level' and losing_game == False: # prevents player jump when game is lost
        if key == keys.SPACE and player.isJumping == False:
            player.dy = -11
            player.isJumping = True
            player.scale = 3
            player.animate()


# Function to draw the words of the story scene s
def story_scenes(): 
    
    global wordCounter, story_scene1_words, story_scene2_words, story_scene3_words, story_scene4_words
    
    story_scene1_words = ['You are starting the game, press the C key to continue throughout the game.', 'One fateful afternoon, a knight and his sister who is a princess, were out on a stroll...',
                      'However, the knight noticed something amiss and when he turned around, he could not see his sister!',
                      'He started searching for his sister, until he heard a scream, and caught a glimpse of her being taken away!!!',
                      'The kidnapper seems to be a wizard...',
                      'Now you must chase after them and save the princess!',
                      'But be aware of the obstacles and enemies ahead, make sure to not touch any mysterious mushrooms',
                      'Good luck! (press the A, D, W, and S keys to move around, click the mouse to attack)', 'Get to the sword.',
                      'Potions give you health, but do not take them if you do not need them'
                        ] # Dialoge
    story_scene2_words = ['Knight: Hey you! Stop right there!', 'Knight: Where is my sister?!', 'Wizard: Mwahaha',
                      'Mysterious Creature: Hey! Do you need help?', 'Knight: Huh... Who are you?',
                      'Buddy: You can call me Buddy and I want to help',
                      "Buddy: I'm tired of the evil wizard evilness! I must help my home.", 'Wizard: Tsk. Annoying pest!',
                      "Buddy: He's gonna jump down, get ready to jump on platforms!", '(Press spacebar to jump)', 'Knight: After him!!', '(Buddy will follow your mouse. Get to the sword)'] #dialoge
    story_scene3_words = ['Knight: Phew we made it out', 'Buddy: Yes, thank you for clearing the monsters',
                      'Buddy: Now my friends can be free of the evil wizard!', 'Knight: Oh your welcome, shall we go in the dungeon?',
                      'Buddy: No.', 'Knight: Why not?', 'Buddy: It is too scary and I have to go help my friends right now.',
                      'Knight: Oh ok, I must hurry inside though...', 'Buddy: You are very brave, good luck in getting your sister back!', '(Unlock the door and avoid the spiders...)'] #dialoge
    story_scene4_words = ['Sister are you there?', 'Oh no...', 'I was too late...', 'I will get revenge!!'] # dialoge text in a list to click  through and clear when need

    #Story scene 1
    if scene == 'story_scene1':   
        
        screen.draw.text(story_scene1_words[wordCounter], (130, (wordCounter*50) + 75), fontsize = 30)
        
    else:      
        story_scene1_words.clear()
    
    # Story scene 2
    if scene == 'story_scene2':   
        
        screen.draw.text(story_scene2_words[wordCounter], (300,645), fontsize = 30, background = 'black')
    
    else:      
        
        story_scene2_words.clear()
        
    # Story scene 3
    
    if scene == 'story_scene3':   
        
        screen.draw.text(story_scene3_words[wordCounter], (420,647), fontsize = 30, background = 'black')
              
    else:      
        
        story_scene3_words.clear()
        
    # Story scene 4
    if scene == 'story_scene4':   
        
        screen.draw.text(story_scene4_words[wordCounter], (650,630), fontsize = 35, background = 'black')

    else:      
        
        story_scene4_words.clear()        


def on_key_up(key):
    
    # Allows player animation to cylce through images during game levels
    if sceneType != None:
        if key == keys.SPACE:
            player.images = player.cycle
        
        # Buddy (flying friend) animation
        if scene == 'platform_level':
            buddy.images = buddy.cycle
        
        # Enemies animation
        for enemy in enemies:
            enemy.images = enemy.cycle
        


def on_mouse_move(pos):
    
    global playerSword, achievement1
    
    if scene == 'platform_level' and losing_game == False:
        
        # Buddy will follow cursor
        buddy.pos = pos
        
        # Buddy will kill flying bees
        for enemy in enemies:
            if buddy.colliderect(enemy) and enemy.image == 'bee':
                enemy.lives -= 1
        
        # If Buddy gets a powerup, player's number of lives increases (if below limit)
        for powerup in powerups:
            if buddy.colliderect(powerup):
                sounds.power_up.play()
                powerups.remove(powerup)
                if player.lives < 4:
                    player.lives += 1
                    
        # makes secret ghost appear if buddy touches the green ghost 
        if buddy.colliderect(ghostButton):
            
            # Other ghost appears
            secret_ghost.pos = (197,204)
            secret_ghost.scale = 1.5
            platformTiles.append(secret_ghost)
        
            sounds.ghost_achievement.play() # Sound
            achievement1 = True # achievement obtained
    
    # If losing game screen appears, music will play 
    if losing_game == True:
        sounds.losing_game.play()
        

def on_mouse_down(pos, button):
    
    global yesButton, losing_game, playerSword, level, level_warning
    
    # During the intro (menu screen), if the newGame button is clicked, a new game will load, if loadGame button is clicked, the previous game will continue
    if scene == 'intro':
        
        #Starts new game
        if newGame.collidepoint_pixel(pos):
            player.score = 0 # Resets score
            level = 1
            load_level(1)
        
        #Loads old game
        if loadGame.collidepoint_pixel(pos):
            load_level(level)
            
        # If load game button is pressed but there is no game progress, variable allows message to appear 
        if loadGame.collidepoint_pixel(pos) and level == 8:
            level_warning = True

    if losing_game == True:
        
        if yesButton.collidepoint_pixel(pos): # Button to let player retry level after they lose
            losing_game = False
            load_level(level)
            
        if noButton.collidepoint_pixel(pos): # Button to go back to the starting screen
            losing_game = False
            load_level(8)
            # level = 8 doesn't happen, The global level variable remains the same, because it can be used later for the player to continue the game
    
    # makes sword appear on mouse press (only during game levels)
    if sceneType == 'maze' or sceneType == 'platform':   
        if playerSword not in platformTiles:
            platformTiles.append(playerSword)
            sounds.sword_slash.play() # sword slashing sound
    
    # Enemies will lose only one life if attacked by sword
    for enemy in enemies:
        
        if playerSword.colliderect(enemy) and enemy.lives > 0:
            sounds.enemy_hit.play()
            enemy.lives -= 1
                  

def on_mouse_up(pos, button):

    # removes player sword (Allows slashing only during mouse click)
    if playerSword in platformTiles:
        platformTiles.remove(playerSword)

# Functions for mouse movement (to be used for maze levels) 
def move_up():
    player.y -= 2
    #Player animation while moving
    player.scale = 3
    player.animate()

def move_down():
    player.y += 2
    # Player animation while moving
    player.scale = 3
    player.animate()
    
def move_left():
    player.x -= 2
    player.flip_x = True # Changes direction character faces
    # Player animation while moving
    player.scale = 3
    player.animate()

def move_right():
    player.x += 2
    player.flip_x = False # Changes direction character faces
    # Player animation while moving
    player.scale = 3
    player.animate()



# Update - Handle ongoing input, update positions, check interactions
def update():
    
    
    global trampoline, key, level, lever1, lever2, lever3, lever4, ghostButton, rocks, losing_game, sword, chest, enemyBullet, achievement1, achievement2, highscore, sceneType
        
    # Stops music when game level is over
    if sceneType != 'maze' and sceneType != 'platform':
        music.stop()
    
    # Updates player size to prevent image errors
    player.scale = 3 
  
    # Buddy animation
    buddy.animate()
    buddy.flip_x = True
    
    
    if losing_game == True:
        
        # Make sceneType None when game is lost to prevent game actions from happening
        sceneType = 'None'          
    
    for enemy in enemies:
                
        # Enemies animation
        enemy.animate()
        
        # When an enemy loses all their lives, they disapear (die) and their points is added to the player score
        if enemy.lives == 0:
            enemies.remove(enemy)
            player.score += enemy.points
    
    for enemy in shooterEnemies:
        
        # If the enemy is killed, it can no longer shoot bullets
        if enemy.lives == 0:
            shooterEnemies.remove(enemy)
    
    # Enemy bullet
    if enemyBullet != None: # (Attempt to) Prevent bullet moving during story scenes
            
        # Bullet shot by enemy will go towards player
        enemyBullet.move_forward(5)
        
        # Plays sound
        sounds.enemy_shoot.play()
        
        # Bullet will disapear if out of boundaries
        if enemyBullet.top > HEIGHT or enemyBullet.bottom < 0 or enemyBullet.left < 0 or enemyBullet.right > WIDTH:
            enemyBullet = None
 
    # If a bullet hits the player, the player loses a life and the bullet disapears
    if enemyBullet != None and player.colliderect(enemyBullet):
        sounds.player_hit.play()
        player.lives -= 1
        enemyBullet = None
        
        
    # Updates highscore
    if player.score > highscore:
        highscore = player.score
        

    if sceneType == 'maze' or sceneType == 'platform':
        
        # When player loses all their lives, they will lose and the screen appears        
        if player.lives <= 0:
            losing_game = True

            # Animates player sword
        if playerSword in platformTiles:
            playerSword.animate()
            
        #Updates y position of sword relative to the player        
        playerSword.y = player.y - 15    
        
        # Updates x position of sword relative to the player
        if player.flip_x == True:
            playerSword.x = player.x - 30
            # changes direction of sword slashing movement
            playerSword.flip_x = True
        else:
            playerSword.x = player.x + 30
        
        # Only allows sword to slash once per mouse click by removing it after it completes animation (for every sword type)
        if (playerSword.image == 'underground_swordbronze4' or playerSword.image == 'underground_swordsilver4' or playerSword.image == 'underground_swordgold4') and playerSword in platformTiles:
            platformTiles.remove(playerSword)
    

    # maze (both) controls
    if sceneType == 'maze' and losing_game == False: # prevents player movement when game is lost              

        old_pos = player.pos # keeps track of player pos, to move them back there if they touch a wall

        # allows movement               
        if keyboard[keys.A] and player.left > 0:
            move_left()
        elif keyboard[keys.D] and player.right < WIDTH:
            move_right()
        elif keyboard[keys.W] and player.top > 0:                   
                move_up()
        elif keyboard[keys.S] and player.bottom < HEIGHT:
            move_down()
            
        # If player touches a mushroom (maze level 1) or spider (maze level 2), they die
        for thing in mazeTiles:
            if player.colliderect(thing) and (thing.image == 'town_0029' or thing.image == 'dungeon_0122'):
                player.lives -= 1
            
       # checks if player is touching a wall and moves them
        if player.collidelist(mazes) != -1:
           player.pos = old_pos


    if scene == 'maze_level1':
            
        # If Player gets a powerup, player's number of lives increases (if below limit)
        for powerup in powerups:
            if player.colliderect(powerup):
                sounds.power_up.play()
                powerups.remove(powerup)
                if player.lives < 5:
                    player.lives += 1

        # When player reaches the door they move on to the next level
        if player.colliderect(sword):
            sounds.level_complete.play() # Exit sound
            level = 3
            load_level(3)
        
        # When player touches the chest, they get an achievement 
        if player.colliderect(chest):
            sounds.chest_achievement.play()
            achievement2 = True 
    
    if scene == 'maze_level2':
        
        # When player reaches the key, the reveal the exit door
        if player.colliderect(unlock):
            
            # Sound plays
            sounds.key.play()
            
            #key disappears
            if unlock in mazeTiles:
                mazeTiles.remove(unlock)
            
            # Exit door appears
            sword = Actor('dungeon_0045') # exit door
            sword.pos = (1143, 70)
            sword.scale = 2
            mazeTiles.append(sword)
        
        # If Player gets a powerup, player's number of lives increases (if below limit)
        for powerup in powerups:
            if player.colliderect(powerup):
                sounds.power_up.play()
                powerups.remove(powerup)
                if player.lives < 3:
                    player.lives += 1
        
        # When player reaches the door, they move on to the next level
        if player.colliderect(sword):
            sounds.level_complete.play() # Exit sound
            level = 7
            load_level(7)
     

    
    # Platform level controls
    if sceneType == 'platform' and losing_game == False: # prevents player movement and action when game is lost

    # Makes bee enemies shift around within boundaries
        for enemy in enemies:
            if enemy.image == 'bee' and enemy.right < WIDTH and enemy.left > 0 and enemy.top > 0 and enemy.bottom < HEIGHT:
                enemy.x += random.randint(1,10)
                enemy.x -= random.randint(1,10)
                enemy.y += random.randint(1,3)
                enemy.y -= random.randint(1,3)
                
        # Moves player left and right (faster than on maze levels)
        if keyboard[keys.A] and player.left > 0:
            player.x -= 3
            player.flip_x = True
            # Player animation while moving
            player.scale = 3
            player.animate()
        elif keyboard[keys.D] and player.right < WIDTH:
            player.x += 3
            player.flip_x = False
            # Player animation while moving
            player.scale = 3
            player.animate()

        # PLayer can jump
        if player.isJumping == True:
            player.dy += 0.5   
            player.y += player.dy
            player.scale = 3
            player.animate() # player animation
        else:
            # Veritcal movement and gravity (player will fall if not on platform)
            player.y -= player.dy
            player.dy -= 0.7
        
        # Player will land on top of platforms 
        for platform in platforms:
            if player.collide_pixel(platform) and player.top < platform.top: # Prevents play from landing on platform just by touching it
                player.dy = 0
                player.isJumping = False
                player.bottom = platform.top
        
        # Player can jump on trampoline 
        if player.colliderect(trampoline):
            player.dy = 10
            if player.y <= 300:
                player.dy = 0
            trampoline.image = 'underground_laserup'
        else:
            trampoline.image = 'underground_laserupshoot'
            trampoline.scale = 0.7
 
         # If Player gets a powerup, player's number of lives increases (if below limit)
        for powerup in powerups:
            if player.colliderect(powerup):
                sounds.power_up.play()
                powerups.remove(powerup)
                if player.lives < 3:
                    player.lives += 1
            
        # Player loses game if they fall off the map
        if player.y > HEIGHT:
            losing_game = True 
        
        #Interactive elements (levers, etc...)
        platform_level_elements(rocks)
        
         # Game level transition
        if sword.colliderect(player):
            sounds.level_complete.play() # Exit sound
            level = 5
            load_level(5)

    # Buddy (flying friend) appears in the middle of the second story scene
    if scene == 'story_scene2' and wordCounter >= 3:
        
        buddy.flip_x = True
        buddy.pos = (222,442)
        story_scene_images.append(buddy)
    
    # Not alive sister appears a little after the last story scene starts
    if scene == 'story_scene4' and wordCounter >= 1:
        
        sister = Actor('dungeon_0099')
        sister.scale = 4
        sister.angle = 90
        sister.pos = (472,680)
        story_scene_images.append(sister)
        
        # Sister's ghost
        sisterGhost = Actor('dungeon_0121')
        sisterGhost.scale = 3
        sisterGhost.pos = (472, 630)
        story_scene_images.append(sisterGhost)

# Score and lives backgrounds
BOX1 = Rect((43, 10), (180, 50)) #background for score
BOX2 = Rect((240, 10), (250, 50)) #background for lives

# Draw
def draw():
    
    screen.clear()
        
    # changes background depended on level
    screen.blit(background, (0,0))
    
        
    # Tiles that player can land on during the platform level
    for platform in platforms:
        platform.draw() 
   
    # maze walls during maze levels
    for maze in mazes:
        maze.draw()
    
    # maze flooring and other elements
    for tile in mazeTiles:
        tile.draw()
        
    for powerup in powerups:
        powerup.draw()

    # Enemies
    for enemy in enemies:
        enemy.draw()

    # draw player
    player.draw()

    # Tiles that player can't land on
    for platform in platformTiles:
        platform.draw() 
    
    # Enemy's bullet
    if enemyBullet != None:
        enemyBullet.draw()
    
    # Powerups
    for powerup in powerups:
        powerup.draw()
    story_scenes()
    
    #Draw characters in story scenes
    for character in story_scene_images:
        character.draw()
    
    # Losing game screen appear when player loses
    if losing_game == True:
        losing_background.draw()
        losing_screen.draw()
        losingscreencover.draw()
        
    if sceneType == 'maze' or sceneType == 'platform':
        
        # Displayes score and 'lives' indicator   
        screen.draw.filled_rect(BOX1, (0,0,0))
        screen.draw.text(f'Score: {player.score}', (50,20), fontsize = 40)
        
        screen.draw.filled_rect(BOX2, (0,0,0))
        screen.draw.text(f'Lives:', (250,20), fontsize = 40)
        
        # Displays icon for each life the player has (number of images = number of lives)
        for i in range(player.lives):
            life.y = 30 
            life.x = (i*30) + 350
            life.scale = 2
            life.draw()
        
        # Show player name
        if losing_game == False:
            screen.draw.text(player.name, (player.left - 10, player.bottom + 1))       
            
    if scene == 'intro':
        

        # Draw badges if the player got the specific achievemnt and if not
        if achievement1 == True:
            badge = Actor('badge')
            badge.scale = 0.1
            badge.pos = (440,400)
            badge.draw()
        else:
            screen.draw.text('Achievement not reached yet.', (350,400))
        
        if achievement2 == True:
            badge = Actor('badge')
            badge.scale = 0.1
            badge.pos = (740,400)
            badge.draw()
        else:
            screen.draw.text('Achievement not reached yet.', (650,400))
            
        # Shows player highscore
        screen.draw.text(f'Highscore: {highscore}', (525,300), fontsize = 40)
    
    # Level warning displayed if player if player tries to load a level with no previous progress
    if level_warning == True and level == 8:
        screen.draw.text('You have no current progress...', (840,519), color = (255,255,255))
    

# Scheduling and Go:

clock.schedule(enemy_shoot, 1)

load_level(8)

pgzrun.go()