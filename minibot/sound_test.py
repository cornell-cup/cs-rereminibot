import pygame 
import os
# Initialize 

pygame.mixer.init() 
# Load and play sound file (replace 'sound.wav' with your file) 
pygame.mixer.music.load("static\\gui/static/sound/drum.wav")
pygame.mixer.music.play()
 # Keep script running while audio plays 

while pygame.mixer.music.get_busy(): 
    pass