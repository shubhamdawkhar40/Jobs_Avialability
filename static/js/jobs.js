// Jobs Module

const JobsModule = {
    jobs: [],
    currentFilter: {
        search: '',
        location: '',
        type: '',
        workplace: '',
        experience: '',
        featured: ''
    },
    activeJobId: null,

    init() {
        this.bindEvents();
        this.fetchJobs();
    },

    refresh() {
        this.fetchJobs();
    },

    bindEvents() {
        const searchInput = document.getElementById('jobs-search-input');
        if (searchInput) {
            let timeout = null;
            searchInput.addEventListener('input', (e) => {
                clearTimeout(timeout);
                timeout = setTimeout(() => {
                    this.currentFilter.search = e.target.value.trim();
                    this.fetchJobs();
                }, 300);
            });
        }

        const locationInput = document.getElementById('jobs-location-filter');
        if (locationInput) {
            locationInput.addEventListener('change', (e) => {
                this.currentFilter.location = e.target.value.trim();
                this.fetchJobs();
            });
        }

        const typeFilter = document.getElementById('jobs-type-filter');
        if (typeFilter) {
            typeFilter.addEventListener('change', (e) => {
                this.currentFilter.type = e.target.value;
                this.fetchJobs();
            });
        }

        const workplaceFilter = document.getElementById('jobs-workplace-filter');
        if (workplaceFilter) {
            workplaceFilter.addEventListener('change', (e) => {
                this.currentFilter.workplace = e.target.value;
                this.fetchJobs();
            });
        }

        const expFilter = document.getElementById('jobs-exp-filter');
        if (expFilter) {
            expFilter.addEventListener('change', (e) => {
                this.currentFilter.experience = e.target.value;
                this.fetchJobs();
            });
        }

        // Post Job Form
        const postJobForm = document.getElementById('post-job-form');
        if (postJobForm) {
            postJobForm.addEventListener('submit', (e) => this.handlePostJob(e));
        }

        // Apply Form
        const applyForm = document.getElementById('apply-job-form');
        if (applyForm) {
            applyForm.addEventListener('submit', (e) => this.handleApplySubmit(e));
        }
    },

    async fetchJobs() {
        const container = document.getElementById('jobs-list-container');
        if (!container) return;

        container.innerHTML = `
            <div class="col-span-full py-16 text-center">
                <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-600 border-t-transparent"></div>
                <p class="mt-2 text-sm text-slate-500">Loading active opportunities...</p>
            </div>
        `;

        try {
            const params = new URLSearchParams();
            if (this.currentFilter.search) params.append('search', this.currentFilter.search);
            if (this.currentFilter.location) params.append('location', this.currentFilter.location);
            if (this.currentFilter.type) params.append('type', this.currentFilter.type);
            if (this.currentFilter.workplace) params.append('workplace', this.currentFilter.workplace);
            if (this.currentFilter.experience) params.append('experience', this.currentFilter.experience);

            const res = await fetch(`/api/jobs?${params.toString()}`);
            const data = await res.json();
            this.jobs = data.jobs || [];

            this.renderJobsList();
        } catch (err) {
            console.error('Error fetching jobs:', err);
            container.innerHTML = `
                <div class="col-span-full py-12 text-center text-rose-600">
                    <p class="font-semibold">Failed to load jobs.</p>
                </div>
            `;
        }
    },

    renderJobsList() {
        const container = document.getElementById('jobs-list-container');
        const countBadge = document.getElementById('jobs-count-badge');
        if (countBadge) countBadge.textContent = `${this.jobs.length} Jobs Found`;

        if (!container) return;

        if (this.jobs.length === 0) {
            container.innerHTML = `
                <div class="col-span-full py-16 text-center bg-white rounded-2xl border border-dashed border-slate-300">
                    <i data-lucide="search-x" class="w-12 h-12 mx-auto text-slate-300 mb-3"></i>
                    <h3 class="text-lg font-semibold text-slate-700">No matching jobs found</h3>
                    <p class="text-sm text-slate-400 mt-1 max-w-sm mx-auto">Try adjusting your filters, location, or search keywords.</p>
                    <button onclick="JobsModule.resetFilters()" class="mt-4 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-lg transition">Clear All Filters</button>
                </div>
            `;
            if (window.lucide) window.lucide.createIcons();
            return;
        }

        container.innerHTML = this.jobs.map(job => `
            <div class="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm hover:shadow-md transition-all duration-200 flex flex-col justify-between group">
                <div>
                    <!-- Header -->
                    <div class="flex items-start justify-between">
                        <div class="flex items-center space-x-3">
                            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-white font-bold text-base shadow-sm" style="background-color: ${job.company_logo_color || '#2563EB'}">
                                ${job.company.substring(0, 2).toUpperCase()}
                            </div>
                            <div>
                                <h3 class="font-bold text-slate-900 group-hover:text-blue-600 transition leading-snug cursor-pointer" onclick="JobsModule.viewJobDetails(${job.id})">
                                    ${job.title}
                                </h3>
                                <div class="flex items-center space-x-2 text-xs text-slate-500 font-medium mt-0.5">
                                    <span>${job.company}</span>
                                    <span>•</span>
                                    <span class="text-slate-600">${job.industry || 'Technology'}</span>
                                </div>
                            </div>
                        </div>
                        <button onclick="JobsModule.toggleSave(${job.id})" class="p-2 rounded-lg text-slate-400 hover:text-amber-500 hover:bg-amber-50 transition" title="${job.is_saved ? 'Remove bookmark' : 'Save job'}">
                            <i data-lucide="bookmark" class="w-5 h-5 ${job.is_saved ? 'fill-amber-500 text-amber-500' : ''}"></i>
                        </button>
                    </div>

                    <!-- Meta Tags -->
                    <div class="flex flex-wrap gap-2 mt-4 text-xs font-medium">
                        <span class="inline-flex items-center px-2.5 py-1 rounded-md bg-blue-50 text-blue-700">
                            <i data-lucide="map-pin" class="w-3 h-3 mr-1"></i> ${job.location}
                        </span>
                        <span class="inline-flex items-center px-2.5 py-1 rounded-md bg-slate-100 text-slate-700">
                            <i data-lucide="briefcase" class="w-3 h-3 mr-1"></i> ${job.job_type}
                        </span>
                        <span class="inline-flex items-center px-2.5 py-1 rounded-md bg-purple-50 text-purple-700">
                            ${job.workplace_type}
                        </span>
                        <span class="inline-flex items-center px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-700">
                            <i data-lucide="award" class="w-3 h-3 mr-1"></i> ${job.experience_level}
                        </span>
                    </div>

                    <!-- Salary & Batches -->
                    <div class="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                        <span class="font-bold text-slate-900 text-sm">${job.salary_range}</span>
                        <span class="text-slate-400 font-medium">${job.eligible_batches || 'Eligible Batches'}</span>
                    </div>

                    <!-- Skills Chips -->
                    <div class="flex flex-wrap gap-1.5 mt-3">
                        ${(job.skills || []).slice(0, 4).map(skill => `
                            <span class="text-[11px] px-2 py-0.5 rounded bg-slate-100 text-slate-600 font-medium">${skill}</span>
                        `).join('')}
                        ${(job.skills || []).length > 4 ? `
                            <span class="text-[11px] px-1.5 py-0.5 rounded bg-slate-100 text-slate-400 font-medium">+${job.skills.length - 4}</span>
                        ` : ''}
                    </div>
                </div>

                <!-- Footer CTAs -->
                <div class="mt-5 pt-4 border-t border-slate-100 flex items-center space-x-2">
                    <button onclick="JobsModule.viewJobDetails(${job.id})" class="flex-1 px-3 py-2 text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-xl transition text-center">
                        View Details
                    </button>
                    ${job.is_applied ? `
                        <button disabled class="flex-1 px-3 py-2 text-xs font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 rounded-xl text-center flex items-center justify-center space-x-1">
                            <i data-lucide="check" class="w-3.5 h-3.5"></i>
                            <span>Applied</span>
                        </button>
                    ` : `
                        <button onclick="JobsModule.openApplyModal(${job.id})" class="flex-1 px-3 py-2 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-xl transition text-center shadow-sm">
                            Easy Apply
                        </button>
                    `}
                </div>
            </div>
        `).join('');

        if (window.lucide) window.lucide.createIcons();
    },

    resetFilters() {
        this.currentFilter = { search: '', location: '', type: '', workplace: '', experience: '', featured: '' };
        const s = document.getElementById('jobs-search-input');
        if (s) s.value = '';
        const l = document.getElementById('jobs-location-filter');
        if (l) l.value = '';
        const t = document.getElementById('jobs-type-filter');
        if (t) t.value = '';
        const w = document.getElementById('jobs-workplace-filter');
        if (w) w.value = '';
        const e = document.getElementById('jobs-exp-filter');
        if (e) e.value = '';
        this.fetchJobs();
    },

    async viewJobDetails(jobId) {
        this.activeJobId = jobId;
        const modal = document.getElementById('job-details-modal');
        const content = document.getElementById('job-details-modal-content');
        if (!modal || !content) return;

        modal.classList.remove('hidden');
        content.innerHTML = `
            <div class="p-12 text-center">
                <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-600 border-t-transparent"></div>
            </div>
        `;

        try {
            const res = await fetch(`/api/jobs/${jobId}`);
            const job = await res.json();

            content.innerHTML = `
                <div class="p-6 md:p-8">
                    <!-- Header -->
                    <div class="flex items-start justify-between pb-6 border-b border-slate-100">
                        <div class="flex items-start space-x-4">
                            <div class="w-16 h-16 rounded-2xl flex items-center justify-center text-white font-extrabold text-xl shadow-md" style="background-color: ${job.company_logo_color || '#2563EB'}">
                                ${job.company.substring(0, 2).toUpperCase()}
                            </div>
                            <div>
                                <h2 class="text-2xl font-bold text-slate-900">${job.title}</h2>
                                <p class="text-base text-slate-600 font-medium mt-0.5">${job.company} • <span class="text-slate-400 text-sm">${job.location}</span></p>
                                <div class="flex flex-wrap gap-2 mt-3">
                                    <span class="px-2.5 py-1 text-xs font-semibold rounded-md bg-blue-50 text-blue-700">${job.job_type}</span>
                                    <span class="px-2.5 py-1 text-xs font-semibold rounded-md bg-purple-50 text-purple-700">${job.workplace_type}</span>
                                    <span class="px-2.5 py-1 text-xs font-semibold rounded-md bg-emerald-50 text-emerald-700">${job.salary_range}</span>
                                    <span class="px-2.5 py-1 text-xs font-semibold rounded-md bg-slate-100 text-slate-700">${job.experience_level}</span>
                                </div>
                            </div>
                        </div>
                        <button onclick="JobsModule.closeJobDetails()" class="p-2 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100">
                            <i data-lucide="x" class="w-6 h-6"></i>
                        </button>
                    </div>

                    <!-- Body -->
                    <div class="py-6 space-y-6 text-sm text-slate-700">
                        <div>
                            <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">About the Role</h4>
                            <p class="leading-relaxed text-slate-600">${job.description}</p>
                        </div>

                        <div>
                            <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">Key Requirements & Eligibility</h4>
                            <ul class="space-y-2">
                                ${(job.requirements || []).map(req => `
                                    <li class="flex items-start space-x-2.5">
                                        <i data-lucide="check-circle-2" class="w-4 h-4 text-emerald-500 mt-0.5 flex-shrink-0"></i>
                                        <span>${req}</span>
                                    </li>
                                `).join('')}
                            </ul>
                        </div>

                        <div>
                            <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">Skills & Technologies</h4>
                            <div class="flex flex-wrap gap-2">
                                ${(job.skills || []).map(skill => `
                                    <span class="px-3 py-1 rounded-lg bg-slate-100 text-slate-700 text-xs font-semibold">${skill}</span>
                                `).join('')}
                            </div>
                        </div>

                        <div>
                            <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">Perks & Benefits</h4>
                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                                ${(job.benefits || []).map(ben => `
                                    <div class="flex items-center space-x-2 p-2.5 rounded-xl bg-slate-50 border border-slate-100">
                                        <i data-lucide="gift" class="w-4 h-4 text-blue-500"></i>
                                        <span class="text-xs font-medium text-slate-700">${ben}</span>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    </div>

                    <!-- Footer Action -->
                    <div class="pt-6 border-t border-slate-100 flex items-center justify-between">
                        <div class="text-xs text-slate-400">
                            <span>Posted on: ${job.posted_date || 'Recently'}</span>
                            <span class="mx-1.5">•</span>
                            <span>Deadline: ${job.deadline || 'Ongoing'}</span>
                        </div>
                        <div class="flex items-center space-x-3">
                            <button onclick="JobsModule.toggleSave(${job.id})" class="px-4 py-2.5 rounded-xl border border-slate-200 text-slate-700 hover:bg-slate-50 text-xs font-semibold flex items-center space-x-1.5">
                                <i data-lucide="bookmark" class="w-4 h-4 ${job.is_saved ? 'fill-amber-500 text-amber-500' : ''}"></i>
                                <span>${job.is_saved ? 'Saved' : 'Save Job'}</span>
                            </button>
                            ${job.application ? `
                                <div class="px-5 py-2.5 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-xl text-xs font-bold flex items-center space-x-1.5">
                                    <i data-lucide="check-check" class="w-4 h-4"></i>
                                    <span>Applied on ${job.application.applied_at} (${job.application.status})</span>
                                </div>
                            ` : `
                                <button onclick="JobsModule.closeJobDetails(); JobsModule.openApplyModal(${job.id})" class="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-bold shadow-md hover:shadow-lg transition">
                                    Apply Now
                                </button>
                            `}
                        </div>
                    </div>
                </div>
            `;
            if (window.lucide) window.lucide.createIcons();
        } catch (err) {
            console.error('Error fetching job details:', err);
            content.innerHTML = `<p class="p-8 text-rose-500 text-center">Failed to load job details.</p>`;
        }
    },

    closeJobDetails() {
        const modal = document.getElementById('job-details-modal');
        if (modal) modal.classList.add('hidden');
    },

    async toggleSave(jobId) {
        try {
            const res = await fetch(`/api/jobs/${jobId}/save`, { method: 'POST' });
            const data = await res.json();
            if (data.success) {
                App.showToast(data.message);
                this.fetchJobs();
                if (App.stats) App.loadDashboardStats();
            }
        } catch (err) {
            console.error('Error toggling save job:', err);
        }
    },

    openApplyModal(jobId) {
        const job = this.jobs.find(j => j.id === jobId);
        if (!job) return;

        const modal = document.getElementById('apply-modal');
        const titleEl = document.getElementById('apply-modal-job-title');
        const jobIdInput = document.getElementById('apply-job-id');

        if (titleEl) titleEl.textContent = `Apply for ${job.title} at ${job.company}`;
        if (jobIdInput) jobIdInput.value = jobId;

        if (modal) modal.classList.remove('hidden');
    },

    closeApplyModal() {
        const modal = document.getElementById('apply-modal');
        if (modal) modal.classList.add('hidden');
    },

    async handleApplySubmit(e) {
        e.preventDefault();
        const jobId = document.getElementById('apply-job-id').value;
        const name = document.getElementById('apply-name').value.trim();
        const email = document.getElementById('apply-email').value.trim();
        const phone = document.getElementById('apply-phone').value.trim();
        const experience = document.getElementById('apply-exp').value;
        const portfolio = document.getElementById('apply-portfolio').value.trim();
        const coverNote = document.getElementById('apply-cover-note').value.trim();

        if (!name || !email) {
            App.showToast('Name and Email are required', 'error');
            return;
        }

        try {
            const res = await fetch(`/api/jobs/${jobId}/apply`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name, email, phone, experience, portfolio, cover_note: coverNote,
                    resume_name: `${name.replace(/\s+/g, '_')}_Resume.pdf`
                })
            });

            const data = await res.json();
            if (res.ok) {
                App.showToast(data.message, 'success');
                this.closeApplyModal();
                this.fetchJobs();
                if (App.stats) App.loadDashboardStats();
            } else {
                App.showToast(data.error || 'Failed to submit application', 'error');
            }
        } catch (err) {
            console.error('Apply error:', err);
            App.showToast('Application submission failed. Try again.', 'error');
        }
    },

    openPostJobModal() {
        const modal = document.getElementById('post-job-modal');
        if (modal) modal.classList.remove('hidden');
    },

    closePostJobModal() {
        const modal = document.getElementById('post-job-modal');
        if (modal) modal.classList.add('hidden');
    },

    async handlePostJob(e) {
        e.preventDefault();
        const title = document.getElementById('post-title').value.trim();
        const company = document.getElementById('post-company').value.trim();
        const industry = document.getElementById('post-industry').value.trim();
        const location = document.getElementById('post-location').value.trim();
        const workplace_type = document.getElementById('post-workplace').value;
        const job_type = document.getElementById('post-type').value;
        const experience_level = document.getElementById('post-experience').value;
        const salary_range = document.getElementById('post-salary').value.trim();
        const description = document.getElementById('post-desc').value.trim();
        const requirementsRaw = document.getElementById('post-requirements').value.trim();
        const skillsRaw = document.getElementById('post-skills').value.trim();
        const eligible_batches = document.getElementById('post-batches').value.trim();

        const requirements = requirementsRaw.split('\n').map(s => s.trim()).filter(Boolean);
        const skills = skillsRaw.split(',').map(s => s.trim()).filter(Boolean);

        try {
            const res = await fetch('/api/jobs', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    title, company, industry, location, workplace_type,
                    job_type, experience_level, salary_range, description,
                    requirements, skills, eligible_batches,
                    company_logo_color: '#3B82F6'
                })
            });

            const data = await res.json();
            if (res.ok) {
                App.showToast('Job listing created successfully!', 'success');
                this.closePostJobModal();
                e.target.reset();
                this.fetchJobs();
                if (App.stats) App.loadDashboardStats();
            } else {
                App.showToast(data.error || 'Failed to create job', 'error');
            }
        } catch (err) {
            console.error('Post job error:', err);
            App.showToast('Failed to post job. Please try again.', 'error');
        }
    }
};

window.JobsModule = JobsModule;
