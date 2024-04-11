import { SpritesheetJS } from "./Spritesheet.js"

const relativePathToExpressionsImgFolder = "./static/img/Expressions/";
const relativePathToExpressionsJSFolder = "./static/js/components/Expression/";

export class AvatarJS
{
  
  constructor(expressions = {}, currentExpression = null, currentPlaybackSpeed = 10.0, autoSaveExpressions = false) {
    this.expressions = expressions;
    this.jsonExpressionsDict = {};
    this.currentExpressionName = null;
    this.currentPlaybackSpeed = currentPlaybackSpeed;
    this.currentFrame = 0.0;
    this.restartOnNextUpdate = true;
    this.autoSaveExpressions = autoSaveExpressions;

    let setArbitraryStartingExpression = Object.keys(expressions).length > 0;

    if (currentExpression !== null) {
        if (expressions.hasOwnProperty(currentExpression)) {
            this.currentExpressionName = currentExpression;
            setArbitraryStartingExpression = false;
        }
    }

    if (setArbitraryStartingExpression) {
        this.currentExpressionName = Object.keys(expressions)[0];
    }

    this.prevUpdateTime = Date.now();
  }

  addOrUpdateExpression(expressionName, expressionSpritesheet) {
    this.expressions[expressionName] = expressionSpritesheet;
    this.jsonExpressionsDict[expressionName] = {
        frameWidth: expressionSpritesheet.frameWidth,
        frameHeight: expressionSpritesheet.frameHeight,
        frameCount: expressionSpritesheet.frameCount,
        sheetSrc: expressionSpritesheet.imageSrc
    };
    if (this.autoSaveExpressions) {
        this.saveExpressionsJson(relativePathToExpressionsJSFolder + "expressions_autosave.json");
    }
  }

  async loadExpressionsJson(json_src = relativePathToExpressionsJSFolder + "expressions.json", 
                      img_dir = relativePathToExpressionsImgFolder) {
    try {
        console.log(json_src);
        
        const response = await fetch(json_src);
        const jsonData = await response.json();

        for (const key in jsonData) {
            const sheet = new SpritesheetJS(
                img_dir + jsonData[key].sheet_src,
                jsonData[key].frame_width,
                jsonData[key].frame_height,
                jsonData[key].frame_count
            );
            console.log(`Created Spritesheet for ${key}`);
            this.addOrUpdateExpression(key, sheet);
        }
        return true;
    } catch (error) {
        console.error(error.message);
        return false;
    }
  }

  saveExpressionsJson(path) {
    try {
        // const fs = require('fs');
        // fs.writeFileSync(path, JSON.stringify(this.jsonExpressionsDict, null, 2));
        return false;
    } catch (error) {
        console.error(error);
        return false;
    }
  }

  validCurrentExpression() {
    const expressionNotPresent = !this.expressions.hasOwnProperty(this.currentExpressionName);
    const expressionNull = this.currentExpressionName === null;
    
    if(expressionNull || expressionNotPresent)
        return false;

    return this.expressions[this.currentExpressionName].loadedCorrectly;
  }

  getExpression(expressionName) {
    return this.expressions[expressionName] || null;
  }

  clearCurrentExpression() {
    this.currentExpressionName = null;
  }

  setCurrentExpression(expressionName) {
    if (expressionName === this.currentExpressionName) {
      return true;
    }
    if (expressionName === null || 
        expressionName === "" || 
        expressionName === "none") {
      this.clearCurrentExpression();
      return true;
    }
    if (this.expressions.hasOwnProperty(expressionName)) {
      this.currentExpressionName = expressionName;
      this.restartOnNextUpdate = true;
      console.log("Current Frame Reset!");
      return true;
    }
    return false;
  }

  setPlaybackSpeed(newSpeed) {
    this.currentPlaybackSpeed = newSpeed;
  }

  update() {
    // Check to see if current expression is valid
    if(!this.validCurrentExpression()){
      // console.log("Invalid Expression Found During Update");
      // console.log(`Expressions: ${this.expressions}`) ;
      // console.log(`Current Expression: ${this.currentExpression}`); 
      return;
    }
    
    const numFrames = this.expressions[this.currentExpressionName].frameCount;

    if(numFrames == null || isNaN(numFrames)){
      console.error("Null or NaN number of frames encountered! This should not happen!");
      return;
    }

    // Get time since last frame
    const currentTime = Date.now();

    if(this.restartOnNextUpdate){
      this.currentFrame = 0.0;
      this.restartOnNextUpdate = false;
    }
    else{
      const deltaTime = (currentTime - this.prevUpdateTime) / 1000;

      // Compute temporal position of new frame (frame index but with decimals)
      this.currentFrame += deltaTime * this.currentPlaybackSpeed;
    }

    // Update previous frame time variable
    this.prevUpdateTime = currentTime;

    // Keep the temporal position with the range [0, total number of frames)
    while (this.currentFrame >= numFrames) {
        this.currentFrame -= numFrames;
    }

    while (this.currentFrame < 0) {
        this.currentFrame += numFrames;
    }
  }

  drawCurrentDisplay(canvas) {  
    if(!this.validCurrentExpression())
      return false;

    return this.expressions[this.currentExpressionName].drawFrame(this.currentFrame, canvas);
  }

  getCurrentFrameCount() {
    if(!this.validCurrentExpression())
        return 0;
    return this.expressions[this.currentExpressionName].frameCount;
  }

  getExpressionNames() {
      return Object.keys(this.expressions);
  }

}

const basestationAvatar = new AvatarJS();

export {basestationAvatar};