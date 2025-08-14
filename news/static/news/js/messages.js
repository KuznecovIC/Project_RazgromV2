class GooeyMessages {
    constructor() {
        this.messages = [];
        this.init();
    }

    init() {
        document.querySelectorAll('.gooey-message').forEach(message => {
            this.setupMessage(message);
        });
    }

    setupMessage(message) {
        const messageObj = {
            element: message,
            timer: null,
            id: message.dataset.messageId
        };

        // Анимация появления
        setTimeout(() => {
            this.createParticles(message);
        }, 300);

        // Кнопка закрытия
        const closeBtn = message.querySelector('.gooey-message-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                this.closeMessage(messageObj);
            });
        }

        // Автозакрытие через 5 секунд
        messageObj.timer = setTimeout(() => {
            this.closeMessage(messageObj);
        }, 5000);

        this.messages.push(messageObj);
    }

    createParticles(message) {
        const container = message.querySelector('.gooey-message-particles');
        if (!container) return;

        const rect = message.getBoundingClientRect();
        const color = window.getComputedStyle(message).backgroundColor;
        const count = 10 + Math.floor(Math.random() * 5);

        for (let i = 0; i < count; i++) {
            const particle = document.createElement('div');
            particle.className = 'gooey-particle';
            particle.style.backgroundColor = color;
            
            const startX = rect.width / 2;
            const startY = rect.height / 2;
            const endX = Math.random() * rect.width;
            const endY = Math.random() * rect.height;
            const tx = (Math.random() - 0.5) * 50;
            const ty = (Math.random() - 0.5) * 50;
            
            particle.style.setProperty('--tx', `${tx}px`);
            particle.style.setProperty('--ty', `${ty}px`);
            particle.style.left = `${startX}px`;
            particle.style.top = `${startY}px`;
            particle.style.transform = 'scale(0)';
            
            container.appendChild(particle);
            
            setTimeout(() => {
                particle.style.transition = 'all 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
                particle.style.left = `${endX}px`;
                particle.style.top = `${endY}px`;
                particle.style.transform = 'scale(1)';
                
                setTimeout(() => {
                    particle.style.animation = 'particleFloat 1s forwards';
                }, 500);
            }, 50);
        }
    }

    closeMessage(messageObj) {
        if (!messageObj.element.parentNode) return;
        
        clearTimeout(messageObj.timer);
        messageObj.element.style.transform = 'translateX(120%)';
        
        setTimeout(() => {
            messageObj.element.remove();
            this.messages = this.messages.filter(m => m.id !== messageObj.id);
        }, 500);
    }
}

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', () => {
    window.gooeyMessages = new GooeyMessages();
});