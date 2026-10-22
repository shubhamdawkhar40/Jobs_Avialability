// Main App State & Navigation Logic

const App = {
    currentTab: 'dashboard',
    stats: null,

    init() {
        this.setupNavigation();
        this.loadDashboardStats();
        
        // Initialize child modules
        if (window.JobsModule) window.JobsModule.init();
        if (window.PrepModule) window.PrepModule.init();
        if (window.CompaniesModule) window.CompaniesModule.init();

        // Check URL hash for direct tab navigation
        const hash = window.location.hash.replace('#', '');
        if (hash && ['dashboard', 'jobs', 'prep', 'companies', 'tracker'].includes(hash)) {
            this.switchTab(hash);
        }
    },

    setupNavigation() {
        document.querySelectorAll('[data-tab-target]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const target = btn.getAttribute('data-tab-target');
                this.switchTab(target);
            });
        });
    },

    switchTab(tabId) {
        this.currentTab = tabId;
        window.location.hash = tabId;

        // Hide all views
        document.querySelectorAll('.tab-view').forEach(view => {
            view.classList.add('hidden');
        });

        // Show target view
        const targetView = document.getElementById(`view-${tabId}`);
        if (targetView) {
            targetView.classList.remove('hidden');
            targetView.classList.add('animate-fade-in');
        }

        // Update nav button active states
        document.querySelectorAll('[data-tab-target]').forEach(btn => {
            const isCurrent = btn.getAttribute('data-tab-target') === tabId;
            if (isCurrent) {
                btn.classList.add('bg-blue-600', 'text-white', 'shadow-sm');
                btn.classList.remove('text-slate-600', 'hover:bg-slate-100');
            } else {
                btn.classList.remove('bg-blue-600', 'text-white', 'shadow-sm');
                btn.classList.add('text-slate-600', 'hover:bg-slate-100');
            }
        });

        // Tab-specific refreshes
        if (tabId === 'dashboard') {
            this.loadDashboardStats();
        } else if (tabId === 'jobs' && window.JobsModule) {
            window.JobsModule.refresh();
        } else if (tabId === 'prep' && window.PrepModule) {
            window.PrepModule.refresh();
        } else if (tabId === 'companies' && window.CompaniesModule) {
            window.CompaniesModule.refresh();
        } else if (tabId === 'tracker') {
            this.loadTrackerData();
        }

        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    },

    async loadDashboardStats() {
        try {
            const res = await fetch('/api/stats');
            const data = await res.json();
            this.stats = data;

            // Update stats DOM
            const elTotalJobs = document.getElementById('stat-total-jobs');
            const elTotalProblems = document.getElementById('stat-total-problems');
            const elTotalCompanies = document.getElementById('stat-total-companies');
            const elReadinessScore = document.getElementById('stat-readiness-score');
            const elReadinessBar = document.getElementById('stat-readiness-bar');
            const elSolvedCount = document.getElementById('stat-solved-count');

            if (elTotalJobs) elTotalJobs.textContent = data.total_jobs;
            if (elTotalProblems) elTotalProblems.textContent = data.total_problems;
            if (elTotalCompanies) elTotalCompanies.textContent = data.total_companies;
            if (elReadinessScore) elReadinessScore.textContent = `${data.readiness_score}%`;
            if (elReadinessBar) elReadinessBar.style.width = `${data.readiness_score}%`;
            if (elSolvedCount) elSolvedCount.textContent = `${data.problems_solved} / ${data.total_problems} Solved`;

            // Update category breakdown
            const catContainer = document.getElementById('dashboard-cat-pills');
            if (catContainer && data.category_breakdown) {
                catContainer.innerHTML = Object.entries(data.category_breakdown).map(([cat, count]) => `
                    <div class="flex items-center justify-between p-3 bg-slate-50 border border-slate-200 rounded-xl hover:bg-blue-50 transition cursor-pointer" onclick="App.navigateToPrepCategory('${cat}')">
                        <div class="flex items-center space-x-2.5">
                            <span class="w-2.5 h-2.5 rounded-full ${cat === 'Aptitude' ? 'bg-amber-500' : cat === 'DSA' ? 'bg-emerald-500' : cat === 'Technical' ? 'bg-blue-500' : 'bg-purple-500'}"></span>
                            <span class="font-medium text-slate-800 text-sm">${cat}</span>
                        </div>
                        <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-white border border-slate-200 text-slate-600">${count} Qs</span>
                    </div>
                `).join('');
            }
        } catch (err) {
            console.error('Failed to load stats:', err);
        }
    },

    async loadTrackerData() {
        try {
            // Load application tracking
            const resApps = await fetch('/api/applications');
            const dataApps = await resApps.json();
            const trackerAppsList = document.getElementById('tracker-apps-list');
            if (trackerAppsList) {
                if (dataApps.applications.length === 0) {
                    trackerAppsList.innerHTML = `
                        <div class="text-center py-10 bg-slate-50 rounded-xl border border-dashed border-slate-300">
                            <i data-lucide="briefcase" class="w-10 h-10 mx-auto text-slate-400 mb-2"></i>
                            <p class="text-slate-600 font-medium">No applications submitted yet</p>
                            <p class="text-xs text-slate-400 mt-1">Browse jobs and submit applications to track them here.</p>
                            <button onclick="App.switchTab('jobs')" class="mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-medium rounded-lg">Explore Jobs</button>
                        </div>
                    `;
                } else {
                    trackerAppsList.innerHTML = dataApps.applications.map(app => `
                        <div class="p-4 bg-white border border-slate-200 rounded-xl shadow-sm hover:shadow-md transition">
                            <div class="flex items-start justify-between">
                                <div>
                                    <h4 class="font-semibold text-slate-900">${app.title}</h4>
                                    <p class="text-xs text-slate-500 font-medium">${app.company} • ${app.location}</p>
                                </div>
                                <span class="px-2.5 py-1 text-xs font-semibold rounded-full ${
                                    app.status === 'Submitted' ? 'bg-blue-50 text-blue-700 border border-blue-200' :
                                    app.status === 'Shortlisted' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' :
                                    'bg-purple-50 text-purple-700 border border-purple-200'
                                }">${app.status}</span>
                            </div>
                            <div class="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-400">
                                <span>Applied on: ${app.applied_at}</span>
                                <span class="text-slate-600 font-medium">${app.salary_range}</span>
                            </div>
                        </div>
                    `).join('');
                }
            }

            // Load saved jobs
            const resSaved = await fetch('/api/saved-jobs');
            const dataSaved = await resSaved.json();
            const trackerSavedList = document.getElementById('tracker-saved-list');
            if (trackerSavedList) {
                if (dataSaved.saved_jobs.length === 0) {
                    trackerSavedList.innerHTML = `<p class="text-slate-400 text-sm text-center py-6">No saved jobs yet.</p>`;
                } else {
                    trackerSavedList.innerHTML = dataSaved.saved_jobs.map(job => `
                        <div class="p-3 bg-white border border-slate-200 rounded-xl flex items-center justify-between hover:border-blue-300 transition">
                            <div class="flex items-center space-x-3">
                                <div class="w-10 h-10 rounded-lg flex items-center justify-center text-white font-bold text-xs" style="background-color: ${job.company_logo_color || '#3b82f6'}">
                                    ${job.company.substring(0, 2).toUpperCase()}
                                </div>
                                <div>
                                    <h5 class="text-sm font-semibold text-slate-800">${job.title}</h5>
                                    <p class="text-xs text-slate-500">${job.company} • ${job.salary_range}</p>
                                </div>
                            </div>
                            <button onclick="JobsModule.viewJobDetails(${job.id})" class="px-3 py-1.5 bg-slate-100 hover:bg-blue-600 hover:text-white text-slate-700 text-xs font-medium rounded-lg transition">View</button>
                        </div>
                    `).join('');
                }
            }

            // Load problem progress
            const resProgress = await fetch('/api/prep/progress');
            const dataProgress = await resProgress.json();
            const trackerAttemptsList = document.getElementById('tracker-attempts-list');
            if (trackerAttemptsList) {
                if (dataProgress.recent_attempts.length === 0) {
                    trackerAttemptsList.innerHTML = `<p class="text-slate-400 text-sm text-center py-6">No problems attempted yet. Jump into Preparation Hub!</p>`;
                } else {
                    trackerAttemptsList.innerHTML = dataProgress.recent_attempts.map(att => `
                        <div class="flex items-center justify-between p-3 border-b border-slate-100 last:border-0 hover:bg-slate-50">
                            <div>
                                <span class="text-xs font-medium px-2 py-0.5 rounded bg-slate-100 text-slate-600 mr-2">${att.category}</span>
                                <span class="text-sm font-semibold text-slate-800">${att.title}</span>
                                <span class="text-xs text-slate-400 block mt-0.5">${att.attempted_at}</span>
                            </div>
                            <span class="px-2 py-1 text-xs font-semibold rounded-full ${att.status === 'Solved' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}">
                                ${att.status} (+${att.score} pts)
                            </span>
                        </div>
                    `).join('');
                }
            }

            if (window.lucide) window.lucide.createIcons();
        } catch (err) {
            console.error('Failed to load tracker data:', err);
        }
    },

    navigateToPrepCategory(category) {
        this.switchTab('prep');
        if (window.PrepModule) {
            window.PrepModule.setCategory(category);
        }
    },

    showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `fixed bottom-5 right-5 z-50 flex items-center space-x-3 px-4 py-3 rounded-xl shadow-lg border text-sm font-medium transition-all duration-300 transform translate-y-2 opacity-0 ${
            type === 'success' ? 'bg-emerald-900 text-white border-emerald-700' :
            type === 'error' ? 'bg-rose-900 text-white border-rose-700' :
            'bg-slate-900 text-white border-slate-700'
        }`;
        
        const iconName = type === 'success' ? 'check-circle' : type === 'error' ? 'alert-triangle' : 'info';
        toast.innerHTML = `<i data-lucide="${iconName}" class="w-4 h-4"></i><span>${message}</span>`;
        document.body.appendChild(toast);
        if (window.lucide) window.lucide.createIcons();

        // Animate in
        requestAnimationFrame(() => {
            toast.classList.remove('translate-y-2', 'opacity-0');
            toast.classList.add('translate-y-0', 'opacity-100');
        });

        // Remove after 3.5s
        setTimeout(() => {
            toast.classList.add('translate-y-2', 'opacity-0');
            setTimeout(() => toast.remove(), 300);
        }, 3500);
    }
};

window.App = App;
document.addEventListener('DOMContentLoaded', () => App.init());
