// counter.js
class Counter {
    constructor(element, value) {
        this.element = element;
        this.value = value;
        this.digits = [];
        this.init();
    }

    init() {
        const valueStr = this.value.toString();
        this.element.innerHTML = '';
        
        for (let i = 0; i < valueStr.length; i++) {
            const digitContainer = document.createElement('div');
            digitContainer.className = 'counter-digit';
            
            const numberSpan = document.createElement('span');
            numberSpan.className = 'counter-number';
            numberSpan.textContent = valueStr[i];
            
            digitContainer.appendChild(numberSpan);
            this.element.appendChild(digitContainer);
            this.digits.push(digitContainer);
        }
    }

    update(newValue) {
        const oldStr = this.value.toString();
        const newStr = newValue.toString();
        
        // Добавляем ведущие нули для выравнивания длин
        const maxLength = Math.max(oldStr.length, newStr.length);
        const oldPadded = oldStr.padStart(maxLength, '0');
        const newPadded = newStr.padStart(maxLength, '0');
        
        this.value = newValue;
        
        // Обновляем каждую цифру с анимацией
        for (let i = 0; i < maxLength; i++) {
            const oldDigit = parseInt(oldPadded[i]);
            const newDigit = parseInt(newPadded[i]);
            
            if (oldDigit !== newDigit) {
                this.animateDigit(this.digits[i], oldDigit, newDigit);
            }
        }
    }

    animateDigit(digitElement, oldDigit, newDigit) {
        digitElement.classList.add('animating');
        
        const currentNumber = digitElement.querySelector('.counter-number');
        const newNumber = currentNumber.cloneNode(true);
        newNumber.textContent = newDigit;
        newNumber.classList.add('new');
        
        digitElement.appendChild(newNumber);
        
        setTimeout(() => {
            digitElement.removeChild(currentNumber);
            newNumber.classList.remove('new');
            digitElement.classList.remove('animating');
        }, 500);
    }
}

// Функция для увеличения счетчика просмотров
async function incrementViews(newsId) {
    try {
        const response = await fetch(`/news/${newsId}/increment_views/`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            return data.views;
        }
    } catch (error) {
        console.error('Error incrementing views:', error);
    }
    return null;
}

// Функция для получения CSRF токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Инициализация счетчиков при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Создаем счетчики для каждого элемента просмотров
    const viewCounts = document.querySelectorAll('.views-count');
    const counters = new Map();
    
    viewCounts.forEach(element => {
        const initialValue = parseInt(element.dataset.views);
        const counter = new Counter(element, initialValue);
        counters.set(element, counter);
    });
    
    // Отслеживаем появление карточек в viewport
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const newsCard = entry.target;
                const newsId = newsCard.dataset.newsId;
                const viewsElement = newsCard.querySelector('.views-count');
                
                // Увеличиваем счетчик просмотров
                incrementViews(newsId).then(newViews => {
                    if (newViews !== null && counters.has(viewsElement)) {
                        counters.get(viewsElement).update(newViews);
                    }
                });
                
                // Прекращаем наблюдение после первого появления
                observer.unobserve(newsCard);
            }
        });
    }, {
        threshold: 0.5, // Срабатывает когда 50% элемента видно
        rootMargin: '0px 0px -100px 0px' // Не учитывает нижние 100px
    });
    
    // Начинаем наблюдение за карточками новостей
    const newsCards = document.querySelectorAll('.telegram-post-card');
    newsCards.forEach(card => {
        observer.observe(card);
    });
});

export { Counter };