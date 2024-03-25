import React, { useEffect, useRef } from 'react';

import { basestationAvatar } from "./Avatar.js";

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

    const renderFrame = () => {
      basestationAvatar.update();
      basestationAvatar.drawCurrentDisplay(canvas);
    };

    frameTimer = setInterval(renderFrame, 1000 / refreshRate);

    renderFrame();

    return () => {
      clearInterval(frameTimer);
    };
  }, [refreshRate, basestationAvatar.currentExpression]);

  return <canvas ref={canvasRef} width={480} height={320} style={{ backgroundColor: 'black', border: '2px solid white' }}/>;
}

export default ExpressionAnimation;