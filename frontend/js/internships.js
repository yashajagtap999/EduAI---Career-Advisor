/* ── INTERNSHIP RECOMMENDATION ENGINE CONTROLLER ── */

document.addEventListener('DOMContentLoaded', async () => {
    if (window.location.pathname !== '/internships') return;

    const form = document.getElementById('internship-form');
    const branchSelect = document.getElementById('internship-branch');
    const cgpaInput = document.getElementById('internship-cgpa');
    const locationInput = document.getElementById('internship-location');
    const skillsInput = document.getElementById('internship-skills');
    
    const loadingEl = document.getElementById('internships-loading');
    const emptyEl = document.getElementById('internships-empty');
    const listContainer = document.getElementById('internships-list');

    // Upload Elements
    const uploadZone = document.getElementById('internship-upload-zone');
    const fileInput = document.getElementById('internship-resume-file');
    const uploadProgress = document.getElementById('internship-upload-progress');

    let isResumeSearch = false;
    let isAutoSubmit = false;
    let scannedRole = '';

    // 1. Try to auto-populate and trigger matching from scanned resume on page load
    try {
        const stats = await Api.getStats().catch(() => ({ has_scan: false }));
        if (stats.has_scan) {
            isResumeSearch = true;
            scannedRole = stats.predicted_role || 'Selected Domain';
            
            // Select domain option matching predicted role
            if (stats.predicted_role) {
                const roleLower = stats.predicted_role.toLowerCase();
                for (let option of branchSelect.options) {
                    if (roleLower.includes(option.value.toLowerCase()) || option.value.toLowerCase().includes(roleLower)) {
                        branchSelect.value = option.value;
                        break;
                    }
                }
            }

            // Fetch actual scanned skills (not chart categories)
            if (stats.skills && stats.skills.length > 0) {
                skillsInput.value = stats.skills.join(', ');
            }

            // Set default CGPA if empty
            if (!cgpaInput.value) {
                cgpaInput.value = "8.0";
            }

            // Auto-trigger search using resume profile
            isAutoSubmit = true;
            form.dispatchEvent(new Event('submit'));
        }
    } catch (e) {
        console.error('Error pre-populating fields:', e);
    }

    // 2. Drag & Drop File Upload Handlers
    if (uploadZone && fileInput) {
        uploadZone.addEventListener('click', () => fileInput.click());

        uploadZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadZone.style.borderColor = 'var(--primary-blue)';
            uploadZone.style.backgroundColor = 'rgba(79, 70, 229, 0.05)';
        });

        uploadZone.addEventListener('dragleave', () => {
            uploadZone.style.borderColor = 'var(--border-color)';
            uploadZone.style.backgroundColor = 'var(--bg-primary)';
        });

        uploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadZone.style.borderColor = 'var(--border-color)';
            uploadZone.style.backgroundColor = 'var(--bg-primary)';
            if (e.dataTransfer.files.length > 0) {
                handleResumeUpload(e.dataTransfer.files[0]);
            }
        });

        fileInput.addEventListener('change', () => {
            if (fileInput.files.length > 0) {
                handleResumeUpload(fileInput.files[0]);
            }
        });
    }

    async function handleResumeUpload(file) {
        if (!uploadProgress || !uploadZone) return;
        uploadProgress.style.display = 'flex';
        uploadZone.style.opacity = '0.5';

        try {
            const data = await Api.scanResume(file);
            uploadProgress.style.display = 'none';
            uploadZone.style.opacity = '1';

            if (data.success) {
                // Populate forms dynamically from scanned result
                isResumeSearch = true;
                scannedRole = data.predicted_role || 'Selected Domain';

                // Select domain
                const roleLower = scannedRole.toLowerCase();
                let foundMatch = false;
                for (let option of branchSelect.options) {
                    if (roleLower.includes(option.value.toLowerCase()) || option.value.toLowerCase().includes(roleLower)) {
                        branchSelect.value = option.value;
                        foundMatch = true;
                        break;
                    }
                }
                
                // Fallback: If no exact match, select a general tech role or keep current
                if (!foundMatch && (roleLower.includes('developer') || roleLower.includes('engineer'))) {
                    branchSelect.value = "Web Developer";
                }

                // Populate skills
                if (data.matched_skills && data.matched_skills.length > 0) {
                    skillsInput.value = data.matched_skills.join(', ');
                }

                if (!cgpaInput.value) {
                    cgpaInput.value = "8.0";
                }

                // Auto trigger submit
                isAutoSubmit = true;
                form.dispatchEvent(new Event('submit'));
            } else {
                alert("Scan failed: " + (data.error || "Unknown error"));
            }
        } catch (err) {
            uploadProgress.style.display = 'none';
            uploadZone.style.opacity = '1';
            console.error("Error uploading resume:", err);
            alert("Failed to upload and scan resume.");
        }
    }

    // 3. Handle search submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (!isAutoSubmit) {
            isResumeSearch = false;
        }
        isAutoSubmit = false; // Reset for manual queries

        const branch = branchSelect.value;
        const cgpa = parseFloat(cgpaInput.value);
        const location = locationInput.value.trim();
        const skillsRaw = skillsInput.value;
        
        // Parse skills array
        const skillsArray = skillsRaw.split(',').map(s => s.trim()).filter(s => s.length > 0);

        // UI states
        loadingEl.style.display = 'flex';
        emptyEl.style.display = 'none';
        listContainer.innerHTML = '';

        try {
            const data = await Api.recommendInternships(skillsArray, cgpa, location, branch);
            loadingEl.style.display = 'none';

            if (data.error) {
                listContainer.innerHTML = `
                    <div style="color: var(--danger); font-weight: 600; padding: 20px; text-align: center; font-size: 13px;">
                        ⚠️ ${data.error}
                    </div>
                `;
                return;
            }

            if (!data.results || data.results.length === 0) {
                listContainer.innerHTML = `
                    <div style="color: var(--text-muted); font-style: italic; padding: 40px; text-align: center; font-size: 13px;">
                        No internships matching your criteria were found on Adzuna. Try adjusting your location or skills!
                    </div>
                `;
                return;
            }

            // Render matching banner if resume search was used
            if (isResumeSearch) {
                listContainer.innerHTML = `
                    <div class="resume-match-banner" style="background: linear-gradient(135deg, rgba(79, 70, 229, 0.12), rgba(139, 92, 246, 0.12)); border: 1.5px solid rgba(139, 92, 246, 0.25); border-radius: var(--radius-md); padding: 14px 18px; margin-bottom: 20px; display: flex; align-items: center; gap: 14px; animation: slideIn 0.4s ease-out; width: 100%;">
                        <span style="font-size: 24px; filter: drop-shadow(0 0 4px rgba(139, 92, 246, 0.4));">🧠</span>
                        <div>
                            <h4 style="font-size: 13.5px; color: var(--text-primary); margin: 0; font-weight: 700;">Resume Profile Matching Active</h4>
                            <p style="font-size: 12px; color: var(--text-secondary); margin: 2px 0 0 0;">Opportunities matched with your scanned resume, optimized for: <strong>${scannedRole}</strong>.</p>
                        </div>
                    </div>
                `;
            }

            // Render internship items
            data.results.forEach(job => {
                listContainer.innerHTML += `
                    <div class="dash-list-item" style="flex-direction: column; align-items: flex-start; gap: 12px; padding: 18px; border: 1.5px solid var(--border-color); border-radius: var(--radius-md); background-color: var(--bg-secondary); margin-bottom: 12px; width: 100%;">
                        <div style="display: flex; justify-content: space-between; align-items: center; width: 100%; flex-wrap: wrap; gap: 8px;">
                            <div>
                                <h4 style="font-size: 15px; color: var(--text-primary); margin: 0;">${job.title}</h4>
                                <p style="font-size: 12.5px; color: var(--text-secondary); margin: 2px 0 0 0;">🏢 ${job.company} &bull; 📍 ${job.location}</p>
                            </div>
                            <span class="list-item-badge ${job.match_class}">${job.eligibility}</span>
                        </div>
                        
                        <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.5; margin: 0;">${job.description}</p>
                        
                        <div style="display: flex; justify-content: space-between; align-items: center; width: 100%; margin-top: 8px;">
                            <span style="font-size: 12.5px; color: var(--text-primary); font-weight: 700;">💰 Salary min: ${job.salary}</span>
                            <a href="${job.url}" target="_blank" class="btn-primary" style="padding: 6px 14px; font-size: 12px; text-decoration: none; border-radius: var(--radius-sm); font-weight: 600; display: inline-flex; align-items: center; gap: 6px;">
                                Apply <i class="fa-solid fa-arrow-up-right-from-square" style="font-size: 10px;"></i>
                            </a>
                        </div>
                    </div>
                `;
            });

        } catch (err) {
            loadingEl.style.display = 'none';
            console.error('Error fetching internships:', err);
            listContainer.innerHTML = `
                <div style="color: var(--danger); font-weight: 600; padding: 20px; text-align: center; font-size: 13px;">
                    ⚠️ Failed to fetch recommendations. Please check your network connection and try again.
                </div>
            `;
        }
    });
});
