from avatar import Avatar
from spritesheet import Spritesheet
import time
import pygame
import random
import numpy as np
import json

MIN_ANIMATION_DURATION = 4

def add_expression(avatar : Avatar, expr_name : str, sheet_src : str, frame_count : int, frame_width : int, frame_height : int):
    sheet = Spritesheet(src=sheet_src,
                             frame_width=frame_width,
                             frame_height=frame_height,
                             frame_count=frame_count)
    
    if not sheet._loaded_correctly:
        print("Expression " + expr_name + " could not be added. Spritesheet did not load correctly!")
        return

    avatar.add_or_update_expression(expr_name, sheet)

def run_demo():
    pygame.init()
    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
    pygame.display.set_caption('Avatar Demo')
    pygame.mouse.set_visible(0)

    demo_ava = Avatar()
    # add_expression(demo_ava, "flash", "sprites/ColorFlash.png", 8)

    demo_ava.load_expressions_json("expressions.json")
    


    print("Loaded the following expressions:")
    for expression in demo_ava.get_expression_names():
        print(" - ", expression)

    print("Playback speed is currently at " + str(demo_ava._current_playback_speed))
    print("")
    demo_ava.set_playback_speed(20)


    for expression in demo_ava.get_expression_names():
      

        if demo_ava.set_current_expression(expression):
            animation_duration = 3 * demo_ava.get_current_frame_count() / abs(demo_ava._current_playback_speed)
            start_time = time.time()

            while time.time() - start_time < animation_duration:
                demo_ava.update()
                frame = demo_ava.get_current_display()
                frame_np = np.array(frame)
                if len(frame_np.shape) == 2:  # Grayscale to RGB
                    frame_np = np.stack([frame_np]*3, axis=-1)
                elif frame_np.shape[2] == 4:  # RGBA to RGB
                    frame_np = frame_np[:, :, :3]
                frame_surface = pygame.surfarray.make_surface(frame_np.swapaxes(0,1))
                frame_surface = pygame.transform.scale(frame_surface, (infoObject.current_w, infoObject.current_h))
                screen.blit(frame_surface, (0, 0))
                pygame.display.update()
                time.sleep(0.01)  # Adjust as needed for framerate
        else:
            print("Expression could not be found! Try another expression!")
   
    print("Demo Complete!")
    pygame.quit()
    

if __name__ == "__main__":
    run_demo()
