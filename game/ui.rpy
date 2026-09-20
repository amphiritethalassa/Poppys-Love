# ============================================================
# POPPY'S LOVE — UI
# ============================================================


# ============================================================
# UI STYLES
# ============================================================

style ui_text:
    size 32
    color "#304b68"


style ui_name:
    size 34
    color "#304b68"
    bold True


style ui_button:
    size 27
    color "#304b68"
    hover_color "#ffffff"


# ============================================================
# DIALOGUE SCREEN
# ============================================================

screen say(who, what):

    frame:

        background "ui_deco.jpg"

        xalign 0.5
        yalign 0.78

        xsize 1450
        ysize 260

        padding (55, 35)

        vbox:

            spacing 12

            if who is not None:

                text who style "ui_name"

            text what style "ui_text"


    use quick_menu


# ============================================================
# QUICK MENU
#
# S = Skip
# A = Auto
# H = History
# T = Settings
# M = Main Menu
# ============================================================

screen quick_menu():

    hbox:

        xalign 0.5
        yalign 0.965

        spacing 25


        textbutton "S - Skip":

            style "ui_button"

            action Skip()


        textbutton "A - Auto":

            style "ui_button"

            action Preference(
                "auto-forward",
                "toggle"
            )


        textbutton "H - History":

            style "ui_button"

            action ShowMenu("history")


        textbutton "T - Settings":

            style "ui_button"

            action ShowMenu("preferences")


        textbutton "M - Main Menu":

            style "ui_button"

            action ShowMenu("main_menu")


# ============================================================
# CHOICE SCREEN
# ============================================================

screen choice(items):

    vbox:

        xalign 0.5
        yalign 0.55

        spacing 15

        for i in items:

            frame:

                background "ui_deco.jpg"

                xsize 1250
                ysize 95

                padding (30, 15)

                textbutton i.caption:

                    style "ui_button"

                    xalign 0.5
                    yalign 0.5

                    action i.action


# ============================================================
# HISTORY
# ============================================================

screen history():

    tag menu

    frame:

        background "ui_deco.jpg"

        xalign 0.5
        yalign 0.5

        xsize 1450
        ysize 800

        padding (50, 40)

        viewport:

            scrollbars "vertical"
            mousewheel True

            vbox:

                spacing 15

                for h in _history:

                    if h.who:

                        text "[h.who]: [h.what]" style "ui_text"

                    else:

                        text h.what style "ui_text"


        textbutton "Back":

            style "ui_button"

            xalign 0.95
            yalign 0.95

            action Return()


# ============================================================
# MAIN MENU
# ============================================================

screen main_menu():

    tag menu

    add "main_menu_bg.jpg"

    vbox:

        xalign 0.5
        yalign 0.52

        spacing 18


        textbutton "START":

            style "ui_button"

            xalign 0.5

            action Start("start")


        textbutton "LOAD":

            style "ui_button"

            xalign 0.5

            action ShowMenu("load")


        textbutton "SETTINGS":

            style "ui_button"

            xalign 0.5

            action ShowMenu("preferences")


        textbutton "QUIT":

            style "ui_button"

            xalign 0.5

            action Quit(confirm=True)


# ============================================================
# SETTINGS
# ============================================================

screen preferences():

    tag menu

    frame:

        background "ui_deco.jpg"

        xalign 0.5
        yalign 0.5

        xsize 1450
        ysize 800

        padding (60, 50)

        vbox:

            spacing 30

            text "Settings" style "ui_name"


            text "Text Speed" style "ui_text"

            bar:

                value Preference("text speed")

                xsize 900


            text "Auto-Forward Time" style "ui_text"

            bar:

                value Preference("auto-forward time")

                xsize 900


            textbutton "Fullscreen":

                style "ui_button"

                action Preference(
                    "display",
                    "fullscreen"
                )


            textbutton "Back":

                style "ui_button"

                action Return()


# ============================================================
# LOAD
# ============================================================

screen load():

    tag menu

    frame:

        background "ui_deco.jpg"

        xalign 0.5
        yalign 0.5

        xsize 1450
        ysize 800

        padding (50, 40)

        vbox:

            spacing 20

            text "Load Game" style "ui_name"

            grid 2 3:

                spacing 20

                for slot in range(1, 7):

                    textbutton "Slot [slot]":

                        style "ui_button"

                        action FileLoad(slot)


            textbutton "Back":

                style "ui_button"

                action Return()


# ============================================================
# SAVE
# ============================================================

screen save():

    tag menu

    frame:

        background "ui_deco.jpg"

        xalign 0.5
        yalign 0.5

        xsize 1450
        ysize 800

        padding (50, 40)

        vbox:

            spacing 20

            text "Save Game" style "ui_name"

            grid 2 3:

                spacing 20

                for slot in range(1, 7):

                    textbutton "Slot [slot]":

                        style "ui_button"

                        action FileSave(slot)


            textbutton "Back":

                style "ui_button"

                action Return()
