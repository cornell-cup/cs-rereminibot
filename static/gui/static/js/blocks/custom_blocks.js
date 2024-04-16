/*
  Code generators for custom blocks.
*/
var BOT_HEADER = "bot.";
var FCN_ENDING = "\n";

/**
 * Generate a wait command, including its stop function
 * @param time The time (in seconds)to wait for
 */
function generateWait(time) {
  return BOT_HEADER + "wait(" + time + ")" + FCN_ENDING + BOT_HEADER + "stop()" + FCN_ENDING
}

// ================ DO WHILE BLOCK ================ //

Blockly.Blocks['do_while'] = {
  init: function () {
    this.jsonInit(miniblocks.do_while);
  }
};

Blockly.Python['do_while'] = function (block) {
  var do_statement = Blockly.Python.statementToCode(block, 'do_statement');
  var negation = (block.getFieldValue('while_or_until') == 'until') ? '' : '!';
  var condition = Blockly.Python.valueToCode(block, 'condition', Blockly.Python.ORDER_NONE);
  var do_statement = Blockly.Python.addLoopTrap(do_statement, block.id);

  return 'while True:\n' + do_statement + '  break if ' + negation + '(' + condition + ')\n';
};

// ================ MOVE BLOCK ================ //
Blockly.Blocks['move'] = {
  init: function () {
    this.jsonInit(miniblocks.move);
  }
};

Blockly.Python['move'] = function (block) {
  // from blockly
  var dropdown_direction = block.getFieldValue('direction');
  var number_speed = block.getFieldValue('speed');

  //string representation of function
  var fcn = {
    fwd: "move_forward(",
    bkw: "move_backward("
  }[dropdown_direction];
  return [fcn + number_speed + ")", Blockly.Python.ORDER_NONE];
};

// ================ TURN BLOCK ================ //
Blockly.Blocks['turn'] = {
  init: function () {
    this.jsonInit(miniblocks.turn);
  }
};

Blockly.Python['turn'] = function (block) {
  var dropdown_direction = block.getFieldValue('direction');
  var number_power = block.getFieldValue('power');
  var code = dropdown_direction + "(" + number_power + ")";
  return [code, Blockly.Python.ORDER_NONE];
};

// ================ SET WHEELPOWER BLOCK ================ //
Blockly.Blocks['setwheelpower'] = {
  init: function () {
    this.jsonInit(miniblocks.setwheelpower);
  }
};
Blockly.Python['setwheelpower'] = function (block) {
  var wheels = ['FL', 'FR', 'BL', 'BR']
  var power = [0, 0, 0, 0];

  // dealing with wrong inputs
  for (var i = 0; i < 4; i++) {
    power[i] = Blockly.Python.valueToCode(block, wheels[i], Blockly.Python.ORDER_ATOMIC) || 0;
    if (power[i] < 100) {
    }
    else if (power[i] > 100) {
      alert("Oops! Please insert a number between 0 and 100.");
      power[i] = 100;
    }
    else {
      alert("Oops! Please insert a number between 0 and 100.");
      power[i] = 0;
    }
  }
  var code = 'set_wheel_power('
    + power[0] + ','
    + power[1] + ','
    + power[2] + ','
    + power[3] + ')';
  return [code, Blockly.Python.ORDER_NONE];
};

// ================== WAIT BLOCK ================== //
Blockly.Blocks['wait'] = {
  init: function () {
    this.jsonInit(miniblocks.wait);
  }
};
Blockly.Python['wait'] = function (block) {
  var time = Blockly.Python.valueToCode(block, 'time', Blockly.Python.ORDER_ATOMIC) || 0;
  var code = generateWait(time)
  return [code, Blockly.Python.ORDER_NONE];
};

// ================== COLOR SENSOR BLOCK ================== //
Blockly.Blocks['minibot_color'] = {
  init: function () {
    this.jsonInit(miniblocks.minibot_color);
  }
};

Blockly.Python['minibot_color'] = function (block) {
  var dropdown_hue = block.getFieldValue('hue');
  var code = 'colorSensed = ' + dropdown_hue;
  return [code, Blockly.Python.ORDER_NONE];
};

/////////////////////////////////* NEW BLOCK TEST *//////////////////////////

// ================ MOVE BLOCKS ================ //

Blockly.Blocks['move_power'] = {
  init: function () {
    this.jsonInit(miniblocks.move_power);
  }
};

Blockly.Python['move_power'] = function (block) {
  var dropdown_direction = block.getFieldValue('direction');
  var number_speed = block.getFieldValue('speed');

  var fcn = {
    fwd: "move_forward(",
    bk: "move_backward("
  }[dropdown_direction];
  return BOT_HEADER + fcn + number_speed + ")" + FCN_ENDING;
};

Blockly.Blocks['move_power_time'] = {
  init: function () {
    this.jsonInit(miniblocks.move_power_time);
  }
};

Blockly.Python['move_power_time'] = function (block) {
  var dropdown_direction = block.getFieldValue('direction');
  var number_speed = block.getFieldValue('speed');
  var number_seconds = block.getFieldValue('seconds');

  var fcn = {
    fwd: "move_forward(",
    bk: "move_backward("
  }[dropdown_direction];

  return BOT_HEADER + fcn + number_speed + ")\n" + generateWait(number_seconds);
};


Blockly.Blocks['move_distance'] = {
  init: function () {
    this.jsonInit(miniblocks.move_distance);
  }
};

Blockly.Python['move_distance'] = function (block) {
  var dropdown_direction = block.getFieldValue('direction');
  var number_inches = block.getFieldValue('inches');

  var fcn = {
    fwd_dst: "move_forward_distance(",
    bk_dst: "move_backward_distance("
  }[dropdown_direction];

  return BOT_HEADER + fcn + number_inches + ")\n";
};

Blockly.Blocks['move_to_position'] = {
  init: function () {
    this.jsonInit(miniblocks.move_to_position);
  }
};

Blockly.Python['move_to_position'] = function (block) {
  var x_inches = block.getFieldValue('x_inches');
  var y_inches = block.getFieldValue('y_inches');

  var fcn = "move_to("

  return BOT_HEADER + fcn + x_inches + "," + y_inches + ")\n";
};

Blockly.Blocks['path_plan_to_position'] = {
  init: function () {
    this.jsonInit(miniblocks.path_plan_to_position);
  }
};

Blockly.Python['path_plan_to_position'] = function (block) {
  var x_inches = block.getFieldValue('x_inches');
  var y_inches = block.getFieldValue('y_inches');

  var fcn = "path_plan_to("

  return BOT_HEADER + fcn + x_inches + "," + y_inches + ")\n";
};



Blockly.Blocks['stop_moving'] = {
  init: function () {
    this.jsonInit(miniblocks.stop_moving);
  }
};

Blockly.Python['stop_moving'] = function (block) {
  // TODO: Assemble Python into code variable.
  var code = 'stop()';
  return BOT_HEADER + code + FCN_ENDING;
};

Blockly.Blocks['set_power'] = {
  init: function () {
    this.jsonInit(miniblocks.set_power);
  }
};

Blockly.Python['set_power'] = function (block) {
  var number_left_speed = block.getFieldValue('left_speed');
  var number_right_speed = block.getFieldValue('right_speed');
  // TODO: Assemble Python into code variable.

  var code = 'set_wheel_power(' + number_left_speed + "," + number_right_speed + ")";
  return BOT_HEADER + code + FCN_ENDING;
};

// ================ TURN BLOCKS ================ //

Blockly.Blocks['turn_power'] = {
  init: function () {
    this.jsonInit(miniblocks.turn_power);
  }
};

Blockly.Python['turn_power'] = function (block) {
  var dropdown_direction = block.getFieldValue('direction');
  var number_percent = block.getFieldValue('percent');
  // TODO: Assemble Python into code variable.
  var fcn = {
    turn_clockwise: "turn_clockwise(",
    turn_counter_clockwise: "turn_counter_clockwise("
  }[dropdown_direction];

  return BOT_HEADER + fcn + number_percent + ")" + FCN_ENDING;
};

Blockly.Blocks['turn_power_time'] = {
  init: function () {
    this.jsonInit(miniblocks.turn_power_time);
  }
};

Blockly.Python['turn_power_time'] = function (block) {
  var dropdown_direction = block.getFieldValue('direction');
  var number_percent = block.getFieldValue('percent');
  var number_seconds = block.getFieldValue('seconds');

  var fcn = {
    turn_clockwise: "turn_clockwise(",
    turn_counter_clockwise: "turn_counter_clockwise("
  }[dropdown_direction];

  return BOT_HEADER + fcn + number_percent + ")\n" + generateWait(number_seconds);
};

Blockly.Blocks['turn_angle'] = {
  init: function () {
    this.jsonInit(miniblocks.turn_angle);
  }
};

Blockly.Python['turn_angle'] = function (block) {
  var dropdown_direction = block.getFieldValue('direction');
  var number_degrees = block.getFieldValue('degrees');

  var fcn = {
    turn_clockwise_angle: "turn_clockwise_angle(",
    turn_counter_clockwise_angle: "turn_counter_clockwise_angle("
  }[dropdown_direction];

  return BOT_HEADER + fcn + number_degrees + ")\n";
};

Blockly.Blocks['turn_to_angle'] = {
  init: function () {
    this.jsonInit(miniblocks.turn_to_angle);
  }
};

Blockly.Python['turn_to_angle'] = function (block) {
  var angle_degrees = block.getFieldValue('angle_degrees');

  var fcn = "turn_to("

  return BOT_HEADER + fcn + angle_degrees + ")\n";
};

// ================ WAIT BLOCK ================ //

Blockly.Blocks['wait_seconds'] = {
  init: function () {
    this.jsonInit(miniblocks.wait_seconds);
  }
};

Blockly.Python['wait_seconds'] = function (block) {
  var number_seconds = block.getFieldValue('seconds');
  return generateWait(number_seconds)
};

// ================ COMMUNICATION BLOCKS ================ //

Blockly.Blocks['send_commands'] = {
  init: function () {
    this.jsonInit(miniblocks.send_commands);
  }
};

Blockly.Python['send_commands'] = function (block) {
  var dropdown_bot_name = block.getFieldValue('bot_name');
  var statements_send_commands = Blockly.Python.statementToCode(block, 'send_commands');
  // TODO: Assemble Python into code variable.
  var code = 'pass #TODO Implement backend for send_commands';
  return code + FCN_ENDING;
};

Blockly.Blocks['wait_for_commands'] = {
  init: function () {
    this.jsonInit(miniblocks.wait_for_commands);
  }
};

Blockly.Python['wait_for_commands'] = function (block) {
  var dropdown_bot_name = block.getFieldValue('bot_name');
  // TODO: Assemble Python into code variable.
  var code = 'pass #TODO Implement backend for wait_for_commands';
  return code + FCN_ENDING;
};

Blockly.Blocks['while_wait_for_commands'] = {
  init: function () {
    this.jsonInit(miniblocks.while_wait_for_commands);
  }
};

Blockly.Python['while_wait_for_commands'] = function (block) {
  var dropdown_bot_name = block.getFieldValue('bot_name');
  var statements_wait_commands = Blockly.Python.statementToCode(block, 'wait_commands');
  // TODO: Assemble Python into code variable.
  var code = 'pass #TODO Implement backend for while_wait_for_commands';
  return code + FCN_ENDING;
};

// ================ SERVO BLOCKS ================ //

Blockly.Blocks['move_servo'] = {
  init: function () {
    this.jsonInit(miniblocks.move_servo);
  }
}

Blockly.Python['move_servo'] = function (block) {
  var angle = block.getFieldValue('angle');
  var funcCall = "move_servo(" + angle + ")";

  return BOT_HEADER + funcCall + FCN_ENDING;
}

// ================ ULTRASONIC BLOCKS ================ //

Blockly.Blocks['read_ultrasonic'] = {
  init: function () {
    this.jsonInit(miniblocks.read_ultrasonic)
  }
}

Blockly.Python['read_ultrasonic'] = function (block) {
  var lowerBound = "0 < ";
  var upperLimit = block.getFieldValue('input');
  var upperBound = " <= " + upperLimit;
  var funcName = "read_ultrasonic()";

  return [lowerBound + BOT_HEADER + funcName + upperBound, Blockly.Python.ORDER_NONE];
}

// ================ COLOR SENSING BLOCKS ================ //

Blockly.Blocks['sees_color'] = {
  init: function () {
    this.jsonInit(miniblocks.sees_color);
  }
};

Blockly.Python['sees_color'] = function (block) {
  var dropdown_sensor_name = block.getFieldValue('sensor_name');
  var dropdown_color_name = block.getFieldValue('color_name');
  var sensor_read = {
    color1: "color_sensor1",
    color2: "color_sensor2",
    color3: "color_sensor3"
  }[dropdown_sensor_name];

  //TODO Change to sensor getter function
  var sensor_code = 'sensors[' + sensor_read + '].get_color_name()';

  var color_check = {
    red: "\"RED\"",
    blue: "\"BLUE\"",
    green: "\"GREEN\"",
    yellow: "\"YELLOW\"",
    violet: "\"VIOLET\"",
    white: "\"WHITE\"",
  }[dropdown_color_name];

  var color_code = '==' + color_check;

  return [BOT_HEADER + sensor_code + color_code, Blockly.Python.ORDER_NONE];
};

// ============= EMOTIONAL SUBSYSTEM BLOCKS ============== //

Blockly.Blocks['create_emotion'] = {
  init: function () {
    this.jsonInit(miniblocks.create_emotion)
  }
};

Blockly.Python['create_emotion'] = function (block) {
  var emotion_name = Blockly.Python.valueToCode(block, 'emotion_name', Blockly.Python.ORDER_NONE);
  var emotion_action_steps = Blockly.Python.statementToCode(block, 'emotion_action_steps');

  // TODO: Assemble python into code variable.
  var processed_eas = 'def emotion_action_steps():\n';
  processed_eas += emotion_action_steps;
  processed_eas += '  \n';

  // TODO: Assemble python into code variable.
  var code = processed_eas;
  code += 'self.emotion_repo[' + emotion_name + '] = Emotion(' + emotion_name + ',';
  code += 'emotion_action_steps)\n';
  return code;
};

Blockly.Blocks['add_emotion'] = {
  init: function () {
    this.jsonInit(miniblocks.add_emotion)
  }
};

Blockly.Python['add_emotion'] = function (block) {
  var emotion_name = Blockly.Python.valueToCode(block, 'emotion_name', Blockly.Python.ORDER_NONE);
  var emotion_priority = Blockly.Python.valueToCode(block, 'emotion_priority', Blockly.Python.ORDER_NONE);

  // TODO: Assemble python into code variable.
  var code = 'added_emotions[' + emotion_name + '] = ' + emotion_priority + '\n';
  return code;
};

Blockly.Blocks['add_required_device'] = {
  init: function () {
    this.jsonInit(miniblocks.add_required_device)
  }
};

Blockly.Python['add_required_device'] = function (block) {
  var dropdown_device_name = block.getFieldValue('device_name');
  var emotion_name = Blockly.Python.valueToCode(block, 'emotion_name', Blockly.Python.ORDER_NONE);

  // TODO: Assemble python into code variable.
  var code = 'self.emotion_repo[' + emotion_name + '].add_required_device(\"' + dropdown_device_name + '\")\n';
  return code;
};

Blockly.Blocks['set_device_emotion_status'] = {
  init: function () {
    this.jsonInit(miniblocks.set_device_emotion_status)
  }
};

Blockly.Python['set_device_emotion_status'] = function (block) {
  var dropdown_device_name = block.getFieldValue('device_name');
  var device_status = Blockly.Python.valueToCode(block, 'device_status', Blockly.Python.ORDER_NONE);

  // TODO: Assemble python into code variable.
  var code = 'devices_emotional_status[\"' + dropdown_device_name + '\"] = ' + device_status + '\n';
  return code;
};

Blockly.Blocks['set_emotion_if_possible'] = {
  init: function () {
    this.jsonInit(miniblocks.set_emotion_if_possible)
  }
};

Blockly.Python['set_emotion_if_possible'] = function (block) {
  var emotion_name = Blockly.Python.valueToCode(block, 'emotion_name', Blockly.Python.ORDER_NONE);

  // TODO: Assemble python into code variable.
  var code = 'if ' + emotion_name + ' in added_emotions:\n';
     code += '    if current_emotion != None: \n';
     code += '        if added_emotions[' + emotion_name + '] > added_emotions[current_emotion]:\n';
     code += '            current_emotion = ' + emotion_name + '\n';
     code += '    else:\n';
     code += '        current_emotion = ' + emotion_name + '\n';
  return code;
};

Blockly.Blocks['clear_current_emotion'] = {
  init: function () {
    this.jsonInit(miniblocks.clear_current_emotion)
  }
};

Blockly.Python['clear_current_emotion'] = function (block) {
  // TODO: Assemble python into code variable.
  var code = 'current_emotion = None';
  return code;
};

Blockly.Blocks['process_current_emotion'] = {
  init: function () {
    this.jsonInit(miniblocks.process_current_emotion)
  }
};

Blockly.Python['process_current_emotion'] = function (block) {
  // TODO: Assemble python into code variable.
  var code = 'if current_emotion is not None and current_emotion in self.emotion_repo:\n';
     code += '    if self.emotion_repo[current_emotion].check_devices(devices_emotional_status):\n';
    //  code += '        bot.move_forward(100)\n'
    //  code += '        bot.wait(0.25)\n'
    //  code += '        bot.stop()\n'
    //  code += '        bot.wait(1)\n'
     code += '        self.emotion_repo[current_emotion].process_emotion()\n'; 
  // var code = "emotion_repo[current_emotion].process_emotion()\n"
  return code;
};

// ============= FACIAL ANIMATION BLOCKS ============== //

Blockly.Blocks['set_current_expression'] = {
  init: function () {
    this.jsonInit(miniblocks.set_current_expression)
  }
};

Blockly.Python['set_current_expression'] = function (block) {
  var expression_name = Blockly.Python.valueToCode(block, 'expression_name', Blockly.Python.ORDER_NONE);

  // TODO: Assemble python into code variable.
  var code = 'self.current_expression = ' + expression_name + '\n';
  code = code.replaceAll("\'", "\"");
  return code;
};

Blockly.Blocks['clear_current_expression'] = {
  init: function () {
    this.jsonInit(miniblocks.clear_current_expression)
  }
};

Blockly.Python['clear_current_expression'] = function (block) {

  // TODO: Assemble python into code variable.
  var code = 'self.current_expression = None\n';
  return code;
};

Blockly.Blocks['set_current_playback_speed'] = {
  init: function () {
    this.jsonInit(miniblocks.set_current_playback_speed)
  }
};

Blockly.Python['set_current_playback_speed'] = function (block) {
  var new_speed = Blockly.Python.valueToCode(block, 'new_speed', Blockly.Python.ORDER_NONE);

  // TODO: Assemble python into code variable.
  var code = 'self.current_expression_playback_speed = ' + new_speed + '\n';
  return code;
};
