class GooeyNav {
    constructor() {
        this.navContainers = [];
        this.init();
    }

    init() {
        try {
            this.initTheme();
            this.initNavContainers();
            this.setupThemeSwitch();
            this.setupGithubCardHoverEffect(); // Добавляем вызов новой функции для GitHub-карточки
        } catch (error) {
            console.error('GooeyNav initialization error:', error);
        }
    }

    initTheme() {
        try {
            const savedTheme = localStorage.getItem('theme');
            const checkbox = document.getElementById('theme-checkbox');
            
            if (savedTheme === 'dark') {
                document.body.classList.add('dark-theme');
                if (checkbox) {
                    checkbox.checked = true;
                }
            } else {
                document.body.classList.remove('dark-theme');
                if (checkbox) {
                    checkbox.checked = false;
                }
            }
        } catch (error) {
            console.error('Theme initialization error:', error);
        }
    }

    setupThemeSwitch() {
        try {
            const checkbox = document.getElementById('theme-checkbox');
            if (!checkbox) return;

            checkbox.addEventListener('change', (e) => {
                const isDark = e.target.checked;
                document.body.classList.toggle('dark-theme', isDark);
                localStorage.setItem('theme', isDark ? 'dark' : 'light');
                
                document.dispatchEvent(new CustomEvent('themeChanged'));

                this.updateAllNavs();
            });
        } catch (error) {
            console.error('Theme switch setup error:', error);
        }
    }

    initNavContainers() {
        try {
            const containers = document.querySelectorAll('.gooey-nav-container');
            if (!containers.length) {
                console.warn('No gooey-nav-container elements found');
                return;
            }

            containers.forEach(container => {
                try {
                    const nav = {
                        container,
                        activeBg: this.createActiveBg(container),
                        particleContainer: this.createParticleContainer(container),
                        currentActiveLink: null
                    };
                    
                    this.setupNavLinks(nav);
                    this.navContainers.push(nav);
                } catch (error) {
                    console.error('Error initializing nav container:', error, container);
                }
            });
        } catch (error) {
            console.error('Nav containers initialization error:', error);
        }
    }

    createActiveBg(container) {
        try {
            const bg = document.createElement('div');
            bg.className = 'active-bg';
            container.appendChild(bg);
            return bg;
        } catch (error) {
            console.error('Error creating active background:', error);
            return null;
        }
    }

    createParticleContainer(container) {
        try {
            const particles = document.createElement('div');
            particles.className = 'particle-container';
            container.appendChild(particles);
            return particles;
        } catch (error) {
            console.error('Error creating particle container:', error);
            return null;
        }
    }

    setupNavLinks(nav) {
        if (!nav?.container) return;

        try {
            const links = nav.container.querySelectorAll('.gooey-nav a');
            if (!links.length) {
                console.warn('No navigation links found in container:', nav.container);
                return;
            }

            const currentPath = window.location.pathname;
            
            links.forEach(link => {
                try {
                    if (link.getAttribute('href') === currentPath) {
                        this.setActiveLink(nav, link);
                    }

                    link.addEventListener('click', (e) => {
                        e.preventDefault();
                        this.handleNavClick(e, nav);
                    });
                } catch (error) {
                    console.error('Error setting up nav link:', error, link);
                }
            });

            if (!nav.currentActiveLink && links.length > 0) {
                this.setActiveLink(nav, links[0]);
            }
        } catch (error) {
            console.error('Error setting up nav links:', error);
        }
    }

    setActiveLink(nav, link) {
        if (!nav || !link) return;

        try {
            if (nav.currentActiveLink) {
                nav.currentActiveLink.classList.remove('active');
            }
            link.classList.add('active');
            nav.currentActiveLink = link;
            this.updateActiveBg(nav);
        } catch (error) {
            console.error('Error setting active link:', error);
        }
    }

    handleNavClick(event, nav) {
        if (!event || !nav) return;

        try {
            const link = event.currentTarget;
            if (!link) return;

            this.setActiveLink(nav, link);
            this.createParticles(link, nav.particleContainer);

            setTimeout(() => {
                try {
                    if (link.href) {
                        window.location.href = link.href;
                    }
                } catch (error) {
                    console.error('Navigation error:', error);
                }
            }, 500);
        } catch (error) {
            console.error('Error handling nav click:', error);
        }
    }

    updateActiveBg(nav) {
        if (!nav?.currentActiveLink || !nav.activeBg) return;

        try {
            const linkRect = nav.currentActiveLink.getBoundingClientRect();
            const containerRect = nav.container.getBoundingClientRect();
            
            nav.activeBg.style.left = `${linkRect.left - containerRect.left}px`;
            nav.activeBg.style.width = `${linkRect.width}px`;
            
            const isDark = document.body.classList.contains('dark-theme');
            nav.activeBg.style.backgroundColor = isDark ? '#f0f0f0' : '#313131';
            
            nav.container.querySelectorAll('.gooey-nav a').forEach(l => {
                l.style.color = isDark ? '#e0e0e0' : '#313131';
            });
            nav.currentActiveLink.style.color = isDark ? '#1a1a1a' : '#fff';
        } catch (error) {
            console.error('Error updating active background:', error);
        }
    }

    createParticles(target, container) {
        if (!target || !container) return;

        try {
            const particleCount = 15;
            const targetRect = target.getBoundingClientRect();
            const centerX = targetRect.left + targetRect.width / 2;
            const centerY = targetRect.top + targetRect.height / 2;
            const colors = ['#4a90e2', '#bd10e0', '#f5a623', '#50e3c2'];

            for (let i = 0; i < particleCount; i++) {
                try {
                    const particle = document.createElement('div');
                    particle.className = 'particle';

                    const angle = Math.random() * 2 * Math.PI;
                    const radius = 50 + Math.random() * 40;
                    const startX = centerX + Math.cos(angle) * radius;
                    const startY = centerY + Math.sin(angle) * radius;
                    const time = 600 + Math.random() * 300;

                    particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                    particle.style.setProperty('--time', `${time}ms`);
                    
                    const containerRect = container.getBoundingClientRect();
                    particle.style.setProperty('--start-x', `${startX - containerRect.left}px`);
                    particle.style.setProperty('--start-y', `${startY - containerRect.top}px`);
                    particle.style.setProperty('--end-x', `${centerX - containerRect.left}px`);
                    particle.style.setProperty('--end-y', `${centerY - containerRect.top}px`);
                    
                    container.appendChild(particle);
                    setTimeout(() => {
                        try {
                            if (particle.parentNode === container) {
                                container.removeChild(particle);
                            }
                        } catch (error) {
                            console.error('Error removing particle:', error);
                        }
                    }, time);
                } catch (error) {
                    console.error('Error creating particle:', error);
                }
            }
        } catch (error) {
            console.error('Error creating particles:', error);
        }
    }

    updateAllNavs() {
        try {
            this.navContainers.forEach(nav => {
                try {
                    this.updateActiveBg(nav);
                } catch (error) {
                    console.error('Error updating nav:', error, nav);
                }
            });
        } catch (error) {
            console.error('Error updating all navs:', error);
        }
    }

    setupGithubCardHoverEffect() {
        const cardContainer = document.querySelector('.github-card-container');
        if (!cardContainer) return;

        const card = cardContainer.querySelector('.github-card');
        if (!card) return;

        cardContainer.addEventListener('mousemove', (e) => {
            const rect = cardContainer.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            card.style.setProperty('--x', `${x}px`);
            card.style.setProperty('--y', `${y}px`);
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    try {
        window.gooeyNav = new GooeyNav();
    } catch (error) {
        console.error('Failed to initialize GooeyNav:', error);
    }
});