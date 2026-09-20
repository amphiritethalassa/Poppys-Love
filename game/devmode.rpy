# ============================================================
# POPPY'S LOVE — DEV MODE
# ============================================================

default dev_mode = False


# ============================================================
# DEV MODE BUTTON
# ============================================================

screen dev_mode_button():

    if dev_mode:

        textbutton "DEV":

            xalign 0.98
            yalign 0.02

            style "ui_button"

            action ShowMenu("dev_mode_menu")


# ============================================================
# DEV MODE MENU
# ============================================================

screen dev_mode_menu():

    tag menu

    frame:

        background "ui_deco.jpg"

        xalign 0.5
        yalign 0.5

        xsize 1400
        ysize 800

        padding (50, 40)

        vbox:

            spacing 15

            text "DEV MODE" style "ui_name"


            text "Affection: [affection]" style "ui_text"

            text "Name: [player_name]" style "ui_text"

            text "Pronouns: [player_pronouns]" style "ui_text"

            text "Birthday: [player_birthday]" style "ui_text"

            text "First Install: [persistent.first_install_date]" style "ui_text"

            text "Playtime: [persistent.total_playtime]" style "ui_text"

            text "Background: [current_bg_stage]" style "ui_text"


            null height 10


            textbutton "+10 Affection":

                style "ui_button"

                action SetVariable(
                    "affection",
                    affection + 10
                )


            textbutton "Unlock Insult Apology":

                style "ui_button"

                action SetVariable(
                    "insult_unlocked",
                    True
                )


            textbutton "Unlock Crash Apology":

                style "ui_button"

                action SetVariable(
                    "crash_apology_unlocked",
                    True
                )


            textbutton "Reset Idle Timer":

                style "ui_button"

                action SetVariable(
                    "idle_time",
                    0.0
                )


            textbutton "Force Next Background":

                style "ui_button"

                action SetVariable(
                    "current_bg_stage",
                    (current_bg_stage + 1) % 4
                )


            textbutton "Pretend Game Crashed":

                style "ui_button"

                action SetVariable(
                    "persistent.clean_exit",
                    False
                )


            textbutton "Close":

                style "ui_button"

                action Return()


# ============================================================
# BACKGROUND CYCLE
# ============================================================

screen background_cycle():

    if current_bg_stage == 0:

        add "images/bg_noon.jpg"


    elif current_bg_stage == 1:

        add "images/bg_day.jpg"


    elif current_bg_stage == 2:

        add "images/bg_evening.jpg"


    elif current_bg_stage == 3:

        add "images/bg_night.jpg"


# ============================================================
# PLAYTIME TIMER
# ============================================================

screen playtime_timer():

    timer 1.0 repeat True action [

        SetVariable(
            "persistent.total_playtime",
            persistent.total_playtime + 1.0
        ),

        SetVariable(
            "current_bg_stage",
            get_background_stage(
                persistent.total_playtime
            )
        )

    ]

    timer 60.0 repeat True action Function(
        renpy.save_persistent
    )


# ============================================================
# IDLE TIMER
# ============================================================

screen idle_timer():

    timer 1.0 repeat True action Function(
        update_idle_time
    )


init python:

    def update_idle_time():

        if store.away_mode:
            return

        if store.idle_conversation_running:
            return

        store.idle_time += 1.0

        if store.idle_time >= 300.0:

            store.idle_time = 0.0

            renpy.call_in_new_context(
                "random_idle_conversation"
            )


    def reset_idle_timer():

        store.idle_time = 0.0
