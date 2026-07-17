/* ── GLOBAL APPLICATION CONFIGURATION & ROUTING ── */

document.addEventListener('DOMContentLoaded', async () => {
    // 1. Session check & Page Guard
    const session = await Api.getSession().catch(() => ({ logged_in: false }));
    const rawPath = window.location.pathname;
    const pathname = rawPath.endsWith('.html') ? rawPath.slice(0, -5) : rawPath;

    const privateRoutes = ['/dashboard', '/roadmap', '/internships', '/resume', '/chatbot', '/college-finder', '/analytics', '/profile'];

    if (session.logged_in) {
        // Save details locally for access
        localStorage.setItem('username', session.username);
        localStorage.setItem('full_name', session.full_name);

        if (pathname === '/' || pathname === '/index') {
            updateLandingNavUI(session);
        } else if (pathname === '/login') {
            updateLoginNavUI(session);
        }
    } else {
        localStorage.removeItem('username');
        localStorage.removeItem('full_name');

        if (privateRoutes.includes(pathname)) {
            window.location.href = '/login';
            return;
        }
    }

    // 2. Inject Common UI Elements (Sidebar) if we are on a private dashboard page
    if (privateRoutes.includes(pathname)) {
        injectSidebar(session);
        setupSidebarEvents();
    }

    // 3. Theme Toggle Setup
    setupTheme();
});

// Dynamic Landing Page Nav update for active sessions
function updateLandingNavUI(session) {
    const loginBtn = document.getElementById('login-nav-btn');
    const signupBtn = document.getElementById('signup-nav-btn');

    if (loginBtn) {
        loginBtn.href = '/dashboard';
        loginBtn.textContent = 'Dashboard 🏠';
        loginBtn.className = 'btn-primary';
    }
    if (signupBtn) {
        signupBtn.href = '#';
        signupBtn.textContent = 'Logout 🚪';
        signupBtn.className = 'btn-secondary';
        signupBtn.style.boxShadow = 'none';
        signupBtn.onclick = async (e) => {
            e.preventDefault();
            await Api.logout();
            localStorage.removeItem('username');
            localStorage.removeItem('full_name');
            window.location.reload();
        };
    }

    const heroBtn = document.querySelector('.hero-left .btn-primary');
    if (heroBtn) {
        heroBtn.href = '/dashboard';
        heroBtn.textContent = 'Go to Dashboard 🚀';
    }
}

// Dynamic Login Page Banner update for active sessions
function updateLoginNavUI(session) {
    const alertBox = document.getElementById('alert-box');
    if (alertBox) {
        alertBox.style.display = 'block';
        alertBox.style.backgroundColor = 'rgba(59, 130, 246, 0.1)';
        alertBox.style.color = 'var(--primary-blue)';
        alertBox.style.border = '1px solid rgba(59, 130, 246, 0.3)';
        alertBox.innerHTML = `
            <span>Logged in as <strong>${session.full_name || session.username}</strong></span>
            <div style="margin-top: 8px; display: flex; gap: 8px;">
                <a href="/dashboard" class="btn-primary" style="padding: 6px 12px; font-size: 12px;">Go to Dashboard 🚀</a>
                <button id="session-logout-btn" class="btn-secondary" style="padding: 6px 12px; font-size: 12px;">Logout 🚪</button>
            </div>
        `;
        
        const logoutBtn = document.getElementById('session-logout-btn');
        if (logoutBtn) {
            logoutBtn.onclick = async () => {
                await Api.logout();
                localStorage.removeItem('username');
                localStorage.removeItem('full_name');
                window.location.reload();
            };
        }
    }
}

// Sidebar injection wrapper
function injectSidebar(session) {
    const sidebarContainer = document.getElementById('sidebar-container');
    if (!sidebarContainer) return;

    const rawPath = window.location.pathname;
    const pathname = rawPath.endsWith('.html') ? rawPath.slice(0, -5) : rawPath;
    const fullName = session.full_name || localStorage.getItem('full_name') || 'Student';
    const username = session.username || localStorage.getItem('username') || 'user';
    const initial = fullName.charAt(0).toUpperCase();

    const menuItems = [
        { path: '/dashboard', label: '🏠 Dashboard' },
        { path: '/roadmap', label: '🗺️ AI Roadmap' },
        { path: '/internships', label: '💼 Internships' },
        { path: '/chatbot', label: '🧠 AI Mentor' },
        { path: '/resume', label: '📄 Resume X-Ray' },
        { path: '/college-finder', label: '🎓 College Finder' },
        { path: '/analytics', label: '📊 Analytics' },
        { path: '/profile', label: '👤 Profile' }
    ];

    let menuHTML = '';
    menuItems.forEach(item => {
        const isActive = pathname === item.path ? 'class="active"' : '';
        // Extract emoji and label
        const parts = item.label.split(' ');
        const emoji = parts[0];
        const text = parts.slice(1).join(' ');
        
        menuHTML += `
            <li ${isActive}>
                <a href="${item.path}">
                    <span class="nav-icon">${emoji}</span>
                    <span class="nav-text">${text}</span>
                </a>
            </li>
        `;
    });

    sidebarContainer.innerHTML = `
        <div class="sidebar" id="sidebar">
            <div class="sidebar-header">
                <a href="/dashboard" class="logo">
                    <img src="/assets/images/eduai_premium_logo.png" alt="EduAI Logo" onerror="this.style.display='none'">
                    <span class="sidebar-title">EduAI.</span>
                </a>
                <p class="sidebar-subtitle" style="font-size: 11px; color: var(--text-muted); margin-top: 4px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; padding-left: 2px;">Your Career Co-Pilot</p>
            </div>
            <ul class="sidebar-menu">
                ${menuHTML}
            </ul>
            <div class="sidebar-footer">
                <div class="user-profile-widget" style="margin-bottom: 12px;">
                    <div class="user-avatar">${initial}</div>
                    <div class="user-info">
                        <p style="font-weight: 700; color: var(--text-primary); font-size: 14px; line-height: 1.2;">${fullName}</p>
                        <p style="font-size: 11px; color: var(--text-muted);">@${username}</p>
                    </div>
                </div>
                <!-- Dynamic theme toggle in sidebar -->
                <button id="sidebar-theme-toggle-btn" style="width: 100%; border: none; background: transparent; padding: 12px 14px; border-radius: var(--radius-md); text-align: left; color: var(--text-secondary); cursor: pointer; font-weight: 600; display: flex; align-items: center; gap: 10px; transition: var(--transition);">
                    <span id="sidebar-theme-icon">🌙</span>
                    <span class="nav-text" id="sidebar-theme-text">Dark Mode</span>
                </button>
                <button id="logout-btn" style="width: 100%; border: none; background: transparent; padding: 12px 14px; border-radius: var(--radius-md); text-align: left; margin-top: 8px; color: var(--danger); cursor: pointer; font-weight: 600; display: flex; align-items: center; gap: 10px;">
                    <span>🚪</span>
                    <span class="nav-text">Logout</span>
                </button>
            </div>
        </div>
    `;
}

function setupSidebarEvents() {
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async () => {
            if (confirm('Are you sure you want to log out?')) {
                await Api.logout();
                localStorage.removeItem('username');
                localStorage.removeItem('full_name');
                window.location.href = '/';
            }
        });
    }
    
    // Theme toggle binding in sidebar
    const themeBtn = document.getElementById('sidebar-theme-toggle-btn');
    if (themeBtn) {
        const currentTheme = localStorage.getItem('theme') || 'light';
        updateSidebarThemeUI(currentTheme);

        themeBtn.addEventListener('click', () => {
            const currentTheme = localStorage.getItem('theme') || 'light';
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            localStorage.setItem('theme', newTheme);
            document.documentElement.setAttribute('data-theme', newTheme);
            updateSidebarThemeUI(newTheme);

            // If we are on profile page, also update its buttons
            const lightProfileBtn = document.getElementById('theme-light-btn');
            const darkProfileBtn = document.getElementById('theme-dark-btn');
            if (lightProfileBtn && darkProfileBtn) {
                if (newTheme === 'light') {
                    lightProfileBtn.className = 'btn-primary';
                    darkProfileBtn.className = 'btn-secondary';
                    darkProfileBtn.style.boxShadow = 'none';
                } else {
                    lightProfileBtn.className = 'btn-secondary';
                    lightProfileBtn.style.boxShadow = 'none';
                    darkProfileBtn.className = 'btn-primary';
                }
            }
        });
    }

    // Add sidebar responsive toggle listener if logo or toggle element is clicked
    const logoLink = document.querySelector('.sidebar .logo');
    if (logoLink) {
        logoLink.addEventListener('click', (e) => {
            // Only collapse if on desktop view width
            if (window.innerWidth > 1024) {
                e.preventDefault();
                const sidebar = document.getElementById('sidebar');
                const wrapper = document.querySelector('.dashboard-wrapper');
                if (sidebar) {
                    sidebar.classList.toggle('collapsed');
                }
                if (wrapper) {
                    wrapper.classList.toggle('sidebar-collapsed');
                }
            }
        });
    }
}

function updateSidebarThemeUI(theme) {
    const icon = document.getElementById('sidebar-theme-icon');
    const text = document.getElementById('sidebar-theme-text');
    if (icon && text) {
        if (theme === 'light') {
            icon.textContent = '🌙';
            text.textContent = 'Dark Mode';
        } else {
            icon.textContent = '☀️';
            text.textContent = 'Light Mode';
        }
    }
}

// Manage Light/Dark Theme Setup
function setupTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
}
