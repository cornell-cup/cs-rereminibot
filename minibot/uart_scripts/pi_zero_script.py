from avatar import Avatar
import xrp_sr_2 as sound
from spritesheet import Spritesheet
import time
import pygame
import numpy as np
#from memory_profiler import profile

import serial
import os
import psutil
from PIL import Image

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

#@profile
def run_pi_zero(demo_expression : str = "excited"):
    pygame.init()
    print("init")
    time.sleep(1)
    print("sleep")
    infoObject = pygame.display.Info()
    #screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((320, 320), pygame.RESIZABLE) # Used to test in windowed mode
    print("start screen")
    pygame.display.set_caption('Avatar Demo')
    pygame.mouse.set_visible(0)
    print("window stuff")

    pi_ava = Avatar()

    path_to_expression_json = "./static/gui/static/js/components/Expression/expressions.json"
    path_to_img_dir = "./static/gui/static/img/Expressions/"

    pid = os.getpid()
    process = psutil.Process(pid)
    memory_info = process.memory_info()
    print(f'RAM usage: {memory_info.rss / 1000 / 1000} MB')
    #pi_ava.load_expressions_json(path_to_expression_json, path_to_img_dir)

    print("Loaded the following expressions:")
    for expression in pi_ava.get_expression_names():
        print(" - ", expression)

    pi_ava.set_playback_speed(15)

    print("Playback speed is currently at " + str(pi_ava._current_playback_speed))
    print("")

    # pi_ava.set_current_expression(demo_expression)

    # timeout=None means there is no timeout between messages
    # xonoff is software control for 
    serial_connected = 0
    print(os.path.exists('/dev/ttyACM0'))
    if os.path.exists('/dev/ttyACM0'):
        ser = serial.Serial('/dev/ttyACM0', 115200)
        serial_connected = 1
        time.sleep(1)

    message_asked = False
    running = True
    no = False
    while running:
        print(f"Device exists {os.path.exists('/dev/ttyACM0')}")
        try:
            # Handle UART Signals
            print(ser)
            print(ser.inWaiting())
            # Run UART receive, nonblocking 
            if ser is not None:# and ser.inWaiting() > 0:
                message = ser.readline().decode()
                if len(message) > 0:
                    print(message)
                if message.startswith("SPR"): # some key that represents an animation LCD[emotion]
                    print("reached here1 ")
                    message_asked = False
                    # Run LCD methods
                    expression_name = message.split(",")[1].replace("\n", "").strip()
                    print("reached here2")
                    print("Expression Name: \'" + expression_name + "\'")

                    if expression_name == "":
                        pi_ava.clear_current_expression()
                    else:
                        pi_ava.clear_current_expression()
                        pi_ava.load_single_expression_json(path_to_expression_json, expression_name, path_to_img_dir)
                        sound.play_expression(expression_name)

                elif message.startswith("PBS"):
                    message_asked = False
                    playback_speed = message.split(",")[1]

                    pi_ava.set_playback_speed(float(playback_speed))

                elif message.startswith("ASK"):
                    message_asked = True
                    white = (255, 255, 255)
                    black = (0, 0, 0)
                    expression_ask = message.split(",")[1]
                    font = pygame.font.Font(None, 60)
                    screen.fill(black)
                    ask_phrase = "Play " + expression_ask[:-2] + "?"
                    text = font.render(ask_phrase, True, white)
                    textRect = text.get_rect()
                    textRect.center = (infoObject.current_w//2, infoObject.current_h//2)
                    screen.blit(text, textRect)
                    print("ask")

                # Send OK message back
                # ser.write(b'OK')
            

            # Update avatar
            pi_ava.update()
            frame = pi_ava.get_current_display()
            #if not no:
            #    frame.show()
            #    no = True
            #print(pi_ava._current_expression)

            # Update Pygame Screen
            if frame is None:
                frame_np = np.zeros((320,480))
            else:
                frame_np = np.array(frame)

            if len(frame_np.shape) == 2:  # Grayscale to RGB
                frame_np = np.stack([frame_np]*3, axis=-1)
            elif frame_np.shape[2] == 4:  # RGBA to RGB
                frame_np = frame_np[:, :, :3]
            frame_surface = pygame.surfarray.make_surface(frame_np.swapaxes(0,1))
            frame_surface = pygame.transform.scale(frame_surface, (infoObject.current_w, infoObject.current_h))
            #frame_surface = pygame.transform.scale(frame_surface, (50, 50)) # Used to test in windowed mode
            if not message_asked:
                screen.blit(frame_surface, (0, 0))
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("escape pressed")
                        pygame.quit()
                        running = False
            
            time.sleep(0.005)  # Adjust as needed for framerate
        except KeyboardInterrupt as ki:
            running = False
            continue
        except OSError:
            print("Remove power and plug it back in")
            break
        except Exception as e:
            print("in exception")
            print(type(e))
            print(e)
            # running = False
            # print("Encountered Exception!")
            # print(type(e), e)
            # print(traceback.format_exc())
            print(f"Device exists {os.path.exists('/dev/ttyACM0')}")
            if os.path.exists('/dev/ttyACM0'):
                print("Reinitializing ser")
                ser = serial.Serial('/dev/ttyACM0', 115200)
                serial_connected = 1
                time.sleep(1)
    
    print("Pi Zero Script Complete.")
    pygame.quit()

if __name__ == "__main__":
    run_pi_zero()
