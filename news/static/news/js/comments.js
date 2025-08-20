document.addEventListener('DOMContentLoaded', function() {
    // --- Selectors ---
    const imageBtn = document.getElementById('image-btn');
    const fileInput = document.getElementById('file-input');
    const imageModal = document.querySelector('.image-modal');
    const imagePreview = document.querySelector('.image-preview');
    const modalSendBtn = document.querySelector('.btn-modal-send');
    const modalCancelBtn = document.querySelector('.btn-modal-cancel');
    const commentForm = document.querySelector('.comment-form');
    const commentInputField = document.querySelector('.comment-input-area textarea');
    const commentsContainer = document.querySelector('.comments-container');
    const voiceDurationInput = document.getElementById('voice-duration-input');

    const voiceBtn = document.getElementById('voice-btn');
    const voiceModal = document.querySelector('.voice-modal');
    const voiceVisualizer = document.getElementById('voice-visualizer');
    const voiceRecordBtn = document.getElementById('voice-record-btn');
    const voiceStopBtn = document.getElementById('voice-stop-btn');
    const voiceSendBtn = document.getElementById('voice-send-btn');
    const voiceCancelBtn = document.getElementById('voice-cancel-btn');
    const voiceDurationDisplay = voiceModal.querySelector('.voice-duration');

    let audioStream = null;
    let mediaRecorder = null;
    let audioChunks = [];
    let audioContext = null;
    let analyser = null;
    let visualizerLoop = null;
    let timerInterval = null;
    let startTime = 0;
    let recordedDuration = 0;

    // Function to format seconds into MM:SS format
    function formatTime(seconds) {
        if (seconds === null || seconds === undefined || isNaN(seconds)) return "0:00";
        
        try {
            seconds = parseInt(seconds);
            const minutes = Math.floor(seconds / 60);
            const remainingSeconds = Math.floor(seconds % 60);
            const formattedSeconds = remainingSeconds < 10 ? `0${remainingSeconds}` : remainingSeconds;
            return `${minutes}:${formattedSeconds}`;
        } catch (error) {
            return "0:00";
        }
    }

    // Function to update all duration displays on page load
    function updateAllDurations() {
        document.querySelectorAll('.voice-duration').forEach(element => {
            const duration = element.dataset.duration || element.textContent;
            element.textContent = formatTime(duration);
        });
    }

    // Функция для показа сообщений
    function showMessage(message, isError = true) {
        console.log(isError ? 'Ошибка:' : 'Успех:', message);
        
        // Создаем элемент для сообщения
        const messageDiv = document.createElement('div');
        messageDiv.className = isError ? 'error-message' : 'success-message';
        messageDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px;
            border-radius: 5px;
            color: white;
            z-index: 10000;
            max-width: 300px;
            ${isError ? 'background-color: #ff4757;' : 'background-color: #2ed573;'}
        `;
        messageDiv.textContent = message;
        
        document.body.appendChild(messageDiv);
        
        // Удаляем сообщение через 5 секунд
        setTimeout(() => {
            if (document.body.contains(messageDiv)) {
                document.body.removeChild(messageDiv);
            }
        }, 5000);
    }

    // --- Image Modal Logic ---
    if (imageBtn) {
        imageBtn.addEventListener('click', function() {
            fileInput.click();
        });
    }

    fileInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                imageModal.classList.add('active');
            };
            reader.readAsDataURL(file);
        }
    });

    if (modalCancelBtn) {
        modalCancelBtn.addEventListener('click', function() {
            imageModal.classList.remove('active');
            fileInput.value = '';
            imageModal.querySelector('.comment-field').value = '';
        });
    }

    if (modalSendBtn) {
        modalSendBtn.addEventListener('click', function() {
            const commentText = imageModal.querySelector('.comment-field').value;
            const file = fileInput.files[0];
            if (file) {
                sendComment(commentText, file, 'image');
                imageModal.classList.remove('active');
                fileInput.value = '';
                imageModal.querySelector('.comment-field').value = '';
            }
        });
    }

    // --- Voice Modal Logic ---
    if (voiceBtn) {
        voiceBtn.addEventListener('click', () => {
            voiceModal.style.display = 'flex';
            resetVoiceModal();
        });
    }

    function resetVoiceModal() {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
        }
        if (audioStream) {
            audioStream.getTracks().forEach(track => track.stop());
        }
        audioChunks = [];
        if (visualizerLoop) {
            cancelAnimationFrame(visualizerLoop);
        }
        if (timerInterval) {
            clearInterval(timerInterval);
        }
        voiceRecordBtn.style.display = 'inline-block';
        voiceStopBtn.style.display = 'none';
        voiceSendBtn.style.display = 'none';
        voiceDurationDisplay.textContent = '0:00';
        recordedDuration = 0;
        if (voiceVisualizer) {
            const canvasCtx = voiceVisualizer.getContext('2d');
            canvasCtx.clearRect(0, 0, voiceVisualizer.width, voiceVisualizer.height);
        }
    }

    // Voice Record Button
    if (voiceRecordBtn) {
        voiceRecordBtn.addEventListener('click', async () => {
            try {
                audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
                voiceRecordBtn.style.display = 'none';
                voiceStopBtn.style.display = 'inline-block';
                voiceSendBtn.style.display = 'none';

                mediaRecorder = new MediaRecorder(audioStream, { mimeType: 'audio/webm' });

                mediaRecorder.ondataavailable = event => {
                    audioChunks.push(event.data);
                };
                
                mediaRecorder.start();
                
                startTime = Date.now();
                timerInterval = setInterval(() => {
                    const elapsedTime = Date.now() - startTime;
                    recordedDuration = Math.floor(elapsedTime / 1000);
                    voiceDurationDisplay.textContent = formatTime(recordedDuration);
                }, 1000);

                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                analyser = audioContext.createAnalyser();
                analyser.fftSize = 256;
                analyser.smoothingTimeConstant = 0.2;

                const source = audioContext.createMediaStreamSource(audioStream);
                source.connect(analyser);

                drawVisualizer();

            } catch (error) {
                console.error('Error accessing microphone:', error);
                showMessage('Не удалось получить доступ к микрофону. Пожалуйста, разрешите доступ. ' + error.name);
                voiceModal.style.display = 'none';
            }
        });
    }

    // Voice Stop Button
    if (voiceStopBtn) {
        voiceStopBtn.addEventListener('click', () => {
            if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                mediaRecorder.stop();
            }
            if (audioStream) {
                audioStream.getTracks().forEach(track => track.stop());
            }
            if (visualizerLoop) {
                cancelAnimationFrame(visualizerLoop);
            }
            if (timerInterval) {
                clearInterval(timerInterval);
            }
            voiceStopBtn.style.display = 'none';
            voiceRecordBtn.style.display = 'none';
            voiceSendBtn.style.display = 'inline-block';
        });
    }

    // Voice Cancel Button
    if (voiceCancelBtn) {
        voiceCancelBtn.addEventListener('click', () => {
            resetVoiceModal();
            voiceModal.style.display = 'none';
        });
    }

    // Voice Send Button
    if (voiceSendBtn) {
        voiceSendBtn.addEventListener('click', () => {
            if (audioChunks.length > 0) {
                // Сохраняем длительность в скрытое поле формы
                voiceDurationInput.value = recordedDuration;
                
                const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                sendComment('', audioBlob, 'audio');
            }
            voiceModal.style.display = 'none';
            audioChunks = [];
        });
    }

    // Function to draw the voice visualizer
    function drawVisualizer() {
        if (!voiceVisualizer || !analyser) return;
        const canvas = voiceVisualizer;
        const canvasCtx = canvas.getContext('2d');
        const bufferLength = analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);

        canvasCtx.clearRect(0, 0, canvas.width, canvas.height);

        const draw = () => {
            visualizerLoop = requestAnimationFrame(draw);
            analyser.getByteFrequencyData(dataArray);

            canvasCtx.fillStyle = 'rgba(43, 82, 120, 0.5)';
            canvasCtx.fillRect(0, 0, canvas.width, canvas.height);

            const barWidth = (canvas.width / bufferLength) * 2;
            let barHeight;
            let x = 0;

            for(let i = 0; i < bufferLength; i++) {
                barHeight = dataArray[i] / 2;
                canvasCtx.fillStyle = '#52a4e8';
                canvasCtx.fillRect(x, (canvas.height - barHeight) / 2, barWidth, barHeight);
                x += barWidth + 1;
            }
        };
        draw();
    }

    // --- Form Submission ---
    if(commentForm) {
        commentForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const commentText = commentInputField.value.trim();
            if (commentText) {
                // Сбрасываем длительность для текстовых сообщений
                voiceDurationInput.value = 0;
                sendComment(commentText, null, 'text');
                commentInputField.value = '';
            }
        });
    }

    async function sendComment(text, file, type) {
        const formData = new FormData();
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        if (!csrfToken) {
            showMessage('Ошибка безопасности. Пожалуйста, перезагрузите страницу.');
            return;
        }
        
        formData.append('csrfmiddlewaretoken', csrfToken);
        formData.append('comment_text', text);
        
        // Добавляем длительность для голосовых сообщений
        if (type === 'audio') {
            formData.append('voice_duration', voiceDurationInput.value);
        }

        if (type === 'image') {
            if (file) {
                formData.append('image', file);
            } else {
                showMessage('Ошибка: файл изображения не выбран');
                return;
            }
        } else if (type === 'audio') {
            if (file) {
                formData.append('audio', file, 'voice_message.webm');
            } else {
                showMessage('Ошибка: аудиофайл не создан');
                return;
            }
        }

        const url = commentForm.action;

        try {
            showMessage('Отправка комментария...', false);
            
            const response = await fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            // Проверяем статус ответа
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP error! status: ${response.status}, response: ${errorText}`);
            }

            const result = await response.json();
            
            if (result.status === 'success') {
                if (result.comment_html) {
                    appendNewComment(result.comment_html);
                    commentInputField.value = '';
                    voiceDurationInput.value = '0';
                }
            } else {
                showMessage(result.message || 'Ошибка при отправке комментария');
            }
        } catch (error) {
            console.error('Network error:', error);
            if (error.name === 'TypeError') {
                showMessage('Ошибка сети. Проверьте подключение к интернету.');
            } else if (error.name === 'SyntaxError') {
                showMessage('Ошибка обработки ответа сервера.');
            } else {
                showMessage('Произошла непредвиденная ошибка: ' + error.message);
            }
        }
    }

    function appendNewComment(commentHtml) {
        try {
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = commentHtml;
            const newComment = tempDiv.firstChild;
            
            if (newComment) {
                commentsContainer.appendChild(newComment);
                commentsContainer.scrollTop = commentsContainer.scrollHeight;

                // Обновляем длительность для голосовых сообщений
                const newVoiceBtn = newComment.querySelector('.voice-play-btn');
                if (newVoiceBtn) {
                    initVoicePlayback(newVoiceBtn);
                }
                
                // Показываем сообщение об успехе
                showMessage('Комментарий успешно добавлен!', false);
            }
        } catch (error) {
            console.error('Error appending comment:', error);
            showMessage('Ошибка при отображении комментария');
        }
    }
    
    // Function to initialize playback for a single voice message
    function initVoicePlayback(button) {
        const audioUrl = button.dataset.audioUrl;
        
        if (!audioUrl) {
            console.error('No audio URL found');
            return;
        }
        
        const audio = new Audio(audioUrl);
        let audioContext, analyser, visualizerDisplay, playbackLoop;

        visualizerDisplay = button.closest('.voice-message-container').querySelector('.voice-visualizer-display');
        const durationSpan = button.closest('.voice-message-container').querySelector('.voice-duration');
        
        // Форматируем длительность
        if (durationSpan.dataset.duration) {
            durationSpan.textContent = formatTime(durationSpan.dataset.duration);
        }
        
        button.addEventListener('click', () => {
            if (!audioContext) {
                try {
                    audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    const source = audioContext.createMediaElementSource(audio);
                    analyser = audioContext.createAnalyser();
                    source.connect(analyser);
                    analyser.connect(audioContext.destination);
                } catch (error) {
                    console.error('Error creating audio context:', error);
                    // Просто воспроизводим без визуализации
                    if (audio.paused) {
                        audio.play();
                        button.innerHTML = '<i class="fas fa-pause"></i>';
                    } else {
                        audio.pause();
                        button.innerHTML = '<i class="fas fa-play"></i>';
                    }
                    return;
                }
            }

            if (audio.paused) {
                audioContext.resume().then(() => {
                    audio.play();
                    button.innerHTML = '<i class="fas fa-pause"></i>';
                    if (analyser && visualizerDisplay) {
                        drawPlaybackVisualizer(visualizerDisplay, analyser);
                    }
                }).catch(error => {
                    console.error('Error resuming audio:', error);
                    audio.play();
                    button.innerHTML = '<i class="fas fa-pause"></i>';
                });
            } else {
                audio.pause();
                button.innerHTML = '<i class="fas fa-play"></i>';
                if (playbackLoop) {
                    cancelAnimationFrame(playbackLoop);
                }
            }
        });

        audio.addEventListener('ended', () => {
            button.innerHTML = '<i class="fas fa-play"></i>';
            if (playbackLoop) {
                cancelAnimationFrame(playbackLoop);
            }
            if (visualizerDisplay) {
                const canvasCtx = visualizerDisplay.getContext('2d');
                canvasCtx.clearRect(0, 0, visualizerDisplay.width, visualizerDisplay.height);
                canvasCtx.fillStyle = 'rgba(43, 82, 120, 0.5)';
                canvasCtx.fillRect(0, 0, visualizerDisplay.width, visualizerDisplay.height);
            }
        });

        function drawPlaybackVisualizer(canvas, analyser) {
            if (!canvas || !analyser) return;
            const canvasCtx = canvas.getContext('2d');
            const bufferLength = analyser.frequencyBinCount;
            const dataArray = new Uint8Array(bufferLength);
            
            const draw = () => {
                playbackLoop = requestAnimationFrame(draw);
                analyser.getByteFrequencyData(dataArray);
                canvasCtx.clearRect(0, 0, canvas.width, canvas.height);
                canvasCtx.fillStyle = 'rgba(43, 82, 120, 0.5)';
                canvasCtx.fillRect(0, 0, canvas.width, canvas.height);
                const barWidth = (canvas.width / bufferLength) * 2;
                let barHeight;
                let x = 0;
                for(let i = 0; i < bufferLength; i++) {
                    barHeight = dataArray[i] / 2;
                    canvasCtx.fillStyle = '#52a4e8';
                    canvasCtx.fillRect(x, (canvas.height - barHeight) / 2, barWidth, barHeight);
                    x += barWidth + 1;
                }
            };
            draw();
        }
    }

    // Initialize playback for all existing voice messages on page load
    const voicePlayBtns = document.querySelectorAll('.voice-play-btn');
    voicePlayBtns.forEach(button => {
        initVoicePlayback(button);
    });

    // Update all durations on page load
    updateAllDurations();
});