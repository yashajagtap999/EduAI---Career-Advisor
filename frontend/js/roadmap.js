/* ── AI ROADMAP CONTROLLER ── */

document.addEventListener('DOMContentLoaded', async () => {
    const pathname = window.location.pathname.replace(/\.html$/, '');
    if (pathname !== '/roadmap') return;

    try {
        // Fetch stats to default the dropdown to predicted role if user scanned
        const stats = await Api.getStats().catch(() => ({ has_scan: false }));
        
        const roadmapSelect = document.getElementById('roadmap-role-select');
        if (roadmapSelect) {
            if (stats.has_scan && stats.predicted_role) {
                for (let option of roadmapSelect.options) {
                    if (stats.predicted_role.toLowerCase().includes(option.value.toLowerCase())) {
                        roadmapSelect.value = option.value;
                        break;
                    }
                }
            }

            // Initial render
            loadRoadmap(roadmapSelect.value);

            // Bind change listener
            roadmapSelect.addEventListener('change', () => {
                loadRoadmap(roadmapSelect.value);
            });
        }
    } catch(e) {
        console.error('Error loading roadmap page context:', e);
        loadRoadmap("Software Developer");
    }
});

async function loadRoadmap(role) {
    const semestersContainer = document.getElementById('roadmap-semesters-list');
    if (!semestersContainer) return;

    try {
        const data = await Api.getRoadmapAndReadiness(role);
        
        // Render Semesters 4-8 Timeline
        semestersContainer.innerHTML = '';
        data.roadmap.forEach((item, index) => {
            semestersContainer.innerHTML += `
                <div style="display: flex; gap: 16px; position: relative; margin-bottom: 8px;">
                    <!-- Line connector -->
                    ${index < data.roadmap.length - 1 ? `<div style="position: absolute; left: 16px; top: 32px; bottom: -24px; width: 2px; background-color: var(--border-color); z-index: 1;"></div>` : ''}
                    
                    <!-- Circle node -->
                    <div style="width: 32px; height: 32px; border-radius: 50%; background: var(--primary-gradient); color: #FFF; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; z-index: 2; flex-shrink: 0; box-shadow: var(--shadow-sm); border: 2px solid var(--bg-primary);">
                        ${item.semester.split(' ')[1]}
                    </div>
                    
                    <!-- Content -->
                    <div style="flex-grow: 1; background-color: var(--bg-secondary); padding: 14px 18px; border-radius: var(--radius-md); border: 1.5px solid var(--border-color);">
                        <h4 style="font-size: 14.5px; color: var(--text-primary); margin-bottom: 4px;">${item.title}</h4>
                        <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.5;">${item.details}</p>
                    </div>
                </div>
            `;
        });

    } catch (e) {
        console.error('Error loading roadmap:', e);
        semestersContainer.innerHTML = '<p style="color: var(--text-muted); font-style: italic;">Failed to load roadmap.</p>';
    }
}
