import React, { useState, useEffect } from 'react';
import axios from 'axios';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { commands } from '../../utils/Constants.js';
import {
  MIC_BTN, MIC_BTNON,
  ACT_MIC_COMMAND
} from "../../utils/Constants.js";

import SpeechRecognitionComp from "../../utils/SpeechRecognitionComp.js";

var lastLen = 0;
const micStyle = {
  width: "75%",
  height: "75%",
  objectFit: "contain",
};

function BotVoiceControl({
  selectedBotName,
  activeMicComponent,
  setActiveMicComponent,
  botVoiceControlMic, setBotVoiceControlMic }) {
  const [text, setText] = useState("");
  const [inputText, setInputText] = useState("");

  const toggle = (e) => {
    e.preventDefault();
    if (selectedBotName) {
      if (activeMicComponent == ACT_MIC_COMMAND) {
        setBotVoiceControlMic(!botVoiceControlMic);
        lastLen = 0; // correctly reset queue length if the button is toggled
        setInputText("Speak to send a command")
      } else {
        setActiveMicComponent(ACT_MIC_COMMAND)
      }
    } else {
      setInputText("Please connect to a bot!")
      window.alert("Please connect to a bot!");
    }
  }

  useEffect(() => {
    let queue = text.split(" ");
    // only read the lastest word in the queue (last item is always ''):
    if (queue.length > lastLen) {
      if (commands.hasOwnProperty(queue[queue.length - 2])) {
        setInputText(queue[queue.length - 2] + ": " + commands[queue[queue.length - 2]]);

        // send command to backend
        axios({
          method: 'POST',
          url: '/speech_recognition',
          headers: {
            'Content-Type': 'application/json'
          },
          data: JSON.stringify({
            bot_name: selectedBotName,
            command: queue[queue.length - 2]
          })
        }).then(function (response) {
          // insert response code here?
        }).catch(function (error) {
          // tell user to connect to bot in the text box
          // setInputText("Please connect to a Minibot!")
          if (error.response.data.error_msg.length > 0)
            window.alert(error.response.data.error_msg);
          else
            console.log("Speech recognition", error);
        })
      }
    }
    lastLen = queue.length;
    // setText("");
  }, [text]);

  return (
    <React.Fragment>
      <div id="speech-button" className="row">
        <input className="text-box" id="textbox" onChange={setInputText}
          value={selectedBotName != "" ? inputText : "Please connect to a Minibot!"}>

        </input>
        <button className="btn btn-danger element-wrapper btn-speech"
          onClick={toggle}>
          <div className="row">
            <span className="col-md-1 align-self-center">
              <div style={{ width: "50px", height: "50px", }}>
                <input type="image"
                  src={botVoiceControlMic ? MIC_BTNON : MIC_BTN}
                  style={micStyle}
                  onClick={(e) => {
                    toggle(e);
                  }} />
              </div>
            </span>
          </div>
        </button>
        <SpeechRecognitionComp setText={setText} mic={botVoiceControlMic} />
      </div>
    </React.Fragment>
  )
}

export default BotVoiceControl;