// Note: This is the path from the directory containing expressions_animation.css file
const relativePathToExpressionsFolder = "./static/img/Expressions/";

// Note: This is the path from the static/gui directory to the expressions.json parent folder
const relativePathToExpressionsJson = "./static/js/components/Expression/"

export function setAnimation(expression_name, fps=10)
{
  console.log(expression_name);
  console.log("Starting JSON read!");

  // Read JSON file to find the correct expression
  fetch(relativePathToExpressionsJson + 'expressions.json')
  .then(response => response.json())
  .then(data => {
    const expressionData = data[expression_name]; // Access expression data dynamically
    if (expressionData) {

      updateAnimationProperties(expressionData, fps);
      
      console.log("Reached end of JSON read!");
    } else {
      console.log(`Expression "${expression_name}" not found in JSON data.\nKeeping current animation instead.`);
    }
  })
  .catch(error => {
    // Handle errors
    console.error('Error fetching data from JSON: ', error);
    console.error('Stack trace:', error.stack);
    console.log("Keeping current animation.")
  });
}

function updateAnimationProperties(expressionData, fps) {
  const spriteElement = document.querySelector('.sprite');
  const styleSheet = document.styleSheets[3];

  var spritesheetPath = relativePathToExpressionsFolder + expressionData.sheet_src;
  var frameWidth = expressionData.frame_width;
  var frameHeight = expressionData.frame_height;
  var numColumns = expressionData.num_columns;
  var frameCount = expressionData.frame_count;

  // Set the CSS properties for the sprite
  spriteElement.style.width = frameWidth + 'px';
  spriteElement.style.height = frameHeight + 'px';
  spriteElement.style.backgroundImage = 'url("' + spritesheetPath +  '")';

  console.log(frameWidth);
  console.log(frameHeight);
  console.log(numColumns);
  console.log(spritesheetPath);
  console.log(frameCount);

  // Calculate and set the animation keyframes dynamically
  let keyframes = '';
  for (let i = 0; i < frameCount; i++) {
      const col = i % numColumns;
      const row = Math.floor(i / numColumns);
      const posX = -col * frameWidth;
      const posY = -row * frameHeight;
      const percentage = (i / frameCount) * 100;
      keyframes += `${percentage}% { background-position: ${posX}px ${posY}px; } `;
  }

  console.log(keyframes);

  // Delete existing keyframes rule from the expressions CSS stylesheet
  const keyframesRule = findKeyframesRule(styleSheet, 'spriteAnimationKeyframes');
  if (keyframesRule) {
    styleSheet.deleteRule(keyframesRule);
    console.log("Deleted existing rule.")
  }

  // Add new keyframes rule to the expressions CSS stylesheet 
  styleSheet.insertRule(`@keyframes spriteAnimationKeyframes { ${keyframes} }`);

  const keyframesRuleCheck = findKeyframesRule(styleSheet, 'spriteAnimationKeyframes');
  if (keyframesRule) {
    console.log("Keyframe Rule:");
    console.log(`  Selector Text: ${styleSheet.cssRules[keyframesRule].selectorText}`);
    console.log(`  Style: ${styleSheet.cssRules[keyframesRule].style.cssText}`);
    console.log(`  Style Map:`);
    styleSheet.cssRules[keyframesRule].styleMap.forEach((value, key) => {
      console.log(`    ${key}: ${value}`);
    });
  }
  else{
    console.log("No Keyframe rule found.")
  }

  // Compute sprite playback duration
  const duration = frameCount / fps;

  console.log(`Frame Count: ${frameCount}`)
  console.log(`FPS: ${fps}`)
  console.log(`Duration: ${duration}`)

  // Apply the animation to the sprite
  //spriteElement.setAttribute('style', `animation: spriteAnimationKeyframes ${duration}s steps(${frameCount}) infinite step-end`);
  spriteElement.style.animation = `spriteAnimationKeyframes ${duration}s steps(${frameCount}) infinite step-end`;

  console.log(`Animation String: ${'spriteAnimationKeyframes ' + duration + 's steps(' + frameCount + ') infinite step-end'}`);
  console.log(`Anmation: ${spriteElement.style.animation}`);

  const computedStyles = window.getComputedStyle(spriteElement);
  console.log(`Animation: ${computedStyles.animation}`);
}

function findKeyframesRule(styleSheet, name) {
  // Iterate through each CSSRule in the stylesheet
  for (let i = 0; i < styleSheet.cssRules.length; i++) {
    const rule = styleSheet.cssRules[i];
    // Check if the rule is a keyframes rule and its name matches the provided name
    if (rule.type === CSSRule.KEYFRAMES_RULE && rule.name === name) {
      return i; // Return the index of the keyframes rule
    }
  }
  return null; // Return null if the keyframes rule is not found
}

// Start the animation
export function startAnimation() {
  //spriteElement.style.animationPlayState = 'running';
  //spriteElement.style.animationDuration = `${1 / fps}s`;
}

// Pause the animation
export function pauseAnimation() {
  //spriteElement.style.animationPlayState = 'paused';
}

// Stop the animation
export function stopAnimation() {
  //spriteElement.style.animationPlayState = 'initial';
}
