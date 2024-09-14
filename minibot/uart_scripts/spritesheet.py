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
        self._image_src = src

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
        Returns the frame with the specified frame number. 
        
        If the specified frame number is a decimal, it is rounded down to the 
        nearest integer.

        If the specified frame number is greater than or equal to the total
        frame count N, it is brought into the range [0,N) by subtracting a
        multiple of N. For instance, if there are ten total frames, and 
        `frame_number` is set to 11, the second frame at index 1 is returned.

        If the specified frame number is less than zero, it is brought into the
        range [0,N) by adding a multiple of N. 

        Parameters
        -------------
        frame_number : float
            The number of the frame being accessed.

        Returns
        -------------
        A PIL Image representing the current frame.
        """
        
        num = abs(int(frame_number)) % self._frame_count
        if frame_number < 0 and num != 0:
            num = 10 - num

        return self._frames[num]

        
    

