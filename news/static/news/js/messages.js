document.addEventListener('DOMContentLoaded', () => {
    initializeGooeyMessages();
});

function initializeGooeyMessages() {
    const messages = document.querySelectorAll('.gooey-message');
    
    messages.forEach(message => {
        // Анимация появления
        setTimeout(() => {
            createMessageParticles(message);
        }, 300);
        
        // Закрытие сообщения
        const closeBtn = message.querySelector('.gooey-message-close');
        closeBtn.addEventListener('click', () => {
            animateMessageOut(message);
        });
        
        // Автоматическое закрытие через 5 секунд
        setTimeout(() => {
            if (message.parentNode) {
                animateMessageOut(message);
            }
        }, 5000);
    });
}

function createMessageParticles(message) {
    const particleContainer = message.querySelector('.gooey-message-particles');
    const rect = message.getBoundingClientRect();
    const color = window.getComputedStyle(message).backgroundColor;
    
    const particleCount = 10 + Math.floor(Math.random() * 5);
    
    for (let i = 0; i < particleCount; i++) {
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
        
        particleContainer.appendChild(particle);
        
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

function animateMessageOut(message) {
    message.style.transform = 'translateX(120%)';
    setTimeout(() => {
        message.remove();
    }, 500);
}