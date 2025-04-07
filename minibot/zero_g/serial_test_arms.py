from XRPLib.defaults import *
import time

# available variables from defaults: left_motor, right_motor, drivetrain,
#      imu, rangefinder, reflectance, servo_one, board, webserver
# Write your code Here

# emotions = ["neutral" , "sick", "scared", "vomit", "vomit2", "wow", "ready_to_race", "excited", "chuckle", "sad", "startled"]
 
emotions = ["chuckle", "ready_to_race", "neutral", "sick", "surprise", "vomit2", "vomit"] 

i = 0
while True: 
    if board.is_button_pressed():
        if i == 0 or i == 1 or i == 6:
            print("PBS,15");
            print(f"SPR,{emotions[i]}");
            time.sleep(1);
        else:
            print("PBS,5");
            print(f"SPR,{emotions[i]}");
            time.sleep(1);
        i += 1
        if i == len(emotions):
            i = 0

    if (emotions[i] == "vomit") or (emotions[i] == "sick") or (emotions[i] == "vomit2"):
        servo_one.set_angle(90)
        servo_two.set_angle(90)
    elif (emotions[i] == "chuckle") or (emotions[i] == "ready_to_race") or (emotions[i] == "surprise"):
        servo_one.set_angle(180)
        servo_two.set_angle(180)
    elif (emotions[i] == "neutral"):
        servo_one.set_angle(0)
        servo_two.set_angle(0)
 