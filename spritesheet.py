from PIL import Image

class Spritesheet:

    def __init__(self, src, frame_width, frame_height, frame_count):
        self._loaded_correctly = False
        
        try:
            self._full_spriteheet = Image.open(src)

        except Exception as e:
            print("Failed to load image! Reason:")
            print(e)

            return self

        self._frame_width = frame_width
        self._frame_height = frame_height
        self._frame_count = frame_count

        num_frames_h = int(self._full_spriteheet.width / frame_width)
        num_frames_v = int(self._full_spriteheet.height / frame_height)
        
        self._frames = []
        break_outer_loop = False

        for i in range(num_frames_v):
            for j in range(num_frames_h):
                if (i * num_frames_h + j) >= frame_count:
                    break_outer_loop = True
                    break
                
                crop_region = (j * frame_width, i * frame_height,
                                (j + 1) * frame_width, (i + 1) * frame_height)
                self._frames.append(self._full_spriteheet.crop(crop_region))

            if break_outer_loop:
                break

        self._loaded_correctly = True

       

    def get_frame(self, frame_number : float) -> Image:
        """
        
        """
        
        while frame_number >= self._frame_count:
            frame_number -= self._frame_count

        while frame_number < 0:
            frame_number += self._frame_count

        return self._frames[int(frame_number)]

        
        

