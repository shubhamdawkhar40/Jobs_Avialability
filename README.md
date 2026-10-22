# CareerCraft: Job Portal & Placement Preparation Website

A modern, full-stack unified Job Portal and Placement Preparation platform built for engineering students, fresh graduates, and tech job seekers.

---

## 🌟 Key Features

### 1. Job Portal
- **Rich Job Listings**: Curated software engineering, fresher, internship, and analyst openings across Top Product companies, High-growth Startups, and IT MNCs (Google, Amazon, Atlassian, Infosys, TCS, Swiggy, Razorpay, etc.).
- **Multi-Filter System**: Instant filtering by Role / Keyword, Location (Bengaluru, Hyderabad, Pune, Remote, etc.), Workplace type (Remote, Hybrid, On-site), Experience Level (Fresher, 1-3 yrs, 3-5 yrs), and Salary.
- **Detailed Job Views**: Responsibilities, requirements checklist, tech stack chips, benefits pills, and deadline notices.
- **One-Click "Easy Apply"**: Interactive modal with pre-configured applicant details, resume attachment, portfolio link, and custom cover note.
- **Post a Job**: Recruiter-friendly form to publish new openings to the live portal.
- **Bookmarks & Saved Jobs**: Bookmark jobs to revisit or track later.

### 2. Comprehensive Preparation Hub
Structured into 4 core pillars with both **Notes & Cheatsheets** and **Interactive Problem Solvers**:

- **Aptitude Mastery**:
  - Quantitative Aptitude (Percentages, Profit & Loss shortcuts, Time, Speed & Distance, Train/Boat problems).
  - Logical Reasoning (Syllogisms Venn diagrams, Blood Relations family tree conventions, Series).
  - Verbal Ability (Subject-Verb agreement, idioms, reading comprehension).
  - Cheatsheets with memorization tables and formula shortcuts.
- **Data Structures & Algorithms (DSA)**:
  - Blind75 / Striver pattern guides: Sliding Window, Two Pointers, Trees, Graphs, Dynamic Programming.
  - Interactive In-Browser Code Runner with multi-language starter code (Python 3, C++ 20, Java 17).
  - Real-time test case evaluation, complexity breakdown, and solution code reveal.
- **Technical Core Subjects (CS)**:
  - **DBMS**: ACID properties, Transaction Isolation Anomalies (Dirty, Non-repeatable, Phantom Read), Normalization rules (1NF to BCNF), and B-Tree vs Hash Indexing.
  - **Operating Systems**: Process vs Thread context switching, 4 Coffman Deadlock conditions & Banker's Algorithm, Virtual Memory & Paging.
  - **Computer Networks**: OSI 7-layer model, TCP 3-way handshake vs UDP, HTTP/1.1 vs HTTP/2 vs HTTP/3 (QUIC).
- **HR & Behavioral Interview Preparation**:
  - The **STAR Framework** (Situation, Task, Action 50%, Result).
  - Top 25 behavioral questions with sample winning answers.
  - Conflict resolution scenarios, handling failure, salary negotiation scripts, and Dos & Don'ts.

### 3. Companies Hiring Process Roadmaps
Deep-dive placement guides for Top Tech and IT Giants:
- **TCS** (NQT Ninja, Digital & Prime cadres)
- **Infosys** (InfyTQ, Specialist Programmer - SP, Digital Specialist Engineer - DSE)
- **Amazon** (SDE-1 & Intern - 16 Leadership Principles, OA, Bar Raiser)
- **Google** (GOC challenge, SWE loops, Googliness)
- **Microsoft** (Codility assessment, LLD, AA round)
- **Accenture** (Cognitive, Coding elimination, Automated Communication, Interview)

For each company:
- **Interactive Eligibility Calculator**: Input your CGPA, active backlogs, and gap years to get an instant eligibility verdict and advice!
- **Round-by-Round Exam Pattern**: Timing, platforms (HackerRank, TCS iON, Codility, Wheebox), question distributions, negative marking policies.
- **Comprehensive Sectional Syllabus**: Complete topic checklists for numerical, reasoning, verbal, coding, and CS foundations.
- **Selection Workflow Timeline**: Step-by-step roadmap from registration to offer rollout.
- **Insider Tips & Previous Questions**: High-yield advice and authentic interview questions.

### 4. Progress & Application Tracker
- Live Placement Readiness Meter (`0 - 100%`).
- Problem-solving activity log with earned scores.
- Category mastery breakdown.
- Job application status tracking (Submitted, Under Review, Shortlisted).

---

## 🚀 Quickstart & Setup Guide

### Prerequisites
- Python 3.9+ (Installed on macOS)

### Running the Application

1. **Navigate to the project directory**:
   ```bash
   cd /Users/shubhamdawkhar/.gemini/antigravity/scratch/career-prep-portal
   ```

2. **Activate the Virtual Environment**:
   ```bash
   source .venv/bin/activate
   ```

3. **Install Dependencies (if not already installed)**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize and Seed the Database** (already initialized, but can re-run safely):
   ```bash
   python database.py
   ```

5. **Start the Web Server**:
   ```bash
   python app.py
   ```

6. **Open in Browser**:
   Visit [http://localhost:5050](http://localhost:5050) or [http://127.0.0.1:5050](http://127.0.0.1:5050).

---

## 📂 Project Architecture

```
career-prep-portal/
├── app.py                 # Flask server with REST APIs for Jobs, Prep & Companies
├── database.py            # SQLite schema initialization and seed dataset
├── portal.db              # SQLite Database file with relational tables
├── requirements.txt       # Python dependencies (Flask >= 3.0.0)
├── README.md              # Documentation and walkthrough
├── static/
│   ├── css/
│   │   └── styles.css     # Custom animations, glassmorphism, markdown typography
│   └── js/
│       ├── app.js         # Core application state, tabs, dashboard metrics, toast notifications
│       ├── jobs.js        # Job search, multi-filters, easy apply, save & post jobs
│       ├── prep.js        # Notes reader, interactive MCQ engine, in-browser code runner
│       └── companies.js   # Hiring roadmaps, exam pattern, syllabus, interactive eligibility calculator
└── templates/
    └── index.html         # Responsive Single Page Application shell with Tailwind & Lucide
```
