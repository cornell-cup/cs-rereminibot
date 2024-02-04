from avatar import Avatar
from spritesheet import Spritesheet

import time

def color_flash_test_avatar():
    test_ava = Avatar()

    color_flash_sheet = Spritesheet(src="ColorFlash.png", 
                                    frame_width=32, 
                                    frame_height=32, 
                                    frame_count=8)
    
    if not color_flash_sheet._loaded_correctly:
        print("Spritesheet did not load correctly!")
        return
    
    test_ava.add_or_update_expression("flash", color_flash_sheet)

    test_ava.set_current_expression("flash")

    for i in range(200):
        test_ava.update()
        frame = test_ava.get_current_display()

        print(frame.getpixel((0,0)))
        time.sleep(0.02)

if __name__ == "__main__":
    color_flash_test_avatar()