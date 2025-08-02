import pygame_sdl2
import os
import time
import sys

from parasitic_lib import _log, _log_warn, _log_err

PARASITIC_VERSION = "2.4"

# Constants
RESOLUTION  = (1280, 720)
DARK_FACTOR = 3
WASH_COLOUR = (50, 50, 50)
WASH_COLOUR_POPUP = (WASH_COLOUR[0]-WASH_COLOUR[0]/DARK_FACTOR, WASH_COLOUR[1]-WASH_COLOUR[1]/DARK_FACTOR, WASH_COLOUR[1]-WASH_COLOUR[1]/DARK_FACTOR)

# Text colours
TEXT_PRIMARY  = (255, 255, 255)
TEXT_HEADER   = (255, 100, 255)
TEXT_FPS      = (150, 150, 150)
TEXT_ENABLED  = (0, 255, 0)
TEXT_WARNING  = (255, 255, 0)
TEXT_DISABLED = (255, 0, 0)

keybinds = [
	"Shortcuts:",
	"Q/ESC - Quit Parasitic",
	"M - Dump to main menu",
	"R - Start new save",
	"B - Toggle music"
]

third_party_keybinds = []

# These are official plugins
# Unofficial ones are listed separately
plugins = {
	"namefix":     False,
	"pluglaunch": False
}

third_party_plugins = []

def _check_for_supported_plugins(PATH:str):
	global keybinds, plugins, third_party_plugins

	# NameFix
	if os.path.exists(f"{PATH}/game/plugins/namefix.rpy"):
		keybinds.append("N - Run NameFix")
		plugins.update(namefix=True)

	# PluginLauncher
	if os.path.exists(f"{PATH}/game/plugins/pluglaunch.rpy"):
		keybinds.append("L - Run Plugin Launcher")
		plugins.update(pluglaunch=True)

	if os.path.exists(f"{PATH}/game/plugins/"):
		# Check for third party plugins
		k_1 = 49
		for plugin in os.listdir(f"{PATH}/game/plugins"):
			if (plugin.split(".")[0] not in plugins.keys()) and ("rpyc" not in plugin) and os.path.isfile(f"{PATH}/game/plugins/{plugin}"):
				third_party_plugins.append(plugin)

				if (k_1+(len(third_party_plugins)-1)) <= 58:
					third_party_keybinds.append(str(k_1+(len(third_party_plugins)-1)))

def _show_confirm_screen(screen, clock, basic_font) -> bool:
	confirming = True

	pup_width  = RESOLUTION[0]/2
	pup_height = RESOLUTION[1]/2

	center_x = RESOLUTION[0]/2
	center_y = RESOLUTION[1]/2

	while confirming:
		screen.fill(pygame_sdl2.color.Color(WASH_COLOUR_POPUP))

		bpc = pygame_sdl2.Rect(center_x-pup_width/2, center_y-pup_height/2, pup_width, pup_height)
		popup_base = pygame_sdl2.draw.rect(screen, WASH_COLOUR, bpc)
		header = basic_font.render("CONFIRM ACTION", True, TEXT_DISABLED)
		body_1 = basic_font.render("The action you have requested can result in data loss!", True, TEXT_PRIMARY)
		body_2 = basic_font.render("Ensure your game is saved BEFORE confirming!", True, TEXT_PRIMARY)
		cfkey1 = basic_font.render("Press Y to confirm", True, TEXT_WARNING)
		cfkey2 = basic_font.render("Press any other key to abort", True, TEXT_WARNING)

		# screen.blit(popup_base, ())
		screen.blit(header, (center_x - header.get_width()/2, (center_y - pup_height/2)+15))
		screen.blit(body_1, (center_x - body_1.get_width()/2, (center_y - pup_height/2)+60))
		screen.blit(body_2, (center_x - body_2.get_width()/2, (center_y - pup_height/2)+90))
		screen.blit(cfkey1, (center_x - cfkey1.get_width()/2, (center_y - pup_height/2)+135))
		screen.blit(cfkey2, (center_x - cfkey2.get_width()/2, (center_y - pup_height/2)+165))

		pygame_sdl2.display.flip()
		clock.tick(60)

		for event in pygame_sdl2.event.get():
			if event.type == pygame_sdl2.QUIT:
				pygame_sdl2.quit()
			elif event.type == pygame_sdl2.KEYDOWN:
				key = event.key

				if key == pygame_sdl2.K_y:
					return True
				else:
					return False

	return False

def _payload(PATH:str, persistent_music:bool=True) -> int|tuple[int,str]:
	global keybinds, plugins, third_party_plugins

	_check_for_supported_plugins(PATH)

	GAME_NAME = PATH.split("/")[len(PATH.split("/"))-1]

	if os.getenv("_parasitic_dev") == "1":
		FLAG_DEV = True

	else:
		FLAG_DEV = False

	if FLAG_DEV:
		keybinds.append("\ - Update Parasitic")

	# The actual payload
	pygame_sdl2.init()

	pygame_sdl2.display.quit()
	pygame_sdl2.display.init()

	# Take control of the game engine
	pygame_sdl2.display.set_mode(RESOLUTION)
	# pygame_sdl2.display.toggle_fullscreen()
	clock  = pygame_sdl2.time.Clock()
	total_audio_channels = pygame_sdl2.mixer.get_num_channels()

	try:
		pygame_sdl2.mixer.music.load(f"{PATH}/_parasitic/menu.ogg")

	except FileNotFoundError:
		_log_warn("Couldn't load menu.ogg")

	except Exception as err:
		_log_warn("Failed to start music: " + str(err))

	# Define some fonts
	basic_font = pygame_sdl2.sysfont.SysFont('Noto Sans', 24)
	mono_font  = pygame_sdl2.font.Font(f"{PATH}/_parasitic/BitcountPropSingle.ttf", 24)

	# Vars
	running = True
	exit_code = 0
	music   = persistent_music

	# Take control of the display
	pygame_sdl2.display.flip()
	screen = pygame_sdl2.display.set_mode(RESOLUTION)

	# Hit play on that epic music
	if music:
		pygame_sdl2.mixer.music.play(loops=-1)

	KEYBINDS = keybinds

	while running:
		fps = clock.get_fps()

		# Process events
		for event in pygame_sdl2.event.get():
			if event.type == pygame_sdl2.QUIT:
				pygame_sdl2.quit()
			elif event.type == pygame_sdl2.KEYDOWN:
				key = event.key

				if key == pygame_sdl2.K_ESCAPE or key == pygame_sdl2.K_q:
					running = False
					exit_code = 0

				if key == pygame_sdl2.K_n:
					running = False
					exit_code = 1

				if key == pygame_sdl2.K_m:
					if _show_confirm_screen(screen, clock, basic_font):
						running = False
						exit_code = -1

				if key == pygame_sdl2.K_r:
					if _show_confirm_screen(screen, clock, basic_font):
						running = False
						exit_code = -2

				if key == pygame_sdl2.K_l:
					running = False
					exit_code = 3

				if key == pygame_sdl2.K_b:
					music = not music

					if music:
						pygame_sdl2.mixer.music.play(loops=-1)
						try:
							os.remove(f"{PATH}/_parasitic/no_music")
						except:
							NotImplemented

					else:
						pygame_sdl2.mixer.music.stop()
						try:
							open(f"{PATH}/_parasitic/no_music", "x").close()
						except:
							NotImplemented

				if key == pygame_sdl2.K_BACKSLASH and FLAG_DEV:
					import shutil

					_magic_number_1 = os.getlogin()

					for file in os.listdir(f"/home/{_magic_number_1}/Documents/Ajax12/parasitic/resources/interface"):
						shutil.copyfile(f"/home/{_magic_number_1}/Documents/Ajax12/parasitic/resources/interface/{file}", f"{PATH}/game/{file}")

					for file in os.listdir(f"/home/{_magic_number_1}/Documents/Ajax12/parasitic/resources/lib"):
						shutil.copyfile(f"/home/{_magic_number_1}/Documents/Ajax12/parasitic/resources/lib/{file}", f"{PATH}/lib/python3.9/{file}")

					running = False
					exit_code = 2000

					del shutil
					del _magic_number_1

				if str(key) in third_party_keybinds:
					running = False
					exit_code = (1000, third_party_plugins[third_party_keybinds.index(str(key))].split(".")[0])


		# Clear the screen
		screen.fill(pygame_sdl2.color.Color(WASH_COLOUR))

		# Create information displays
		display_elements:list[tuple] = []

		display_elements.append((
			basic_font.render(f"Parasitic {PARASITIC_VERSION}", True, TEXT_HEADER),
			(5, 5)
		))

		display_elements.append((
			basic_font.render(f"Game: {GAME_NAME}", True, TEXT_HEADER),
			(5, 5+29)
		))

		display_elements.append((
			basic_font.render(f"Path: {PATH}", True, TEXT_HEADER),
			(5, 5+29+29)
		))

		kb_resHeight = (RESOLUTION[1]/2) - (29*len(KEYBINDS))/2

		menu_initial_build_height  = kb_resHeight

		for keybind in KEYBINDS:
			display_elements.append((
				basic_font.render(keybind, True, TEXT_PRIMARY),
				(5, kb_resHeight)
			))
			kb_resHeight += 29

		# pgin_resHeight = (RESOLUTION[1]/2) - (29*(len(plugins)+1))
		pgin_resHeight = menu_initial_build_height
		display_elements.append((
			basic_font.render("Official Plugins:", True, TEXT_PRIMARY),
			(RESOLUTION[0]/3, pgin_resHeight)
		))
		pgin_resHeight += 29

		for keybind in plugins.keys():
			state = plugins[keybind]

			if state:
				color = TEXT_ENABLED
				state_text = "INSTALLED"
			else:
				color = TEXT_DISABLED
				state_text = "NOT INSTALLED"

			display_elements.append((
				basic_font.render(f"{keybind}: {state_text}", True, color),
				(RESOLUTION[0]/3, pgin_resHeight)
			))
			pgin_resHeight += 29

		if len(third_party_plugins) > 0:
			# trdpgin_resHeight = (RESOLUTION[1]/2) - (29*(len(third_party_plugins)+1))
			trdpgin_resHeight = menu_initial_build_height
			trdpgin_cnt = 1
			display_elements.append((
				basic_font.render("Third-Party Plugins:", True, TEXT_PRIMARY),
				(RESOLUTION[0]/2+125, trdpgin_resHeight)
			))
			trdpgin_resHeight += 29

			for thirdplugin in third_party_plugins:
				display_elements.append((
					basic_font.render(f"{trdpgin_cnt} - " + thirdplugin, True, TEXT_WARNING),
					(RESOLUTION[0]/2+125, trdpgin_resHeight)
				))
				trdpgin_resHeight += 29
				trdpgin_cnt += 1

		display_elements.append((
			mono_font.render(str(round(fps)), True, TEXT_FPS),
			(5, RESOLUTION[1] - (29))
		))

		for element, position in display_elements:
			screen.blit(element, position)

		pygame_sdl2.display.flip()
		clock.tick(60)

	# Hand control back to the game
	screen.fill(WASH_COLOUR_POPUP)
	screen.blit(basic_font.render("Waiting on RenPy...", True, TEXT_WARNING), (5, 5))
	screen.blit(basic_font.render("If you're here for a while, RenPy has frozen. Shift+R might fix the issue", True, TEXT_FPS), (5, 40))
	pygame_sdl2.display.flip()

	pygame_sdl2.mixer.music.stop()

	for audioChannel in range(total_audio_channels):
		pygame_sdl2.mixer.Channel(audioChannel).stop()

	try:
		return exit_code

	except Exception:
		return 0


###################
# AJAX EXIT CODES
#-2 - FORCEFULLY START A NEW GAME
#-1 - FORCEFULLY RETURN TO MENU (INDUCE FULL RENPY RELOAD)
# 0 - TAKE NO ACTION
# 1 - CALL NAMEFIX
# 2 - UNDEFINED
# 3 - CALL PLUGLAUNCH
#
# RENPY EXIT CODES
# 1000 - CALL 3RD PARTY PLUGIN. EXPECTS TUPLE (1000, "PLUGIN NAME")
# 1001 - UNDEFINED
# 1002 - UNDEFINED
# 1003 - UNDEFINED
# 1004 - UNDEFINED
# 1005 - UNDEFINED
#
# CUSTOM NOTIFICATION EXIT CODES
# 2000 - "Parasitic GUI updated"
