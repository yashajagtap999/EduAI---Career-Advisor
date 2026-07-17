/* ── CHARTJS COMMON WRAPPERS ── */

const Charts = {
    // Utility to get current theme colors dynamically
    getThemeColors() {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        return {
            text: isDark ? '#94A3B8' : '#475569',
            grid: isDark ? 'rgba(255, 255, 255, 0.05)' : 'rgba(15, 23, 42, 0.05)',
            border: isDark ? 'rgba(255, 255, 255, 0.08)' : '#E2E8F0',
            primary: '#3B82F6',
            accent: '#8B5CF6'
        };
    },

    // 1. Radar Chart Setup
    createRadar(canvasId, categories, dataset) {
        const colors = this.getThemeColors();
        const ctx = document.getElementById(canvasId).getContext('2d');
        
        return new Chart(ctx, {
            type: 'radar',
            data: {
                labels: categories,
                datasets: [{
                    label: 'Skill Proficiency',
                    data: dataset,
                    backgroundColor: 'rgba(139, 92, 246, 0.12)',
                    borderColor: colors.accent,
                    borderWidth: 2,
                    pointBackgroundColor: colors.accent,
                    pointBorderColor: '#FFF',
                    pointHoverBackgroundColor: '#FFF',
                    pointHoverBorderColor: colors.accent
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    r: {
                        grid: { color: colors.grid },
                        angleLines: { color: colors.grid },
                        pointLabels: {
                            color: colors.text,
                            font: { family: 'Plus Jakarta Sans', size: 11, weight: '600' }
                        },
                        ticks: {
                            display: false,
                            stepSize: 20
                        },
                        suggestedMin: 0,
                        suggestedMax: 100
                    }
                }
            }
        });
    },

    // 2. Spline/Area Chart for Scan History
    createAreaHistory(canvasId, labels, dataPoints) {
        const colors = this.getThemeColors();
        const ctx = document.getElementById(canvasId).getContext('2d');

        // Create gradient fill
        const gradient = ctx.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, 'rgba(59, 130, 246, 0.25)');
        gradient.addColorStop(1, 'rgba(59, 130, 246, 0.0)');

        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'ATS Score',
                    data: dataPoints,
                    fill: true,
                    backgroundColor: gradient,
                    borderColor: colors.primary,
                    borderWidth: 3,
                    tension: 0.4, // spline curve
                    pointBackgroundColor: colors.primary,
                    pointBorderColor: '#FFF',
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        padding: 12,
                        backgroundColor: 'rgba(15, 23, 42, 0.95)',
                        titleFont: { size: 13, weight: '700' },
                        bodyFont: { size: 12 }
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: colors.text }
                    },
                    y: {
                        grid: { color: colors.grid },
                        ticks: { color: colors.text },
                        min: 0,
                        max: 100
                    }
                }
            }
        });
    },

    // 3. Grouped Bar Chart (Tech market projections)
    createGroupedBar(canvasId, years, datasetsConfig) {
        const colors = this.getThemeColors();
        const ctx = document.getElementById(canvasId).getContext('2d');

        // Color palettes for categories
        const palette = ['#3B82F6', '#8B5CF6', '#EC4899', '#06B6D4'];
        const datasets = [];

        let index = 0;
        for (const [key, values] of Object.entries(datasetsConfig)) {
            datasets.push({
                label: key,
                data: values,
                backgroundColor: palette[index % palette.length],
                borderRadius: 4
            });
            index++;
        }

        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: years,
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { color: colors.text, font: { weight: '600' } }
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: colors.text }
                    },
                    y: {
                        grid: { color: colors.grid },
                        ticks: { color: colors.text }
                    }
                }
            }
        });
    },

    // 4. Doughnut/Pie Chart (Career paths distribution)
    createDoughnut(canvasId, labels, dataPoints) {
        const colors = this.getThemeColors();
        const ctx = document.getElementById(canvasId).getContext('2d');

        const palette = ['#3B82F6', '#8B5CF6', '#10B981', '#F59E0B', '#EF4444'];

        return new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: dataPoints,
                    backgroundColor: palette,
                    borderWidth: 2,
                    borderColor: colors.border
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: { color: colors.text, font: { weight: '600' } }
                    }
                },
                cutout: '65%'
            }
        });
    },

    // 5. Histogram/Bar Chart (ATS distribution)
    createHistogram(canvasId, bins, dataCounts) {
        const colors = this.getThemeColors();
        const ctx = document.getElementById(canvasId).getContext('2d');

        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: bins,
                datasets: [{
                    label: 'Candidates Count',
                    data: dataCounts,
                    backgroundColor: 'rgba(59, 130, 246, 0.85)',
                    borderColor: colors.primary,
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: colors.text }
                    },
                    y: {
                        grid: { color: colors.grid },
                        ticks: { color: colors.text }
                    }
                }
            }
        });
    }
};
