/*
  JSON configurations for custom blocks.

  Current custom blocks:
  - move
  - turn
  - set wheel power
  - wait
*/

var miniblocks = {
  do_while: {
    message0: "do %1",
    args0: [
      {
        type: "input_statement",
        name: "do_statement",
      }
    ],
    message1: "repeat %1 %2",
    args1: [
      {
        type: "field_dropdown",
        name: "while_or_until",
        options: [
          ["while", "while"],
          ["until", "until"]
        ]
      },
      {
        type: "input_value",
        name: "condition",
        check: "Boolean"
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 100,
    tooltip: "",
    helpUrl: ""
  },
  // MOVE
  move: {
    type: "move",
    message0: "move %1 with %2 %% power",
    args0: [
      {
        type: "field_dropdown",
        name: "direction",
        options: [["forward", "fwd"], ["backwards", "bkw"]]
      },
      {
        type: "field_number",
        name: "speed",
        value: 50,
        min: 0,
        max: 100
      }
    ],
    output: "Boolean",
    colour: 230,
    tooltip: "",
    helpUrl: ""
  },

  // TURN
  turn: {
    type: "turn",
    message0: "turn %1 with %2 %% power",
    args0: [
      {
        type: "field_dropdown",
        name: "direction",
        options: [
          ["counterclockwise", "turn_counter_clockwise"],
          ["clockwise", "turn_clockwise"]
        ]
      },
      {
        type: "field_number",
        name: "power",
        value: 50,
        min: 0,
        max: 100
      }
    ],
    output: null,
    colour: 230,
    tooltip: "",
    helpUrl: ""
  },

  // SET WHEELPOWER
  setwheelpower: {
    type: "setwheelpower",
    message0:
      "set wheelpower %1 front left (%%) %2 front right (%%) %3 back left (%%) %4 back right (%%) %5",
    args0: [
      {
        type: "input_dummy",
        align: "CENTRE"
      },
      {
        type: "input_value",
        name: "FL",
        check: "Number",
        align: "RIGHT"
      },
      {
        type: "input_value",
        name: "FR",
        check: "Number",
        align: "RIGHT"
      },
      {
        type: "input_value",
        name: "BL",
        check: "Number",
        align: "RIGHT"
      },
      {
        type: "input_value",
        name: "BR",
        check: "Number",
        align: "RIGHT"
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 230,
    tooltip: "",
    helpUrl: ""
  },

  wait: {
    type: "wait",
    message0: "wait for %1 seconds",
    args0: [
      {
        type: "input_value",
        name: "time",
        check: "Number"
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 230,
    tooltip: "",
    helpUrl: ""
  },

  minibot_color: {
    type: "minibot_color",
    message0: "color sensed is %1",
    args0: [
      {
        type: "field_dropdown",
        name: "hue",
        options: [
          ["red", "RED"],
          ["blue", "BLUE"],
          ["green", "GREEN"],
          ["yellow", "YELLOW"],
          ["violet", "VIOLET"],
          ["white", "WHITE"]
        ]
      }
    ],
    inputsInline: false,
    output: "Boolean",
    colour: 230,
    tooltip: "",
    helpUrl: ""
  },

  //* NEW BLOCK TEST *//

  move_power: {
    type: "move_power",
    message0: "move %1 at %2 %% power",
    args0: [
      {
        type: "field_dropdown",
        name: "direction",
        options: [["forwards", "fwd"], ["backwards", "bk"]]
      },
      {
        type: "field_number",
        name: "speed",
        value: 100,
        min: 0,
        max: 100
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 230,
    tooltip: "",
    helpUrl: ""
  },
  move_power_time: {
    type: "move_power_time",
    message0: "move %1 with %2 %% power for %3 seconds",
    args0: [
      {
        type: "field_dropdown",
        name: "direction",
        options: [["forwards", "fwd"], ["backwards", "bk"]]
      },
      {
        type: "field_number",
        name: "speed",
        value: 100,
        min: 0,
        max: 100
      },
      {
        type: "field_number",
        name: "seconds",
        value: 0,
        min: 0
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 230,
    tooltip: "",
    helpUrl: ""
  },
  move_distance: {
    type: "move_distance",
    message0: "move %1 %2 inches",
    args0: [
      {
        type: "field_dropdown",
        name: "direction",
        options: [["forwards", "fwd_dst"], ["backwards", "bk_dst"]]
      },
      {
        type: "field_number",
        name: "inches",
        value: 0
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 230,
    tooltip: "",
    helpUrl: ""
  },
  move_to_position: {
    type: "move_to_position",
    message0: "move to (%1 inches,%2 inches)",
    args0: [
      {
        type: "field_number",
        name: "x_inches",
        value: 0
      },
      {
        type: "field_number",
        name: "y_inches",
        value: 0
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 230,
    tooltip: "",
    helpUrl: ""
  },
  path_plan_to_position: {
    type: "path_plan_to_position",
    message0: "path plan to (%1 inches,%2 inches)",
    args0: [
      {
        type: "field_number",
        name: "x_inches",
        value: 0
      },
      {
        type: "field_number",
        name: "y_inches",
        value: 0
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 230,
    tooltip: "",
    helpUrl: ""
  },
  stop_moving: {
    type: "stop_moving",
    message0: "stop moving",
    previousStatement: null,
    nextStatement: null,
    colour: 230,
    tooltip: "",
    helpUrl: ""
  },

  set_power: {
    type: "set_power",
    message0: "set left motor to %1 %% power %2 set right motor to %3 %% power",
    args0: [
      {
        type: "field_number",
        name: "left_speed",
        value: 100,
        min: 0,
        max: 100
      },
      {
        type: "input_dummy"
      },
      {
        type: "field_number",
        name: "right_speed",
        value: 100,
        min: 0,
        max: 100
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 230,
    tooltip: "",
    helpUrl: ""
  },
  turn_power: {
    type: "turn_power",
    message0: "turn %1 with %2 %% power",
    args0: [
      {
        type: "field_dropdown",
        name: "direction",
        options: [
          ["right", "turn_clockwise"],
          ["left", "turn_counter_clockwise"]
        ]
      },
      {
        type: "field_number",
        name: "percent",
        value: 100,
        min: 0,
        max: 100
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 230,
    tooltip: "",
    helpUrl: ""
  },
  turn_power_time: {
    type: "turn_power_time",
    message0: "turn %1 with %2 %% power for %3 seconds",
    args0: [
      {
        type: "field_dropdown",
        name: "direction",
        options: [
          ["right", "turn_clockwise"],
          ["left", "turn_counter_clockwise"]
        ]
      },
      {
        type: "field_number",
        name: "percent",
        value: 100,
        min: 0,
        max: 100
      },
      {
        type: "field_number",
        name: "seconds",
        value: 0,
        min: 0
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 230,
    tooltip: "",
    helpUrl: ""
  },
  turn_angle: {
    type: "turn_angle",
    message0: "turn %1 %2 degrees",
    args0: [
      {
        type: "field_dropdown",
        name: "direction",
        options: [
          ["right", "turn_clockwise_angle"],
          ["left", "turn_counter_clockwise_angle"]
        ]
      },
      {
        type: "field_number",
        name: "degrees",
        value: 0
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 230,
    tooltip: "",
    helpUrl: ""
  },
  turn_to_angle: {
    type: "turn_to_angle",
    message0: "turn to %1 degrees",
    args0: [
      {
        type: "field_number",
        name: "angle_degrees",
        value: 0
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 230,
    tooltip: "",
    helpUrl: ""
  },
  move_servo: {
    type: "move_servo",
    message0: "move servo to %1 angle",
    args0: [
      {
        type: "field_number",
        name: "angle",
        value: 0,
        min: 0,
        max: 200
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 230,
    tooltip: "",
    helpUrl: ""
  },

  wait_seconds: {
    type: "wait_seconds",
    message0: "wait %1 seconds",
    args0: [
      {
        type: "field_number",
        name: "seconds",
        value: 0,
        min: 0
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 230,
    tooltip: "",
    helpUrl: ""
  },
  send_commands: {
    type: "send_commands",
    message0: "send commands to %1 %2 do %3",
    args0: [
      {
        type: "field_dropdown",
        name: "bot_name",
        options: [["bot1", "bot1"], ["bot2", "bot2"], ["bot3", "bot3"]]
      },
      {
        type: "input_dummy"
      },
      {
        type: "input_statement",
        name: "send_commands"
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 150,
    tooltip: "",
    helpUrl: ""
  },

  wait_for_commands: {
    type: "wait_for_commands",
    message0: "wait for commands from %1",
    args0: [
      {
        type: "field_dropdown",
        name: "bot_name",
        options: [["bot1", "bot1"], ["bot2", "bot2"], ["bot3", "bot3"]]
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 150,
    tooltip: "",
    helpUrl: ""
  },
  while_wait_for_commands: {
    type: "while_wait_for_commands",
    message0: "while waiting for commands from %1 %2 do %3",
    args0: [
      {
        type: "field_dropdown",
        name: "bot_name",
        options: [["bot1", "bot1"], ["bot2", "bot2"], ["bot3", "bot3"]]
      },
      {
        type: "input_dummy"
      },
      {
        type: "input_statement",
        name: "wait_commands"
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 150,
    tooltip: "",
    helpUrl: ""
  },

  read_ultrasonic: {
    type: "read_ultrasonic",
    message0: "ultrasonic sensor detects object within %1",
    args0: [
      {
        type: "field_number",
        name: "input",
        value: 1,
        min: 1
      }
    ],
    output: "Boolean",
    colour: 180,
    tooltip: "",
    helpUrl: ""
  },

  sees_color: {
    type: "sees_color",
    message0: "color sensor %1 sees %2",
    args0: [
      {
        type: "field_dropdown",
        name: "sensor_name",
        options: [
          ["color1", "color1"],
          ["color2", "color2"],
          ["color3", "color3"]
        ]
      },
      {
        type: "field_dropdown",
        name: "color_name",
        options: [
          ["red", "red"],
          ["blue", "blue"],
          ["green", "green"],
          ["yellow", "yellow"],
          ["violet", "violet"],
          ["white", "white"]
        ]
      }
    ],
    output: "Boolean",
    colour: 180,
    tooltip: "",
    helpUrl: ""
  },

  create_emotion: {
    type: "create_emotion",
    message0: "Create Emotion named %1 %2\n which does %3",
    args0: [
      {
        type: "input_value",
        name: "emotion_name",
        check: "String",
      },
      {
        type: "input_dummy"
      },
      {
        type: "input_statement",
        name: "emotion_action_steps"
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 30,
    tooltip: "Creates an Emotion which then can be added to a robot.",
    helpUrl: ""
  },

  add_emotion: {
    type: "add_emotion",
    message0: "Add Emotion named %1\nwith priority %2",
    args0: [
      {
        type: "input_value",
        name: "emotion_name",
        check: "String",
      },
      {
        type: "input_value",
        name: "emotion_priority",
        check: "Number",
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 30,
    tooltip: "Adds an Emotion to the robot with the specified priority.",
    helpUrl: ""
  },

  add_required_device: {
    type: "add_required_device",
    message0: "Add required device %1 to emotion %2",
    args0: [
      {
        type: "field_dropdown",
        name: "device_name",
        options: [
          ["wheels", "wheels"],
          ["screen", "display"],
          ["speaker", "speaker"]
        ]
      },
      {
        type: "input_value",
        name: "emotion_name",
        check: "String",
      },
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 20,
    tooltip: "Adds a required device to an emotion (used to determine whether an emotion is available to be run).",
    helpUrl: ""
  },

  set_device_emotion_status: {
    type: "set_device_emotion_status",
    message0: "Set whether device %1 %2\nis available for emotions to %3",
    args0: [
      {
        type: "field_dropdown",
        name: "device_name",
        options: [
          ["wheels", "wheels"],
          ["screen", "display"],
          ["speaker", "speaker"]
        ]
      },
      {
        type: "input_dummy"
      },
      {
        type: "input_value",
        name: "device_status",
        check: "Boolean",
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 20,
    tooltip: "Specifies whether a device should or should not be used by emotions.",
    helpUrl: ""
  },

  set_emotion_if_possible: {
    type: "set_emotion_if_possible",
    message0: "Try to set emotion to %1",
    args0: [
      {
        type: "input_value",
        name: "emotion_name",
        check: "String",
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 30,
    tooltip: "Sets the robot's emotion to the emotion with the specified name if:\n" + 
              "1) the emotion has been added to the robot, and\n" + 
              "2) the emotion is higher priority than the currently running emotion.\n" + 
              "Note: Use clear emotion first in order to change to a lower priority emotion.",
    helpUrl: ""
  },

  clear_current_emotion: {
    type: "clear_current_emotion",
    message0: "Clear current emotion",
    previousStatement: null,
    nextStatement: null,
    colour: 30,
    tooltip: "Clears the robots current emotion.",
    helpUrl: ""
  },

  process_current_emotion: {
    type: "process_current_emotion",
    message0: "Try to Emote",
    previousStatement: null,
    nextStatement: null,
    colour: 30,
    tooltip: "Runs the code associated with the current emotion, if all required devices are available.",
    helpUrl: ""
  },

  set_current_expression: {
    type: "set_current_expression",
    message0: "Set current expression to %1",
    args0: [
      {
        type: "input_value",
        name: "expression_name",
        check: "String",
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 60,
    tooltip: "Sets the current expression to one with the specified name, if one exists.",
    helpUrl: ""
  },

  clear_current_expression: {
    type: "clear_current_expression",
    message0: "Clear current expression",
    previousStatement: null,
    nextStatement: null,
    colour: 60,
    tooltip: "Clears the current expression, if one is active.",
    helpUrl: ""
  },

  set_current_playback_speed: {
    type: "set_current_playback_speed",
    message0: "Set current playback speed to %1",
    args0: [
      {
        type: "input_value",
        name: "new_speed",
        check: "Number",
      }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 60,
    tooltip: "Sets the current playback speed in frames per second to the specified value.\n" + 
             "Note: Negative values will play the animation backwards.",
    helpUrl: ""
  },
  get_accel_x: {
    type: "get_accel_x",
    message0: "Get accelerometer values in x direction",
    previousStatement: null,
    nextStatement: null,
    colour: 60,
    tooltip: "Get accelerometer values in x direction",
    helpUrl: "",
    output: "Number",
  },
  get_accel_y: {
    type: "get_accel_y",
    message0: "Get accelerometer values in y direction",
    previousStatement: null,
    nextStatement: null,
    colour: 60,
    tooltip: "Get accelerometer values in y direction",
    helpUrl: "",
    output: "Number",
  }, 
  get_accel_z: {
    type: "get_accel_z",
    message0: "Get accelerometer values in z direction",
    previousStatement: null,
    nextStatement: null,
    colour: 60,
    tooltip: "Get accelerometer values in z direction",
    helpUrl: "",
    output: "Number",
  }
};
