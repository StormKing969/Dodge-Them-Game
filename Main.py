import pygame
import time
import random

pygame.init()

# Size Of The Screen
display_width = 800
display_height = 600

# Colors Values
black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)
light_red = (255, 0, 0)
light_green = (0, 255, 0)
beige = (245, 241, 222)

# Car Width
car_width = 80

# Pause Condition
pause = False

# Creeation Of The Game Screen
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Avoid The Them')
clock = pygame.time.Clock()

# Importing The Car Image
carImg = pygame.image.load('Car.png')
carIcon = pygame.image.load('CarIcon.png')

# Screen Icon
pygame.display.set_icon(carIcon)

# Scoring System
def things_dodged(count):
	font = pygame.font.SysFont(None, 25)
	text = font.render('Dodged: ' + str(count), True, light_red)
	gameDisplay.blit(text, (0, 0))

# Obstacles
def things(thingx, thingy, thingw, thingh, color):
	pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

# Buttons Hovering & Function
def button(msg, x, y, w, h, inactive_color, active_color, action = None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	# Button Boundaries
	if (x + w) > mouse[0] > x and (y + h) > mouse[1] > y:
		pygame.draw.rect(gameDisplay, active_color, (x, y ,w , h))
		if click[0] == 1 and action != None:
			action()

	else:
		pygame.draw.rect(gameDisplay, inactive_color, (x, y ,w , h))

	# Button Text
	SmallText = pygame.font.Font('freesansbold.ttf', 20)
	TextSurface, TextRect = text_objects(msg, SmallText)
	TextRect.center = ((x + (w/2)), (y + (h/2)))
	gameDisplay.blit(TextSurface, TextRect) 

# Quit Function
def quitGame():
	pygame.quit()
	quit()

# Creation Of Car Image 
def car(x, y):
	gameDisplay.blit(carImg, (x, y))

# Display Screen When The Car Crashed
def crash():
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		gameDisplay.fill(black)
		LargeText = pygame.font.Font('freesansbold.ttf', 115)
		TextSurface, TextRect = text_objects('You Crashed', LargeText)
		TextRect.center = ((display_width/2), (display_height/2))
		gameDisplay.blit(TextSurface, TextRect)

		button('PLAY AGAIN', 150, 450, 125, 50, green, light_green, game_loop)
		button('QUIT', 550, 450, 100, 50, red, light_red, quitGame)

		pygame.display.update()
		clock.tick(15)

# Text Letters/Size
def text_objects(text, font):
	TextSurface = font.render(text, True, beige)
	return TextSurface, TextSurface.get_rect()

# Unpause Function
def unpaused():
	global pause 
	pause = False

# Pause
def game_pause():
	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		gameDisplay.fill(black)
		LargeText = pygame.font.Font('freesansbold.ttf', 115)
		TextSurface, TextRect = text_objects('PAUSED', LargeText)
		TextRect.center = ((display_width/2), (display_height/2))
		gameDisplay.blit(TextSurface, TextRect)

		button('CONTINUE', 150, 450, 110, 50, green, light_green, unpaused)
		button('QUIT', 550, 450, 100, 50, red, light_red, quitGame)

		pygame.display.update()
		clock.tick(15)

# Introduction
def game_intro():
	intro = True
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		gameDisplay.fill(black)
		LargeText = pygame.font.Font('freesansbold.ttf', 115)
		TextSurface, TextRect = text_objects('DODGE THEM', LargeText)
		TextRect.center = ((display_width/2), (display_height/2))
		gameDisplay.blit(TextSurface, TextRect)

		button('GO !!!', 150, 450, 100, 50, green, light_green, game_loop)
		button('QUIT', 550, 450, 100, 50, red, light_red, quitGame)

		pygame.display.update()
		clock.tick(15)

# Game Function
def game_loop():

	global pause

	# Car Image Location
	x = (display_width * 0.45)
	y = (display_height * 0.8)

	# Diretion Changing Variable
	x_change = 0
	y_change = 0

	#Spawn Location
	thing_startx = random.randrange(0, display_width)
	thing_starty = -600
	thing_speed = 3
	thing_width = 100
	thing_height = 100

	# Score
	dodged = 0

	# Exit Variable
	gameExit = False

	# Logic Loop
	while not gameExit:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			# Car Controls
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					x_change = -6
				elif event.key == pygame.K_RIGHT:
					x_change = 6	
				elif event.key == pygame.K_UP:
					y_change = -6
				elif event.key == pygame.K_DOWN:
					y_change = 6
				elif event.key == pygame.K_p:
					pause = True
					game_pause()

			# Car Controls
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					x_change = 0

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					y_change = 0

		# Car X-Location Variable
		x += x_change
		y += y_change

		# Changing The Color Of The Game's Screen Background
		gameDisplay.fill(black)

		# Creation Of The Obstacles
		things(thing_startx, thing_starty, thing_width, thing_height, white)
		thing_starty += thing_speed

		# Displaying The Car Image On The Screen
		car(x, y)

		# Displaying The Scores
		things_dodged(dodged)

		# Game Boundaries
		if x > (display_width - car_width) or x < 0:
			crash()

		# Continuous Spawning Of Obstacles 
		if thing_starty > display_height:
			thing_starty = 0 - thing_height
			thing_startx = random.randrange(0, display_width)
			dodged += 1
			thing_speed += 0.5

		# Car Crashes Into The Obstacles
		if y < (thing_starty + thing_height):
			if x > thing_startx and x < (thing_startx + thing_width) or (x + car_width) > thing_startx and (x + car_width) < (thing_startx + thing_width):
				crash()

		pygame.display.update()
		clock.tick(60)

# Start Game
game_intro()

# Quit Function
pygame.quit()
quit()
