/* ── STUDENT DASHBOARD CONTROLLER ── */

document.addEventListener('DOMContentLoaded', async () => {
    // Make sure we are on dashboard page
    const pathname = window.location.pathname.replace(/\.html$/, '');
    if (pathname !== '/dashboard') return;

    try {
        // 1. Fetch dashboard metrics
        const stats = await Api.getStats();
        renderDashboardStats(stats);

        // 2. Fetch chart data & render
        const chartsData = await Api.getCharts();
        renderDashboardCharts(chartsData);

        // 3. Load Placement Readiness score details
        const predictedRole = (stats.has_scan && stats.predicted_role) ? stats.predicted_role : "Software Developer";
        loadDashboardReadiness(predictedRole);

    } catch (e) {
        console.error('Error loading dashboard:', e);
        // Show scan CTA if no data
        showScanCTA();
    }
});

function renderDashboardStats(stats) {
    if (!stats.has_scan) {
        showScanCTA();
        return;
    }

    // Hide scan warning overlay if it exists
    const scanWarning = document.getElementById('scan-warning-overlay');
    if (scanWarning) scanWarning.style.display = 'none';

    // Animate KPI counters
    Animations.animateCounter('ats-score-value', stats.ats_score);
    Animations.animateCounter('skills-count-value', stats.skills_count);
    
    // Set text values
    const roleEl = document.getElementById('predicted-role-value');
    if (roleEl) roleEl.textContent = stats.predicted_role;

    Animations.animateCounter('readiness-value', stats.readiness);

    // Animate metric progress bars
    setProgressBar('ats-progress-fill', stats.ats_score);
    setProgressBar('skills-progress-fill', Math.min(stats.skills_count * 10, 100));
    setProgressBar('readiness-progress-fill', stats.readiness);
}

function setProgressBar(elementId, value) {
    const el = document.getElementById(elementId);
    if (el) {
        setTimeout(() => {
            el.style.width = `${value}%`;
        }, 150);
    }
}

function renderDashboardCharts(chartsData) {
    // 1. Render Radar Chart
    if (chartsData.radar && chartsData.radar.values.some(v => v > 0)) {
        Charts.createRadar('radar-chart-canvas', chartsData.radar.categories, chartsData.radar.values);
    } else {
        showEmptyChartPlaceholder('radar-chart-canvas');
    }

    // 2. Render Score History Chart
    if (chartsData.history && chartsData.history.length > 0) {
        const labels = chartsData.history.map(item => item.scan);
        const dataPoints = chartsData.history.map(item => item.score);
        Charts.createAreaHistory('history-chart-canvas', labels, dataPoints);
    } else {
        showEmptyChartPlaceholder('history-chart-canvas');
    }

    // 3. Render Top Career Suggestions
    const suggestionsContainer = document.getElementById('career-suggestions-list');
    if (suggestionsContainer && chartsData.career_suggestions) {
        suggestionsContainer.innerHTML = '';
        chartsData.career_suggestions.forEach(item => {
            suggestionsContainer.innerHTML += `
                <div class="dash-list-item">
                    <div class="list-item-meta">
                        <span class="list-item-title">${item.title}</span>
                        <span class="list-item-subtitle">${item.description}</span>
                    </div>
                    <span class="list-item-badge badge-green">${item.match}% Match</span>
                </div>
            `;
        });
    }

    // 4. Render Skill Progress Bars
    const skillsContainer = document.getElementById('skills-progress-list');
    if (skillsContainer && chartsData.radar) {
        skillsContainer.innerHTML = '';
        const cats = chartsData.radar.categories;
        const vals = chartsData.radar.values;
        
        cats.forEach((cat, index) => {
            const val = vals[index];
            const colors = ['badge-green', 'badge-orange', 'badge-red'];
            const badgeClass = colors[index % colors.length];

            skillsContainer.innerHTML += `
                <div style="margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 13px; font-weight: 600;">
                        <span style="color: var(--text-primary);">${cat} Skills</span>
                        <span class="list-item-badge ${badgeClass}">${val}% Mastery</span>
                    </div>
                    <div class="metric-progress" style="margin-top: 0; background-color: var(--border-color);">
                        <div class="metric-progress-fill" style="width: ${val}%; background: var(--accent-gradient);"></div>
                    </div>
                </div>
            `;
        });
    }
}

async function loadDashboardReadiness(role) {
    const breakdownContainer = document.getElementById('readiness-breakdown-list');
    const overallBadge = document.getElementById('readiness-overall-badge');
    
    if (!breakdownContainer) return;

    try {
        const data = await Api.getRoadmapAndReadiness(role);
        const scores = data.readiness;
        
        // Update Overall Badge
        if (overallBadge) {
            overallBadge.textContent = `Overall: ${scores.overall}%`;
            overallBadge.className = scores.overall >= 80 ? 'list-item-badge badge-green' : (scores.overall >= 60 ? 'list-item-badge badge-orange' : 'list-item-badge badge-red');
        }

        breakdownContainer.innerHTML = '';
        const metricsList = [
            { name: '📝 Resume Match Score', value: scores.resume, color: '#10B981' },
            { name: '🛠️ Technical Skills Base', value: scores.skills, color: '#3B82F6' },
            { name: '💻 Project Quality Index', value: scores.projects, color: '#8B5CF6' },
            { name: '⚡ Coding Proficiency Test', value: scores.coding, color: '#06B6D4' },
            { name: '🗣️ Communication & Leadership', value: scores.communication, color: '#F59E0B' }
        ];

        metricsList.forEach(m => {
            breakdownContainer.innerHTML += `
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; font-weight: 600; margin-bottom: 6px;">
                        <span style="color: var(--text-primary);">${m.name}</span>
                        <span style="color: ${m.color}; font-weight: 800;">${m.value}%</span>
                    </div>
                    <div class="metric-progress" style="margin-top: 0; background-color: var(--border-color); height: 8px;">
                        <div class="metric-progress-fill" style="width: ${m.value}%; background-color: ${m.color};"></div>
                    </div>
                </div>
            `;
        });

    } catch (e) {
        console.error('Error loading dashboard readiness:', e);
        breakdownContainer.innerHTML = '<p style="color: var(--text-muted); font-style: italic;">Failed to load readiness scores.</p>';
    }
}

function showScanCTA() {
    const scanWarning = document.getElementById('scan-warning-overlay');
    if (scanWarning) {
        scanWarning.style.display = 'flex';
    }
    
    // Set zeros for metrics
    const elements = ['ats-score-value', 'skills-count-value', 'readiness-value'];
    elements.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.textContent = '--';
    });
    
    const roleEl = document.getElementById('predicted-role-value');
    if (roleEl) roleEl.textContent = 'Not Predicted';

    showEmptyChartPlaceholder('radar-chart-canvas');
    showEmptyChartPlaceholder('history-chart-canvas');

    // Load default Software Developer readiness scores
    loadDashboardReadiness("Software Developer");
}

function showEmptyChartPlaceholder(canvasId) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    const parent = canvas.parentElement;
    parent.innerHTML = `
        <div style="height: 250px; display: flex; flex-direction: column; align-items: center; justify-content: center; color: var(--text-muted);">
            <span style="font-size: 40px; margin-bottom: 12px;">📊</span>
            <p style="font-size: 13px; font-weight: 600;">No scan data available. Scan your resume first!</p>
            <a href="/resume" class="btn-primary" style="padding: 8px 16px; font-size: 12px; margin-top: 14px;">Scan Now 🚀</a>
        </div>
    `;
}
