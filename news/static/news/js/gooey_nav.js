class GooeyNav {
    constructor() {
        this.navContainers = [];
        this.init();
    }

    init() {
        // Инициализация темы
        this.initTheme();

        // Инициализация навигации
        document.querySelectorAll('.gooey-nav-container').forEach(container => {
            this.setupNavContainer(container);
        });
    }

    initTheme() {
        // Проверяем сохраненную тему
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-theme');
        }

        // Обработчик переключения темы
        const themeSwitch = document.querySelector('.theme-switch');
        if (themeSwitch) {
            themeSwitch.addEventListener('click', () => {
                document.body.classList.toggle('dark-theme');
                const isDark = document.body.classList.contains('dark-theme');
                localStorage.setItem('theme', isDark ? 'dark' : 'light');
                
                // Отправляем событие об изменении темы
                document.dispatchEvent(new CustomEvent('themeChanged'));
                
                // Обновляем все навигационные контейнеры
                this.updateAllNavs();
            });
        }
    }

    setupNavContainer(container) {
        const nav = {
            container,
            activeBg: null,
            particleContainer: null,
            currentActiveLink: null
        };

        // Создаем фон для активной кнопки
        nav.activeBg = document.createElement('div');
        nav.activeBg.className = 'active-bg';
        container.appendChild(nav.activeBg);

        // Создаем контейнер для частиц
        nav.particleContainer = document.createElement('div');
        nav.particleContainer.className = 'particle-container';
        container.appendChild(nav.particleContainer);

        // Инициализируем ссылки
        this.setupNavLinks(nav);
        this.navContainers.push(nav);
    }

    setupNavLinks(nav) {
        const links = nav.container.querySelectorAll('.gooey-nav a');
        
        // Находим активную ссылку по текущему URL
        const currentPath = window.location.pathname;
        links.forEach(link => {
            const linkPath = link.getAttribute('href');
            if (currentPath === linkPath) {
                link.classList.add('active');
                nav.currentActiveLink = link;
                this.updateActiveBg(nav);
            }

            link.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleNavClick(e, nav);
            });
        });

        // Если активная ссылка не найдена, выбираем первую
        if (!nav.currentActiveLink && links.length > 0) {
            links[0].classList.add('active');
            nav.currentActiveLink = links[0];
            this.updateActiveBg(nav);
        }
    }

    handleNavClick(event, nav) {
        const link = event.currentTarget;
        const href = link.href;
        
        // Убираем активный класс у всех ссылок
        nav.container.querySelectorAll('.gooey-nav a').forEach(l => {
            l.classList.remove('active');
        });
        
        // Устанавливаем активный класс для текущей ссылки
        link.classList.add('active');
        nav.currentActiveLink = link;
        
        // Обновляем фон и создаем частицы
        this.updateActiveBg(nav);
        this.createParticles(link, nav.particleContainer);

        // Переходим по ссылке с задержкой
        setTimeout(() => {
            window.location.href = href;
        }, 500);
    }

    updateActiveBg(nav) {
        if (!nav.currentActiveLink) return;
        
        const linkRect = nav.currentActiveLink.getBoundingClientRect();
        const containerRect = nav.container.getBoundingClientRect();
        
        nav.activeBg.style.left = `${linkRect.left - containerRect.left}px`;
        nav.activeBg.style.width = `${linkRect.width}px`;
        
        // Устанавливаем цвет в зависимости от темы
        const isDark = document.body.classList.contains('dark-theme');
        nav.activeBg.style.backgroundColor = isDark ? '#f0f0f0' : '#313131';
        
        // Обновляем цвета ссылок
        nav.container.querySelectorAll('.gooey-nav a').forEach(l => {
            l.style.color = isDark ? '#e0e0e0' : '#313131';
        });
        nav.currentActiveLink.style.color = isDark ? '#1a1a1a' : '#fff';
    }

    createParticles(target, container) {
        const particleCount = 15;
        const targetRect = target.getBoundingClientRect();
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
            particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            particle.style.setProperty('--time', `${animationTime}ms`);
            
            const containerRect = container.getBoundingClientRect();
            particle.style.setProperty('--start-x', `${startX - containerRect.left}px`);
            particle.style.setProperty('--start-y', `${startY - containerRect.top}px`);
            particle.style.setProperty('--end-x', `${centerX - containerRect.left}px`);
            particle.style.setProperty('--end-y', `${centerY - containerRect.top}px`);
            
            container.appendChild(particle);
            
            setTimeout(() => {
                particle.remove();
            }, animationTime);
        }
    }

    updateAllNavs() {
        this.navContainers.forEach(nav => {
            this.updateActiveBg(nav);
        });
    }
}

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', () => {
    window.gooeyNav = new GooeyNav();
});