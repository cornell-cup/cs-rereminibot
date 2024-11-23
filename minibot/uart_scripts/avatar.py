from spritesheet import Spritesheet
import time
import json

class Avatar:

    def __init__(self, expressions : dict = {}, current_expression : str = None, 
                 current_playback_speed : float = 10.0, auto_save_expressions : bool = False):
        """
        A collection of expressions used together. These animations are 
        called "expressions" and consist of a name and associated spritesheet.

        For example, one might have an expression "idle" and a spritesheet
        that contains the frames of an "idle" animation.

        Parameters
        -----------
        expressions : dict
            A dictionary of expressions. This dictionary should have the following structure:
            - Keys should be the names of the expressions
            - Values should be the spritesheet of the expression

        current_expression : str
            The name of the expression that should start as active. If this expression cannot
            be found in the supplied dictionary or is left as None, an arbitrary expression
            will be chosen instead.

        current_playback_speed : float
            The speed at which the current spritesheet animation should be shown
            in frames per second. Negative values will play the animation backwards.
        """
        self._expressions = expressions
        self.json_expressions_dict = {}
        self._current_expression = None
        self._current_playback_speed = current_playback_speed
        self._current_frame = 0.0
        self.restartOnNextUpdate = True

        self.auto_save_expressions = auto_save_expressions

        set_arbitrary_starting_expression = len(expressions) > 0

        if current_expression is not None:
            try:
                expressions[current_expression]
                self._current_expression = current_expression
                set_arbitrary_starting_expression = False
            except KeyError as e:
                pass

        if set_arbitrary_starting_expression:
            # Get an arbitrary element from the dictionary to set as the current expression
            self._current_expression = next(iter(expressions.keys()))

        self._prev_update_time = time.time()

    def add_or_update_expression(self, expression_name : str, 
                                 expression_spritesheet : Spritesheet):
        """
        Adds an expression to this avatar. If an expression with the supplied 
        name already exists, updates that expression to use the supplied
        spritesheet.

        Parameters
        -----------
        expression_name : str
            The name of the expression to be added/updated.

        expression_spritesheet : Image
            The spritesheet of the expression to be added/updated.

        expression_playback_speed : float
            The speed at which the spritesheet animation should be shown
            in frames per second. Negative values will play the animation
            backwards.
        """
        print("avatar/add_or_update_expression")
        self._expressions[expression_name] = expression_spritesheet
        self.json_expressions_dict[expression_name] = {
            "frame_width" : expression_spritesheet._frame_width,
            "frame_height" : expression_spritesheet._frame_height,
            "frame_count" : expression_spritesheet._frame_count,
            "sheet_src" : expression_spritesheet._image_src
        }
        if self.auto_save_expressions:
            self.save_expressions_json("expressions.json")
        print("exit avatar/add_or_update_expression")

    def load_expressions_json(self, json_src : str, img_parent_dir : str = ""):
        """
        """
        print("avatar/load_expression_json")
        temp_dict = {}
        try:
            with open(json_src, "r") as read_file:
                temp_dict = json.load(read_file)
                print(temp_dict.keys())
                for key in temp_dict.keys():
                    print(key)
                    sheet = Spritesheet(src=img_parent_dir + temp_dict[key]["sheet_src"],
                                frame_width=temp_dict[key]["frame_width"],
                                frame_height=temp_dict[key]["frame_height"],
                                frame_count=temp_dict[key]["frame_count"])
                    # self.add_or_update_expression(key, sheet)
                print("exited forloop")
            print("exited with")
            return True
        except Exception as e:
            print(e)
            return False
        
        

    def save_expressions_json(self, path : str):
        """
        """
        try:
            with open(path, "w") as write_file:
                json.dump(self.json_expressions_dict, write_file, indent=2)
            return True
        except Exception as e:
            print(e)
            return False



    def get_expression(self, expression_name : str):
        """
        Returns the spritesheet and playback speed associated with the 
        supplied expression name. Returns "None" if no expression with 
        the supplied name exists.
        
        Parameters
        -----------
        expression_name : str
            The name of the expression.
        """
        try:
            return self._expressions[expression_name]
        except KeyError as e:
            return None
        
    def set_current_expression(self, expression_name : str):
        """
        Sets the avatar's current expression to the specified expression, 
        if an expression with the specified name has been added to the avatar.
        If no such expression exists, the current expression will not be changed.

        Parameters
        -----------------
        expression_name : str
            The name of the expression which will be set as the current expression.

        Returns
        -----------------
        Whether or not the expression was able to be set. If `True`, the current 
        expression was set to the expression with the specified name. If `False`, 
        the current expression was not changed.
        """
        
        if expression_name == self._current_expression:
            return True
        if expression_name is None or \
            expression_name == "" or \
            expression_name == "none":
            self.clear_current_expression()
            return True
        try:
            self._expressions[expression_name]
            self._current_expression = expression_name
            self._current_frame = 0
            return True
        except KeyError as e:
            return False

    def clear_current_expression(self):
        """
        Sets the avatar's current expression to None.
        """
        self._current_expression = None  

    def set_playback_speed(self, new_speed : float):
        """
        Sets the avatar's playback speed to the specified value. 
        """
        self._current_playback_speed = new_speed


    def update(self):
        """
        Updates the current frame being displayed by the avatar based on the 
        time change since the previous update.
        """ 

        if self._current_expression is None:
            return

        # Get current time
        current_time = time.time()

        if self.restartOnNextUpdate:
            self._current_frame = 0.0
            self.restartOnNextUpdate = False
        else:
            # Compute time difference from last update
            delta_t = current_time - self._prev_update_time

             # Update current frame
            self._current_frame += delta_t * self._current_playback_speed

        # Update value of previous update timestamp
        self._prev_update_time = current_time
        
        # Get current expression spritesheet 
        # TODO: Handle 'None' case
        current_expression = self._expressions[self._current_expression]

        while self._current_frame >= current_expression._frame_count:
            self._current_frame -= current_expression._frame_count

        while self._current_frame < 0:
            self._current_frame += current_expression._frame_count

    def get_current_display(self):
        """
        Returns the active animation frame (should typically be called after 
        calling `update()`).

        Returns
        ---------------
        The active animation frame of the current expression's spritesheet. 
        See Spritesheet.get_frame() for the return type.
        """
        if self._current_expression == None:
            return None

        return self._expressions[self._current_expression].get_frame(self._current_frame)   

    def get_current_frame_count(self):
        """
        Returns the active animation's total frame count.
        """
        return self._expressions[self._current_expression]._frame_count 

    def get_expression_names(self):
        """
        Returns a list of the names of all expressions current available
        on this avatar.
        """
        return list(self._expressions.keys()) 

