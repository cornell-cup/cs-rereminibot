"""
THIS IS a failed attempt to get raylib to convert numpy to pyray Image to cast as a texture. 
    The documentation recommends that pyray images to be careatd with reference to image path.
    
    *** If this library is used for future uses we should consider saving sprite images out to a 
    temporary working directory and passing that path in to create an image. ***
"""

from avatar import Avatar
from spritesheet import Spritesheet
import time
import numpy as np
import pyray as pr
from ctypes import c_void_p, memmove


pr.init_window( 480,320, "Demo Pyray")
pr.set_target_fps(60)

MIN_ANIMATION_DURATION = 4

def add_expression(avatar: Avatar, expr_name: str, sheet_src: str, frame_count: int):
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
    # add_expression(demo_ava, "flash", "sprites/ColorFlash.png", 8)
    add_expression(demo_ava, "idle", "sprites/Eyes_Idle.png", 20) 
    add_expression(demo_ava, "roll", "sprites/Eyes_Roll.png", 30) 
    add_expression(demo_ava, "brow_raise", "sprites/Eyes_Eyebrow_Raise.png", 30)
    
    print("Loaded the following expressions:")
    for expression in demo_ava.get_expression_names():
        print(" - ", expression)

    print("Playback speed is currently at " + str(demo_ava._current_playback_speed))
    print("")

    
    
    while not pr.window_should_close():
      
        for expression in demo_ava.get_expression_names():
            demo_ava.set_playback_speed(20)

            if demo_ava.set_current_expression(expression):
                demo_ava.update()
                frame = demo_ava.get_current_display()
                frame_np = np.array(frame)

                pr.clear_background(pr.RAYWHITE)

                if len(frame_np.shape) == 2:  # Grayscale to RGB
                    frame_np = np.stack([frame_np]*3, axis=-1)
                elif frame_np.shape[2] == 4:  # RGBA to RGB
                    frame_np = frame_np[:, :, :3]
                
                pr.begin_drawing()
                
                frame_np = frame_np.astype(np.uint8)
                image = pr.Image(frame_np.ctypes.data_as(pr.POINTER(pr.c_ubyte)), frame_np.shape[1], frame_np.shape[0], 3, pr.UNCOMPRESSED_R8G8B8)
                texture = pr.load_texture_from_image(image)
                pr.draw_texture(texture)

                pr.end_drawing()
                if demo_ava._current_playback_speed == 0:
                    animation_duration = MIN_ANIMATION_DURATION
                else:
                    two_cycles_duration = 2 * demo_ava.get_current_frame_count() / abs(demo_ava._current_playback_speed)
                    animation_duration = max(MIN_ANIMATION_DURATION, two_cycles_duration)

                start_time = time.time()

                while time.time() - start_time < animation_duration:
                    pr.begin_drawing()
                    demo_ava.update()
                    frame = demo_ava.get_current_display()
                    frame_np = np.array(frame)
                    if len(frame_np.shape) == 2:  # Grayscale to RGB
                        frame_np = np.stack([frame_np]*3, axis=-1)
                    elif frame_np.shape[2] == 4:  # RGBA to RGB
                        frame_np = frame_np[:, :, :3]
                    image = pr.Image(frame_np.ctypes.data_as(c_void_p), frame_np.shape[1], frame_np.shape[0], frame_np.shape[2], pr.PIXELFORMAT_UNCOMPRESSED_R8G8B8A8)
                    texture = pr.load_texture_from_image(image)
                    pr.draw_texture(texture)
                    pr.end_drawing()
                    time.sleep(0.01)  # Adjust as needed for framerate
            else:
                print("Expression could not be found! Try another expression!")


        pr.close_window()
        print("Demo Complete!")

if __name__ == "__main__":
    run_demo()
