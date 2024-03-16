const spriteElement = document.querySelector('.sprite');
const fps = 24; // Set the desired frames per second

// Start the animation
function startAnimation() {
  spriteElement.style.animationPlayState = 'running';
  spriteElement.style.animationDuration = `${1 / fps}s`;
}

// Pause the animation
function pauseAnimation() {
  spriteElement.style.animationPlayState = 'paused';
}

// Stop the animation
function stopAnimation() {
  spriteElement.style.animationPlayState = 'initial';
}

// Start the animation by default
startAnimation();