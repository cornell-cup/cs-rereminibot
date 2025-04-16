from avatar import Avatar
import xrp_sr_2 as sound
from spritesheet import Spritesheet
import time
import pygame
import numpy as np
import serial
import os
import psutil
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
    print("Initializing pygame...")
    time.sleep(1)
    infoObject = pygame.display.Info()
    
    # Choose between fullscreen or windowed mode based on your needs
    #screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((320, 320), pygame.RESIZABLE)  # Used to test in windowed mode
    print("Screen initialized")
    pygame.display.set_caption('Avatar Demo')
    pygame.mouse.set_visible(0)

    # Initialize avatar
    pi_ava = Avatar()
    path_to_expression_json = "./static/gui/static/js/components/Expression/expressions.json"
    path_to_img_dir = "./static/gui/static/img/Expressions/"

    # Log memory usage
    pid = os.getpid()
    process = psutil.Process(pid)
    memory_info = process.memory_info()
    print(f'RAM usage: {memory_info.rss / 1000 / 1000} MB')
    
    # Load expressions
    pi_ava.load_expressions_json(path_to_expression_json, path_to_img_dir)

    print("Loaded the following expressions:")
    for expression in pi_ava.get_expression_names():
        print(" - ", expression)

    pi_ava.set_playback_speed(15)
    print("Playback speed is currently at " + str(pi_ava._current_playback_speed))
    print("")

    # Initialize serial connection
    serial_connected = 0
    ser = None
    
    if os.path.exists('/dev/ttyACM0'):
        try:
            ser = serial.Serial('/dev/ttyACM0', 115200)
            serial_connected = 1
            time.sleep(1)
            print("Serial connection established")
        except Exception as e:
            print(f"Serial connection failed: {e}")
    
    # Initialize sound module
    sound.init_gpio()
    
    message_asked = False
    running = True
    current_expression = None
    expression_change_time = 0
    
    # Main loop
    while running:
        try:
            # Handle UART signals if connected
            if serial_connected and ser is not None and ser.inWaiting() > 0:
                message = ser.readline().decode()
                if len(message) > 0:
                    print(f"Received message: {message}")
                
                # Process expression change commands
                if message.startswith("SPR"):
                    message_asked = False
                    expression_name = message.split(",")[1].replace("\n", "").strip()
                    print(f"Expression request: '{expression_name}'")

                    # Only change expression if animation of current one is complete or it's the first one
                    if pi_ava.is_animation_complete() or current_expression is None:
                        if expression_name == "":
                            pi_ava.clear_current_expression()
                            current_expression = None
                        else:
                            # Load and switch to new expression
                            current_expression = expression_name
                            pi_ava.clear_current_expression()
                            success = pi_ava.load_single_expression_json(path_to_expression_json, expression_name, path_to_img_dir)
                            
                            if success:
                                # Play sound for new expression
                                sound.play_expression(expression_name)
                                expression_change_time = time.time()
                    else:
                        print(f"Ignoring expression change to '{expression_name}' - current animation not complete")

                # Process playback speed commands
                elif message.startswith("PBS"):
                    message_asked = False
                    playback_speed = message.split(",")[1]
                    pi_ava.set_playback_speed(float(playback_speed))

                # Process ask/prompt commands
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
                    print("Displaying prompt")
            
            # Update avatar animation state
            pi_ava.update()
            
            # Get current frame for display
            frame = pi_ava.get_current_display()

            # Check for animation completion after minimum duration
            if (current_expression is not None and 
                pi_ava.is_animation_complete() and 
                time.time() - expression_change_time >= MIN_ANIMATION_DURATION):
                print(f"Animation for '{current_expression}' completed")
                
            # Prepare frame for display
            if frame is None:
                frame_np = np.zeros((320, 320, 3), dtype=np.uint8)
            else:
                frame_np = np.array(frame)

            # Convert image format if needed
            if len(frame_np.shape) == 2:  # Grayscale to RGB
                frame_np = np.stack([frame_np]*3, axis=-1)
            elif frame_np.shape[2] == 4:  # RGBA to RGB
                frame_np = frame_np[:, :, :3]
                
            # Create pygame surface and scale it
            frame_surface = pygame.surfarray.make_surface(frame_np.swapaxes(0, 1))
            frame_surface = pygame.transform.scale(frame_surface, (infoObject.current_w, infoObject.current_h))
            
            # Update display
            if not message_asked:
                screen.blit(frame_surface, (0, 0))
            pygame.display.update()
            
            # Handle pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("Escape pressed, quitting")
                        running = False
            
            time.sleep(0.005)  # Adjust as needed for framerate
            
        except KeyboardInterrupt:
            print("Keyboard interrupt received, exiting")
            running = False
            
        except serial.SerialException:
            print("Serial connection lost, attempting to reconnect...")
            if os.path.exists('/dev/ttyACM0'):
                try:
                    ser = serial.Serial('/dev/ttyACM0', 115200)
                    serial_connected = 1
                    time.sleep(1)
                    print("Serial reconnected")
                except Exception as e:
                    print(f"Serial reconnection failed: {e}")
                    time.sleep(2)  # Wait before trying again
                    
        except Exception as e:
            print(f"Exception caught: {type(e)}, {e}")
            print(traceback.format_exc())
            
            # Try to reconnect serial if that's the issue
            if os.path.exists('/dev/ttyACM0'):
                try:
                    ser = serial.Serial('/dev/ttyACM0', 115200)
                    serial_connected = 1
                    time.sleep(1)
                    print("Serial reconnected after exception")
                except:
                    pass
    
    # Clean up resources
    print("Pi Zero Script Complete, cleaning up...")
    sound.cleanup()  # Clean up GPIO
    pygame.quit()

if __name__ == "__main__":
    run_pi_zero()