import time
import RPi.GPIO as GPIO

# Set up GPIO
BUZZER_PIN = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
pwm = GPIO.PWM(BUZZER_PIN, 1000)  # Initialize PWM on pin 20 with 1000 Hz

# Mapping letters to sounds
sound_library = {
    'A': [(1200, 0.07)],  # Happy Beep
    'B': [(300, 0.4)],  # Sad Beep
    'C': [(1800, 0.06)],  # Excited Chirp
    'D': [(750, 0.08)],  # Angry Honk
    'E': [(500, 0.12)],  # Calm Hum
    'F': [(1300, 0.05, 1450)],  # Playful Whistle (pitch slide)
    'G': [(1600, 0.04, 1400, 0.04)],  # Goofy Trill
    'H': [(1000, 0.07, 1400)],  # Curious Rising Tone
    'I': [(1500, 0.03, 600, 0.03)],  # Fast Whirr
    'J': [(1100, 0.03, 900, 0.03)],  # Short Warble
    'K': [(900, 0.3, 1800)],  # Long Whistle
    'L': [(1400, 0.8, 600)],  # Sad Downslide
    'M': [(1900, 0.05), (2100, 0.05)],  # Alert Chirps
    'N': [(2300, 0.08)],  # Surprise Zing
    'O': [(650, 0.08)],  # Neutral Sigh
}

sound_mappings = {
    "big_no": ['D','O','L','D','O','L'],
    "big_yes": ['A', 'I','C','A','I','C'],
    "chuckle": ['G','G','G'],
    "surprise": ['N','M','N'],
    "no": ['O','O','O'],
    "ready_to_race": ['F','I','F','I','F','I','F'],
    "sad": ['L','L','B','L','L','B'],
    "idle_stable": ['E','E','E','E'],
    "startled": ['M','N','M','N'],
    "yes": ['A','A','A'],
    "love_it": ['A','F','A','F','A'],
    "vomit": ['B','L','G','B','L','G'],
    "blink_awake": ['E','M','E','M']
}

def generate_sound(frequency, duration, end_freq=None):
    """Generate a beep sound with optional pitch sliding using a piezo buzzer."""
    pwm.start(50)  # Start PWM with 50% duty cycle
    
    if end_freq:
        # For sliding pitches, we'll step through frequencies
        steps = int(duration * 100)  # 100 steps per second
        step_time = duration / steps
        for i in range(steps):
            current_freq = frequency + (end_freq - frequency) * (i / steps)
            pwm.ChangeFrequency(current_freq)
            time.sleep(step_time)
    else:
        # For constant pitches
        pwm.ChangeFrequency(frequency)
        time.sleep(duration)
    
    pwm.stop()  # Stop PWM
    time.sleep(0.01)  # Small gap between sounds

def play_beeps(beep_sequence):
    """Generate and play beeps dynamically, mimicking R2-D2-style expressive speech."""
    for beep in beep_sequence:
        if beep is None:
            time.sleep(0.03)  # Reduced pause for more natural flow
        elif len(beep) == 2:
            generate_sound(beep[0], beep[1])
        elif len(beep) == 3:
            generate_sound(beep[0], beep[1], beep[2])
        elif len(beep) > 3:
            for i in range(0, len(beep), 2):
                if i+1 < len(beep):  # Make sure we don't go out of bounds
                    generate_sound(beep[i], beep[i+1])
                    time.sleep(0.01)

def play_expression(expression_name):
    """Play sounds corresponding to a specific expression name."""
    if expression_name in sound_mappings:
        beep_sequence = []
        for letter in sound_mappings[expression_name]:
            if letter in sound_library:
                beep_sequence.extend(sound_library[letter])
        
        print(f"Playing '{expression_name}' expression...")
        play_beeps(beep_sequence)
        GPIO.cleanup()
        return True
    else:
        print(f"Expression '{expression_name}' not found in sound mappings.")
        GPIO.cleanup()
        return False
