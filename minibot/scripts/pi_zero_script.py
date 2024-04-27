from avatar import Avatar
from spritesheet import Spritesheet
import time
import pygame
import numpy as np

import serial
from .message_utils import *

import traceback

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

def run_pi_zero(demo_expression : str = "excited"):
    pygame.init()
    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
    pygame.display.set_caption('Avatar Demo')
    pygame.mouse.set_visible(0)

    pi_ava = Avatar()

    path_to_expression_json = "./static/gui/static/js/components/Expression/expressions.json"
    path_to_img_dir = "./static/gui/static/img/Expressions/"

    pi_ava.load_expressions_json(path_to_expression_json, path_to_img_dir)

    print("Loaded the following expressions:")
    for expression in pi_ava.get_expression_names():
        print(" - ", expression)

    pi_ava.set_playback_speed(30)

    print("Playback speed is currently at " + str(pi_ava._current_playback_speed))
    print("")

    pi_ava.set_current_expression(demo_expression)

    # timeout=None means there is no timeout between messages
    # xonoff is software control for 
    ser = serial.Serial('/dev/ttyAMA0', baudrate=115200, timeout=0, stopbits=serial.STOPBITS_ONE)

    running = True
    while running:
        try:
            # Handle UART Signals
            
            # Run UART receive, nonblocking 
            request = ser.readline().decode() # Decoding gets rid of newline character at the end 

            # un-format request
            if request == 'Write.':
                pass
            elif validate_crc_message(request):
                request = unpack_crc_message(request)

                if request.startswith("SPR"): # some key that represents an animation LCD[emotion]
                    # Run LCD methods
                    expression_name = request.split(",")[1]

                    pi_ava.set_current_expression(expression_name)

                elif request.startswith("PBS"):
                    playback_speed = request.split(",")[1]

                    pi_ava.set_playback_speed(float(playback_speed))

                # Send OK message back
                # ser.write(b'OK')
            

            # Update avatar
            pi_ava.update()
            frame = pi_ava.get_current_display()
            

            # Update Pygame Screen
            frame_np = np.array(frame)
            if len(frame_np.shape) == 2:  # Grayscale to RGB
                frame_np = np.stack([frame_np]*3, axis=-1)
            elif frame_np.shape[2] == 4:  # RGBA to RGB
                frame_np = frame_np[:, :, :3]
            frame_surface = pygame.surfarray.make_surface(frame_np.swapaxes(0,1))
            frame_surface = pygame.transform.scale(frame_surface, (infoObject.current_w, infoObject.current_h))
            screen.blit(frame_surface, (0, 0))
            pygame.display.update()
            
            
            time.sleep(0.005)  # Adjust as needed for framerate
        except KeyboardInterrupt as ki:
            running = False
            continue
        except Exception as e:
            running = False
            print("Encountered Exception!")
            print(type(e), e)
            print(traceback.format_exc())
    
    print("Pi Zero Script Complete.")
    pygame.quit()

if __name__ == "__main__":
    run_pi_zero()
