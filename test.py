from avatar import Avatar
from spritesheet import Spritesheet

from matplotlib import pyplot as plt

def test_avatar():
    test_ava = Avatar()

    color_flash_sheet = Spritesheet(src="sprites/ColorFlash.png", 
                                    frame_width=480, 
                                    frame_height=320, 
                                    frame_count=8)
    
    if not color_flash_sheet._loaded_correctly:
        print("Color Flash Spritesheet did not load correctly!")
        return

    eyes_sheet = Spritesheet(src="sprites/Eyes_Idle.png",
                             frame_width=480,
                             frame_height=320,
                             frame_count=20)
    
    if not eyes_sheet._loaded_correctly:
        print("Eyes Spritesheet did not load correctly!")
        return
    
    test_ava.add_or_update_expression("flash", color_flash_sheet)
    test_ava.add_or_update_expression("idle", eyes_sheet)

    test_ava.set_current_expression("flash")

    for i in range(250):
        test_ava.update()
        frame = test_ava.get_current_display()

        if i == 0:
            img_fig = plt.imshow(frame)
        else:
            img_fig.set_data(frame)

        plt.pause(0.01)

    test_ava.set_current_expression("idle")
    plt.close()

    for i in range(250):
        test_ava.update()
        frame = test_ava.get_current_display()

        if i == 0:
            img_fig = plt.imshow(frame)
        else:
            img_fig.set_data(frame)

        plt.pause(0.01)

if __name__ == "__main__":
    test_avatar()