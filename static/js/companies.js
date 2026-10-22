// Companies Module: Hiring Process, Exam Pattern, Syllabus, Eligibility Calculator

const CompaniesModule = {
    companies: [],
    currentTier: 'all',
    activeCompany: null,

    init() {
        this.bindEvents();
        this.fetchCompanies();
    },

    refresh() {
        this.fetchCompanies();
    },

    bindEvents() {
        const searchInput = document.getElementById('company-search-input');
        if (searchInput) {
            let timeout = null;
            searchInput.addEventListener('input', (e) => {
                clearTimeout(timeout);
                timeout = setTimeout(() => {
                    this.fetchCompanies(e.target.value.trim());
                }, 300);
            });
        }

        document.querySelectorAll('[data-company-tier]').forEach(btn => {
            btn.addEventListener('click', () => {
                const tier = btn.getAttribute('data-company-tier');
                this.currentTier = tier;
                
                document.querySelectorAll('[data-company-tier]').forEach(b => {
                    b.className = b.getAttribute('data-company-tier') === tier
                        ? "px-4 py-2 text-xs font-bold rounded-xl bg-blue-600 text-white shadow-sm transition"
                        : "px-4 py-2 text-xs font-semibold rounded-xl text-slate-600 hover:bg-slate-100 transition";
                });

                this.fetchCompanies();
            });
        });
    },

    async fetchCompanies(searchTerm = '') {
        const container = document.getElementById('companies-list-container');
        if (!container) return;

        container.innerHTML = `
            <div class="col-span-full py-16 text-center text-slate-400">
                <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-600 border-t-transparent"></div>
                <p class="mt-2 text-sm text-slate-500">Loading hiring roadmaps...</p>
            </div>
        `;

        try {
            const params = new URLSearchParams();
            if (searchTerm) params.append('search', searchTerm);
            if (this.currentTier && this.currentTier !== 'all') params.append('tier', this.currentTier);

            const res = await fetch(`/api/companies?${params.toString()}`);
            const data = await res.json();
            this.companies = data.companies || [];

            this.renderCompaniesList();
        } catch (err) {
            console.error('Error fetching companies:', err);
        }
    },

    renderCompaniesList() {
        const container = document.getElementById('companies-list-container');
        if (!container) return;

        if (this.companies.length === 0) {
            container.innerHTML = `
                <div class="col-span-full py-16 text-center bg-white rounded-2xl border border-dashed border-slate-300">
                    <i data-lucide="building-2" class="w-12 h-12 mx-auto text-slate-300 mb-2"></i>
                    <p class="font-semibold text-slate-700">No companies found matching criteria.</p>
                </div>
            `;
            if (window.lucide) window.lucide.createIcons();
            return;
        }

        container.innerHTML = this.companies.map(c => `
            <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm hover:shadow-md hover:border-blue-400 transition-all duration-200 flex flex-col justify-between group">
                <div>
                    <!-- Top Info -->
                    <div class="flex items-start justify-between">
                        <div class="w-14 h-14 rounded-2xl flex items-center justify-center text-white font-extrabold text-lg shadow-sm" style="background-color: ${c.logo_color || '#2563EB'}">
                            ${c.name.substring(0, 2).toUpperCase()}
                        </div>
                        <span class="px-2.5 py-1 rounded-md text-xs font-semibold ${
                            c.difficulty_rating === 'Very Hard' ? 'bg-rose-50 text-rose-700' :
                            c.difficulty_rating === 'Hard' ? 'bg-amber-50 text-amber-700' :
                            'bg-blue-50 text-blue-700'
                        }">
                            ${c.difficulty_rating}
                        </span>
                    </div>

                    <h3 class="text-xl font-bold text-slate-900 group-hover:text-blue-600 transition mt-4 leading-tight">
                        ${c.name}
                    </h3>
                    <p class="text-xs text-slate-500 font-medium mt-1 line-clamp-2">
                        ${c.tagline || c.tier}
                    </p>

                    <!-- Package & Roles -->
                    <div class="mt-4 p-3 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-between">
                        <div>
                            <span class="text-[11px] uppercase tracking-wider text-slate-400 font-bold block">Avg CTC</span>
                            <span class="text-xs font-extrabold text-slate-900">${c.avg_package}</span>
                        </div>
                        <div class="text-right">
                            <span class="text-[11px] uppercase tracking-wider text-slate-400 font-bold block">Hiring Season</span>
                            <span class="text-xs font-semibold text-slate-700">${c.hiring_season || 'Year-round'}</span>
                        </div>
                    </div>

                    <!-- Roles Offered Chips -->
                    <div class="flex flex-wrap gap-1.5 mt-3">
                        ${(c.roles_offered || []).map(r => `
                            <span class="text-[11px] px-2 py-0.5 rounded bg-blue-50 text-blue-700 font-medium">${r}</span>
                        `).join('')}
                    </div>
                </div>

                <div class="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between">
                    <span class="text-xs font-semibold text-slate-500 flex items-center">
                        <i data-lucide="check-circle" class="w-3.5 h-3.5 text-emerald-500 mr-1.5"></i> Syllabus & Pattern
                    </span>
                    <button onclick="CompaniesModule.viewCompanyHiringProcess('${c.slug}')" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-bold shadow-sm transition flex items-center space-x-1">
                        <span>Hiring Guide</span>
                        <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
                    </button>
                </div>
            </div>
        `).join('');

        if (window.lucide) window.lucide.createIcons();
    },

    async viewCompanyHiringProcess(slug) {
        const modal = document.getElementById('company-details-modal');
        const content = document.getElementById('company-details-content');
        if (!modal || !content) return;

        modal.classList.remove('hidden');
        content.innerHTML = `
            <div class="p-16 text-center">
                <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-600 border-t-transparent"></div>
                <p class="mt-2 text-xs text-slate-500">Loading comprehensive hiring roadmap...</p>
            </div>
        `;

        try {
            const res = await fetch(`/api/companies/${slug}`);
            const comp = await res.json();
            this.activeCompany = comp;

            content.innerHTML = `
                <div class="p-6 md:p-10">
                    <!-- Top Header -->
                    <div class="flex items-start justify-between pb-6 border-b border-slate-200">
                        <div class="flex items-center space-x-4">
                            <div class="w-16 h-16 rounded-2xl flex items-center justify-center text-white font-extrabold text-2xl shadow-md" style="background-color: ${comp.logo_color || '#2563EB'}">
                                ${comp.name.substring(0, 2).toUpperCase()}
                            </div>
                            <div>
                                <div class="flex items-center space-x-2 text-xs font-semibold">
                                    <span class="px-2.5 py-0.5 rounded bg-blue-100 text-blue-800">${comp.tier}</span>
                                    <span class="text-slate-400">•</span>
                                    <span class="text-slate-500">${comp.hiring_season}</span>
                                </div>
                                <h2 class="text-2xl md:text-3xl font-extrabold text-slate-900 mt-1">${comp.name} Hiring Process</h2>
                                <p class="text-xs text-slate-500 mt-0.5">${comp.tagline || ''}</p>
                            </div>
                        </div>
                        <button onclick="CompaniesModule.closeCompanyModal()" class="p-2 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-xl">
                            <i data-lucide="x" class="w-6 h-6"></i>
                        </button>
                    </div>

                    <!-- Package & Roles Bar -->
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 my-6">
                        <div class="p-4 rounded-xl bg-slate-50 border border-slate-200">
                            <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400">Average Compensation</span>
                            <h4 class="text-lg font-extrabold text-slate-900 mt-0.5">${comp.avg_package}</h4>
                        </div>
                        <div class="p-4 rounded-xl bg-slate-50 border border-slate-200">
                            <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400">Exam Difficulty</span>
                            <h4 class="text-lg font-extrabold text-amber-600 mt-0.5">${comp.difficulty_rating}</h4>
                        </div>
                        <div class="p-4 rounded-xl bg-slate-50 border border-slate-200">
                            <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400">Key Roles Offered</span>
                            <h4 class="text-xs font-bold text-slate-800 mt-1">${(comp.roles_offered || []).join(', ')}</h4>
                        </div>
                    </div>

                    <!-- SECTION 1: INTERACTIVE ELIGIBILITY CHECKER -->
                    <div class="my-8 p-6 rounded-2xl bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200">
                        <div class="flex items-center space-x-2 text-blue-900 font-bold text-base mb-1">
                            <i data-lucide="check-square" class="w-5 h-5 text-blue-600"></i>
                            <span>Interactive Eligibility Calculator</span>
                        </div>
                        <p class="text-xs text-slate-600 mb-4">Enter your academic credentials to verify if you meet ${comp.name}'s official eligibility criteria.</p>

                        <div class="grid grid-cols-1 sm:grid-cols-4 gap-3">
                            <div>
                                <label class="text-[11px] font-bold text-slate-700 block mb-1">Your CGPA / %</label>
                                <input type="number" step="0.1" id="el-cgpa" value="7.5" class="w-full px-3 py-2 text-xs border border-slate-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500">
                            </div>
                            <div>
                                <label class="text-[11px] font-bold text-slate-700 block mb-1">Active Backlogs</label>
                                <input type="number" id="el-backlogs" value="0" class="w-full px-3 py-2 text-xs border border-slate-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500">
                            </div>
                            <div>
                                <label class="text-[11px] font-bold text-slate-700 block mb-1">Gap Years (if any)</label>
                                <input type="number" id="el-gap" value="0" class="w-full px-3 py-2 text-xs border border-slate-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500">
                            </div>
                            <div class="flex items-end">
                                <button onclick="CompaniesModule.checkEligibility('${comp.slug}')" class="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-lg transition shadow-sm">
                                    Check Eligibility
                                </button>
                            </div>
                        </div>

                        <!-- Eligibility Result Box -->
                        <div id="eligibility-result-box" class="hidden mt-4 p-4 rounded-xl text-xs"></div>
                    </div>

                    <!-- SECTION 2: OFFICIAL ELIGIBILITY CRITERIA BREAKDOWN -->
                    <div class="my-6">
                        <h4 class="text-sm font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center space-x-2">
                            <i data-lucide="file-check" class="w-4 h-4 text-blue-600"></i>
                            <span>Official Eligibility Criteria Breakdown</span>
                        </h4>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                            <div class="p-3 bg-white border border-slate-200 rounded-xl">
                                <span class="font-bold text-slate-500 block">Minimum Academic Marks:</span>
                                <span class="font-semibold text-slate-900 mt-0.5 block">${comp.eligibility.min_cgpa || '60% throughout'}</span>
                            </div>
                            <div class="p-3 bg-white border border-slate-200 rounded-xl">
                                <span class="font-bold text-slate-500 block">Backlog Policy:</span>
                                <span class="font-semibold text-slate-900 mt-0.5 block">${comp.eligibility.backlogs || 'No active backlogs'}</span>
                            </div>
                            <div class="p-3 bg-white border border-slate-200 rounded-xl">
                                <span class="font-bold text-slate-500 block">Permissible Academic Gap:</span>
                                <span class="font-semibold text-slate-900 mt-0.5 block">${comp.eligibility.gap_allowed || 'Max 1 year'}</span>
                            </div>
                            <div class="p-3 bg-white border border-slate-200 rounded-xl">
                                <span class="font-bold text-slate-500 block">Eligible Degrees & Streams:</span>
                                <span class="font-semibold text-slate-900 mt-0.5 block">${comp.eligibility.eligible_degrees || 'B.Tech / M.Tech / MCA'}</span>
                            </div>
                        </div>
                    </div>

                    <!-- SECTION 3: EXAM PATTERN & ROUNDS -->
                    <div class="my-8">
                        <h4 class="text-sm font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center space-x-2">
                            <i data-lucide="layers" class="w-4 h-4 text-blue-600"></i>
                            <span>Exam Pattern & Test Structure</span>
                        </h4>
                        <div class="space-y-4">
                            ${(comp.exam_pattern || []).map((round, idx) => `
                                <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
                                    <div class="flex items-center justify-between pb-3 border-b border-slate-100">
                                        <div class="flex items-center space-x-2.5">
                                            <span class="w-6 h-6 rounded-full bg-blue-600 text-white font-bold text-xs flex items-center justify-center">${round.round_number || idx + 1}</span>
                                            <h5 class="text-sm font-bold text-slate-900">${round.round_name}</h5>
                                        </div>
                                        <div class="flex items-center space-x-3 text-xs text-slate-500 font-medium">
                                            <span><i data-lucide="clock" class="w-3.5 h-3.5 inline mr-1"></i>${round.duration}</span>
                                            <span>•</span>
                                            <span class="px-2 py-0.5 rounded bg-slate-100 font-semibold">${round.platform}</span>
                                        </div>
                                    </div>

                                    <div class="mt-3 space-y-2">
                                        ${(round.sections || []).map(sec => `
                                            <div class="p-2.5 bg-slate-50 rounded-lg text-xs flex items-start justify-between">
                                                <div>
                                                    <span class="font-bold text-slate-800">${sec.name}</span>
                                                    <p class="text-slate-500 mt-0.5">${sec.details}</p>
                                                </div>
                                                <span class="font-semibold text-blue-700 text-[11px] whitespace-nowrap ml-4">${sec.duration}</span>
                                            </div>
                                        `).join('')}
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>

                    <!-- SECTION 4: SYLLABUS TOPICS -->
                    <div class="my-8">
                        <h4 class="text-sm font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center space-x-2">
                            <i data-lucide="book-open" class="w-4 h-4 text-blue-600"></i>
                            <span>Detailed Sectional Syllabus</span>
                        </h4>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            ${(comp.syllabus || []).map(s => `
                                <div class="bg-white border border-slate-200 rounded-xl p-4">
                                    <h6 class="text-xs font-extrabold text-blue-700 uppercase tracking-wider mb-2">${s.section}</h6>
                                    <div class="flex flex-wrap gap-1.5">
                                        ${(s.topics || []).map(topic => `
                                            <span class="px-2.5 py-1 rounded-md bg-slate-100 text-slate-700 text-xs font-medium">${topic}</span>
                                        `).join('')}
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>

                    <!-- SECTION 5: SELECTION PROCESS ROADMAP -->
                    <div class="my-8">
                        <h4 class="text-sm font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center space-x-2">
                            <i data-lucide="git-commit" class="w-4 h-4 text-blue-600"></i>
                            <span>End-to-End Selection Workflow</span>
                        </h4>
                        <div class="space-y-3">
                            ${(comp.selection_process || []).map((step, idx) => `
                                <div class="flex items-start space-x-3 text-xs p-3 rounded-xl bg-slate-50 border border-slate-100">
                                    <span class="w-5 h-5 rounded-full bg-blue-100 text-blue-700 font-bold flex items-center justify-center flex-shrink-0 mt-0.5">${idx + 1}</span>
                                    <span class="font-medium text-slate-700 leading-relaxed">${step}</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>

                    <!-- SECTION 6: PREPARATION TIPS & PREVIOUS QUESTIONS -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-8">
                        <div class="p-5 rounded-2xl bg-amber-50/70 border border-amber-200">
                            <h5 class="text-xs font-bold uppercase tracking-wider text-amber-900 mb-3 flex items-center space-x-1.5">
                                <i data-lucide="lightbulb" class="w-4 h-4 text-amber-600"></i>
                                <span>Insider Interview Tips</span>
                            </h5>
                            <ul class="text-xs text-amber-950 space-y-2 list-disc pl-4 font-medium">
                                ${(comp.interview_tips || []).map(tip => `<li>${tip}</li>`).join('')}
                            </ul>
                        </div>

                        <div class="p-5 rounded-2xl bg-slate-50 border border-slate-200">
                            <h5 class="text-xs font-bold uppercase tracking-wider text-slate-800 mb-3 flex items-center space-x-1.5">
                                <i data-lucide="help-circle" class="w-4 h-4 text-blue-600"></i>
                                <span>Recent Real Interview Questions</span>
                            </h5>
                            <ul class="text-xs text-slate-700 space-y-2.5 font-medium">
                                ${(comp.frequent_questions || []).map(q => `
                                    <li class="flex items-start space-x-2">
                                        <i data-lucide="chevron-right" class="w-3.5 h-3.5 text-blue-500 mt-0.5 flex-shrink-0"></i>
                                        <span>${q}</span>
                                    </li>
                                `).join('')}
                            </ul>
                        </div>
                    </div>

                    <!-- Footer Action -->
                    <div class="pt-6 border-t border-slate-200 flex justify-between items-center">
                        <button onclick="CompaniesModule.closeCompanyModal()" class="px-5 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition">
                            Close Guide
                        </button>
                        <button onclick="CompaniesModule.closeCompanyModal(); App.switchTab('prep');" class="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-xl shadow-sm transition">
                            Practice Questions for ${comp.name} →
                        </button>
                    </div>
                </div>
            `;
            if (window.lucide) window.lucide.createIcons();
        } catch (err) {
            console.error('Error viewing company hiring process:', err);
            content.innerHTML = `<p class="p-8 text-rose-500 text-center">Failed to load hiring process details.</p>`;
        }
    },

    closeCompanyModal() {
        const modal = document.getElementById('company-details-modal');
        if (modal) modal.classList.add('hidden');
    },

    async checkEligibility(slug) {
        const cgpa = document.getElementById('el-cgpa').value;
        const backlogs = document.getElementById('el-backlogs').value;
        const gap = document.getElementById('el-gap').value;
        const resultBox = document.getElementById('eligibility-result-box');

        if (!resultBox) return;

        resultBox.innerHTML = `Checking criteria...`;
        resultBox.classList.remove('hidden');

        try {
            const res = await fetch(`/api/companies/${slug}/check-eligibility`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    cgpa: parseFloat(cgpa) || 0,
                    backlogs: parseInt(backlogs) || 0,
                    gap_years: parseInt(gap) || 0
                })
            });

            const data = await res.json();

            if (data.eligible) {
                resultBox.className = "mt-4 p-4 rounded-xl bg-emerald-100 border border-emerald-300 text-emerald-950 text-xs";
                resultBox.innerHTML = `
                    <div class="flex items-center space-x-2 font-bold text-emerald-800 text-sm mb-1">
                        <i data-lucide="check-circle" class="w-4 h-4"></i>
                        <span>${data.message}</span>
                    </div>
                    <p class="font-medium mt-1">${data.recommended_action}</p>
                `;
            } else {
                resultBox.className = "mt-4 p-4 rounded-xl bg-rose-100 border border-rose-300 text-rose-950 text-xs";
                resultBox.innerHTML = `
                    <div class="flex items-center space-x-2 font-bold text-rose-800 text-sm mb-1">
                        <i data-lucide="alert-triangle" class="w-4 h-4"></i>
                        <span>${data.message}</span>
                    </div>
                    <ul class="list-disc pl-4 space-y-1 mt-1 font-medium">
                        ${(data.reasons || []).map(r => `<li>${r}</li>`).join('')}
                    </ul>
                    <p class="text-rose-900 mt-2 font-semibold">Tip: ${data.recommended_action}</p>
                `;
            }

            if (window.lucide) window.lucide.createIcons();
        } catch (err) {
            console.error('Eligibility check error:', err);
            resultBox.innerHTML = `<span class="text-rose-600">Error verifying eligibility.</span>`;
        }
    }
};

window.CompaniesModule = CompaniesModule;
