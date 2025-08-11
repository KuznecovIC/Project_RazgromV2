// gooey_particles.js
document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.gooey-nav a');
    const navBar = document.querySelector('.gooey-nav');
    const themeToggleButton = document.getElementById('theme-toggle');

    if (!navLinks.length || !navBar) return;

    // Создаем элемент для фона
    const activeBg = document.createElement('div');
    activeBg.className = 'active-bg';
    navBar.appendChild(activeBg);

    // Загрузка темы
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
    }

    // Установка начального активного состояния и фона
    let currentActiveLink = document.querySelector('.gooey-nav a.active');
    if (!currentActiveLink) {
        currentActiveLink = navLinks[0];
        currentActiveLink.classList.add('active');
    }
    updateActiveBg(currentActiveLink);

    // Обработчик для переключения тем
    if (themeToggleButton) {
        themeToggleButton.addEventListener('click', () => {
            document.body.classList.toggle('dark-theme');
            const isDark = document.body.classList.contains('dark-theme');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');

            updateActiveBg(currentActiveLink);
        });
    }

    // Обработчик для кликов по ссылкам
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            navLinks.forEach(l => l.classList.remove('active'));
            e.target.classList.add('active');
            currentActiveLink = e.target;
            updateActiveBg(currentActiveLink);
        });
    });

    // Функция для обновления фона
    function updateActiveBg(target) {
        const targetRect = target.getBoundingClientRect();
        const navRect = navBar.getBoundingClientRect();
        
        activeBg.style.left = `${targetRect.left - navRect.left}px`;
        activeBg.style.width = `${targetRect.width}px`;
        
        const isDark = document.body.classList.contains('dark-theme');
        activeBg.style.backgroundColor = isDark ? '#fff' : '#313131';
    }
});