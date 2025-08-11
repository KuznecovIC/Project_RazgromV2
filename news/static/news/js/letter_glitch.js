document.addEventListener('DOMContentLoaded', () => {
    class LetterGlitch {
        constructor(container, options = {}) {
            this.container = container;
            this.canvas = document.createElement('canvas');
            this.context = this.canvas.getContext('2d');
            this.container.appendChild(this.canvas);
            
            this.glitchColors = options.glitchColors || ['#2b4539', '#61dca3', '#61b3dc'];
            this.glitchSpeed = options.glitchSpeed || 50;
            this.smooth = options.smooth !== undefined ? options.smooth : true;

            this.letters = [];
            this.grid = { columns: 0, rows: 0 };
            this.lastGlitchTime = Date.now();
            this.animationRef = null;

            this.fontSize = 16;
            this.charWidth = 10;
            this.charHeight = 20;
            this.lettersAndSymbols = [
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                '!', '@', '#', '$', '&', '*', '(', ')', '-', '_', '+', '=', '/',
                '[', ']', '{', '}', ';', ':', '<', '>', ',', '0', '1', '2', '3',
                '4', '5', '6', '7', '8', '9'
            ];

            this.init();
        }

        init() {
            window.addEventListener('resize', this.handleResize.bind(this));
            this.resizeCanvas();
            this.animate();
        }

        getRandomChar() {
            return this.lettersAndSymbols[Math.floor(Math.random() * this.lettersAndSymbols.length)];
        }

        getRandomColor() {
            return this.glitchColors[Math.floor(Math.random() * this.glitchColors.length)];
        }

        hexToRgb(hex) {
            const shorthandRegex = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
            hex = hex.replace(shorthandRegex, (m, r, g, b) => r + r + g + g + b + b);
            const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
            return result ? {
                r: parseInt(result[1], 16),
                g: parseInt(result[2], 16),
                b: parseInt(result[3], 16)
            } : null;
        }

        interpolateColor(start, end, factor) {
            const result = {
                r: Math.round(start.r + (end.r - start.r) * factor),
                g: Math.round(start.g + (end.g - start.g) * factor),
                b: Math.round(start.b + (end.b - start.b) * factor),
            };
            return `rgb(${result.r}, ${result.g}, ${result.b})`;
        }

        calculateGrid(width, height) {
            const columns = Math.ceil(width / this.charWidth);
            const rows = Math.ceil(height / this.charHeight);
            return { columns, rows };
        }

        initializeLetters(columns, rows) {
            this.grid = { columns, rows };
            const totalLetters = columns * rows;
            this.letters = Array.from({ length: totalLetters }, () => ({
                char: this.getRandomChar(),
                color: this.getRandomColor(),
                targetColor: this.getRandomColor(),
                colorProgress: 1,
            }));
        }

        resizeCanvas() {
            const dpr = window.devicePixelRatio || 1;
            const rect = this.container.getBoundingClientRect();
            this.canvas.width = rect.width * dpr;
            this.canvas.height = rect.height * dpr;
            this.canvas.style.width = `${rect.width}px`;
            this.canvas.style.height = `${rect.height}px`;

            this.context.setTransform(dpr, 0, 0, dpr, 0, 0);

            const { columns, rows } = this.calculateGrid(rect.width, rect.height);
            this.initializeLetters(columns, rows);
            this.drawLetters();
        }

        drawLetters() {
            if (!this.context || this.letters.length === 0) return;
            const ctx = this.context;
            const { width, height } = this.container.getBoundingClientRect();
            ctx.clearRect(0, 0, width, height);
            ctx.font = `${this.fontSize}px monospace`;
            ctx.textBaseline = 'top';

            this.letters.forEach((letter, index) => {
                const x = (index % this.grid.columns) * this.charWidth;
                const y = Math.floor(index / this.grid.columns) * this.charHeight;
                ctx.fillStyle = letter.color;
                ctx.fillText(letter.char, x, y);
            });
        }

        updateLetters() {
            if (!this.letters || this.letters.length === 0) return;
            const updateCount = Math.max(1, Math.floor(this.letters.length * 0.05));

            for (let i = 0; i < updateCount; i++) {
                const index = Math.floor(Math.random() * this.letters.length);
                if (!this.letters[index]) continue;

                this.letters[index].char = this.getRandomChar();
                this.letters[index].targetColor = this.getRandomColor();

                if (!this.smooth) {
                    this.letters[index].color = this.letters[index].targetColor;
                    this.letters[index].colorProgress = 1;
                } else {
                    this.letters[index].colorProgress = 0;
                }
            }
        }

        handleSmoothTransitions() {
            let needsRedraw = false;
            this.letters.forEach((letter) => {
                if (letter.colorProgress < 1) {
                    letter.colorProgress += 0.05;
                    if (letter.colorProgress > 1) letter.colorProgress = 1;

                    const startRgb = this.hexToRgb(letter.color);
                    const endRgb = this.hexToRgb(letter.targetColor);
                    if (startRgb && endRgb) {
                        letter.color = this.interpolateColor(startRgb, endRgb, letter.colorProgress);
                        needsRedraw = true;
                    }
                }
            });

            if (needsRedraw) {
                this.drawLetters();
            }
        }

        animate() {
            const now = Date.now();
            if (now - this.lastGlitchTime >= this.glitchSpeed) {
                this.updateLetters();
                this.drawLetters();
                this.lastGlitchTime = now;
            }

            if (this.smooth) {
                this.handleSmoothTransitions();
            }

            this.animationRef = requestAnimationFrame(this.animate.bind(this));
        }

        handleResize() {
            clearTimeout(this.resizeTimeout);
            this.resizeTimeout = setTimeout(() => {
                cancelAnimationFrame(this.animationRef);
                this.resizeCanvas();
                this.animate();
            }, 100);
        }
    }

    const glitchContainer = document.querySelector('.letter-glitch-container');
    if (glitchContainer) {
        new LetterGlitch(glitchContainer, {
            glitchSpeed: 50,
            smooth: true
        });
    }
});