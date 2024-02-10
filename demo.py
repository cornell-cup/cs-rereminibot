from avatar import Avatar
from spritesheet import Spritesheet

from matplotlib import pyplot as plt

import time

MIN_ANIAMTION_DURATION = 4

def add_expression(avatar : Avatar, expr_name : str, sheet_src : str, frame_count : int):
    sheet = Spritesheet(src=sheet_src,
                             frame_width=480,
                             frame_height=320,
                             frame_count=frame_count)
    
    if not sheet._loaded_correctly:
        print("Expression " + expr_name + " could not be added. Spritesheet did not load correctly!")
        return

    avatar.add_or_update_expression(expr_name, sheet)

def run_demo():
    demo_ava = Avatar()

    add_expression(demo_ava, "flash", "sprites/ColorFlash.png", 8)

    add_expression(demo_ava, "idle", "sprites/Eyes_Idle.png", 20) 
    add_expression(demo_ava, "roll", "sprites/Eyes_Roll.png", 30) 
    add_expression(demo_ava, "brow_raise", "sprites/Eyes_Eyebrow_Raise.png", 30)
    
    print("Loaded the following expressions:")
    for expression in demo_ava.get_expression_names():
        print(" - ", expression)

    print("Playback speed is currently at " + str(demo_ava._current_playback_speed))
    print("")

    while True:
        user_input = input("Enter expression, a number for new playback speed, or q to quit:")

        if user_input == "q":
            break

        if user_input.isnumeric() or (user_input[0] == '-' and user_input[1:].isnumeric()):
            demo_ava._current_playback_speed = float(user_input)
            print("Current Playback Speed Set to " + user_input)
            continue

        if demo_ava.set_current_expression(user_input):
            demo_ava.update()
            frame = demo_ava.get_current_display()
            img_fig = plt.imshow(frame)

            two_cycles_duration = 2 * demo_ava.get_current_frame_count() / abs(demo_ava._current_playback_speed)
            animation_duration = max(MIN_ANIAMTION_DURATION, two_cycles_duration)

            start_time = time.time()

            while time.time() - start_time < animation_duration:
                demo_ava.update()
                frame = demo_ava.get_current_display()
                img_fig.set_data(frame)
                plt.pause(0.01)
            plt.close()
        else:
            print("Expression could not be found! Try another expression!")

    print("Demo Complete!")

if __name__ == "__main__":
    run_demo()