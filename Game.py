import pygame
from Camera import Camera
from Player import Player 
from Platform import Platform
from PlatformController import PlatformController
from Constants import *
from Utils import *

pygame.init()

game_display = pygame.display.set_mode(res)
pygame.display.set_caption(GAME_CAPTION)

black = (0,0,0)
blue = (0,0, 255)
white = (255,255,255)

def display_game_over_screen(game_display, background, player, text_color):
    # Darken the background for a more dramatic effect
    dark_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    dark_overlay.set_alpha(150)  # Transparency level
    dark_overlay.fill((0, 0, 0))
    game_display.blit(background, (0, 0))
    game_display.blit(dark_overlay, (0, 0))

    # Display "Game Over" text with a fiery effect
    if pygame.font:
        fiery_font = pygame.font.Font("firetxt.TTF", 100)  # Replace with a fiery-themed font
        game_over_text = fiery_font.render("Game Over", True, (255, 69, 0))  # Fiery orange color
        game_display.blit(game_over_text, 
            (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))

        # Display player's score with a red glow effect
        glow_font = pygame.font.Font("scoretxt.TTF", 60)  # Replace with a glowing-themed font
        score_text = glow_font.render(f"Score: {player.score}", True, (255, 0, 0))  # Blood red color
        game_display.blit(score_text, 
            (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2.5))

        # Display restart prompt with a flickering effect
        flicker_font = pygame.font.Font("scoretxt.TTF", 50)  # Replace with a flickering-themed font
        restart_prompt = flicker_font.render("Press SPACE to Descend Again", True, text_color)
        game_display.blit(restart_prompt, 
            (SCREEN_WIDTH // 2 - restart_prompt.get_width() // 2, SCREEN_HEIGHT // 2))

        # Display return to menu prompt with a dim glow effect
        menu_prompt = flicker_font.render("Press ESC to Escape the Abyss", True, (139, 0, 0))  # Dark red
        game_display.blit(menu_prompt, 
            (SCREEN_WIDTH // 2 - menu_prompt.get_width() // 2, SCREEN_HEIGHT // 1.8))

    # Add some flames at the bottom of the screen
    # flames_image = load_image("flames.png")  # Load a flames image
    # game_display.blit(flames_image, (0, SCREEN_HEIGHT - flames_image.get_height()))

    pygame.display.update()


def reinit():
	global player
	global platform_controller
	global floor
	global camera
	player = Player()
	platform_controller = PlatformController()
	floor = Platform(0, SCREEN_HEIGHT-36, SCREEN_WIDTH, 36)
	camera = Camera(player)

# Initialize game objects
reinit()

try:
	arrow_image = load_image("arrow.png")
	background = load_image('pixel-hell.webp')
except Exception as e:
	print(f"Error loading images: {e}")
	pygame.quit()
	quit()

selected_option = 0.30
game_state = 'Menu'
game_loop = True
clock = pygame.time.Clock()
fps = 60

while game_loop:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game_loop = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				if game_state in ['Playing', 'Game Over', 'About']:
					game_state = 'Menu'
			elif game_state == 'Game Over':
				if event.key == pygame.K_SPACE:
					reinit()
					game_state = 'Playing'
			elif game_state == "Menu": #----------------Menu Events-------------
				if event.key == pygame.K_DOWN:
					if selected_option < 0.45:
						selected_option += 0.10
					else:
						selected_option = 0.30
				elif event.key == pygame.K_UP:
					if selected_option > 0.35:
						selected_option -= 0.10
					else: 
						selected_option = 0.50
				elif event.key == pygame.K_RETURN:
					if selected_option < 0.35:
						reinit()
						game_state = 'Playing'
					elif selected_option == 0.40:
						game_state = 'About'
					elif selected_option == 0.50:
						game_loop = False

	keys_pressed = pygame.key.get_pressed()
	if keys_pressed[pygame.K_LEFT]:
		player.vel_x -= player.acceleration
		if player.vel_x < -player.max_vel_x:
			player.vel_x = -player.max_vel_x
		player.sprite_index_y = 2
	elif keys_pressed[pygame.K_RIGHT]:
		player.vel_x += player.acceleration
		if player.vel_x > player.max_vel_x:
			player.vel_x = player.max_vel_x
		player.sprite_index_y = 1
	else:
		if player.vel_x < 0:
			player.vel_x += player.acceleration
			player.vel_x -= ICE_RESISTANCE
			if player.vel_x > 0:
				player.vel_x = 0
		else:
			player.vel_x -= player.acceleration
			player.vel_x += ICE_RESISTANCE
			if player.vel_x < 0:
				player.vel_x = 0

		if player.vel_y >= JUMP_VELOCITY / 2:
			player.sprite_index_y = 0

	#---------------------------MENU----------------------------
	if game_state == "Menu":
		game_display.blit(background, (0, 0))
		game_display.blit(arrow_image, (MENU_START_X + ARROW_HALF_WIDTH, MENU_START_Y + SCREEN_HEIGHT * selected_option - ARROW_HALF_HEIGHT))
		if pygame.font:
			message_display(game_display, "Down The Hell", 0, MENU_START_Y + round(SCREEN_HEIGHT * 0.15), 60, white, True)
			message_display(game_display, "Play", 0, MENU_START_Y + round(SCREEN_HEIGHT * 0.30), 50, white, True)
			message_display(game_display, "About", 0, MENU_START_Y + round(SCREEN_HEIGHT * 0.40), 50, white, True)
			message_display(game_display, "Quit", 0, MENU_START_Y + round(SCREEN_HEIGHT * 0.50), 50, white, True)
	
	#-------------------------PLAYING---------------------------
	elif game_state == 'Playing':
		if keys_pressed[pygame.K_SPACE]:
			if player.on_any_platform(platform_controller, floor):
				player.sprite_index_y = 3
				if player.vel_y >= JUMP_VELOCITY / 2:
					player.vel_y = -JUMP_VELOCITY

		player.update()
		player.combo()
		player.collide_platform(floor, 0)
		platform_controller.collide_set(player)

		platform_controller.score = player.score
		camera.update(player.score)
		platform_controller.generate_new_platforms(camera)

		if player.fallen_off_screen(camera):
			game_state = 'Game Over'

		game_display.blit(background, (0, 0))
		floor.draw(game_display, camera)
		platform_controller.draw(game_display, camera)
		player.draw(game_display, camera)
		message_display(game_display, str(player.score), 25, 30, 36, white)

	#------------------------GAME OVER--------------------------
	elif game_state == 'Game Over':
		display_game_over_screen(game_display, background, player, white)

	#--------------------------ABOUT----------------------------
	elif game_state == 'About':
		game_display.blit(background, (0, 0))
		if pygame.font:
			font = pygame.font.SysFont("Arial", 30)
			for i, line in enumerate(ABOUT_MESSAGE):
				text = font.render(line, True, white)
				game_display.blit(text, (0, MENU_START_Y + i * 35))
			font = pygame.font.SysFont("Arial", 40)
			text = font.render("Press ESC to return to menu!", True, white)
			game_display.blit(text, (0, 500))

	pygame.display.update()
	clock.tick(fps)

pygame.quit()
quit()
