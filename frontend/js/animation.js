/* ── INTERACTIVE ANIMATION CONTROLLER (GSAP / AOS) ── */

const Animations = {
    // 1. Initialize AOS (Animate on Scroll)
    initScrollReveal() {
        if (typeof AOS !== 'undefined') {
            AOS.init({
                duration: 800,
                easing: 'ease-in-out',
                once: true,
                offset: 50
            });
        }
    },

    // 2. Typewriter Effect using GSAP
    typewriter(elementId, text, speed = 0.08) {
        const element = document.getElementById(elementId);
        if (!element || typeof gsap === 'undefined') return;

        element.innerHTML = '';
        const chars = text.split('');
        
        chars.forEach((char) => {
            const span = document.createElement('span');
            span.textContent = char;
            span.style.opacity = 0;
            element.appendChild(span);
        });

        gsap.to(element.children, {
            opacity: 1,
            stagger: speed,
            duration: 0.1,
            ease: "none"
        });
    },

    // 3. Floating Parallax effect for mouse movements
    setupMouseParallax(containerClass, targetClass, depthFactor = 0.03) {
        const container = document.querySelector(containerClass);
        const targets = document.querySelectorAll(targetClass);

        if (!container || targets.length === 0) return;

        container.addEventListener('mousemove', (e) => {
            const width = window.innerWidth;
            const height = window.innerHeight;
            const mouseX = e.clientX - width / 2;
            const mouseY = e.clientY - height / 2;

            targets.forEach((target, index) => {
                const depth = (index + 1) * depthFactor;
                const moveX = mouseX * depth;
                const moveY = mouseY * depth;
                
                if (typeof gsap !== 'undefined') {
                    gsap.to(target, {
                        x: moveX,
                        y: moveY,
                        duration: 0.6,
                        ease: "power2.out"
                    });
                } else {
                    target.style.transform = `translate(${moveX}px, ${moveY}px)`;
                }
            });
        });
    },

    // 4. Statistics counter animation
    animateCounter(elementId, targetValue, durationMs = 1500) {
        const element = document.getElementById(elementId);
        if (!element) return;

        let start = 0;
        const end = parseInt(targetValue, 10);
        if (isNaN(end)) {
            element.textContent = targetValue;
            return;
        }

        const stepTime = Math.abs(Math.floor(durationMs / end));
        const timer = setInterval(() => {
            start += Math.ceil(end / 30); // Increment 30 steps
            if (start >= end) {
                element.textContent = end;
                clearInterval(timer);
            } else {
                element.textContent = start;
            }
        }, Math.max(stepTime, 25));
    }
};

// Auto-run on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    Animations.initScrollReveal();
});
