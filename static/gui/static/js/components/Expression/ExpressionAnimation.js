import React, { useEffect, useRef } from 'react';
import axios from 'axios';

import { basestationAvatar } from "./Avatar.js";

const EXPRESSION_UPDATE_RATE = 10;

function ExpressionAnimation({ startingExpression = null, startingFPS = 10, refreshRate = 60}) {
  const canvasRef = useRef(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log("Starting JSON Load");
        await basestationAvatar.loadExpressionsJson(); // Wait for the JSON data to be loaded
        console.log(`Expressions: ${basestationAvatar.getExpressionNames()}`);
        console.log(`Starting Expression: ${startingExpression}`);
        console.log(`Setting Current Expression: ${basestationAvatar.setCurrentExpression(startingExpression)}`);
        basestationAvatar.setPlaybackSpeed(startingFPS);
      } catch (error) {
        console.error('An error occurred while loading the expressions JSON file:');
        console.error(error.message);
        console.trace();
      }
    };

    fetchData();
    
  }, [])

  useEffect(() => {
    const canvas = canvasRef.current;
    let frameTimer = null;
    let checkForExprUpdateTimer = null;

    const renderFrame = () => {
      basestationAvatar.update();
      
      const context = canvas.getContext('2d');
      context.clearRect(0, 0, canvas.width, canvas.height); 
      basestationAvatar.drawCurrentDisplay(canvas);
    };

    const checkForExpressionUpdate = () => {
      axios({
        method: 'POST',
        url: '/expression-update',
        headers: {
            'Content-Type': 'application/json'
        },
        data: JSON.stringify({
            current_expression: basestationAvatar.currentExpression
        }),
      }).then((response) => {
          basestationAvatar.setCurrentExpression(response.data["expression"])
          basestationAvatar.setPlaybackSpeed(response.data["speed"])
      }).catch((error) => {
          console.error(error);
      })
    }

    frameTimer = setInterval(renderFrame, 1000 / refreshRate);
    checkForExprUpdateTimer = setInterval(checkForExpressionUpdate, 1000 / EXPRESSION_UPDATE_RATE);

    renderFrame();

    return () => {
      clearInterval(frameTimer);
      clearInterval(checkForExprUpdateTimer);
    };
  }, [refreshRate, basestationAvatar.currentExpression]);

  return <canvas ref={canvasRef} width={480} height={320} style={{ backgroundColor: 'black', border: '2px solid white' }}/>;
}

export default ExpressionAnimation;