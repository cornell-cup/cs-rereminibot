from spritesheet import Spritesheet
import time
import json
import traceback

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
        self._current_expression_s = None
        self._current_playback_speed = current_playback_speed
        self._current_frame = 0.0
        self.restartOnNextUpdate = True
        self.auto_save_expressions = auto_save_expressions
        
        # Animation tracking attributes
        self._animation_complete = False
        self._expression_start_time = time.time()
        self._last_expression = None
        self._frame_count = 0

        # Set initial expression if provided
        if current_expression is not None and current_expression in expressions:
            self._current_expression = current_expression
        elif len(expressions) > 0:
            # Get an arbitrary element as default
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

        expression_spritesheet : Spritesheet
            The spritesheet of the expression to be added/updated.
        """
        print(f"Adding/updating expression: {expression_name}")
        self._expressions[expression_name] = expression_spritesheet
        self.json_expressions_dict[expression_name] = {
            "frame_width": expression_spritesheet._frame_width,
            "frame_height": expression_spritesheet._frame_height,
            "frame_count": expression_spritesheet._frame_count,
            "sheet_src": expression_spritesheet._image_src
        }
        
        # Auto-save if enabled
        if self.auto_save_expressions:
            self.save_expressions_json("expressions.json")
        
        # If this is the first expression, set it as current
        if self._current_expression is None:
            self._current_expression = expression_name
            self._current_frame = 0.0
            self.restartOnNextUpdate = True
            self._animation_complete = False
            self._expression_start_time = time.time()
            self._last_expression = expression_name
            self._frame_count = 0

    def load_single_expression_json(self, json_src : str, key : str, img_parent_dir : str = ""):
        """
        Load a single expression from a JSON file and set it as the current expression.
        
        Parameters
        -----------
        json_src : str
            Path to the JSON file containing expression definitions
            
        key : str
            The name/key of the expression to load
            
        img_parent_dir : str
            Parent directory for image paths in the JSON
        """
        print(f"Loading expression '{key}' from {json_src}")
        try:
            with open(json_src, "r") as read_file:
                temp_dict = json.load(read_file)
                
                if key not in temp_dict:
                    print(f"Expression '{key}' not found in {json_src}")
                    return False
                
                # Create spritesheet from JSON data
                sheet = Spritesheet(
                    src=img_parent_dir + temp_dict[key]["sheet_src"],
                    frame_width=temp_dict[key]["frame_width"],
                    frame_height=temp_dict[key]["frame_height"],
                    frame_count=temp_dict[key]["frame_count"]
                )
                
                # Check if spritesheet loaded correctly
                if not sheet._loaded_correctly:
                    print(f"Failed to load spritesheet for '{key}'")
                    return False
                
                # Add expression to avatar and set as current
                self.add_or_update_expression(key, sheet)
                self._current_expression = key
                self._current_frame = 0.0
                self.restartOnNextUpdate = True
                self._animation_complete = False
                self._expression_start_time = time.time()
                self._last_expression = key
                self._frame_count = 0
                
                print(f"Successfully loaded expression '{key}'")
                return True
                
        except Exception as e:
            print(f"Error loading expression '{key}': {e}")
            traceback.print_exc()
            return False

    def load_expressions_json(self, json_src : str, img_parent_dir : str = ""):
        """
        Load multiple expressions from a JSON file.
        
        Parameters
        -----------
        json_src : str
            Path to the JSON file containing expression definitions
            
        img_parent_dir : str
            Parent directory for image paths in the JSON
        """
        print(f"Loading expressions from {json_src}")
        try:
            with open(json_src, "r") as read_file:
                temp_dict = json.load(read_file)
                loaded_count = 0
                
                for key in temp_dict.keys():
                    try:
                        # Create spritesheet from JSON data
                        sheet = Spritesheet(
                            src=img_parent_dir + temp_dict[key]["sheet_src"],
                            frame_width=temp_dict[key]["frame_width"],
                            frame_height=temp_dict[key]["frame_height"],
                            frame_count=temp_dict[key]["frame_count"]
                        )
                        
                        # Add expression to avatar
                        if sheet._loaded_correctly:
                            self.add_or_update_expression(key, sheet)
                            loaded_count += 1
                        else:
                            print(f"Failed to load spritesheet for '{key}'")
                    
                    except Exception as e:
                        print(f"Error loading expression '{key}': {e}")
                
                print(f"Successfully loaded {loaded_count} expressions")
                return loaded_count > 0
                
        except Exception as e:
            print(f"Error loading expressions: {e}")
            return False

    def save_expressions_json(self, path : str):
        """
        Save the current expressions to a JSON file.
        
        Parameters
        -----------
        path : str
            Path where to save the JSON file
        """
        try:
            with open(path, "w") as write_file:
                json.dump(self.json_expressions_dict, write_file, indent=2)
            return True
        except Exception as e:
            print(f"Error saving expressions to {path}: {e}")
            return False

    def get_expression(self, expression_name : str):
        """
        Returns the spritesheet associated with the supplied expression name.
        Returns "None" if no expression with the supplied name exists.
        
        Parameters
        -----------
        expression_name : str
            The name of the expression.
        """
        try:
            return self._expressions[expression_name]
        except KeyError:
            return None
        
    def get_expression_names(self):
        """
        Returns a list of all available expression names.
        """
        return list(self._expressions.keys())
        
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
        # Check if this is the already active expression
        if expression_name == self._current_expression:
            return True
            
        # Handle None/empty expression
        if expression_name is None or expression_name == "" or expression_name == "none":
            self.clear_current_expression()
            return True
            
        # Check if expression exists
        if expression_name in self._expressions:
            self._current_expression = expression_name
            self._current_frame = 0.0
            self.restartOnNextUpdate = True
            self._animation_complete = False
            self._expression_start_time = time.time()
            self._last_expression = expression_name
            self._frame_count = 0
            return True
        else:
            print(f"Expression '{expression_name}' not found in avatar")
            return False

    def clear_current_expression(self):
        """
        Sets the avatar's current expression to None.
        """
        self._current_expression = None
        self._current_frame = 0.0
        self._animation_complete = True
        self._last_expression = None

    def set_playback_speed(self, new_speed : float):
        """
        Sets the avatar's playback speed to the specified value. 
        """
        self._current_playback_speed = new_speed

    def is_animation_complete(self):
        """
        Returns True if the current expression's animation has completed at least one full cycle.
        """
        if self._current_expression is None:
            return True
            
        if self._animation_complete:
            return True
            
        return False
        
    def get_current_display(self):
        """
        Returns the current frame to be displayed based on the current expression and frame.
        """
        if self._current_expression is None or self._current_expression not in self._expressions:
            return None
            
        current_expression = self._expressions[self._current_expression]
        frame_count = current_expression._frame_count
        
        # Calculate the current frame index
        frame_index = int(self._current_frame) % frame_count
        
        # Get the frame from the spritesheet
        return current_expression.get_frame(frame_index)

    def update(self):
        """
        Updates the current frame being displayed by the avatar based on the 
        time change since the previous update.
        """ 
        # Nothing to update if no expression is set
        if self._current_expression is None:
            return

        # Track expression changes
        if self._last_expression != self._current_expression:
            self._last_expression = self._current_expression
            self._animation_complete = False
            self._frame_count = 0
            self._expression_start_time = time.time()

        # Get current time for delta calculation
        current_time = time.time()

        # Store previous frame for completion detection
        prev_frame = int(self._current_frame) if not self.restartOnNextUpdate else 0

        # Reset frame counter if needed
        if self.restartOnNextUpdate:
            self._current_frame = 0.0
            self.restartOnNextUpdate = False
        else:
            # Calculate time since last update
            delta_t = current_time - self._prev_update_time
            
            # Update current frame position based on playback speed
            self._current_frame += delta_t * self._current_playback_speed

        # Update timestamp for next frame calculation
        self._prev_update_time = current_time
        
        # Handle frame wrapping
        if self._current_expression in self._expressions:
            # Get current expression's spritesheet
            current_expression = self._expressions[self._current_expression]
            
            # Ensure frame index stays within valid range
            frame_count = current_expression._frame_count
            
            # Detect animation completion
            current_frame = int(self._current_frame) % frame_count
            if prev_frame > current_frame:  # We wrapped around
                self._frame_count += 1
                if self._frame_count >= 1:  # One full cycle completed
                    self._animation_complete = True
                    
            # Ensure frame stays within bounds
            while self._current_frame >= frame_count:
                self._current_frame -= frame_count
                
            while self._current_frame < 0:
                self._current_frame += frame_count
