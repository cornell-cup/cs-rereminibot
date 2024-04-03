export class SpritesheetJS{
    constructor(src, frameWidth, frameHeight, frameCount) {
        this.loadedCorrectly = false;
        this.frameWidth = frameWidth;
        this.frameHeight = frameHeight;
        this.frameCount = frameCount;
        this.imageSrc = src;

        console.log(`Image Src: ${src}`);

        this.loaded = new Promise((resolve, reject) => {
            this.fullSpritesheet = new Image();
            this.fullSpritesheet.src = src;
            this.fullSpritesheet.onload = () => {
                this.loadedCorrectly = true;
                resolve();
            };
            this.fullSpritesheet.onerror = () => {
                this.loadedCorrectly = false;
                reject(new Error('Failed to load spritesheet'));
              };
        });
    }

    /**
     * Draw the specified frame on the specified canvas.
     * @param {number} frameNumber - The number of the frame to draw.
     * @param {number} canvas - The canvas element on which to draw the frame.
     * @returns {boolean} Whether the frame was successfully drawn on the canvas.
     */
    drawFrame(frameNumber, canvas) {
        if (!this.loadedCorrectly || !canvas)
            return false;
    
        while (frameNumber >= this.frameCount) {
            frameNumber -= this.frameCount;
        }
        while (frameNumber < 0) {
            frameNumber += this.frameCount;
        }

        const frameIndex = Math.floor(frameNumber);
        const numFramesH = Math.floor(this.fullSpritesheet.width / this.frameWidth);
        const row = Math.floor(frameIndex / numFramesH);
        const col = frameIndex % numFramesH;
        const sx = col * this.frameWidth;
        const sy = row * this.frameHeight;
        const context = canvas.getContext('2d');
        context.drawImage(this.fullSpritesheet, sx, sy, this.frameWidth, this.frameHeight, 0, 0, canvas.width, canvas.height);
        return true;
    }
}