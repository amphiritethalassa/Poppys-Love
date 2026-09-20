# ============================================================
# POPPY'S LOVE
# MAIN GAME
# ============================================================

define p = Character("Poppy")


# ============================================================
# PLAYER DATA
# ============================================================

default affection = 0

default player_name = ""
default player_pronouns = ""
default player_birthday = ""

default insult_unlocked = False
default crash_apology_unlocked = False

default away_mode = False

default idle_time = 0.0
default idle_conversation_running = False

default current_bg_stage = 0


# ============================================================
# PERSISTENT DATA
# ============================================================

init python:

    import datetime

    if persistent.first_install_date is None:
        persistent.first_install_date = ""

    if persistent.total_playtime is None:
        persistent.total_playtime = 0.0

    if persistent.clean_exit is None:
        persistent.clean_exit = True


# ============================================================
# BACKGROUND SYSTEM
#
# 0 = Noon
# 1 = Day
# 2 = Evening
# 3 = Night
#
# Every 1 hour of actual game time changes the background.
# After 4 hours, the cycle starts over.
# ============================================================

init python:

    def get_background_stage(playtime):

        cycle_time = playtime % 14400.0

        if cycle_time < 3600.0:
            return 0

        elif cycle_time < 7200.0:
            return 1

        elif cycle_time < 10800.0:
            return 2

        else:
            return 3


# ============================================================
# START
# ============================================================

label start:

    # First installation date
    if persistent.first_install_date == "":

        $ persistent.first_install_date = datetime.datetime.now().strftime("%m-%d-%Y")


    # Check previous session
    if not persistent.clean_exit:

        $ crash_apology_unlocked = True

        p "That was scary.. I hope that wasn't a crash!"


    # Current session is now considered active.
    # Goodbye will turn this back to True.
    $ persistent.clean_exit = False
    $ renpy.save_persistent()


    # Background
    $ current_bg_stage = get_background_stage(
        persistent.total_playtime
    )


    # Start the game's systems
    show screen background_cycle
    show screen playtime_timer
    show screen idle_timer

    if dev_mode:
        show screen dev_mode_button


    p "Oh! I remember you!"

    p "Welcome to Poppy's Love!"

    p "You can press Talk whenever you want to talk to me."

    p "You can pick different things to talk about!"

    p "Music and game options will be added soon, too."

    jump main_screen


# ============================================================
# MAIN GAME SCREEN
# ============================================================

label main_screen:

    $ reset_idle_timer()

    menu:

        "Talk":
            jump talk

        "Nevermind":
            jump main_screen


# ============================================================
# TALK
# ============================================================

label talk:

    $ reset_idle_timer()

    if away_mode:

        $ away_mode = False

        p "Welcome back!"


    menu:

        "Hey, Poppy":
            jump hey_poppy

        "I love you":
            $ affection += 10
            jump love_you

        "I'm feeling":
            jump im_feeling

        "Bye":
            jump bye_menu

        "Nevermind":
            jump main_screen


# ============================================================
# HEY, POPPY
# ============================================================

label hey_poppy:

    $ reset_idle_timer()

    menu:

        "Compliments":
            jump compliments

        "Insults":
            jump insults

        "Apologize":
            jump apologize

        "Poppy":
            jump poppy_category

        "You":
            jump you_category

        "Be right back":
            jump be_right_back

        "Back":
            jump talk


# ============================================================
# COMPLIMENTS
# Every compliment gives +10 affection.
# ============================================================

label compliments:

    $ reset_idle_timer()

    menu:

        "You look pretty!":

            $ affection += 10

            p "Aww, you think so? Thank you!"

            jump compliments


        "I look up to you!":

            $ affection += 10

            p "You do? That actually means a lot to me."

            jump compliments


        "You're the best toon!":

            $ affection += 10

            p "The best? Oh, you're really trying to make me blush now!"

            jump compliments


        "You're cute!":

            $ affection += 10

            p "Cute?! Hehe... I'll take that as a compliment."

            jump compliments


        "Back":
            jump hey_poppy


# ============================================================
# INSULTS
# ============================================================

label insults:

    $ reset_idle_timer()

    menu:

        "Your bow doesn't suit you.":

            $ insult_unlocked = True

            p "...Oh. Well, I like my bow."

            jump insults


        "You're ugly.":

            $ insult_unlocked = True

            p "Wow. That's a little harsh, don't you think?"

            jump insults


        "I hate you.":

            $ insult_unlocked = True

            p "...You hate me? Did I do something to upset you?"

            jump insults


        "Back":
            jump hey_poppy


# ============================================================
# APOLOGIZE
# ============================================================

label apologize:

    $ reset_idle_timer()

    menu:

        "I apologize for insulting you." if insult_unlocked:

            $ insult_unlocked = False

            p "It's okay. I appreciate you apologizing."

            p "Just... try not to be so mean to me next time, okay?"

            jump apologize


        "I apologize for the game crashing." if crash_apology_unlocked:

            $ crash_apology_unlocked = False

            p "You don't have to apologize for that!"

            p "It wasn't your fault. I'm just glad you came back."

            jump apologize


        "I apologize for something.":

            p "Hmm? You don't have to apologize unless you actually did something."

            p "But... I appreciate the thought."

            jump apologize


        "Back":
            jump hey_poppy


# ============================================================
# POPPY CATEGORY
# ============================================================

label poppy_category:

    $ reset_idle_timer()

    menu:

        "When is your birthday?":

            p "Hmm... I don't actually know my birthday."

            p "I was released on June 14th, 2024, though, so I guess you could consider that my birthday!"

            if player_birthday == "":

                p "Oh yeah! You didn't tell me your birthday yet, have you? When is it?"

                call ask_birthday

            jump poppy_category


        "How old are you?":

            p "I don't know how old I am."

            jump poppy_category


        "When did we first meet?":

            p "I don't remember when we first met..."

            p "But I do remember that we started dating on November 9th, 2024."

            p "That's our anniversary!"

            jump poppy_category


        "When did I first install this game?":

            p "You first installed this game on [persistent.first_install_date]."

            p "I remember that."

            jump poppy_category


        "Back":
            jump hey_poppy


# ============================================================
# BIRTHDAY INPUT
# ============================================================

label ask_birthday:

    $ birthday_input = renpy.input(
        "When is your birthday? Must be numbers only. in this format: Month-Day-Year. E.g: 11-11-1111",
        length=10
    )

    $ birthday_input = birthday_input.strip()


    if (
        len(birthday_input) == 10
        and birthday_input[2] == "-"
        and birthday_input[5] == "-"
        and birthday_input[:2].isdigit()
        and birthday_input[3:5].isdigit()
        and birthday_input[6:].isdigit()
    ):

        $ player_birthday = birthday_input

        p "Got it! I'll remember that!"

        return


    else:

        p "Uhh.. Are you putting it in numbers only and in Month-Day-Year format? Try again!"

        jump ask_birthday


# ============================================================
# YOU CATEGORY
# ============================================================

label you_category:

    $ reset_idle_timer()

    menu:

        "When is my birthday?" if player_birthday != "":

            p "Oh! I remember! It was on [player_birthday]!"

            jump you_category


        "Can I change my pronouns?" if player_pronouns != "":

            p "Sure! What's your new one?"

            $ new_pronouns = renpy.input(
                "What are your new pronouns?"
            )

            $ new_pronouns = new_pronouns.strip()

            if new_pronouns != "":

                $ player_pronouns = new_pronouns

                p "Got it! I'll use those for you!"

            jump you_category


        "Can I change my name?" if player_name != "":

            p "Sure! Do you not like your past one? Oh well!"

            $ new_name = renpy.input(
                "What's your new name?"
            )

            $ new_name = new_name.strip()

            if new_name != "":

                $ player_name = new_name

                p "Ooo! That's a cool name! I'll use it for you!"

            jump you_category


        "Back":
            jump hey_poppy


# ============================================================
# BE RIGHT BACK
# ============================================================

label be_right_back:

    $ reset_idle_timer()

    menu:

        "I'm gonna code.":

            p "Ooo, I didn't know you could code! Have fun!"

            $ away_mode = True

            jump main_screen


        "I'm gonna rest.":

            p "It's good to rest!"

            $ away_mode = True

            jump main_screen


        "I'm gonna game.":

            p "Have fun!"

            $ away_mode = True

            jump main_screen


        "I'm gonna scroll.":

            p "Okay! I wish I could see what you're doing, hehe!"

            $ away_mode = True

            jump main_screen


        "I'm gonna use another app.":

            p "Ooo, which one?"

            $ away_mode = True

            jump main_screen


        "Be right back.":

            p "Okay!"

            $ away_mode = True

            jump main_screen


# ============================================================
# I LOVE YOU
# ============================================================

label love_you:

    $ reset_idle_timer()

    $ love_response = renpy.random.randint(1, 20)


    if love_response == 1:

        p "I love you too!"


    elif love_response == 2:

        p "Aww... I love you too!"


    elif love_response == 3:

        p "Hehe, I love you more!"


    elif love_response == 4:

        p "You really know how to make me smile."


    elif love_response == 5:

        p "I love hearing you say that."


    elif love_response == 6:

        p "You're so sweet."


    elif love_response == 7:

        p "And I love having you here with me."


    elif love_response == 8:

        p "I love you, silly!"


    elif love_response == 9:

        p "Aww! You're making me blush."


    elif love_response == 10:

        p "You have no idea how happy that makes me."


    elif love_response == 11:

        p "I love you too. More than you know."


    elif love_response == 12:

        p "Hehe... you're making me blush."


    elif love_response == 13:

        p "I was hoping you'd say that."


    elif love_response == 14:

        p "You're pretty lovable yourself, you know."


    elif love_response == 15:

        p "I love you! Don't forget that."


    elif love_response == 16:

        p "Aww... that's such a nice thing to hear."


    elif love_response == 17:

        p "I love you too! I'm glad we're together."


    elif love_response == 18:

        p "You always manage to make my day better."


    elif love_response == 19:

        p "Hehe. I love you, dummy."


    else:

        p "And I'll keep loving you right back."


    jump talk


# ============================================================
# I'M FEELING
# ============================================================

label im_feeling:

    $ reset_idle_timer()

    menu:

        "Happy":

            p "Ooo, that's good to know! If you're happy, I am too!"

            jump im_feeling


        "Sad":

            p "Why? You should turn that frown upside down!"

            jump im_feeling


        "Inadequate":

            p "You're always enough! Don't think that way!"

            jump im_feeling


        "Grateful":

            p "Ooo! For what?"

            $ affection += 10

            p "That makes me so happy to hear!!"

            jump im_feeling


        "Bored":

            p "You should come play with me!"

            jump im_feeling


        "Back":
            jump talk


# ============================================================
# BYE
# ============================================================

label bye_menu:

    $ reset_idle_timer()

    menu:

        "I'm going out.":

            p "Okay! Stay safe!"

            jump talk


        "I'm going to shower.":

            p "Yay, it's good that you're trying to! Stay clean!"

            jump talk


        "I'm going to school.":

            p "Okay, education is important!"

            jump talk


        "I'm going to work out.":

            p "Ooo, you work out?"

            jump talk


        "I'm going to sleep.":

            p "Okay, goodnight! Sweet dreams!"

            jump talk


        "I'm going to take you somewhere.":

            p "Ooo, okay! I'll be in the \"Poppy\" file in the characters folder!"

            p "You can take me anywhere! Maybe just save a backup before taking me out though? Hehe!"

            jump talk


        "I'm leaving for a bit.":

            p "Okay! I'll be waiting as long as you leave for! Don't take too long, hehe!"

            jump talk


        "Goodbye.":

            p "Bye!"

            # This is the proper clean exit.
            $ persistent.clean_exit = True
            $ renpy.save_persistent()

            return


        "Back":
            jump talk


# ============================================================
# RANDOM IDLE CONVERSATIONS
# ============================================================

label random_idle_conversation:

    $ idle_conversation_running = True

    $ conversation = renpy.random.randint(1, 3)


    if conversation == 1:

        p "Ooo! Do you know?"

        p "The creator of this game made this specifically for you!"

        p "That's because you're special, hehe!"


    elif conversation == 2:

        p "Hehe, this may be surprising to hear from me but.."

        p "What's your pronouns? I don't want to default to some random!"

        $ new_pronouns = renpy.input(
            "What's your pronouns?"
        )

        $ new_pronouns = new_pronouns.strip()

        if new_pronouns != "":

            $ player_pronouns = new_pronouns

            p "Got it! I'll use those for you!"


    elif conversation == 3:

        p "Can I know your name?"

        p "Hehe.. I don't mean to be random!"

        p "I just don't want to mistake your name and accidentally set it on its own!"

        $ new_name = renpy.input(
            "What's your name?"
        )

        $ new_name = new_name.strip()

        if new_name != "":

            $ player_name = new_name

            p "Ooo! That's a cool name! I'll use it for you!"


    $ idle_conversation_running = False

    return
