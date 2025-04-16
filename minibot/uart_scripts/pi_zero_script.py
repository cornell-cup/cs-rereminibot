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
import threading
import traceback

MIN_ANIMATION_DURATION = 4

# Flag to interrupt current sound playback
sound_interrupt_flag = threading.Event()
# Flag to indicate when the animation is complete
animation_complete_flag = threading.Event()

def add_expression(avatar : Avatar, expr_name : str, sheet_src : str, frame_count : int, frame_width : int, frame_height : int):
    sheet = Spritesheet(src=sheet_src,
                             frame_width=frame_width,
                             frame_height=frame_height,
                             frame_count=frame_count)
    
    if not sheet._loaded_correctly:
        print("Expression " + expr_name + " could not be added. Spritesheet did not load correctly!")
        return

    avatar.add_or_update_expression(expr_name, sheet)

def play_sound_thread(expression_name, animation_duration=None):
    """Function to run in a separate thread for sound playback that plays for the duration of animation"""
    try:
        # Reset interrupt flag at beginning of new sound
        sound_interrupt_flag.clear()
        animation_complete_flag.clear()
        
        print(f"Starting sound for '{expression_name}' with animation duration ~{animation_duration}s")
        
        # Keep playing the sound until the animation completes or an interrupt occurs
        start_time = time.time()
        while not sound_interrupt_flag.is_set() and not animation_complete_flag.is_set():
            # Play the sound once
            sound.play_expression(expression_name, sound_interrupt_flag)
            
            # Check if we've played for the expected animation duration
            if animation_duration and (time.time() - start_time) >= animation_duration:
                break
                
            # Short pause between repetitions to avoid abrupt transitions
            if not sound_interrupt_flag.is_set() and not animation_complete_flag.is_set():
                time.sleep(0.1)
                
        print(f"Sound playback for '{expression_name}' completed or interrupted")
            
    except Exception as e:
        print(f"Sound playback error: {e}")
        traceback.print_exc()  # Print full error for debugging

def get_animation_duration(avatar, expression_name):
    """Estimate the duration of an animation based on frame count and playback speed"""
    if expression_name not in avatar._expressions:
        return None
    
    # Get the frame count and playback speed
    frame_count = avatar._expressions[expression_name]._frame_count
    playback_speed = avatar._current_playback_speed
    
    # Calculate approximate duration in seconds
    # The playback_speed is in frames per second
    if playback_speed > 0:
        return frame_count / playback_speed
    return None

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

    # Serial setup
    serial_connected = 0
    ser = None
    print(os.path.exists('/dev/ttyACM0'))
    if os.path.exists('/dev/ttyACM0'):
        ser = serial.Serial('/dev/ttyACM0', 115200)
        serial_connected = 1
        time.sleep(1)

    message_asked = False
    running = True
    no = False
    
    # Animation tracking variables
    sound_thread = None
    current_expression = None
    animation_in_progress = False
    frame_count = 0
    last_frame_time = time.time()
    animation_start_time = None
    
    # Expression queue to ensure we complete one before starting another
    expression_queue = []
    
    while running:
        try:
            # Handle UART Signals if serial port exists
            if ser is not None and os.path.exists('/dev/ttyACM0'):
                try:
                    if ser.inWaiting() > 0:
                        message = ser.readline().decode()
                        if len(message) > 0:
                            print(message)
                        
                        # Handle SPR (expression) messages
                        if message.startswith("SPR"):
                            print("reached here1 ")
                            message_asked = False
                            expression_name = message.split(",")[1].replace("\n", "").strip()
                            print("reached here2")
                            print("Expression Name: \'" + expression_name + "\'")
                            
                            # Add expression to queue instead of processing immediately
                            expression_queue.append(expression_name)
                            
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
                except Exception as e:
                    print(f"Serial read error: {e}")
            
            # Process next expression from queue if we're not currently animating
            if not animation_in_progress and expression_queue:
                # Signal any running sound thread to stop
                sound_interrupt_flag.set()
                animation_complete_flag.set()
                
                # If there's a thread running, wait briefly for it to terminate
                if sound_thread and sound_thread.is_alive():
                    sound_thread.join(0.1)  # Wait briefly, but don't block indefinitely
                
                # Get next expression
                expression_name = expression_queue.pop(0)
                
                if expression_name == "":
                    pi_ava.clear_current_expression()
                    current_expression = None
                else:
                    pi_ava.clear_current_expression()
                    pi_ava.load_single_expression_json(path_to_expression_json, expression_name, path_to_img_dir)
                    current_expression = expression_name
                    frame_count = 0  # Reset frame counter for new expression
                    animation_in_progress = True
                    animation_start_time = time.time()
                    
                    # Get animation duration for synchronized sound playback
                    animation_duration = get_animation_duration(pi_ava, expression_name)
                    if animation_duration:
                        # Ensure minimum duration for very short animations
                        animation_duration = max(animation_duration, MIN_ANIMATION_DURATION)
                        print(f"Animation duration: {animation_duration}s")
                    
                    # Reset flags
                    sound_interrupt_flag.clear()
                    animation_complete_flag.clear()
                    
                    # Create and start a new thread for sound playback
                    sound_thread = threading.Thread(
                        target=play_sound_thread, 
                        args=(expression_name, animation_duration)
                    )
                    sound_thread.daemon = True  # Make thread daemon so it exits when main program exits
                    sound_thread.start()
                    
                    print(f"Started animation and sound for {expression_name}")
            
            # Update avatar
            pi_ava.update()
            frame = pi_ava.get_current_display()
            
            # Check if we have an ongoing animation to track
            if animation_in_progress and current_expression:
                now = time.time()
                
                # Check if animation has been running long enough to complete
                if frame is not None:
                    frame_count += 1
                    last_frame_time = now
                    
                    # Get the total frames in the animation
                    total_frames = pi_ava._expressions.get(current_expression)._frame_count if current_expression in pi_ava._expressions else 0
                    
                    # Determine if we've gone through at least one full cycle
                    # We check either if we've seen enough frames or if enough time has passed
                    animation_elapsed_time = now - animation_start_time
                    animation_duration = get_animation_duration(pi_ava, current_expression)
                    
                    # Check if we've completed at least one full cycle
                    if (frame_count >= total_frames or 
                        (animation_duration and animation_elapsed_time >= animation_duration * 1.5)):
                        
                        print(f"Animation for {current_expression} completed after {frame_count} frames")
                        print(f"Animation took {animation_elapsed_time:.2f} seconds")
                        
                        # Mark animation as complete
                        animation_complete_flag.set()
                        animation_in_progress = False
                        
                        # Only stop sound if there are no more expressions in queue
                        if not expression_queue:
                            sound_interrupt_flag.set()

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
            
            # Handle Pygame events
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
            
        except KeyboardInterrupt:
            running = False
            continue
        except OSError:
            print("Remove power and plug it back in")
            break
        except Exception as e:
            print("in exception")
            print(type(e))
            print(e)
            traceback.print_exc()  # Add full traceback for better debugging
            print(f"Device exists {os.path.exists('/dev/ttyACM0')}")
            if os.path.exists('/dev/ttyACM0'):
                print("Reinitializing ser")
                ser = serial.Serial('/dev/ttyACM0', 115200)
                serial_connected = 1
                time.sleep(1)
    
    # Signal all threads to terminate
    sound_interrupt_flag.set()
    animation_complete_flag.set()
    print("Pi Zero Script Complete.")
    pygame.quit()