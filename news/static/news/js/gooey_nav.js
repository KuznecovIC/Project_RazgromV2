// gooey_nav.js
document.addEventListener('DOMContentLoaded', () => {

    const themeSwitch = document.querySelector('.theme-switch');
    if (themeSwitch) {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-theme');
        }

        themeSwitch.addEventListener('click', () => {
            document.body.classList.toggle('dark-theme');
            const isDark = document.body.classList.contains('dark-theme');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            
            initializeGooeyNavs();
        });
    }

    function initializeGooeyNavs() {
        const navContainers = document.querySelectorAll('.gooey-nav-container');

        navContainers.forEach(navContainer => {
            let activeBg = navContainer.querySelector('.active-bg');
            let particleContainer = navContainer.querySelector('.particle-container');

            if (!activeBg) {
                activeBg = document.createElement('div');
                activeBg.className = 'active-bg';
                navContainer.appendChild(activeBg);
            }

            if (!particleContainer) {
                particleContainer = document.createElement('div');
                particleContainer.className = 'particle-container';
                navContainer.appendChild(particleContainer);
            }
            
            const navLinks = navContainer.querySelectorAll('.gooey-nav a');

            let currentActiveLink = null;
            // Новая логика: ищем активную ссылку по текущему URL
            const currentPathname = window.location.pathname.endsWith('/') 
                ? window.location.pathname 
                : window.location.pathname + '/';

            navLinks.forEach(link => {
                const linkPathname = link.getAttribute('href').endsWith('/')
                    ? link.getAttribute('href')
                    : link.getAttribute('href') + '/';
                if (linkPathname === currentPathname) {
                    currentActiveLink = link;
                    link.classList.add('active');
                } else {
                    link.classList.remove('active');
                }
            });

            // Если не нашли по URL, используем первую ссылку в контейнере
            if (!currentActiveLink && navLinks.length > 0) {
                currentActiveLink = navLinks[0];
                currentActiveLink.classList.add('active');
            }
            
            if (currentActiveLink) {
                updateActiveBg(navContainer, currentActiveLink, activeBg);
            }
            
            navLinks.forEach(link => {
                link.addEventListener('click', (e) => {
                    const href = e.target.href;
                    if (!href) return;
                    
                    e.preventDefault();
                    
                    const parentNav = e.target.closest('.gooey-nav');
                    parentNav.querySelectorAll('a').forEach(l => l.classList.remove('active'));
                    e.target.classList.add('active');
                    currentActiveLink = e.target;
                    
                    updateActiveBg(navContainer, currentActiveLink, activeBg);
                    createParticles(e.target, particleContainer);

                    setTimeout(() => {
                        window.location.href = href;
                    }, 500);
                });
            });
        });
    }

    const createParticles = (targetElement, particleContainer) => {
        const particleCount = 15;
        const targetRect = targetElement.getBoundingClientRect();
        
        const centerX = targetRect.left + targetRect.width / 2;
        const centerY = targetRect.top + targetRect.height / 2;
        
        const colors = ['#4a90e2', '#bd10e0', '#f5a623', '#50e3c2'];

        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';

            const startAngle = Math.random() * 2 * Math.PI;
            const startRadius = 50 + Math.random() * 40;
            const startX = centerX + Math.cos(startAngle) * startRadius;
            const startY = centerY + Math.sin(startAngle) * startRadius;

            const animationTime = 600 + Math.random() * 300;
            const particleColor = colors[Math.floor(Math.random() * colors.length)];
            
            particle.style.backgroundColor = particleColor;
            particle.style.setProperty('--time', `${animationTime}ms`);
            
            const navRect = particleContainer.closest('.gooey-nav-container').getBoundingClientRect();
            particle.style.setProperty('--start-x', `${startX - navRect.left}px`);
            particle.style.setProperty('--start-y', `${startY - navRect.top}px`);
            particle.style.setProperty('--end-x', `${centerX - navRect.left}px`);
            particle.style.setProperty('--end-y', `${centerY - navRect.top}px`);
            
            particleContainer.appendChild(particle);
            
            setTimeout(() => {
                particle.remove();
            }, animationTime);
        }
    };

    function updateActiveBg(navContainer, target, activeBg) {
        const targetRect = target.getBoundingClientRect();
        const navRect = navContainer.getBoundingClientRect();
        
        activeBg.style.left = `${targetRect.left - navRect.left}px`;
        activeBg.style.width = `${targetRect.width}px`;
        
        const isDark = document.body.classList.contains('dark-theme');
        activeBg.style.backgroundColor = isDark ? '#f0f0f0' : '#313131';
        
        const navLinks = navContainer.querySelectorAll('.gooey-nav a');
        navLinks.forEach(l => l.style.color = isDark ? '#e0e0e0' : '#313131');
        target.style.color = isDark ? '#1a1a1a' : '#fff';
    }
    
    initializeGooeyNavs();
});