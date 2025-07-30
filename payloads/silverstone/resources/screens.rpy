################################################################################
## Initialization
################################################################################

init offset = -1

init python:
    print("Using modified screen manager")

################################################################################
## Styles
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb_offset 4
    top_gutter 0
    bottom_gutter 0

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"
    thumb_offset 2
    top_gutter 0
    bottom_gutter 0

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)



################################################################################
## In-game screens
################################################################################


## Say screen ##################################################################
##
## The say screen is used to display dialogue to the player. It takes two
## parameters, who and what, which are the name of the speaking character and
## the text to be displayed, respectively. (The who parameter can be None if no
## name is given.)
##
## This screen must create a text displayable with id "what", as Ren'Py uses
## this to manage text display. It can also create displayables with id "who"
## and id "window" to apply style properties.
##
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what, side_image=None, two_window=False, who_window_style="say_who_window"):
    style_prefix "say"

    default two_window = True

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"


    ## If there's a side image, display it above the text. Do not display on the
    ## phone variant - there's no room.
    #if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0

    #Use Quick Menu
    use quick_menu


## Make the namebox available for styling through the Character object.
init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos
    line_spacing 15

    adjust_spacing False

## Input screen ################################################################
##
## This screen is used to display renpy.input. The prompt parameter is used to
## pass a text prompt in.
##
## This screen must create an input displayable with id "input" to accept the
## various input parameters.
##
## https://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xanchor gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Choice screen ###############################################################
##
## This screen is used to display the in-game choices presented by the menu
## statement. The one parameter, items, is a list of objects, each with caption
## and action fields.
##
## https://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items, background=None):
    style_prefix "choice"

    if background is not None:
        # This adds a specific background image behind the choices.
        # By default, there will be no background unless you pass a menu argument.
        # 'background' must be a string matching an image filename (without .png).
        # The image must exist in your game/images folder or you’ll get an error.
        add "[background].png" xalign 0.5 ypos 405 yanchor 0.5 # Positioning matches the default "choice_vbox", feel free to change.

    vbox:
        $ visible_items = [i for i in items if i.kwargs.get("condition", True)]
        for i in visible_items:
            $ color = i.kwargs.get("color", None)
            $ hover = i.kwargs.get("hover", None)
            $ tooltip_text = i.kwargs.get("tooltip_text", None) # Optional: Only needed for tooltip functionality.

            textbutton i.caption:
                action i.action
                sensitive i.kwargs.get("sensitive", True)

                # Only apply custom colors if the button is active.
                # Disabled choices will use gui.choice_button_text_insensitive_color
                if i.kwargs.get("sensitive", True):
                    if color is not None:
                        text_color color
                    if hover is not None:
                        text_hover_color hover


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 405
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")
    activate_sound "audio/click.ogg"

style choice_button_text is default:
    properties gui.text_properties("choice_button")


## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the out-of-game
## menus.

screen quick_menu():

    ## Ensure this appears on top of other screens.
    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"

            #xalign 0.5
            #yalign 1.0

            #textbutton _("Back") action Rollback()
            #imagebutton auto "gui/back_%s.png" xpos 154 ypos 774 focus_mask True action Rollback()
            #textbutton _("History") action ShowMenu('history')
            #imagebutton auto "gui/history_%s.png" xpos 158 ypos 774 focus_mask True action ShowMenu('history') activate_sound "audio/click.ogg"
            #textbutton _("Fast-Forward") action Skip(fast=False, confirm=False)
            #imagebutton auto "gui/fforward_%s.png" xpos 430 ypos 774 focus_mask True action Skip(fast=False, confirm=False) activate_sound "audio/click.ogg"
            #textbutton _("Auto") action Preference("auto-forward", "toggle")
            #imagebutton auto "gui/auto_%s.png" xpos 434 ypos 774 focus_mask True action Preference("auto-forward", "toggle") activate_sound "audio/click.ogg"

            if not renpy.variant("pc"):
                imagebutton auto "gui/hide_%s.png" xpos 453 ypos 884 focus_mask True action HideInterface() activate_sound "audio/click.ogg"


## This code ensures that the quick_menu screen is displayed in-game, whenever
## the player has not explicitly hidden the interface.


################################################################################
## Main and Game Menu Screens
################################################################################

## Navigation screen ###########################################################
##
## This screen is included in the main and game menus, and provides navigation
## to other menus, and to start the game.

screen navigation():

    vbox:
        style_prefix "navigation"

        #xpos gui.navigation_xpos
        #yalign 0.5

        spacing gui.navigation_spacing

        if main_menu:

            #textbutton _("Start") action Start()

            imagebutton auto "gui/mm_newgame_%s.png" focus_mask True action Start()

        else:

            textbutton _("History") action ShowMenu("history")

            textbutton _("Save") action ShowMenu("save")

        #textbutton _("Load") action ShowMenu("load")

        imagebutton auto "gui/mm_load_%s.png" focus_mask True action ShowMenu("file_picker_mm")

        #textbutton _("Preferences") action ShowMenu("preferences")

        imagebutton auto "gui/mm_options_%s.png" focus_mask True action ShowMenu("pref")

        imagebutton auto "gui/mm_help_%s.png" focus_mask True action ShowMenu("hel")

        if _in_replay:

            textbutton _("End Replay") action EndReplay(confirm=True)

        elif not main_menu:

            textbutton _("Main Menu") action MainMenu()

        textbutton _("About") action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):

            ## Help isn't necessary or relevant to mobile devices.
            textbutton _("Help") action ShowMenu("help")

        if renpy.variant("pc"):

            ## The quit button is banned on iOS and unnecessary on Android and
            ## Web.
            #textbutton _("Quit") action Quit(confirm=not main_menu)

            imagebutton auto "gui/mm_quit_%s.png" focus_mask True action Quit(confirm=not main_menu)


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.text_properties("navigation_button")


## Main Menu screen ############################################################
##
## Used to display the main menu when Ren'Py starts.
##
## https://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu():

    ## This ensures that any other menu screen is replaced.
    tag menu

    add gui.main_menu_background

    ## This empty frame darkens the main menu.
    #frame:
    #    style "main_menu_frame"

    ## The use statement includes another screen inside this one. The actual
    ## contents of the main menu are in the navigation screen.
    use navigation2

    if gui.show_name:

        vbox:
            style "main_menu_vbox"

            text "[config.name!t]":
                style "main_menu_title"

            text "[config.version]":
                style "main_menu_version"


style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_frame:
    xsize 420
    yfill True

    background "gui/overlay/main_menu.png"

style main_menu_vbox:
    xalign 1.0
    xoffset -30
    xmaximum 1200
    yalign 1.0
    yoffset -30

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    properties gui.text_properties("title")

style main_menu_version:
    properties gui.text_properties("version")

screen navigation2():

    fixed:
        style_prefix "navigation"

        #xpos gui.navigation_xpos
        #yalign 0.5

        spacing gui.navigation_spacing

        if main_menu and renpy.variant("pc"):

            #textbutton _("Start") action Start()

            imagebutton auto "gui/mm_newgame_%s.png" xpos 10 ypos 960 focus_mask True action [ (Play("sound", "audio/click.ogg"), Start()) ]

            imagebutton auto "gui/mm_load_%s.png" xpos 330 ypos 960 focus_mask True action [ (ShowMenu("load"), Play("sound", "audio/click.ogg")) ]

            #textbutton _("Preferences") action ShowMenu("preferences")

            imagebutton auto "gui/mm_options_%s.png" xpos 651 ypos 960 focus_mask True action [ (ShowMenu("preferences"), Play("sound", "audio/click.ogg")) ]

            imagebutton auto "gui/mm_extras_%s.png" xpos 1289 ypos 960 focus_mask True action [ (ShowMenu("imagegallery_pre"), Play("sound", "audio/click.ogg")) ]

        else:

            imagebutton auto "gui/mm_newgame_%s.png" xpos 122 ypos 960 focus_mask True action [ (Play("sound", "audio/click.ogg"), Start()) ]

            imagebutton auto "gui/mm_load_%s.png" xpos 570 ypos 960 focus_mask True action [ (ShowMenu("load"), Play("sound", "audio/click.ogg")) ]

            #textbutton _("Preferences") action ShowMenu("preferences")

            imagebutton auto "gui/mm_options_%s.png" xpos 1050 ypos 960 focus_mask True action [ (ShowMenu("preferences"), Play("sound", "audio/click.ogg")) ]

            imagebutton auto "gui/mm_extras_%s.png" xpos 1498 ypos 960 focus_mask True action [ (ShowMenu("imagegallery_pre"), Play("sound", "audio/click.ogg")) ]

            #textbutton _("History") action ShowMenu("history")

            #textbutton _("Save") action ShowMenu("save")

        #textbutton _("Load") action ShowMenu("load")

        #if _in_replay:

        #    textbutton _("End Replay") action EndReplay(confirm=True)

        #elif not main_menu:

        #    textbutton _("Main Menu") action MainMenu()

        #textbutton _("About") action ShowMenu("about")

        #if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):

            ## Help isn't necessary or relevant to mobile devices.
        #    textbutton _("Help") action ShowMenu("help")

        if renpy.variant("pc"):

            ## The quit button is banned on iOS and unnecessary on Android and
            ## Web.
            #textbutton _("Quit") action Quit(confirm=not main_menu)

            imagebutton auto "gui/mm_help_%s.png" xpos 968 ypos 960 focus_mask True action [ (ShowMenu("help"), Play("sound", "audio/click.ogg")) ]

            imagebutton auto "gui/mm_quit_%s.png" xpos 1610 ypos 960 focus_mask True action [ (Quit(confirm=not main_menu), Play("sound", "audio/click.ogg")) ]


## Game Menu screen ############################################################
##
## This lays out the basic common structure of a game menu screen. It's called
## with the screen title, and displays the background, title, and navigation.
##
## The scroll parameter can be None, or one of "viewport" or "vpgrid".
## This screen is intended to be used with one or more children, which are
## transcluded (placed) inside it.

screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):

    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background
    else:
        add gui.game_menu_background

    frame:
        style "game_menu_outer_frame"

        hbox:

            ## Reserve space for the navigation section.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            spacing spacing

                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        spacing spacing

                        transclude

                else:

                    transclude

    use navigation

    textbutton _("Return"):
        style "return_button"

        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame:
    bottom_padding 30
    top_padding 120
    background "gui/game_menu.png"
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 45
    top_padding 180

    background "gui/overlay/game_menu.png"

style game_menu_navigation_frame:
    xsize 175
    yalign -0.4
    xalign -0.015
    yfill False

style game_menu_content_frame:
    left_margin 60
    right_margin 30
    top_margin 15

style game_menu_viewport:
    xsize 1380

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 15

style game_menu_label:
    xpos 75
    ysize 180

style game_menu_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -45


## About screen ################################################################
##
## This screen gives credit and copyright information about the game and Ren'Py.
##
## There's nothing special about this screen, and hence it also serves as an
## example of how to make a custom screen.

screen about():

    tag menu

    ## This use statement includes the game_menu screen inside this one. The
    ## vbox child is then included inside the viewport inside the game_menu
    ## screen.
    use game_menu(_("About"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Version [config.version!t]\n")

            ## gui.about is usually set in options.rpy.
            if gui.about:
                text "[gui.about!t]\n"

            text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and load
## it again. Since they share nearly everything in common, both are implemented
## in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save https://
## www.renpy.org/doc/html/screen_special.html#load

screen file_picker_mm():

    modal True

    window:
        style_group "config_bg"
        xpadding 250
        use bottom_menu
        #imagebutton auto "gui/gm_back_%s.png" action [Play ("ex_sfx", "audio/click.ogg"), Return()]  xoffset 707 yoffset 575

        frame:
            background "gui/options_bg.png"
            xmaximum 808
            ymaximum 458
            yalign -0.4
            xalign -0.015
            has vbox
            frame:
                style_group "file_picker"
                top_margin 0.08
                background None
                $ columns = 2
                $ rows = 4

                # Display a grid of file slots.
                grid columns rows:
                    transpose True
                    xfill False
                    spacing 15

                    # Display ten file slots, numbered 1 - 8.
                    for i in range(1, columns * rows + 1):

                        # Each file slot is a button.
                        button:
                            action FileAction(i) activate_sound "audio/click.ogg"
                            xfill False
                            xpadding 40
                            yoffset 0
                            yminimum 20
                            background None
                            has hbox

                            # Add the screenshot.
                            add FileScreenshot(i) size(288,162)

                            $ file_name = FileSlotName(i, columns * rows)
                            $ file_time = FileTime(i, empty=_("Empty"))
                            $ save_name = FileSaveName(i)

                            text "    [file_name]. [file_time!t]\n[save_name!t]"

                            key "save_delete" action FileDelete(i)

            # File Navigator
            hbox:
                yoffset 40
                xoffset 300
                style_group "file_picker_nav"

                textbutton _("Auto") text_style "text_color":
                    action FilePage("auto")

                text ("{color=#000}  |   {/color}")

                textbutton _("Quick") text_style "text_color":
                    action FilePage("quick")

                text ("{color=#000}  |   {/color}")

                textbutton _("Previous ") text_style "text_color":
                    action FilePagePrevious()

                for i in range(1, 9):
                    textbutton str(i):
                        action FilePage(i)
                        text_style "text_color"

                textbutton _(" Next") text_style "text_color":
                    action FilePageNext()

screen file_picker_sav():

    modal True

    window:
        style_group "config_bg"
        xpadding 250
        use bottom_menu_load
        #imagebutton auto "gui/gm_back_%s.png" action [Play ("ex_sfx", "audio/click.ogg"), Return()]  xoffset 707 yoffset 575

        frame:
            background "gui/options_bg.png"
            xmaximum 808
            ymaximum 458
            yalign -0.4
            xalign -0.015
            has vbox
            frame:
                style_group "file_picker"
                top_margin 0.08
                background None
                $ columns = 2
                $ rows = 4

                # Display a grid of file slots.
                grid columns rows:
                    transpose True
                    xfill False
                    spacing 15

                    # Display ten file slots, numbered 1 - 8.
                    for i in range(1, columns * rows + 1):

                        # Each file slot is a button.
                        button:
                            action FileLoad(i) activate_sound "audio/click.ogg"
                            xfill False
                            xpadding 40
                            yoffset 0
                            yminimum 20
                            background None
                            has hbox

                            # Add the screenshot.
                            add FileScreenshot(i) size(288,162)

                            $ file_name = FileSlotName(i, columns * rows)
                            $ file_time = FileTime(i, empty=_("Empty"))
                            $ save_name = FileSaveName(i)

                            text "    [file_name]. [file_time!t]\n[save_name!t]"

                            key "save_delete" action FileDelete(i)

            # File Navigator
            hbox:
                yoffset 40
                xoffset 300
                style_group "file_picker_nav"

                textbutton _("Auto") text_style "text_color":
                    action FilePage("auto")

                text "  |   " color "#000"

                textbutton _("Quick") text_style "text_color":
                    action FilePage("quick")

                text "  |   " color "#000"

                textbutton _("Previous ") text_style "text_color":
                    action FilePagePrevious()

                for i in range(1, 9):
                    textbutton str(i):
                        action FilePage(i)
                        text_style "text_color"

                textbutton _(" Next") text_style "text_color":
                    action FilePageNext()

screen file_picker_load():

    modal True

    window:
        style_group "config_bg"
        xpadding 250
        use bottom_menu_sav
        #imagebutton auto "gui/gm_back_%s.png" action [Play ("ex_sfx", "audio/click.ogg"), Return()]  xoffset 707 yoffset 575

        frame:
            background "gui/options_bg.png"
            xmaximum 808
            ymaximum 458
            yalign -0.4
            xalign -0.015
            has vbox
            frame:
                style_group "file_picker"
                top_margin 0.08
                background None
                $ columns = 2
                $ rows = 4

                # Display a grid of file slots.
                grid columns rows:
                    transpose True
                    xfill False
                    spacing 15

                    # Display ten file slots, numbered 1 - 8.
                    for i in range(1, columns * rows + 1):

                        # Each file slot is a button.
                        button:
                            action FileSave(i) activate_sound "audio/click.ogg"
                            xfill False
                            xpadding 40
                            yoffset 0
                            yminimum 20
                            background None
                            has hbox

                            # Add the screenshot.
                            add FileScreenshot(i) size(288,162)

                            $ file_name = FileSlotName(i, columns * rows)
                            $ file_time = FileTime(i, empty=_("Empty"))
                            $ save_name = FileSaveName(i)

                            text "    [file_name]. [file_time!t]\n[save_name!t]"

                            key "save_delete" action FileDelete(i)

            # File Navigator
            hbox:
                yoffset 40
                xoffset 300
                style_group "file_picker_nav"

                textbutton _("Auto") text_style "text_color":
                    action FilePage("auto")

                text "  |   " color "#000"

                textbutton _("Quick") text_style "text_color":
                    action FilePage("quick")

                text "  |   " color "#000"

                textbutton _("Previous ") text_style "text_color":
                    action FilePagePrevious()

                for i in range(1, 9):
                    textbutton str(i):
                        action FilePage(i)
                        text_style "text_color"

                textbutton _(" Next") text_style "text_color":
                    action FilePageNext()

screen save():

    tag menu

    use file_picker_load

screen load2():

    tag menu

    use file_picker_sav

screen load():

    tag menu

    use file_picker_mm

style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style text_color:
    idle_color "#000000"
    hover_color "#ffffff"
    selected_color "#ffdbb7"

style page_label:
    xpadding 75
    ypadding 5

style page_label_text:
    textalign 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.text_properties("slot_button")


## Preferences screen ##########################################################
##
## The preferences screen allows the player to configure the game to better suit
## themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen pref():

    modal True

    window:
        style_group "config_bg"
        xpadding 250
        use bottom_menu
        #imagebutton auto "gui/gm_back_%s.png" action [Play ("ex_sfx", "audio/click.ogg"), Return()]  xoffset 707 yoffset 575

        frame:
            background "gui/options_bg.png"
            xmaximum 808
            ymaximum 458
            yalign -0.4
            xalign -0.015
            has vbox
            frame:
                style_group "pref"
                top_margin 4.08
                background None

        vbox:

            hbox:
                box_wrap True

                if renpy.variant("pc") or renpy.variant("web"):

                    xpos 200
                    ypos 150

                    vbox:
                        style_prefix "radio"
                        label _("   DISPLAY")
                        textbutton _("Window") action Preference("display", "window") activate_sound "audio/click.ogg"
                        textbutton _("Fullscreen") action Preference("display", "fullscreen") activate_sound "audio/click.ogg"

                if renpy.variant("pc") or renpy.variant("web"):

                    xpos 200
                    ypos 150

                    vbox:
                        style_prefix "check"
                        label _("         SKIP")
                        textbutton _("Unseen Text") action Preference("skip", "toggle") activate_sound "audio/click.ogg"
                        textbutton _("After Choices") action Preference("after choices", "toggle") activate_sound "audio/click.ogg"
                        textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle")) activate_sound "audio/click.ogg"

                if renpy.variant("pc") or renpy.variant("web"):

                    xpos 200
                    ypos 150

                    vbox:
                        style_prefix "radio"
                        label _("         CHOICES")
                        textbutton _("Show Important Choices") action SetVariable("choices", True) activate_sound "audio/click.ogg"
                        textbutton _("Don't Show Important Choices") action SetVariable("choices", False) activate_sound "audio/click.ogg"

                if renpy.variant("small") or renpy.variant("touch"):

                    xpos 380
                    ypos 150

                    vbox:
                        style_prefix "check"
                        label _("        SKIP")
                        textbutton _("Unseen Text") action Preference("skip", "toggle") activate_sound "audio/click.ogg"
                        textbutton _("After Choices") action Preference("after choices", "toggle") activate_sound "audio/click.ogg"
                        textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle")) activate_sound "audio/click.ogg"

                if renpy.variant("small") or renpy.variant("touch"):

                    xpos 380
                    ypos 150

                    vbox:
                        style_prefix "radio"
                        label _("         CHOICES")
                        textbutton _("Show Important Choices") action SetVariable("choices", True) activate_sound "audio/click.ogg"
                        textbutton _("Don't Show Important Choices") action SetVariable("choices", False) activate_sound "audio/click.ogg"


                ## Additional vboxes of type "radio_pref" or "check_pref" can be
                ## added here, to add additional creator-defined preferences.

            null height (4 * gui.pref_spacing)

            hbox:
                xpos 111
                ypos 150
                style_prefix "slider"
                box_wrap True

                vbox:

                    label _("                 TEXT SPEED")

                    bar value Preference("text speed")

                    label _("       AUTO-FORWARD TIME")

                    bar value Preference("auto-forward time")

                vbox:

                    if config.has_music:
                        label _("              MUSIC VOLUME")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:

                        label _("              SOUND VOLUME")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound)


                    if config.has_voice:
                        label _("               VOICE VOLUME")

                        hbox:
                            bar value Preference("voice volume")

                            if config.sample_voice:
                                textbutton _("Test") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("                   MUTE ALL"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 3

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 338

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.text_properties("check_button")

style slider_slider:
    xsize 525

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 15

style slider_button_text:
    properties gui.text_properties("slider_button")

style slider_vbox:
    xsize 675

init -2:

    style config_bg_window:
        background "gui/game_menu.png"
        xpadding 115
        yalign 0.0

screen preferences():

    tag menu

    use pref


## History screen ##############################################################
##
## This is a screen that displays the dialogue history to the player. While
## there isn't anything special about this screen, it does have to access the
## dialogue history stored in _history_list.
##
## https://www.renpy.org/doc/html/history.html

screen his():

    modal True

    window:
        style_group "config_bg"
        xpadding 250
        use bottom_menu
        #imagebutton auto "gui/gm_back_%s.png" action [Play ("ex_sfx", "audio/click.ogg"), Return()]  xoffset 707 yoffset 575

        frame:
            background "gui/options_bg.png"
            xmaximum 808
            ymaximum 458
            yalign -0.4
            xalign -0.015
            has vbox
            frame:
                style_group "his"
                top_margin 4.08
                background None

    ## Avoid predicting this screen, as it can be very large.
    predict False

    vpgrid:

        style_prefix "history"

        cols 1
        yinitial 1.0
        spacing gui.history_spacing

        mousewheel True
        draggable True
        scrollbars "vertical"

        side_ysize 710
        side_xsize 1570
        side_xpos 50
        side_ypos 120

        for h in _history_list:

            window:

                ## This lays things out properly if history_height is None.
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"
                        substitute None

                        ## Take the color of the who text from the Character, if
                        ## set.
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False

        if not _history_list:
            label _("The dialogue history is empty.")


## This determines what tags are allowed to be displayed on the history screen.

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5

screen history():

    tag menu

    use his

## Help screen #################################################################
##
## A screen that gives information about key and mouse bindings. It uses other
## screens (keyboard_help, mouse_help, and gamepad_help) to display the actual
## help.

screen hel():

    modal True

    window:
        style_group "config_bg"
        xpadding 250
        use bottom_menu
        default device = "keyboard"
        #imagebutton auto "gui/gm_back_%s.png" action [Play ("ex_sfx", "audio/click.ogg"), Return()]  xoffset 707 yoffset 575

        frame:
            background "gui/options_bg.png"
            xmaximum 808
            ymaximum 458
            yalign -0.4
            xalign -0.015
            has vbox
            frame:
                style_group "hel"
                top_margin 4.08
                background None

        vbox:
            spacing 23

            use keyboard_help


screen keyboard_help():

    vbox:

        xpos 70
        ypos 135

        vbox:

            spacing 15

            hbox:
                label _("Enter/Left Click: ")
                text _("Advances dialogue and activates the interface.")

            hbox:
                label _("Space: ")
                text _("Advances dialogue without selecting choices.")

            hbox:
                label _("Arrow Keys: ")
                text _("Navigate the interface.")

            hbox:
                label _("Escape/Right Click: ")
                text _("Accesses the game menu.")

            hbox:
                label _("Ctrl: ")
                text _("Skips dialogue while held down.")

            hbox:
                label _("Tab: ")
                text _("Toggles dialogue skipping.")

            hbox:
                label _("Page Up/Mouse Wheel Up: ")
                text _("Rolls back to earlier dialogue.")

            hbox:
                label _("Page Down/Mouse Wheel Down: ")
                text _("Rolls forward to later dialogue.")

            hbox:
                label "H/Middle Click: "
                text _("Hides the user interface.")

            hbox:
                label "S: "
                text _("Takes a screenshot.")

            hbox:
                label "V: "
                text _("Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}.")

            hbox:
                label "Shift+A: "
                text _("Opens the accessibility menu.")


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin 12

style help_button_text:
    properties gui.text_properties("help_button")

style help_label:
    xsize 375
    right_padding 30

style help_label_text:
    size gui.text_size
    xalign 1.0
    textalign 1.0

screen help():

    tag menu

    use hel


################################################################################
## Additional screens
################################################################################

##############################################################################
# Bottom Menu
#
# Screen that's included in other screens to display the game menu
# navigation and background.
# http://www.renpy.org/doc/html/screen_special.html#navigation
screen bottom_menu():

    modal True

    # The background of the game menu.
    window:
        style "gm_nav"
        imagebutton auto "gui/gm_quit_%s.png" action [Play ("ex_sfx", "audio/click.ogg"), Quit()]  xoffset -9 yoffset 975
        imagebutton auto "gui/gm_menu_%s.png" action [Play ("ex_sfx", "audio/click.ogg"), MainMenu(confirm=True)]  xoffset 295 yoffset 975
        #imagebutton auto "gui/gm_save_%s.png" action [Play ("ex_sfx", "audio/click.ogg"), ShowMenu("save")]  xoffset 284 yoffset 575
        #imagebutton auto "gui/gm_load_%s.png" action [Play ("ex_sfx", "audio/click.ogg"), ShowMenu("load")]  xoffset 426 yoffset 575
        imagebutton auto "gui/gm_help_%s.png" action [Play ("ex_sfx", "audio/click.ogg"), Help()]  xoffset 919 yoffset 975
        imagebutton auto "gui/gm_back_%s.png" action [Play ("ex_sfx", "audio/click.ogg"), Return()]  xoffset 1223 yoffset 975

screen bottom_menu_sav():

    modal True

    # The background of the game menu.
    window:
        style "gm_nav"
        imagebutton auto "gui/gm_quit_%s.png" action [Play ("ex_sfx", "audio/click.ogg"), Quit()]  xoffset -9 yoffset 975
        imagebutton auto "gui/gm_menu_%s.png" action [Play ("ex_sfx", "audio/click.ogg"), MainMenu(confirm=True)]  xoffset 295 yoffset 975
        imagebutton auto "gui/gm_load_%s.png" action [Play ("ex_sfx", "audio/click.ogg"), ShowMenu("load2")]  xoffset 607 yoffset 975
        imagebutton auto "gui/gm_help_%s.png" action [Play ("ex_sfx", "audio/click.ogg"), Help()]  xoffset 919 yoffset 975
        imagebutton auto "gui/gm_back_%s.png" action [Play ("ex_sfx", "audio/click.ogg"), Return()]  xoffset 1223 yoffset 975

screen bottom_menu_load():

    modal True

    # The background of the game menu.
    window:
        style "gm_nav"
        imagebutton auto "gui/gm_quit_%s.png" action [Play ("ex_sfx", "audio/click.ogg"), Quit()]  xoffset -9 yoffset 975
        imagebutton auto "gui/gm_menu_%s.png" action [Play ("ex_sfx", "audio/click.ogg"), MainMenu(confirm=True)]  xoffset 295 yoffset 975
        imagebutton auto "gui/gm_save_%s.png" action [Play ("ex_sfx", "audio/click.ogg"), ShowMenu("save")]  xoffset 607 yoffset 975
        imagebutton auto "gui/gm_help_%s.png" action [Play ("ex_sfx", "audio/click.ogg"), Help()]  xoffset 919 yoffset 975
        imagebutton auto "gui/gm_back_%s.png" action [Play ("ex_sfx", "audio/click.ogg"), Return()]  xoffset 1223 yoffset 975

init python:
    renpy.music.register_channel("ex_sfx", "sfx", False)

init -2:
    style gm_nav_window:
        background None

    style gm_nav is default

## Confirm screen ##############################################################
##
## The confirm screen is called when Ren'Py wants to ask the player a yes or no
## question.
##
## https://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 45

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 150

                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action

    ## Right-click and escape answer "no".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    textalign 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.text_properties("confirm_button")


## Skip indicator screen #######################################################
##
## The skip_indicator screen is displayed to indicate that skipping is in
## progress.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 9

            text _("Skipping")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## This transform is used to blink the arrows one after another.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    ## glyph in it.
    font "DejaVuSans.ttf"


## Notify screen ###############################################################
##
## The notify screen is used to show the player a message. (For example, when
## the game is quicksaved or a screenshot has been taken.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")


## NVL screen ##################################################################
##
## This screen is used for NVL-mode dialogue and menus.
##
## https://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## Displays dialogue in either a vpgrid or the vbox.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## Displays the menu, if given. The menu may be displayed incorrectly if
        ## config.narrator_menu is set to True.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## This controls the maximum number of NVL-mode entries that can be displayed at
## once.
define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    textalign gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    textalign gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    textalign gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.text_properties("nvl_button")


## Bubble screen ###############################################################
##
## The bubble screen is used to display dialogue to the player when using speech
## bubbles. The bubble screen takes the same parameters as the say screen, must
## create a displayable with the id of "what", and can create displayables with
## the "namebox", "who", and "window" ids.
##
## https://www.renpy.org/doc/html/bubble.html#bubble-screen

screen bubble(who, what):
    style_prefix "bubble"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "bubble_namebox"

                text who:
                    id "who"

        text what:
            id "what"

style bubble_window is empty
style bubble_namebox is empty
style bubble_who is default
style bubble_what is default

style bubble_window:
    xpadding 30
    top_padding 5
    bottom_padding 5

style bubble_namebox:
    xalign 0.5

style bubble_who:
    xalign 0.5
    textalign 0.5
    color "#000"

style bubble_what:
    align (0.5, 0.5)
    text_align 0.5
    layout "subtitle"
    color "#000"

define bubble.frame = Frame("gui/bubble.png", 55, 55, 55, 95)
define bubble.thoughtframe = Frame("gui/thoughtbubble.png", 55, 55, 55, 55)

define bubble.properties = {
    "bottom_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "bottom_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "top_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "top_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "thought" : {
        "window_background" : bubble.thoughtframe,
    }
}

define bubble.expand_area = {
    "bottom_left" : (0, 0, 0, 22),
    "bottom_right" : (0, 0, 0, 22),
    "top_left" : (0, 22, 0, 0),
    "top_right" : (0, 22, 0, 0),
    "thought" : (0, 0, 0, 0),
}
