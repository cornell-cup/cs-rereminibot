from spritesheet import Spritesheet
import time

class Avatar:

    def __init__(self, expressions : dict = {}, current_expression : str = None, current_playback_speed : float = 10.0):
        """
        An collection of expressions used together. These animations are 
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
        
        self._current_expression = None
        self._current_playback_speed = current_playback_speed
        self._current_frame = 0.0

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

        self._expressions[expression_name] = expression_spritesheet

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
        
        try:
            self._expressions[expression_name]
            self._current_expression = expression_name
            self._current_frame = 0
            return True
        except KeyError as e:
            return False

    def update(self):
        """
        Updates the current frame being displayed by the avatar based on the 
        time change since the previous update.
        """ 

        # Get current time
        current_time = time.time()

        # Compute time difference from last update
        delta_t = current_time - self._prev_update_time
        
        # Get current expression spritesheet
        current_expression = self._expressions[self._current_expression]

        # Update current frame
        self._current_frame += delta_t * self._current_playback_speed

        while self._current_frame >= current_expression._frame_count:
            self._current_frame -= current_expression._frame_count

        while self._current_frame < 0:
            self._current_frame += current_expression._frame_count

        # Update value of previous update timestamp
        self._prev_update_time = current_time

    def get_current_display(self):
        """
        Returns the active animation frame (should typically be called after 
        calling `update()`).

        Returns
        ---------------
        The active animation frame of the current expression's spritesheet. 
        See Spritesheet.get_frame() for the return type.
        """
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

