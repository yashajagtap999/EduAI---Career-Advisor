/* ── CENTRAL BACKEND API WRAPPER ── */

const API_BASE = '/api';

const Api = {
    // Utility Fetch Wrapper
    async request(path, options = {}) {
        const url = `${API_BASE}${path}`;
        
        // Ensure headers are initialized
        options.headers = options.headers || {};
        
        // Set content type if it's not a FormData payload
        if (!(options.body instanceof FormData) && !options.headers['Content-Type']) {
            options.headers['Content-Type'] = 'application/json';
        }
        
        // Include credentials for session cookies
        options.credentials = 'include';

        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP error! Status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`API Error on path ${path}:`, error);
            throw error;
        }
    },

    // ── AUTHENTICATION APIs ──
    async register(username, password, fullName) {
        return this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ username, password, full_name: fullName })
        });
    },

    async login(username, password) {
        return this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
    },

    async logout() {
        return this.request('/auth/logout', { method: 'POST' });
    },

    async getSession() {
        return this.request('/auth/session', { method: 'GET' });
    },

    // ── DASHBOARD APIs ──
    async getStats() {
        return this.request('/dashboard/stats', { method: 'GET' });
    },

    async getCharts() {
        return this.request('/dashboard/charts', { method: 'GET' });
    },

    async getRoadmapAndReadiness(role) {
        return this.request(`/dashboard/roadmap?role=${encodeURIComponent(role)}`, { method: 'GET' });
    },

    async recommendInternships(skills, cgpa, location, branch) {
        return this.request('/internships/recommend', {
            method: 'POST',
            body: JSON.stringify({ skills, cgpa, location, branch })
        });
    },

    // ── RESUME SCAN & OPTIMIZATION APIs ──
    async scanResume(file) {
        const formData = new FormData();
        formData.append('file', file);
        return this.request('/resume/scan', {
            method: 'POST',
            body: formData
        });
    },

    async optimizeResume(resumeText, missingSkills, jobRole) {
        return this.request('/resume/optimize', {
            method: 'POST',
            body: JSON.stringify({
                username: localStorage.getItem('username') || '',
                resume_text: resumeText,
                missing_skills: missingSkills,
                job_role: jobRole
            })
        });
    },

    // ── COLLEGE FINDER APIs ──
    async getFields() {
        return this.request('/college/fields', { method: 'GET' });
    },

    async getColleges(field, city = '') {
        let path = `/college/recommendations?field=${encodeURIComponent(field)}`;
        if (city) {
            path += `&city=${encodeURIComponent(city)}`;
        }
        return this.request(path, { method: 'GET' });
    },

    async getRoadmap(field) {
        return this.request(`/college/roadmap?field=${encodeURIComponent(field)}`, { method: 'GET' });
    },

    // ── GLOBAL ANALYTICS API ──
    async getGlobalAnalytics() {
        return this.request('/analytics/global', { method: 'GET' });
    },

    // ── CHATBOT CHUNKS STREAMING API ──
    // Uses standard fetch with ReadableStream to support POST payload with SSE chunk reads
    async streamChat(message, history, onChunk, onError, onDone) {
        const url = `${API_BASE}/mentor/chat`;
        
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({ message, history })
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(errorText || 'Failed to start chat stream');
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';

            while (true) {
                const { value, done } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                
                // Parse Server-Sent Events lines (data: ...)
                const lines = buffer.split('\n');
                // Keep the last partial line in the buffer
                buffer = lines.pop();

                for (const line of lines) {
                    const cleanLine = line.trim();
                    if (!cleanLine) continue;

                    if (cleanLine.startsWith('data: ')) {
                        const dataStr = cleanLine.slice(6);
                        
                        if (dataStr === '[DONE]') {
                            if (onDone) onDone();
                            return;
                        }

                        try {
                            const parsed = JSON.parse(dataStr);
                            if (parsed.error) {
                                if (onError) onError(new Error(parsed.error));
                            } else if (parsed.text) {
                                if (onChunk) onChunk(parsed.text);
                            }
                        } catch (e) {
                            console.warn('Could not parse SSE JSON line:', dataStr, e);
                        }
                    }
                }
            }

            if (onDone) onDone();
        } catch (error) {
            console.error('Chat stream exception:', error);
            if (onError) onError(error);
        }
    }
};
