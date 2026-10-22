// Preparation Module: Notes, Interactive Practice, Code Runner & HR Simulator

const PrepModule = {
    currentCategory: 'Aptitude', // Aptitude, DSA, Technical, HR
    currentSubView: 'notes',    // 'notes' or 'practice'
    notes: [],
    problems: [],
    activeProblem: null,
    activeLanguage: 'python',
    activeNoteId: null,

    init() {
        this.bindEvents();
        this.loadCategoryData();
    },

    refresh() {
        this.loadCategoryData();
    },

    setCategory(category) {
        this.currentCategory = category;
        this.updateCategoryTabs();
        this.loadCategoryData();
    },

    bindEvents() {
        // Category buttons
        document.querySelectorAll('[data-prep-cat]').forEach(btn => {
            btn.addEventListener('click', () => {
                const cat = btn.getAttribute('data-prep-cat');
                this.currentCategory = cat;
                this.updateCategoryTabs();
                this.loadCategoryData();
            });
        });

        // Subview toggles (Notes vs Practice)
        const btnNotes = document.getElementById('prep-view-notes-btn');
        const btnPractice = document.getElementById('prep-view-practice-btn');

        if (btnNotes && btnPractice) {
            btnNotes.addEventListener('click', () => {
                this.currentSubView = 'notes';
                this.updateSubViewToggles();
            });
            btnPractice.addEventListener('click', () => {
                this.currentSubView = 'practice';
                this.updateSubViewToggles();
            });
        }
    },

    updateCategoryTabs() {
        document.querySelectorAll('[data-prep-cat]').forEach(btn => {
            const cat = btn.getAttribute('data-prep-cat');
            if (cat === this.currentCategory) {
                btn.className = "px-4 py-2 text-xs font-bold rounded-xl bg-blue-600 text-white shadow-sm flex items-center space-x-1.5 transition";
            } else {
                btn.className = "px-4 py-2 text-xs font-semibold rounded-xl text-slate-600 hover:bg-slate-100 flex items-center space-x-1.5 transition";
            }
        });

        const titleEl = document.getElementById('prep-category-title');
        const descEl = document.getElementById('prep-category-desc');

        const meta = {
            'Aptitude': {
                title: 'Aptitude Preparation',
                desc: 'Quantitative Aptitude, Logical Reasoning, and Verbal Ability notes with instant formula cheatsheets and timed practice.'
            },
            'DSA': {
                title: 'Data Structures & Algorithms (DSA)',
                desc: 'Pattern-based problem solving (Sliding Window, Two Pointers, Trees, DP) with interactive in-browser multi-language code runner.'
            },
            'Technical': {
                title: 'Technical Core Subjects',
                desc: 'Deep-dive revision for DBMS, Operating Systems, Computer Networks, and System Design with high-frequency interview questions.'
            },
            'HR': {
                title: 'HR & Behavioral Interview Prep',
                desc: 'Master the STAR framework, top 25 behavioral questions, situational conflict management, and salary negotiation tactics.'
            }
        };

        if (titleEl && meta[this.currentCategory]) titleEl.textContent = meta[this.currentCategory].title;
        if (descEl && meta[this.currentCategory]) descEl.textContent = meta[this.currentCategory].desc;
    },

    updateSubViewToggles() {
        const btnNotes = document.getElementById('prep-view-notes-btn');
        const btnPractice = document.getElementById('prep-view-practice-btn');
        const containerNotes = document.getElementById('prep-notes-container');
        const containerPractice = document.getElementById('prep-practice-container');

        if (this.currentSubView === 'notes') {
            btnNotes.className = "px-4 py-1.5 text-xs font-bold rounded-lg bg-white text-slate-900 shadow-sm transition";
            btnPractice.className = "px-4 py-1.5 text-xs font-medium text-slate-500 hover:text-slate-900 transition";
            if (containerNotes) containerNotes.classList.remove('hidden');
            if (containerPractice) containerPractice.classList.add('hidden');
        } else {
            btnPractice.className = "px-4 py-1.5 text-xs font-bold rounded-lg bg-white text-slate-900 shadow-sm transition";
            btnNotes.className = "px-4 py-1.5 text-xs font-medium text-slate-500 hover:text-slate-900 transition";
            if (containerPractice) containerPractice.classList.remove('hidden');
            if (containerNotes) containerNotes.classList.add('hidden');
        }
    },

    async loadCategoryData() {
        await Promise.all([
            this.fetchNotes(),
            this.fetchProblems()
        ]);
        this.updateSubViewToggles();
    },

    async fetchNotes() {
        const container = document.getElementById('prep-notes-list');
        if (!container) return;

        container.innerHTML = `
            <div class="col-span-full py-12 text-center text-slate-400">
                <div class="inline-block animate-spin rounded-full h-7 w-7 border-3 border-blue-600 border-t-transparent"></div>
            </div>
        `;

        try {
            const res = await fetch(`/api/prep/notes?category=${this.currentCategory}`);
            const data = await res.json();
            this.notes = data.notes || [];

            this.renderNotesList();
        } catch (err) {
            console.error('Error fetching prep notes:', err);
        }
    },

    renderNotesList() {
        const container = document.getElementById('prep-notes-list');
        if (!container) return;

        if (this.notes.length === 0) {
            container.innerHTML = `
                <div class="col-span-full py-12 text-center text-slate-400">
                    <p>No notes found for this category yet.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = this.notes.map(note => `
            <div class="bg-white rounded-2xl border border-slate-200 p-6 hover:shadow-md hover:border-blue-300 transition duration-200 flex flex-col justify-between group cursor-pointer" onclick="PrepModule.openNoteModal(${note.id})">
                <div>
                    <div class="flex items-center justify-between text-xs font-semibold mb-3">
                        <span class="px-2.5 py-1 rounded-md bg-blue-50 text-blue-700">${note.subcategory}</span>
                        <div class="flex items-center space-x-2 text-slate-400">
                            <span><i data-lucide="clock" class="w-3.5 h-3.5 inline mr-0.5"></i>${note.read_time}</span>
                            <span>•</span>
                            <span class="${note.difficulty === 'Beginner' ? 'text-emerald-600' : note.difficulty === 'Intermediate' ? 'text-amber-600' : 'text-rose-600'}">${note.difficulty}</span>
                        </div>
                    </div>

                    <h3 class="text-base font-bold text-slate-900 group-hover:text-blue-600 transition leading-snug">
                        ${note.title}
                    </h3>
                    <p class="text-xs text-slate-500 mt-2 line-clamp-3 leading-relaxed">
                        ${note.summary}
                    </p>

                    ${note.formula_sheet ? `
                        <div class="mt-4 p-2.5 bg-slate-50 rounded-xl border border-slate-100 text-[11px] font-mono text-slate-700 truncate">
                            <span class="text-blue-600 font-bold">⚡ Key:</span> ${note.formula_sheet}
                        </div>
                    ` : ''}
                </div>

                <div class="mt-5 pt-4 border-t border-slate-100 flex items-center justify-between text-xs font-semibold text-blue-600 group-hover:translate-x-1 transition-transform duration-200">
                    <span>Read Study Guide</span>
                    <i data-lucide="arrow-right" class="w-4 h-4"></i>
                </div>
            </div>
        `).join('');

        if (window.lucide) window.lucide.createIcons();
    },

    async openNoteModal(noteId) {
        const modal = document.getElementById('note-reader-modal');
        const content = document.getElementById('note-reader-content');
        if (!modal || !content) return;

        modal.classList.remove('hidden');
        content.innerHTML = `
            <div class="p-12 text-center">
                <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-600 border-t-transparent"></div>
            </div>
        `;

        try {
            const res = await fetch(`/api/prep/notes/${noteId}`);
            const note = await res.json();

            // Render Markdown
            const htmlContent = window.marked ? window.marked.parse(note.content_markdown) : `<pre>${note.content_markdown}</pre>`;

            content.innerHTML = `
                <div class="p-6 md:p-10">
                    <!-- Header -->
                    <div class="flex items-start justify-between pb-6 border-b border-slate-200">
                        <div>
                            <div class="flex items-center space-x-2 text-xs font-semibold mb-2">
                                <span class="px-2.5 py-1 rounded bg-blue-100 text-blue-800">${note.category}</span>
                                <span class="text-slate-400">›</span>
                                <span class="text-slate-600">${note.subcategory}</span>
                                <span class="text-slate-400">•</span>
                                <span class="text-slate-500"><i data-lucide="clock" class="w-3.5 h-3.5 inline mr-1"></i>${note.read_time}</span>
                            </div>
                            <h2 class="text-2xl md:text-3xl font-extrabold text-slate-900">${note.title}</h2>
                        </div>
                        <button onclick="PrepModule.closeNoteModal()" class="p-2 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-xl">
                            <i data-lucide="x" class="w-6 h-6"></i>
                        </button>
                    </div>

                    <!-- Key Takeaways Banner -->
                    ${(note.key_takeaways || []).length > 0 ? `
                        <div class="mt-6 p-4 rounded-xl bg-blue-50 border border-blue-100">
                            <h4 class="text-xs font-bold text-blue-900 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
                                <i data-lucide="sparkles" class="w-4 h-4 text-blue-600"></i>
                                <span>Core Takeaways for Interviews</span>
                            </h4>
                            <ul class="text-xs text-blue-950 space-y-1.5 pl-4 list-disc font-medium">
                                ${(note.key_takeaways || []).map(t => `<li>${t}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}

                    <!-- Markdown Body -->
                    <div class="markdown-body mt-6 text-sm text-slate-800 leading-relaxed">
                        ${htmlContent}
                    </div>

                    <!-- Footer Action -->
                    <div class="mt-8 pt-6 border-t border-slate-200 flex justify-between items-center">
                        <button onclick="PrepModule.closeNoteModal()" class="px-5 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition">
                            Back to Notes
                        </button>
                        <button onclick="PrepModule.closeNoteModal(); PrepModule.currentSubView = 'practice'; PrepModule.updateSubViewToggles();" class="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-xl shadow-sm transition">
                            Practice Questions on this Topic →
                        </button>
                    </div>
                </div>
            `;
            if (window.lucide) window.lucide.createIcons();
        } catch (err) {
            console.error('Error opening note:', err);
            content.innerHTML = `<p class="p-8 text-rose-500 text-center">Failed to load note.</p>`;
        }
    },

    closeNoteModal() {
        const modal = document.getElementById('note-reader-modal');
        if (modal) modal.classList.add('hidden');
    },

    async fetchProblems() {
        const listContainer = document.getElementById('prep-problems-selector');
        if (!listContainer) return;

        try {
            const res = await fetch(`/api/prep/problems?category=${this.currentCategory}`);
            const data = await res.json();
            this.problems = data.problems || [];

            this.renderProblemsSelector();
            if (this.problems.length > 0) {
                this.selectProblem(this.problems[0].id);
            } else {
                document.getElementById('prep-problem-workspace').innerHTML = `
                    <div class="p-12 text-center text-slate-400">
                        <p>No practice problems currently available for this category.</p>
                    </div>
                `;
            }
        } catch (err) {
            console.error('Error fetching problems:', err);
        }
    },

    renderProblemsSelector() {
        const container = document.getElementById('prep-problems-selector');
        if (!container) return;

        container.innerHTML = this.problems.map(p => `
            <button onclick="PrepModule.selectProblem(${p.id})" id="prob-item-${p.id}" class="w-full text-left p-3.5 rounded-xl border border-slate-200 hover:border-blue-400 bg-white transition mb-2.5 flex items-start justify-between">
                <div>
                    <div class="flex items-center space-x-2 text-[11px] font-semibold mb-1">
                        <span class="px-2 py-0.5 rounded ${
                            p.difficulty === 'Easy' ? 'bg-emerald-50 text-emerald-700' :
                            p.difficulty === 'Medium' ? 'bg-amber-50 text-amber-700' :
                            'bg-rose-50 text-rose-700'
                        }">${p.difficulty}</span>
                        <span class="text-slate-400">${p.subcategory}</span>
                    </div>
                    <h4 class="text-xs font-bold text-slate-800 line-clamp-1">${p.title}</h4>
                    <div class="flex flex-wrap gap-1 mt-1.5">
                        ${(p.companies_asked || []).slice(0, 2).map(c => `
                            <span class="text-[10px] px-1.5 py-0.2 rounded bg-slate-100 text-slate-600">${c}</span>
                        `).join('')}
                    </div>
                </div>
                ${p.user_status === 'Solved' ? `
                    <span class="p-1 text-emerald-600 bg-emerald-50 rounded-full flex-shrink-0" title="Solved">
                        <i data-lucide="check" class="w-3.5 h-3.5"></i>
                    </span>
                ` : ''}
            </button>
        `).join('');

        if (window.lucide) window.lucide.createIcons();
    },

    async selectProblem(problemId) {
        // Highlight active selector item
        document.querySelectorAll('#prep-problems-selector button').forEach(b => {
            b.classList.remove('border-blue-600', 'bg-blue-50/40', 'ring-1', 'ring-blue-600');
        });
        const selectedBtn = document.getElementById(`prob-item-${problemId}`);
        if (selectedBtn) {
            selectedBtn.classList.add('border-blue-600', 'bg-blue-50/40', 'ring-1', 'ring-blue-600');
        }

        const workspace = document.getElementById('prep-problem-workspace');
        if (!workspace) return;

        workspace.innerHTML = `
            <div class="p-12 text-center text-slate-400">
                <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-600 border-t-transparent"></div>
            </div>
        `;

        try {
            const res = await fetch(`/api/prep/problems/${problemId}`);
            const problem = await res.json();
            this.activeProblem = problem;

            if (problem.problem_type === 'mcq' || problem.problem_type === 'hr_prompt') {
                this.renderMCQWorkspace(problem);
            } else if (problem.problem_type === 'coding') {
                this.renderCodingWorkspace(problem);
            }
        } catch (err) {
            console.error('Error loading problem workspace:', err);
        }
    },

    renderMCQWorkspace(p) {
        const workspace = document.getElementById('prep-problem-workspace');
        if (!workspace) return;

        const options = p.options || [];

        workspace.innerHTML = `
            <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
                <!-- Header -->
                <div class="flex items-center justify-between pb-4 border-b border-slate-100">
                    <div class="flex items-center space-x-2 text-xs font-semibold">
                        <span class="px-2.5 py-1 rounded-md bg-blue-50 text-blue-700">${p.category}</span>
                        <span class="px-2.5 py-1 rounded-md ${p.difficulty === 'Easy' ? 'bg-emerald-50 text-emerald-700' : p.difficulty === 'Medium' ? 'bg-amber-50 text-amber-700' : 'bg-rose-50 text-rose-700'}">${p.difficulty}</span>
                        <span class="text-slate-400">${p.subcategory}</span>
                    </div>
                    <div class="flex items-center space-x-1.5 text-xs text-slate-500 font-medium">
                        <i data-lucide="briefcase" class="w-3.5 h-3.5 text-slate-400"></i>
                        <span>Asked in: ${(p.companies_asked || []).join(', ')}</span>
                    </div>
                </div>

                <!-- Question Text -->
                <div class="py-6">
                    <h3 class="text-lg font-bold text-slate-900 leading-relaxed whitespace-pre-line">${p.question_text}</h3>
                </div>

                <!-- Options List -->
                <div class="space-y-3" id="mcq-options-container">
                    ${options.map((opt, idx) => `
                        <label class="flex items-center p-4 rounded-xl border border-slate-200 hover:border-blue-400 hover:bg-blue-50/30 cursor-pointer transition option-item" id="opt-label-${idx}">
                            <input type="radio" name="mcq_option" value="${opt.replace(/"/g, '&quot;')}" class="w-4 h-4 text-blue-600 focus:ring-blue-500 mr-3">
                            <span class="text-sm font-medium text-slate-800">${opt}</span>
                        </label>
                    `).join('')}
                </div>

                <!-- Explanation Result Container -->
                <div id="mcq-result-box" class="hidden mt-6 p-5 rounded-xl"></div>

                <!-- Footer CTAs -->
                <div class="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between">
                    <span class="text-xs text-slate-400 font-medium">Select an option and submit to check correctness.</span>
                    <button onclick="PrepModule.submitMCQ()" id="mcq-submit-btn" class="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-xl shadow-sm transition">
                        Submit Answer
                    </button>
                </div>
            </div>
        `;

        if (window.lucide) window.lucide.createIcons();
    },

    async submitMCQ() {
        if (!this.activeProblem) return;
        const selected = document.querySelector('input[name="mcq_option"]:checked');
        if (!selected) {
            App.showToast('Please select an option before submitting', 'error');
            return;
        }

        const selectedVal = selected.value;
        const btn = document.getElementById('mcq-submit-btn');
        if (btn) btn.disabled = true;

        try {
            const res = await fetch(`/api/prep/problems/${this.activeProblem.id}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ selected_option: selectedVal })
            });
            const data = await res.json();

            const resultBox = document.getElementById('mcq-result-box');
            resultBox.classList.remove('hidden');

            if (data.is_correct) {
                resultBox.className = "mt-6 p-5 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-950";
                resultBox.innerHTML = `
                    <div class="flex items-center space-x-2 text-emerald-700 font-bold text-sm mb-2">
                        <i data-lucide="check-circle" class="w-5 h-5"></i>
                        <span>Correct Answer! (+${data.score_earned} points)</span>
                    </div>
                    <div class="text-xs leading-relaxed text-slate-700 mt-2 font-mono whitespace-pre-line bg-white/70 p-3 rounded-lg border border-emerald-100">
                        ${data.explanation}
                    </div>
                `;
                App.showToast('Great job! Question marked as solved.', 'success');
            } else {
                resultBox.className = "mt-6 p-5 rounded-xl bg-rose-50 border border-rose-200 text-rose-950";
                resultBox.innerHTML = `
                    <div class="flex items-center space-x-2 text-rose-700 font-bold text-sm mb-2">
                        <i data-lucide="x-circle" class="w-5 h-5"></i>
                        <span>Incorrect. Correct Answer: <span class="font-mono text-slate-900">${data.correct_answer}</span></span>
                    </div>
                    <div class="text-xs leading-relaxed text-slate-700 mt-2 font-mono whitespace-pre-line bg-white/70 p-3 rounded-lg border border-rose-100">
                        ${data.explanation}
                    </div>
                `;
            }

            if (window.lucide) window.lucide.createIcons();
            if (App.stats) App.loadDashboardStats();
        } catch (err) {
            console.error('Error submitting MCQ:', err);
        } finally {
            if (btn) btn.disabled = false;
        }
    },

    renderCodingWorkspace(p) {
        const workspace = document.getElementById('prep-problem-workspace');
        if (!workspace) return;

        const starterCodes = p.starter_code || {};
        const currentCode = starterCodes[this.activeLanguage] || starterCodes['python'] || '';

        workspace.innerHTML = `
            <div class="bg-white rounded-2xl border border-slate-200 shadow-sm flex flex-col overflow-hidden">
                <!-- Problem Statement Section -->
                <div class="p-6 border-b border-slate-200">
                    <div class="flex items-center justify-between pb-3 border-b border-slate-100">
                        <div class="flex items-center space-x-2 text-xs font-semibold">
                            <span class="px-2.5 py-1 rounded-md bg-blue-50 text-blue-700">${p.category}</span>
                            <span class="px-2.5 py-1 rounded-md ${p.difficulty === 'Easy' ? 'bg-emerald-50 text-emerald-700' : p.difficulty === 'Medium' ? 'bg-amber-50 text-amber-700' : 'bg-rose-50 text-rose-700'}">${p.difficulty}</span>
                            <span class="text-slate-400">${p.subcategory}</span>
                        </div>
                        <div class="text-xs font-medium text-slate-500">
                            Asked by: ${(p.companies_asked || []).join(', ')}
                        </div>
                    </div>
                    
                    <h3 class="text-xl font-extrabold text-slate-900 mt-4">${p.title}</h3>
                    <div class="markdown-body text-xs text-slate-600 mt-3 max-h-48 overflow-y-auto pr-2">
                        ${window.marked ? window.marked.parse(p.question_text) : p.question_text}
                    </div>
                </div>

                <!-- Code Editor Control Bar -->
                <div class="bg-slate-900 text-slate-300 px-4 py-2.5 flex items-center justify-between border-b border-slate-800">
                    <!-- Language Selector -->
                    <div class="flex items-center space-x-1.5 text-xs font-semibold">
                        <span class="text-slate-500 mr-1 text-[11px] uppercase">Language:</span>
                        <button onclick="PrepModule.switchLanguage('python')" class="px-2.5 py-1 rounded ${this.activeLanguage === 'python' ? 'bg-blue-600 text-white' : 'hover:bg-slate-800 text-slate-400'}">Python 3</button>
                        <button onclick="PrepModule.switchLanguage('cpp')" class="px-2.5 py-1 rounded ${this.activeLanguage === 'cpp' ? 'bg-blue-600 text-white' : 'hover:bg-slate-800 text-slate-400'}">C++ 20</button>
                        <button onclick="PrepModule.switchLanguage('java')" class="px-2.5 py-1 rounded ${this.activeLanguage === 'java' ? 'bg-blue-600 text-white' : 'hover:bg-slate-800 text-slate-400'}">Java 17</button>
                    </div>

                    <!-- Reset Code -->
                    <button onclick="PrepModule.resetCode()" class="text-xs text-slate-400 hover:text-slate-200 flex items-center space-x-1">
                        <i data-lucide="rotate-ccw" class="w-3.5 h-3.5"></i>
                        <span>Reset</span>
                    </button>
                </div>

                <!-- Code Input Area -->
                <div class="relative bg-slate-950 p-4">
                    <textarea id="code-editor-input" class="w-full h-72 bg-transparent text-emerald-400 font-mono text-xs focus:outline-none resize-none code-editor-area leading-relaxed" spellcheck="false">${currentCode}</textarea>
                </div>

                <!-- Output Console & Test Cases -->
                <div class="p-4 bg-slate-50 border-t border-slate-200">
                    <div class="flex items-center justify-between mb-3">
                        <h5 class="text-xs font-bold text-slate-700 uppercase tracking-wider flex items-center space-x-1.5">
                            <i data-lucide="terminal" class="w-3.5 h-3.5 text-slate-500"></i>
                            <span>Test Case Evaluation</span>
                        </h5>
                        <button onclick="PrepModule.toggleEditorial()" class="text-xs font-bold text-blue-600 hover:text-blue-700">
                            View Editorial / Optimal Solution
                        </button>
                    </div>

                    <div id="code-output-console" class="bg-white rounded-xl border border-slate-200 p-4 text-xs font-mono text-slate-700 space-y-2">
                        <div class="text-slate-400 italic">Click "Run Code" or "Submit Solution" to test against inputs.</div>
                    </div>

                    <div id="code-editorial-box" class="hidden mt-3 p-4 bg-blue-50 border border-blue-200 rounded-xl text-xs text-slate-800">
                        <h6 class="font-bold text-blue-900 mb-1">Optimal Approach & Complexity:</h6>
                        <p class="mb-3 leading-relaxed">${p.explanation || 'Approach details.'}</p>
                    </div>
                </div>

                <!-- Footer Action Buttons -->
                <div class="p-4 bg-white border-t border-slate-200 flex items-center justify-between">
                    <span class="text-xs text-slate-400">Time Limit: 2.0s • Memory: 256MB</span>
                    <div class="flex items-center space-x-3">
                        <button onclick="PrepModule.runCode(false)" class="px-5 py-2 rounded-xl border border-slate-300 hover:bg-slate-100 text-xs font-bold text-slate-700 flex items-center space-x-1.5 transition">
                            <i data-lucide="play" class="w-3.5 h-3.5 text-slate-600"></i>
                            <span>Run Sample Cases</span>
                        </button>
                        <button onclick="PrepModule.runCode(true)" class="px-6 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-xs font-bold text-white shadow-sm flex items-center space-x-1.5 transition">
                            <i data-lucide="send" class="w-3.5 h-3.5"></i>
                            <span>Submit Solution</span>
                        </button>
                    </div>
                </div>
            </div>
        `;

        if (window.lucide) window.lucide.createIcons();
    },

    switchLanguage(lang) {
        this.activeLanguage = lang;
        if (!this.activeProblem) return;
        const starter = (this.activeProblem.starter_code || {})[lang] || '';
        const input = document.getElementById('code-editor-input');
        if (input) input.value = starter;
        this.renderCodingWorkspace(this.activeProblem);
    },

    resetCode() {
        if (!this.activeProblem) return;
        const starter = (this.activeProblem.starter_code || {})[this.activeLanguage] || '';
        const input = document.getElementById('code-editor-input');
        if (input) input.value = starter;
        App.showToast('Code reset to default template', 'info');
    },

    toggleEditorial() {
        const box = document.getElementById('code-editorial-box');
        if (box) box.classList.toggle('hidden');
    },

    async runCode(isSubmit = false) {
        if (!this.activeProblem) return;
        const input = document.getElementById('code-editor-input');
        const code = input ? input.value : '';

        const consoleBox = document.getElementById('code-output-console');
        if (consoleBox) {
            consoleBox.innerHTML = `
                <div class="flex items-center space-x-2 text-slate-500">
                    <div class="animate-spin rounded-full h-4 w-4 border-2 border-blue-600 border-t-transparent"></div>
                    <span>Compiling & executing test cases...</span>
                </div>
            `;
        }

        try {
            const res = await fetch(`/api/prep/problems/${this.activeProblem.id}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    code,
                    language: this.activeLanguage,
                    is_submit: isSubmit
                })
            });

            const data = await res.json();

            if (consoleBox) {
                if (data.success) {
                    consoleBox.innerHTML = `
                        <div class="flex items-center justify-between pb-2 border-b border-slate-100 text-emerald-600 font-bold">
                            <span>✔ All ${data.test_results.length} Test Cases Passed!</span>
                            <span class="text-xs bg-emerald-50 px-2 py-0.5 rounded text-emerald-700 font-semibold">+${data.score_earned} Points</span>
                        </div>
                        <div class="space-y-2 mt-2">
                            ${(data.test_results || []).map(tc => `
                                <div class="p-2.5 rounded-lg bg-emerald-50/50 border border-emerald-200/60">
                                    <div class="text-[11px] text-slate-500">Input: <span class="text-slate-800">${tc.input}</span></div>
                                    <div class="text-[11px] text-slate-500">Expected: <span class="text-emerald-700 font-semibold">${tc.expected}</span> | Actual: <span class="text-emerald-700 font-semibold">${tc.actual}</span></div>
                                </div>
                            `).join('')}
                        </div>
                    `;
                    if (isSubmit) {
                        App.showToast('Congratulations! Problem solved.', 'success');
                        this.fetchProblems();
                        if (App.stats) App.loadDashboardStats();
                    }
                } else {
                    consoleBox.innerHTML = `
                        <div class="text-rose-600 font-bold mb-2">✖ Some Test Cases Failed</div>
                        <div class="space-y-2">
                            ${(data.test_results || []).map(tc => `
                                <div class="p-2.5 rounded-lg ${tc.passed ? 'bg-emerald-50 border border-emerald-100' : 'bg-rose-50 border border-rose-200'}">
                                    <div class="text-[11px] font-semibold ${tc.passed ? 'text-emerald-700' : 'text-rose-700'}">Test Case ${tc.case}: ${tc.passed ? 'PASSED' : 'FAILED'}</div>
                                    <div class="text-[11px] text-slate-600 mt-1">Input: ${tc.input}</div>
                                    <div class="text-[11px] text-slate-600">Expected: ${tc.expected} | Got: <span class="text-rose-700 font-bold">${tc.actual}</span></div>
                                </div>
                            `).join('')}
                        </div>
                    `;
                }
            }
        } catch (err) {
            console.error('Code execution error:', err);
            if (consoleBox) consoleBox.innerHTML = `<span class="text-rose-600">Execution Error. Try again.</span>`;
        }
    }
};

window.PrepModule = PrepModule;
