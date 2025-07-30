import pygame_sdl2
import os
import time
import sys

from parasitic_lib import _log, _log_warn, _log_err

PARASITIC_VERSION = "2.1"

# Constants
RESOLUTION  = (1280, 720)
WASH_COLOUR = (50, 50, 50)

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
	"pyshell":     False,
	"pluglaunch": False
}

third_party_plugins = []

def _check_for_supported_plugins(PATH:str):
	global keybinds, plugins, third_party_plugins

	# NameFix
	if os.path.exists(f"{PATH}/game/plugins/namefix.rpy"):
		keybinds.append("N - Run NameFix")
		plugins.update(namefix=True)

	# PyShell
	if os.path.exists(f"{PATH}/game/plugins/pyshell.rpy"):
		keybinds.append("P - Run PyShell")
		plugins.update(pyshell=True)

	# PluginLauncher
	if os.path.exists(f"{PATH}/game/plugins/pluglaunch.rpy"):
		keybinds.append("L - Run PlugLaunch")
		plugins.update(pluglaunch=True)

	if os.path.exists(f"{PATH}/game/plugins/"):
		# Check for third party plugins
		k_1 = 49
		for plugin in os.listdir(f"{PATH}/game/plugins"):
			if (plugin.split(".")[0] not in plugins.keys()) and ("rpyc" not in plugin) and os.path.isfile(f"{PATH}/game/plugins/{plugin}"):
				third_party_plugins.append(plugin)

				if (k_1+(len(third_party_plugins)-1)) <= 58:
					third_party_keybinds.append(str(k_1+(len(third_party_plugins)-1)))

def _payload(PATH:str, persistent_music:bool=True):
	global keybinds, plugins, third_party_plugins

	_check_for_supported_plugins(PATH)

	GAME_NAME = PATH.split("/")[len(PATH.split("/"))-1]

	FLAG_DEV = True if os.getenv("_parasitic_dev") == "1" else False

	if FLAG_DEV: keybinds.append("\ - Update Parasitic")

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
					running = False
					exit_code = -1

				if key == pygame_sdl2.K_r:
					running = False
					exit_code = -2

				if key == pygame_sdl2.K_p:
					running = False
					exit_code = 2

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

					for file in os.listdir(f"/home/{_magic_number_1}/Documents/Ajax12/payloads/parasitic/resources/interface"):
						shutil.copyfile(f"/home/{_magic_number_1}/Documents/Ajax12/payloads/parasitic/resources/interface/{file}", f"{PATH}/game/")

					for file in os.listdir(f"/home/{_magic_number_1}/Documents/Ajax12/payloads/parasitic/resources/lib"):
						shutil.copyfile(f"/home/{_magic_number_1}/Documents/Ajax12/payloads/parasitic/resources/lib/{file}", f"{PATH}/lib/python3.9/")

					running = False
					exit_code = -1

				if str(key) in third_party_keybinds:
					running = False
					exit_code:tuple[int, str] = (1000, third_party_plugins[third_party_keybinds.index(str(key))].split(".")[0])


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
			basic_font.render(f"Official Plugins:", True, TEXT_PRIMARY),
			(RESOLUTION[0]/3, pgin_resHeight)
		))
		pgin_resHeight += 29

		for keybind in plugins.keys():
			state = plugins[keybind]

			if state == True:
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
				basic_font.render(f"Third-Party Plugins:", True, TEXT_PRIMARY),
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
	screen.fill(WASH_COLOUR)
	return_text = basic_font.render("Returning control", True, TEXT_FPS)
	screen.blit(return_text, (5, 5))
	pygame_sdl2.display.flip()

	pygame_sdl2.mixer.music.stop()

	for audioChannel in range(total_audio_channels):
		pygame_sdl2.mixer.Channel(audioChannel).stop()

	try:
		return exit_code

	except:
		return 0

###################
# AJAX EXIT CODES
#-2 - FORCEFULLY START A NEW GAME
#-1 - FORCEFULLY RETURN TO MENU (INDUCE FULL RENPY RELOAD)
# 0 - TAKE NO ACTION
# 1 - CALL NAMEFIXER
# 2 - CALL PYSHELL
# 3 - CALL PLUGLAUNCH
#
# RENPY EXIT CODES
# 1000 - CALL 3RD PARTY PLUGIN. EXPECTS TUPLE (1000, "PLUGIN NAME")
# 1001 - UNDEFINED
# 1002 - UNDEFINED
# 1003 - UNDEFINED
# 1004 - UNDEFINED
# 1005 - UNDEFINED
