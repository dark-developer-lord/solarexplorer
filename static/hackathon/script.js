document.addEventListener('DOMContentLoaded', () => {
    // Confetti Effect
    function launchConfetti() {
        confetti({
            particleCount: 150,
            spread: 90,
            origin: { y: 0.6 },
            colors: ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#23a6d5', '#23d5ab'],
            scalar: 1.2,
            drift: 0.1,
            gravity: 0.5
        });
    }

    // Success Trigger
    if (new URLSearchParams(window.location.search).get('success')) {
        launchConfetti();
        window.history.replaceState({}, document.title, window.location.pathname);
    }

    // User Indicator
    const userIndicator = document.querySelector('.user-indicator');
    if (userIndicator) {
        userIndicator.addEventListener('click', (e) => {
            e.stopPropagation();
            const menu = userIndicator.querySelector('.profile-menu');
            menu.classList.toggle('hidden');
            if (!menu.classList.contains('hidden')) {
                menu.querySelector('a').focus();
            }
        });
        userIndicator.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                userIndicator.click();
            }
        });
        document.addEventListener('click', () => {
            const menu = userIndicator.querySelector('.profile-menu');
            if (menu) menu.classList.add('hidden');
        });
    }

    // Modal Interactions
    const teamCards = document.querySelectorAll('.team-card');
    const modals = document.querySelectorAll('.modal');
    const closeButtons = document.querySelectorAll('.modal-close');

    teamCards.forEach(card => {
        card.addEventListener('click', (e) => {
            e.stopPropagation();
            const modalId = card.dataset.modal;
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('active');
                modal.style.display = 'flex';
                document.body.style.overflow = 'hidden';
                modal.querySelector('.modal-close').focus();
            }
        });
    });

    closeButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const modal = btn.closest('.modal');
            if (modal) {
                modal.classList.remove('active');
                setTimeout(() => {
                    modal.style.display = 'none';
                    document.body.style.overflow = 'auto';
                }, 400);
            }
        });
        btn.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                btn.click();
            }
        });
    });

    modals.forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
                setTimeout(() => {
                    modal.style.display = 'none';
                    document.body.style.overflow = 'auto';
                }, 400);
            }
        });
    });

    // Form Validation
    const forms = document.querySelectorAll('#register-form, #login-form');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('input', (e) => {
                const group = e.target.closest('.input-group');
                const error = group.querySelector('.input-error');
                const value = e.target.value;
                let isValid = true;
                let message = '';

                if (e.target.name === 'email' && value) {
                    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    isValid = emailRegex.test(value);
                    message = isValid ? '' : 'Invalid email.';
                } else if (e.target.name === 'username' && value.length < 3) {
                    isValid = value.length >= 3;
                    message = isValid ? '' : 'Username too short.';
                } else if (e.target.name.startsWith('password') && value) {
                    const strength = value.length >= 8 && /[A-Z]/.test(value) && /\d/.test(value);
                    isValid = strength;
                    message = isValid ? '' : 'Password too weak.';
                } else if (e.target.name === 'password2' && value) {
                    const pass1 = form.querySelector('input[name="password1"]').value;
                    isValid = value === pass1;
                    message = isValid ? '' : "Passwords don't match.";
                }

                group.classList.toggle('error', !isValid);
                error.textContent = message;
            });
        });
    });

    // Parallax Effect
    const parallaxBgs = document.querySelectorAll('.parallax-bg');
    window.addEventListener('scroll', () => {
        parallaxBgs.forEach(bg => {
            const speed = 0.5;
            const yPos = -(window.scrollY * speed);
            bg.style.transform = `translateY(${yPos}px)`;
        });
    });

    // NASA Charts
    new Chart(document.getElementById('kepler-chart'), {
        type: 'bar',
        data: {
            labels: ['Confirmed', 'Candidates'],
            datasets: [{
                label: 'Kepler KOI',
                data: [4000, 1000],
                backgroundColor: 'rgba(102, 126, 234, 0.5)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            animation: { duration: 1200, easing: 'easeOutQuart' },
            scales: { y: { beginAtZero: true } }
        }
    });

    new Chart(document.getElementById('tess-chart'), {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'TESS TOI',
                data: [{ x: 1, y: 5000 }, { x: 2, y: 6000 }, { x: 3, y: 5500 }],
                backgroundColor: 'rgba(240, 147, 251, 0.5)',
                borderColor: 'rgba(240, 147, 251, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            animation: { duration: 1200, easing: 'easeOutQuart' }
        }
    });

    new Chart(document.getElementById('k2-chart'), {
        type: 'line',
        data: {
            labels: ['2014', '2016', '2018'],
            datasets: [{
                label: 'K2 Discoveries',
                data: [100, 200, 300],
                backgroundColor: 'rgba(35, 213, 171, 0.5)',
                borderColor: 'rgba(35, 213, 171, 1)',
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            responsive: true,
            animation: { duration: 1200, easing: 'easeOutQuart' }
        }
    });

    new Chart(document.getElementById('size-chart'), {
        type: 'pie',
        data: {
            labels: ['Earth-size', 'Super-Earth', 'Neptune-size', 'Jupiter-size'],
            datasets: [{
                label: 'Exoplanet Sizes',
                data: [1500, 2000, 1000, 500],
                backgroundColor: [
                    'rgba(102, 126, 234, 0.5)',
                    'rgba(240, 147, 251, 0.5)',
                    'rgba(35, 213, 171, 0.5)',
                    'rgba(238, 119, 82, 0.5)'
                ],
                borderColor: [
                    'rgba(102, 126, 234, 1)',
                    'rgba(240, 147, 251, 1)',
                    'rgba(35, 213, 171, 1)',
                    'rgba(238, 119, 82, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            animation: { duration: 1200, easing: 'easeOutQuart' }
        }
    });

    // Demo Interaction
    const trialButton = document.getElementById('ai-trial-button');
    const demoPreview = document.getElementById('demo-preview');
    const demoSelect = document.getElementById('demo-select');
    const demoOutput = document.getElementById('demo-output');
    if (trialButton) {
        trialButton.addEventListener('click', () => {
            demoPreview.classList.toggle('hidden');
            if (!demoPreview.classList.contains('hidden')) {
                demoOutput.innerHTML = '<div class="skeleton chaos-loader spinner h-6 w-full"></div>';
                setTimeout(() => {
                    const selected = demoSelect.value;
                    demoOutput.innerHTML = `<p class="chaos-text">Chaos loading ${selected.toUpperCase()}... <span class="chaos-particle">✦</span></p>`;
                }, 1000);
            }
        });
        demoSelect.addEventListener('change', () => {
            demoOutput.innerHTML = '<div class="skeleton chaos-loader spinner h-6 w-full"></div>';
            setTimeout(() => demoOutput.textContent = `Chaos exploring ${demoSelect.value.toUpperCase()} vortex...`, 800);
        });
    }

    // Scroll Animations
    const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
    const chaosObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                chaosObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);
    document.querySelectorAll('.chaos-section, .chaos-card, .user-block').forEach(el => chaosObserver.observe(el));
});

// Utility Styles
const style = document.createElement('style');
style.textContent = `
    .chaos-loader { display: inline-block; width: 20px; height: 20px; border: 2px solid rgba(255,255,255,0.3); border-radius: 50%; border-top-color: var(--chaos-primary); animation: spin 1s ease-in-out infinite; }
    .spinner { animation-duration: 0.8s; }
    @keyframes spin { to { transform: rotate(360deg); } }
    .chaos-particle { animation: particleFloat 2s ease-in-out infinite; display: inline-block; }
    @keyframes particleFloat { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-5px); } }
`;
document.head.appendChild(style);