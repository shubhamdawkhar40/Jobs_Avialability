import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "portal.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # 1. Jobs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        company_logo_color TEXT,
        industry TEXT,
        location TEXT NOT NULL,
        workplace_type TEXT NOT NULL, -- Remote, Hybrid, On-site
        job_type TEXT NOT NULL,       -- Full-time, Internship, Contract
        experience_level TEXT NOT NULL, -- Fresher, 1-3 yrs, 3-5 yrs, 5+ yrs
        salary_range TEXT NOT NULL,
        description TEXT NOT NULL,
        requirements TEXT NOT NULL,   -- JSON array
        skills TEXT NOT NULL,         -- JSON array
        benefits TEXT NOT NULL,       -- JSON array
        deadline TEXT,
        posted_date TEXT,
        eligible_batches TEXT,
        apply_url TEXT,
        featured INTEGER DEFAULT 0
    )
    """)

    # 2. Applications Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id INTEGER NOT NULL,
        applicant_name TEXT NOT NULL,
        applicant_email TEXT NOT NULL,
        applicant_phone TEXT,
        experience_years TEXT,
        portfolio_url TEXT,
        resume_name TEXT,
        cover_note TEXT,
        status TEXT DEFAULT 'Submitted', -- Submitted, Under Review, Shortlisted, Interview Scheduled, Rejected
        applied_at TEXT NOT NULL,
        FOREIGN KEY (job_id) REFERENCES jobs (id)
    )
    """)

    # 3. Saved Jobs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id INTEGER UNIQUE NOT NULL,
        saved_at TEXT NOT NULL,
        FOREIGN KEY (job_id) REFERENCES jobs (id)
    )
    """)

    # 4. Prep Notes Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prep_notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,     -- Aptitude, DSA, Technical, HR
        subcategory TEXT NOT NULL,  -- Quantitative, Logical, Verbal, Arrays, Trees, DBMS, OS, Networks, Behavioral
        title TEXT NOT NULL,
        read_time TEXT,
        difficulty TEXT,            -- Beginner, Intermediate, Advanced
        summary TEXT NOT NULL,
        content_markdown TEXT NOT NULL,
        key_takeaways TEXT,         -- JSON array
        formula_sheet TEXT          -- JSON array or text
    )
    """)

    # 5. Prep Problems Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prep_problems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,       -- Aptitude, DSA, Technical, HR
        subcategory TEXT NOT NULL,
        title TEXT NOT NULL,
        difficulty TEXT NOT NULL,     -- Easy, Medium, Hard
        problem_type TEXT NOT NULL,   -- mcq, coding, hr_prompt
        question_text TEXT NOT NULL,
        options TEXT,                 -- JSON array for MCQ
        correct_answer TEXT,          -- string/index for MCQ
        explanation TEXT,             -- explanation for MCQ / editorial
        starter_code TEXT,            -- JSON {python: '', java: '', cpp: ''}
        solution_code TEXT,           -- JSON {python: '', java: '', cpp: ''}
        test_cases TEXT,              -- JSON array of {input, expected_output, is_sample}
        companies_asked TEXT          -- JSON array
    )
    """)

    # 6. User Problem Attempts & Bookmarks
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        problem_id INTEGER NOT NULL,
        status TEXT NOT NULL,         -- Solved, Attempted, Bookmarked
        user_code TEXT,
        selected_option TEXT,
        score INTEGER DEFAULT 0,
        attempted_at TEXT NOT NULL,
        FOREIGN KEY (problem_id) REFERENCES prep_problems (id)
    )
    """)

    # 7. Companies Hiring Process Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        slug TEXT UNIQUE NOT NULL,
        tier TEXT NOT NULL,           -- Tier-1 Tech / FAANG, High-Growth Product, IT Services, Fintech
        tagline TEXT,
        logo_color TEXT,
        avg_package TEXT,             -- e.g. 18 - 45 LPA
        roles_offered TEXT,           -- JSON array
        eligibility TEXT NOT NULL,    -- JSON object: {cgpa, backlogs, branches, graduation_year, gap_allowed}
        exam_pattern TEXT NOT NULL,   -- JSON array of rounds
        syllabus TEXT NOT NULL,       -- JSON array of sections with topics
        selection_process TEXT NOT NULL, -- JSON array of stages
        interview_tips TEXT NOT NULL, -- JSON array of string tips
        frequent_questions TEXT NOT NULL, -- JSON array of question strings
        difficulty_rating TEXT,       -- Easy, Medium, Hard, Very Hard
        hiring_season TEXT
    )
    """)

    conn.commit()
    conn.close()

def seed_data_if_empty():
    conn = get_db()
    cursor = conn.cursor()

    # Check if jobs exist
    cursor.execute("SELECT COUNT(*) as count FROM jobs")
    if cursor.fetchone()["count"] > 0:
        conn.close()
        return

    print("Seeding Career & Job Portal database with rich data...")

    # --- 1. JOBS SEED DATA ---
    jobs_data = [
        (
            "Software Development Engineer I (SDE-1)",
            "Amazon",
            "#FF9900",
            "Product / Big Tech",
            "Bengaluru, Karnataka (Hybrid)",
            "Hybrid",
            "Full-time",
            "Fresher (0-1 yrs)",
            "₹24 - ₹32 LPA",
            "Amazon is looking for passionate SDE-1 engineers to design, build, and ship massive scale distributed backend systems powering Amazon Prime and AWS services.",
            json.dumps([
                "Bachelor's or Master's degree in Computer Science, IT, or related technical field.",
                "Strong foundation in Data Structures, Algorithms, Object-Oriented Design, and System Architecture.",
                "Proficiency in at least one modern language: Java, C++, Python, or Go.",
                "Familiarity with cloud platforms (AWS preferred), CI/CD pipelines, and relational/NoSQL databases."
            ]),
            json.dumps(["Java", "Data Structures", "Algorithms", "System Design", "AWS", "SQL"]),
            json.dumps(["Relocation Bonus", "Stock Units (RSUs)", "Comprehensive Health Insurance", "Wellness Reimbursement", "Learning Allowance"]),
            "2026-11-30",
            "2026-10-18",
            "2024, 2025, 2026 Batch",
            "",
            1
        ),
        (
            "Graduate Software Engineer",
            "Atlassian",
            "#0052CC",
            "Product / Enterprise SaaS",
            "Bengaluru / Remote (TEAM Anywhere)",
            "Remote",
            "Full-time",
            "Fresher (0-1 yrs)",
            "₹22 - ₹28 LPA",
            "Join Atlassian's TEAM Anywhere and work on Jira, Confluence, and Bitbucket. Help build collaborative tools used by millions of developers and teams across the world.",
            json.dumps([
                "Graduating in 2025/2026 with B.Tech/M.Tech/MCA in CS, SE, or equivalent.",
                "Proven proficiency in TypeScript, React, Java, or Kotlin.",
                "Clear understanding of RESTful API design, microservices, and asynchronous architecture.",
                "Strong analytical and collaborative problem-solving skills."
            ]),
            json.dumps(["TypeScript", "React", "Java", "REST APIs", "Microservices", "Git"]),
            json.dumps(["100% Remote Flexibility", "Home Office Stipend ₹75,000", "Annual Learning Budget", "Mental Wellness Days"]),
            "2026-12-15",
            "2026-10-20",
            "2025, 2026 Batch",
            "",
            1
        ),
        (
            "Systems Engineer (Specialist Programmer - SP)",
            "Infosys",
            "#007CC3",
            "IT Services & Consulting",
            "Pune / Bengaluru / Hyderabad",
            "Hybrid",
            "Full-time",
            "Fresher (0-1 yrs)",
            "₹9.5 - ₹13 LPA",
            "Infosys Specialist Programmer role focuses on advanced programming, competitive coding, high-performance computing, AI/ML integration, and full-stack enterprise solutions.",
            json.dumps([
                "BE/B.Tech/ME/M.Tech/MCA/M.Sc with minimum 65% or 6.5 CGPA throughout academics.",
                "Exceptional algorithmic problem solving and dynamic programming capability.",
                "Proficiency in Python, Java, or C++ with knowledge of database querying (SQL).",
                "No active backlogs at the time of joining."
            ]),
            json.dumps(["Data Structures", "Algorithms", "Python", "Java", "SQL", "Full Stack"]),
            json.dumps(["Fast-track Career Growth", "Global Project Exposure", "Health & Term Insurance", "Higher Education Support"]),
            "2026-11-20",
            "2026-10-15",
            "2025, 2026 Batch",
            "",
            1
        ),
        (
            "Associate Software Engineer (Digital & Prime)",
            "Tata Consultancy Services (TCS)",
            "#0F2537",
            "IT Services & Consulting",
            "Pan India (Chennai, Mumbai, Delhi-NCR, Pune)",
            "On-site",
            "Full-time",
            "Fresher (0-1 yrs)",
            "₹7.5 - ₹11 LPA",
            "TCS Digital and Prime cadre roles offer high-impact engineering work in NextGen technologies like Cloud Architecture, Generative AI, Cyber Security, and Big Data.",
            json.dumps([
                "B.E. / B.Tech / M.E. / M.Tech / MCA / M.Sc with 60% or 6.0 CGPA throughout 10th, 12th, and Degree.",
                "Maximum 1 backlog allowed at the time of TCS NQT, clear by graduation.",
                "Strong conceptual knowledge in DBMS, Computer Networks, and Object-Oriented Programming.",
                "Proficient in C, C++, Java, or Python."
            ]),
            json.dumps(["C++", "Java", "Python", "DBMS", "Computer Networks", "Cybersecurity"]),
            json.dumps(["Digital Certification Incentives", "Medical Cover for Family", "Internal Mobility Programs", "TCS Elevate Growth Scheme"]),
            "2026-11-10",
            "2026-10-12",
            "2024, 2025, 2026 Batch",
            "",
            1
        ),
        (
            "Frontend Engineer - Platform & Growth",
            "Razorpay",
            "#0A2540",
            "Fintech",
            "Bengaluru, Karnataka (On-site)",
            "On-site",
            "Full-time",
            "1-3 yrs",
            "₹16 - ₹22 LPA",
            "Build slick, high-converting payment checkout experiences, merchant dashboards, and banking flows processing billions in daily transaction volume.",
            json.dumps([
                "1+ years of production experience building high-performance SPAs with React, Next.js, and TypeScript.",
                "Deep understanding of browser rendering lifecycle, Web Vitals, and responsive UI design.",
                "Experience with State Management (Redux Toolkit, Zustand) and modern build tools.",
                "Eye for design details, accessibility (a11y), and micro-interactions."
            ]),
            json.dumps(["React", "Next.js", "TypeScript", "Tailwind CSS", "Redux", "Web Performance"]),
            json.dumps(["ESOPs / Stock Options", "Free Gourmet Meals", "Comprehensive Health Cover", "Gadget Allowance"]),
            "2026-12-01",
            "2026-10-19",
            "All Batches",
            "",
            0
        ),
        (
            "Software Engineer Intern (Summer 2027)",
            "Google",
            "#4285F4",
            "Product / Big Tech",
            "Bengaluru / Hyderabad (Hybrid)",
            "Hybrid",
            "Internship",
            "Fresher (0-1 yrs)",
            "₹1,10,000 / month + Relocation",
            "Google invites student developers for a 10-12 week intensive summer engineering internship to work directly on Google Search, Android, Cloud, and YouTube infrastructure.",
            json.dumps([
                "Currently enrolled in a Bachelor's, Master's, or Dual Degree program in Computer Science or related STEM field.",
                "Graduating in 2026 or 2027.",
                "Demonstrated coding skills in C, C++, Java, or Python.",
                "Solid grasp of algorithms, time complexity, and recursion."
            ]),
            json.dumps(["C++", "Python", "Algorithms", "Operating Systems", "Distributed Systems"]),
            json.dumps(["Generous Monthly Stipend", "Relocation & Flights covered", "Free Meals & Barista Coffee", "Mentorship from Senior Staff SWE"]),
            "2026-11-25",
            "2026-10-10",
            "2026, 2027 Batch",
            "",
            1
        ),
        (
            "Associate Consultant - Cloud & AI",
            "Microsoft",
            "#00A4EF",
            "Product / Enterprise",
            "Hyderabad / Noida",
            "Hybrid",
            "Full-time",
            "Fresher (0-1 yrs)",
            "₹18 - ₹25 LPA",
            "Collaborate with enterprise leaders to architect, deploy, and scale enterprise Azure solutions, OpenAI LLM integrations, and robust cloud data foundations.",
            json.dumps([
                "Bachelor's degree in CS, Engineering, Math, or IT with minimum 7.0 CGPA.",
                "Familiarity with cloud concepts (IaaS, PaaS, SaaS) and Python / C# programming.",
                "Outstanding communication, presentation, and client management skills.",
                "Ability to translate business requirements into technical architectures."
            ]),
            json.dumps(["Azure", "Python", "C#", "Cloud Architecture", "Generative AI", "SQL"]),
            json.dumps(["Microsoft RSUs", "Annual Performance Bonus", "Health, Dental & Optical Cover", "Education Reimbursement"]),
            "2026-12-10",
            "2026-10-14",
            "2025, 2026 Batch",
            "",
            0
        ),
        (
            "Data Analyst / BI Engineer",
            "Swiggy",
            "#FC8019",
            "E-commerce / Consumer Tech",
            "Bengaluru, Karnataka (Hybrid)",
            "Hybrid",
            "Full-time",
            "1-3 yrs",
            "₹14 - ₹19 LPA",
            "Analyze order delivery logistics, consumer ordering habits, and restaurant growth metrics to drive algorithmic delivery dispatching and marketing ROI.",
            json.dumps([
                "Proficiency in SQL (window functions, CTEs, complex joins) and Python (Pandas, NumPy).",
                "Hands-on expertise in Tableau / PowerBI dashboard design.",
                "Strong grasp of hypothesis testing, A/B experimentation, and cohort retention.",
                "Degree in Engineering, Statistics, Economics, or Data Science."
            ]),
            json.dumps(["SQL", "Python", "Tableau", "Statistics", "A/B Testing", "Data Warehousing"]),
            json.dumps(["Swiggy One VIP Access", "Flexible Working Hours", "Parental Insurance", "Performance Incentives"]),
            "2026-11-18",
            "2026-10-16",
            "2023, 2024, 2025 Batch",
            "",
            0
        )
    ]

    cursor.executemany("""
    INSERT INTO jobs (
        title, company, company_logo_color, industry, location, workplace_type, job_type,
        experience_level, salary_range, description, requirements, skills, benefits,
        deadline, posted_date, eligible_batches, apply_url, featured
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, jobs_data)

    # --- 2. PREP NOTES SEED DATA ---
    notes_data = [
        # Aptitude - Quantitative
        (
            "Aptitude",
            "Quantitative",
            "Percentages, Profit & Loss Master Cheatsheet",
            "8 min read",
            "Beginner",
            "Core formulas, fraction-to-percentage conversion chart, successive discount tricks, and dishonest dealer shortcuts.",
            """# Percentages, Profit & Loss Master Formula Guide

## 1. Fast Fraction to Percentage Conversions
To solve quantitative problems in under 45 seconds, memorize these fractions:
- $1/2 = 50\%$
- $1/3 = 33.33\%$
- $1/4 = 25\%$
- $1/5 = 20\%$
- $1/6 = 16.66\%$
- $1/7 = 14.28\%$
- $1/8 = 12.5\%$
- $1/9 = 11.11\%$
- $1/11 = 9.09\%$
- $1/12 = 8.33\%$

## 2. Successive Percentage Change Formula
If an item's value changes by $A\\%$ and then successively by $B\\%$, the net percentage change is:
$$\\text{Net Change} = \\left(A + B + \\frac{A \\times B}{100}\\right)\\%$$
*(Use negative sign for decrease or discount)*

## 3. Profit & Loss Key Relations
- **Profit ($P$)**: $\\text{SP} - \\text{CP}$
- **Loss ($L$)**: $\\text{CP} - \\text{SP}$
- **Profit %**: $\\left(\\frac{P}{\\text{CP}}\\right) \\times 100$
- **Loss %**: $\\left(\\frac{L}{\\text{CP}}\\right) \\times 100$
- **Selling Price with Profit**: $\\text{SP} = \\text{CP} \\times \\left(1 + \\frac{P\\%}{100}\\right)$
- **Marked Price (MP) & Discount ($D$)**: $\\text{SP} = \\text{MP} \\times \\left(1 - \\frac{D\\%}{100}\\right)$

## 4. Dishonest Shopkeeper Shortcut
When a shopkeeper claims to sell at Cost Price but uses a false weight of $W_F$ grams instead of standard $W_T$ grams:
$$\\text{Gain % } = \\frac{\\text{Error}}{\\text{True Value} - \\text{Error}} \\times 100 = \\frac{W_T - W_F}{W_F} \\times 100$$
""",
            json.dumps(["Memorize fraction table for 1/2 to 1/12", "Net successive formula: A + B + (AB)/100", "Profit and loss are always computed on CP unless stated otherwise."]),
            "Net Change = A + B + (AB/100) | Gain% = (Error / (True - Error)) * 100"
        ),

        # Aptitude - Quantitative
        (
            "Aptitude",
            "Quantitative",
            "Time, Speed & Distance: Trains, Boats & Relative Speed",
            "10 min read",
            "Intermediate",
            "Speed conversions, relative velocity when moving in same vs opposite directions, upstream & downstream mechanics.",
            """# Time, Speed & Distance: Complete Handbook

## 1. Unit Conversion
- $\\text{Speed in } m/s = \\text{Speed in } km/hr \\times \\frac{5}{18}$
- $\\text{Speed in } km/hr = \\text{Speed in } m/s \\times \\frac{18}{5}$

## 2. Average Speed
- When distance is constant for two trips at speeds $u$ and $v$:
$$\\text{Average Speed} = \\frac{2uv}{u + v}$$
- In general: $\\text{Average Speed} = \\frac{\\text{Total Distance}}{\\text{Total Time Taken}}$

## 3. Relative Speed
- **Moving towards each other (Opposite direction)**: $S_{rel} = S_1 + S_2$
- **Moving away or chasing (Same direction)**: $S_{rel} = |S_1 - S_2|$

## 4. Train Problems
- Time to cross a stationary point object (pole, standing man):
$$\\text{Time} = \\frac{\\text{Length of Train}}{S_{train}}$$
- Time to cross a platform or bridge of length $L_p$:
$$\\text{Time} = \\frac{L_{train} + L_p}{S_{train}}$$
- Two trains of lengths $L_1$ and $L_2$ crossing each other:
$$\\text{Time} = \\frac{L_1 + L_2}{S_{rel}}$$

## 5. Boats & Streams
- Let Speed of Boat in still water $= B$, Speed of Stream $= S$.
- **Downstream Speed ($D$)**: $B + S$
- **Upstream Speed ($U$)**: $B - S$
- **Speed of Boat in Still Water**: $B = \\frac{D + U}{2}$
- **Speed of Stream**: $S = \\frac{D - U}{2}$
""",
            json.dumps(["Multiply by 5/18 to go from km/h to m/s", "Avg speed for equal distances is 2uv/(u+v)", "Downstream = B + S, Upstream = B - S"]),
            "Avg Speed = 2uv/(u+v) | B = (D+U)/2 | S = (D-U)/2"
        ),

        # Aptitude - Logical Reasoning
        (
            "Aptitude",
            "Logical",
            "Syllogisms & Blood Relations Solving Techniques",
            "7 min read",
            "Beginner",
            "Venn diagram rules for Syllogisms (All, Some, No, Some Not, Either-Or) and family tree mapping symbols for Blood Relations.",
            """# Syllogisms & Blood Relations Guide

## 1. Syllogisms: Venn Diagram Representation
- **All A are B**: Circle A is completely inside Circle B.
- **Some A are B**: Circle A overlaps partially with Circle B.
- **No A is B**: Circle A and Circle B have no intersection with a cross line.
- **Some A are not B**: There exists at least one portion of A outside B.

### The Golden "Either-Or" Condition:
Two conclusions form an *Either-Or* pair if:
1. Both conclusions are individually false or doubtful.
2. The subjects and predicates in both conclusions are identical.
3. One conclusion is affirmative and the other is negative (e.g., 'Some A are B' and 'No A is B', or 'All A are B' and 'Some A are not B').

---

## 2. Blood Relations: Standard Tree Notation
Always draw a generational tree:
- **Horizontal double line ($= $)**: Married couple (e.g., $M = F$)
- **Horizontal single line ($-$)**: Siblings (Brother/Sister)
- **Vertical single line ($|$)**: Parent to Child generation step
- **$[+]$**: Male gender
- **$[-]$**: Female gender

### Common Pitfalls to Avoid:
- Never assume gender from a person's name (e.g., "Kiran", "Robin", "Alex"). Only assign gender when explicitly mentioned (e.g., "he", "sister", "maternal uncle").
- "Maternal" refers to mother's side; "Paternal" refers to father's side.
""",
            json.dumps(["Never assume gender from names", "Either-Or condition requires 1 positive + 1 negative conclusion", "Use generation tree for blood relations"]),
            "Generations: Parents above, Children below, Siblings horizontal, Spouses with double line."
        ),

        # DSA - Two Pointers & Sliding Window
        (
            "DSA",
            "Arrays & Strings",
            "Two Pointers & Sliding Window Patterns",
            "12 min read",
            "Intermediate",
            "How to recognize, structure, and code fixed & dynamic window problems, two pointers (converging vs same direction).",
            """# Two Pointers & Sliding Window Masterclass

## 1. When to Use Two Pointers?
- Input array is **sorted** (or can be sorted in $O(N \\log N)$).
- Problem asks for pairs, triplets, or subarrays meeting a condition (e.g., Two Sum II, 3Sum, Container With Most Water).
- Reversing in place, palindrome checks, or partitioning (e.g., Dutch National Flag).

### Template: Converging Two Pointers
```python
def two_pointers(arr, target):
    left = 0
    right = len(arr) - 1
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1  # need larger sum
        else:
            right -= 1 # need smaller sum
    return []
```

---

## 2. When to Use Sliding Window?
- Input is an array or string.
- You are looking for a **contiguous** sequence (longest, shortest, or fixed-length subsegment) that satisfies a constraint.

### Template: Variable Size Sliding Window (e.g., Longest Substring)
```python
def sliding_window(s):
    left = 0
    window_state = {}
    max_len = 0
    
    for right in range(len(s)):
        # 1. Expand window by including s[right]
        char = s[right]
        window_state[char] = window_state.get(char, 0) + 1
        
        # 2. Shrink window while constraint is violated
        while window_is_invalid(window_state):
            left_char = s[left]
            window_state[left_char] -= 1
            left += 1
            
        # 3. Update result
        max_len = max(max_len, right - left + 1)
        
    return max_len
```
""",
            json.dumps(["Use converging pointers on sorted arrays", "Sliding window operates on contiguous subarrays", "Maintain window state with hash map or count array"]),
            "Time Complexity: O(N) | Space: O(1) or O(K) where K is unique elements"
        ),

        # DSA - Trees & Graphs
        (
            "DSA",
            "Trees & Graphs",
            "Binary Trees & BFS/DFS Traversal Blueprint",
            "15 min read",
            "Intermediate",
            "Inorder, Preorder, Postorder, Level-Order traversal, diameter of binary tree, LCA (Lowest Common Ancestor), and graph cycle detection.",
            """# Trees & Graphs Blueprint

## 1. Depth First Search (DFS) on Binary Trees
- **Pre-order**: Root -> Left -> Right
- **In-order**: Left -> Root -> Right *(Yields sorted order in BST!)*
- **Post-order**: Left -> Right -> Root *(Best for bottom-up calculation like height, subtree diameter)*

### Lowest Common Ancestor (LCA) in Binary Tree
```python
def lowestCommonAncestor(root, p, q):
    if not root or root == p or root == q:
        return root
    
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    
    # If both sides returned a node, root is the LCA
    if left and right:
        return root
    return left if left else right
```

---

## 2. Breadth First Search (BFS) / Level-Order Traversal
Queue-based traversal:
```python
from collections import deque

def levelOrder(root):
    if not root:
        return []
    queue = deque([root])
    levels = []
    
    while queue:
        level_size = len(queue)
        current_level = []
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        levels.append(current_level)
    return levels
```

---

## 3. Detecting Cycles in Graphs
- **Undirected Graph**: BFS/DFS tracking `parent` pointer. If visiting an already visited node that is not parent -> Cycle.
- **Directed Graph**: DFS with 3 states (Unvisited = 0, Visiting = 1, Visited = 2). If encountering node in state 1 -> Back edge / Cycle.
- **Kahn's Algorithm (Topological Sort)**: Count in-degrees. If processed nodes < total vertices -> Graph has a cycle.
""",
            json.dumps(["In-order traversal of BST gives sorted keys", "BFS always uses a Queue; DFS uses recursion or Stack", "Directed graph cycle requires 3-color DFS or Kahn's indegree algorithm"]),
            "Tree DFS: O(N) time, O(H) call stack | BFS: O(N) time, O(W) queue space"
        ),

        # Technical - DBMS
        (
            "Technical",
            "DBMS",
            "ACID Properties, Normalization & Indexing Deep Dive",
            "12 min read",
            "Advanced",
            "Atomicity, Consistency, Isolation levels (Dirty Read, Non-repeatable Read, Phantom Read), 1NF to BCNF, B-Tree vs Hash Index.",
            """# DBMS Core: ACID, Normalization & Indexing

## 1. ACID Properties
- **Atomicity**: "All or Nothing". All operations in transaction succeed or entire transaction is rolled back via WAL (Write-Ahead Logging).
- **Consistency**: The database moves from one valid state to another, preserving all integrity constraints (Foreign Keys, Uniqueness, Check constraints).
- **Isolation**: Concurrent transactions execute without interfering.
- **Durability**: Once committed, changes survive power loss or crashes (flushed to non-volatile disk).

### Transaction Isolation Levels & Anomalies
| Isolation Level | Dirty Read | Non-Repeatable Read | Phantom Read |
|---|---|---|---|
| **Read Uncommitted** | Possible | Possible | Possible |
| **Read Committed** | Prevented | Possible | Possible |
| **Repeatable Read** (MySQL default) | Prevented | Prevented | Possible (MVCC helps) |
| **Serializable** | Prevented | Prevented | Prevented |

---

## 2. Normalization Rules
1. **1NF**: Every cell contains atomic (indivisible) values; no repeating groups.
2. **2NF**: In 1NF + No partial dependency (no non-prime attribute depends on a proper subset of candidate key).
3. **3NF**: In 2NF + No transitive dependency ($A \\to B$ and $B \\to C$ where neither is candidate key).
4. **BCNF**: For every functional dependency $X \\to Y$, $X$ must be a super key.

---

## 3. Indexing: Why B-Trees over Binary Search Trees?
- Disk I/O is the bottleneck. B-Trees have high fan-out (hundreds of keys per node), keeping tree height low ($3-4$ levels for millions of records).
- B+ Trees store all actual records in leaf nodes connected as a doubly linked list, providing blistering range query performance (`BETWEEN` queries).
""",
            json.dumps(["ACID ensures database transactional integrity", "Repeatable Read prevents dirty and non-repeatable reads", "B+ Trees minimize disk seeks with high fan-out and linked leaf nodes"]),
            "1NF: Atomic | 2NF: No Partial Dep | 3NF: No Transitive Dep | BCNF: X is Super Key"
        ),

        # Technical - Operating Systems
        (
            "Technical",
            "Operating Systems",
            "Process vs Thread, Deadlocks & Virtual Memory",
            "10 min read",
            "Intermediate",
            "Context switching, Coffman conditions for deadlocks, Banker's Algorithm, Paging, Page Faults, and TLB.",
            """# Operating Systems: Key Placement Concepts

## 1. Process vs Thread
- **Process**: Independent program in execution with its own address space (Text, Data, Heap, Stack). Heavyweight context switch.
- **Thread**: Lightweight unit of execution within a process. Shares code, data, open files, and address space with peer threads, but has its own Program Counter (PC), Registers, and Stack.

## 2. Deadlock & 4 Coffman Conditions
Deadlock occurs if and only if all 4 conditions hold simultaneously:
1. **Mutual Exclusion**: At least one resource must be non-shareable.
2. **Hold and Wait**: Process holding resources requests additional resources.
3. **No Preemption**: Resources cannot be forcibly taken from a process.
4. **Circular Wait**: A closed chain of processes exists where each waits for a resource held by the next.

> **To prevent deadlocks**: Break any one of the 4 conditions (e.g., impose strict global order on resource allocation to prevent circular wait).

## 3. Virtual Memory & Paging
- **Virtual Address**: Generated by CPU. Divided into Page Number ($P$) and Offset ($D$).
- **MMU (Memory Management Unit)**: Translates virtual address to physical frame using Page Table.
- **TLB (Translation Lookaside Buffer)**: High-speed hardware cache for page table lookups.
- **Page Fault**: Occurs when a requested page is not currently in physical RAM. Triggers OS trap to fetch page from disk swap.
""",
            json.dumps(["Threads share address space, processes have isolated address spaces", "Coffman conditions: Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait", "Page fault triggers disk I/O to load missing frame into RAM"]),
            "Coffman 4: Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait"
        ),

        # Technical - Computer Networks
        (
            "Technical",
            "Computer Networks",
            "OSI Layers, TCP vs UDP & HTTP/1.1 vs HTTP/2/3",
            "11 min read",
            "Intermediate",
            "7 layers of OSI, 3-way handshake, 4-way FIN termination, TCP flow & congestion control, UDP, and modern web protocols.",
            """# Computer Networks: High-Yield Interview Notes

## 1. The OSI 7-Layer Model
1. **Physical**: Bits over wire/fiber/radio (Ethernet cable, Repeaters).
2. **Data Link**: Frames, MAC addressing, Error detection (Switch, ARP).
3. **Network**: Packets, Logical IP addressing, Routing (Router, IP, ICMP).
4. **Transport**: End-to-end segmentation, ports, reliability (TCP, UDP).
5. **Session**: Session establishment, checkpoints.
6. **Presentation**: Data encryption, compression, formatting (SSL/TLS, JSON).
7. **Application**: Network applications (HTTP, DNS, SMTP, SSH).

## 2. TCP 3-Way Handshake
Establishes reliable connection:
1. **Client $\\to$ Server**: `SYN` (Sequence Number $= X$)
2. **Server $\\to$ Client**: `SYN-ACK` (Sequence Number $= Y$, Acknowledgment $= X + 1$)
3. **Client $\\to$ Server**: `ACK` (Acknowledgment $= Y + 1$)

### TCP 4-Way Handshake Connection Termination:
`FIN` $\\to$ `ACK` $\\to$ `FIN` $\\to$ `ACK`

## 3. TCP vs UDP Comparison
| Feature | TCP | UDP |
|---|---|---|
| **Connection** | Connection-oriented (Handshake) | Connectionless |
| **Reliability** | Guaranteed delivery (Retransmissions) | Best-effort (Packets may drop) |
| **Ordering** | In-order guaranteed | No order guarantee |
| **Speed / Overhead** | Slower (20-byte header, acks, flow control) | Blazing fast (8-byte header) |
| **Use cases** | Web pages, banking, file download, email | Video streaming, VoIP, Gaming, DNS queries |

## 4. HTTP Protocols Evolution
- **HTTP/1.1**: Persistent TCP connections, but suffers from Head-of-Line (HoL) blocking.
- **HTTP/2**: Multiplexing over single TCP connection, binary framing, header compression (HPACK), server push.
- **HTTP/3**: Built on **QUIC** over UDP. Eliminates TCP head-of-line blocking on packet loss and enables instant connection migration (Wi-Fi to 5G).
""",
            json.dumps(["TCP 3-way handshake: SYN -> SYN-ACK -> ACK", "TCP guarantees ordered, reliable delivery; UDP is low latency", "HTTP/2 multiplexes streams; HTTP/3 runs over QUIC/UDP"]),
            "Handshake: SYN -> SYN-ACK -> ACK | Headers: TCP 20B, UDP 8B"
        ),

        # HR - STAR Method & Behavioral
        (
            "HR",
            "Behavioral",
            "The STAR Method & Behavioral Interview Blueprint",
            "9 min read",
            "Beginner",
            "Framework for answering 'Tell me about a time when...', structuring stories, handling conflict, and culture fit questions.",
            """# The STAR Method & HR Blueprint

## 1. What is the STAR Framework?
Top tech companies (especially Amazon, Google, Microsoft) use behavioral questions to test your real-world judgment, resilience, and ownership. Format every scenario with:

- **S - Situation (15%)**: Set the context. Where were you working? What was the project or challenge? Keep it crisp and relatable.
- **T - Task (15%)**: What was your specific responsibility or goal in that situation? Why was it critical?
- **A - Action (50%)**: What exact steps did **YOU** take? (Use "I", not "We"). Highlight leadership, technical initiative, trade-offs made, and collaboration.
- **R - Result (20%)**: Quantifiable impact and takeaways. (e.g., "Reduced latency by 35%", "Delivered 2 days ahead of schedule", "Trained 3 junior peers").

---

## 2. The 5 Core Stories Every Candidate Must Prepare
Before any interview, draft 5 versatile stories from your college projects or internships:
1. **Technical Challenge**: A complex bug or architectural dilemma you solved under pressure.
2. **Conflict Resolution**: A disagreement with a teammate or peer over technical choices or workload, and how you reached consensus.
3. **Failure & Learning**: A project deadline missed, bug released to production, or wrong assumption, and what you improved.
4. **Leadership / Ownership**: Going beyond your job description to fix an unowned issue or help a struggling peer.
5. **Tight Deadline / Prioritization**: Handling competing priorities and delivering high-value output.

---

## 3. Top HR Questions & Winning Strategies
- **"Tell me about yourself"**: Structure as *Present* (current degree/skills) $\\to$ *Past* (key projects/internships) $\\to$ *Future* (why this role excites you). Keep under 90 seconds.
- **"Why should we hire you?"**: Connect your skills directly to their tech stack + express enthusiasm for their product.
- **"Do you have any questions for us?"**: NEVER say no! Ask about team engineering practices, upcoming roadmap challenges, or mentorship culture.
""",
            json.dumps(["STAR stands for Situation, Task, Action, Result", "Spend 50% of your time detailing your specific Actions", "Always prepare 2-3 thoughtful questions to ask the interviewer"]),
            "STAR: Situation 15% -> Task 15% -> Action 50% -> Result 20%"
        )
    ]

    cursor.executemany("""
    INSERT INTO prep_notes (
        category, subcategory, title, read_time, difficulty, summary,
        content_markdown, key_takeaways, formula_sheet
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, notes_data)

    # --- 3. PREP PROBLEMS SEED DATA (MCQs & CODING) ---
    problems_data = [
        # Aptitude MCQs
        (
            "Aptitude",
            "Quantitative",
            "Dishonest Merchant Weight Error",
            "Medium",
            "mcq",
            "A dishonest grocer professes to sell his goods at cost price, but he uses a false weight of 920 grams for a 1 kg weight. What is his actual profit percentage?",
            json.dumps(["8.00%", "8.69%", "9.20%", "8.25%"]),
            "8.69%",
            "Formula: Gain % = (Error / (True Value - Error)) * 100.\nError = 1000g - 920g = 80g.\nGain % = (80 / 920) * 100 = 8.695% ≈ 8.69%.",
            None,
            None,
            None,
            json.dumps(["TCS", "Infosys", "Wipro"])
        ),
        (
            "Aptitude",
            "Quantitative",
            "Two Trains Crossing in Opposite Directions",
            "Medium",
            "mcq",
            "Two trains of lengths 140 m and 160 m are running in opposite directions on parallel tracks at 60 km/h and 48 km/h respectively. In how many seconds will they completely cross each other?",
            json.dumps(["10 seconds", "12 seconds", "15 seconds", "8 seconds"]),
            "10 seconds",
            "Total Distance to be covered = L1 + L2 = 140 + 160 = 300 meters.\nRelative speed = 60 + 48 = 108 km/h.\nConverting to m/s: 108 * (5/18) = 30 m/s.\nTime taken = Distance / Relative Speed = 300 / 30 = 10 seconds.",
            None,
            None,
            None,
            json.dumps(["Accenture", "Cognizant", "TCS"])
        ),
        (
            "Aptitude",
            "Quantitative",
            "Work and Wages Efficiency Problem",
            "Easy",
            "mcq",
            "A can complete a piece of work in 12 days and B in 18 days. If they work together on it for 4 days, what fraction of the total work is left unfinished?",
            json.dumps(["1/3", "4/9", "5/9", "7/18"]),
            "4/9",
            "A's 1-day work = 1/12, B's 1-day work = 1/18.\nCombined 1-day work = (1/12) + (1/18) = (3 + 2)/36 = 5/36.\nIn 4 days, work done = 4 * (5/36) = 20/36 = 5/9.\nRemaining work = 1 - 5/9 = 4/9.",
            None,
            None,
            None,
            json.dumps(["Capgemini", "Infosys", "TCS"])
        ),
        (
            "Aptitude",
            "Logical",
            "Blood Relations Puzzle",
            "Medium",
            "mcq",
            "Pointing to a photograph of a boy, Suresh said, 'He is the only son of the only daughter of my mother.' How is Suresh related to that boy?",
            json.dumps(["Father", "Maternal Uncle", "Brother", "Cousin"]),
            "Maternal Uncle",
            "Let's break it down step-by-step:\n1. 'My mother' -> Suresh's mother.\n2. 'Only daughter of my mother' -> Suresh's sister.\n3. 'He is the only son of Suresh's sister' -> Suresh's nephew.\nTherefore, Suresh is the Maternal Uncle (mother's brother) of the boy.",
            None,
            None,
            None,
            json.dumps(["Wipro", "TCS", "Mindtree"])
        ),
        (
            "Aptitude",
            "Logical",
            "Number & Letter Series",
            "Easy",
            "mcq",
            "Find the next term in the series: 3, 7, 15, 31, 63, ?",
            json.dumps(["95", "127", "111", "126"]),
            "127",
            "Pattern: Each term is generated by (Previous Term * 2) + 1.\n3 * 2 + 1 = 7\n7 * 2 + 1 = 15\n15 * 2 + 1 = 31\n31 * 2 + 1 = 63\n63 * 2 + 1 = 127.",
            None,
            None,
            None,
            json.dumps(["Accenture", "Cognizant"])
        ),
        (
            "Aptitude",
            "Verbal",
            "Sentence Correction & Idiomatic Usage",
            "Easy",
            "mcq",
            "Choose the option that correctly completes the sentence: 'Neither the manager nor the employees _____ present at the emergency briefing.'",
            json.dumps(["was", "were", "is", "has been"]),
            "were",
            "Subject-Verb Agreement Rule: When two subjects are connected by 'neither... nor' or 'either... or', the verb must agree in number with the closer subject. Here, 'employees' is plural and is closest to the verb, so the plural verb 'were' is correct.",
            None,
            None,
            None,
            json.dumps(["TCS", "Infosys", "Deloitte"])
        ),

        # DSA Coding Problems
        (
            "DSA",
            "Arrays & Hashing",
            "Two Sum (Target Pair Indices)",
            "Easy",
            "coding",
            "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice. Return the indices in ascending order.\n\n### Example 1:\n```\nInput: nums = [2,7,11,15], target = 9\nOutput: [0, 1]\nExplanation: nums[0] + nums[1] == 9, return [0, 1].\n```\n\n### Example 2:\n```\nInput: nums = [3,2,4], target = 6\nOutput: [1, 2]\n```",
            None,
            "[0, 1]",
            "Use a hash map to store the number and its index. For each number x, check if (target - x) is already in the map. If yes, return both indices. Time complexity: O(N), Space: O(N).",
            json.dumps({
                "python": "def twoSum(nums, target):\n    # Write your solution here\n    seen = {}\n    for i, num in enumerate(nums):\n        diff = target - num\n        if diff in seen:\n            return [seen[diff], i]\n        seen[num] = i\n    return []\n",
                "cpp": "#include <vector>\n#include <unordered_map>\nusing namespace std;\n\nvector<int> twoSum(vector<int>& nums, int target) {\n    unordered_map<int, int> seen;\n    for (int i = 0; i < nums.size(); i++) {\n        int complement = target - nums[i];\n        if (seen.find(complement) != seen.end()) {\n            return {seen[complement], i};\n        }\n        seen[nums[i]] = i;\n    }\n    return {};\n}",
                "java": "import java.util.HashMap;\n\nclass Solution {\n    public int[] twoSum(int[] nums, int target) {\n        HashMap<Integer, Integer> map = new HashMap<>();\n        for (int i = 0; i < nums.length; i++) {\n            int complement = target - nums[i];\n            if (map.containsKey(complement)) {\n                return new int[] { map.get(complement), i };\n            }\n            map.put(nums[i], i);\n        }\n        return new int[]{};\n    }\n}"
            }),
            json.dumps({
                "python": "def twoSum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        diff = target - num\n        if diff in seen:\n            return [seen[diff], i]\n        seen[num] = i\n    return []\n"
            }),
            json.dumps([
                {"input": "nums = [2, 7, 11, 15], target = 9", "expected_output": "[0, 1]", "is_sample": True},
                {"input": "nums = [3, 2, 4], target = 6", "expected_output": "[1, 2]", "is_sample": True},
                {"input": "nums = [3, 3], target = 6", "expected_output": "[0, 1]", "is_sample": False}
            ]),
            json.dumps(["Google", "Amazon", "Microsoft", "Meta", "Apple"])
        ),
        (
            "DSA",
            "Arrays",
            "Best Time to Buy and Sell Stock",
            "Easy",
            "coding",
            "You are given an array `prices` where `prices[i]` is the price of a given stock on the $i^{\\text{th}}$ day.\n\nYou want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.\n\nReturn the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return `0`.\n\n### Example 1:\n```\nInput: prices = [7,1,5,3,6,4]\nOutput: 5\nExplanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6 - 1 = 5.\n```\n\n### Example 2:\n```\nInput: prices = [7,6,4,3,1]\nOutput: 0\nExplanation: In this case, no transactions are done and max profit = 0.\n```",
            None,
            "5",
            "Keep track of the minimum price encountered so far. At each day, calculate potential profit: price - min_price. Update max_profit accordingly. Single pass O(N) time and O(1) space.",
            json.dumps({
                "python": "def maxProfit(prices):\n    # Write your solution here\n    min_price = float('inf')\n    max_profit = 0\n    for p in prices:\n        if p < min_price:\n            min_price = p\n        elif p - min_price > max_profit:\n            max_profit = p - min_price\n    return max_profit\n",
                "cpp": "#include <vector>\n#include <algorithm>\nusing namespace std;\n\nint maxProfit(vector<int>& prices) {\n    int minPrice = 1e9, maxProfit = 0;\n    for (int p : prices) {\n        minPrice = min(minPrice, p);\n        maxProfit = max(maxProfit, p - minPrice);\n    }\n    return maxProfit;\n}",
                "java": "class Solution {\n    public int maxProfit(int[] prices) {\n        int minPrice = Integer.MAX_VALUE;\n        int maxProfit = 0;\n        for (int p : prices) {\n            if (p < minPrice) minPrice = p;\n            else if (p - minPrice > maxProfit) maxProfit = p - minPrice;\n        }\n        return maxProfit;\n    }\n}"
            }),
            json.dumps({
                "python": "def maxProfit(prices):\n    min_price = float('inf')\n    max_profit = 0\n    for p in prices:\n        if p < min_price:\n            min_price = p\n        elif p - min_price > max_profit:\n            max_profit = p - min_price\n    return max_profit\n"
            }),
            json.dumps([
                {"input": "prices = [7, 1, 5, 3, 6, 4]", "expected_output": "5", "is_sample": True},
                {"input": "prices = [7, 6, 4, 3, 1]", "expected_output": "0", "is_sample": True},
                {"input": "prices = [2, 4, 1]", "expected_output": "2", "is_sample": False}
            ]),
            json.dumps(["Amazon", "Microsoft", "Goldman Sachs", "TCS Digital"])
        ),
        (
            "DSA",
            "Strings & Stacks",
            "Valid Parentheses Matching",
            "Easy",
            "coding",
            "Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.\n\nAn input string is valid if:\n1. Open brackets must be closed by the same type of brackets.\n2. Open brackets must be closed in the correct order.\n3. Every close bracket has a corresponding open bracket of the same type.\n\n### Example 1:\n```\nInput: s = \"()[]{}\"\nOutput: True\n```\n\n### Example 2:\n```\nInput: s = \"(]\"\nOutput: False\n```",
            None,
            "True",
            "Use a Stack. Push opening brackets. When a closing bracket arrives, verify if the top of the stack matches its corresponding open bracket. If stack is empty at end, it's valid. O(N) time and O(N) space.",
            json.dumps({
                "python": "def isValid(s: str) -> bool:\n    # Write your solution here\n    stack = []\n    bracket_map = {')': '(', '}': '{', ']': '['}\n    for char in s:\n        if char in bracket_map:\n            top = stack.pop() if stack else '#'\n            if bracket_map[char] != top:\n                return False\n        else:\n            stack.append(char)\n    return not stack\n",
                "cpp": "#include <string>\n#include <stack>\nusing namespace std;\n\nbool isValid(string s) {\n    stack<char> st;\n    for (char c : s) {\n        if (c == '(' || c == '{' || c == '[') st.push(c);\n        else {\n            if (st.empty()) return false;\n            if (c == ')' && st.top() != '(') return false;\n            if (c == '}' && st.top() != '{') return false;\n            if (c == ']' && st.top() != '[') return false;\n            st.pop();\n        }\n    }\n    return st.empty();\n}",
                "java": "import java.util.Stack;\n\nclass Solution {\n    public boolean isValid(String s) {\n        Stack<Character> stack = new Stack<>();\n        for (char c : s.toCharArray()) {\n            if (c == '(' || c == '{' || c == '[') stack.push(c);\n            else {\n                if (stack.isEmpty()) return false;\n                char top = stack.pop();\n                if (c == ')' && top != '(') return false;\n                if (c == '}' && top != '{') return false;\n                if (c == ']' && top != '[') return false;\n            }\n        }\n        return stack.isEmpty();\n    }\n}"
            }),
            json.dumps({
                "python": "def isValid(s: str) -> bool:\n    stack = []\n    bracket_map = {')': '(', '}': '{', ']': '['}\n    for char in s:\n        if char in bracket_map:\n            top = stack.pop() if stack else '#'\n            if bracket_map[char] != top:\n                return False\n        else:\n            stack.append(char)\n    return not stack\n"
            }),
            json.dumps([
                {"input": "s = \"()[]{}\"", "expected_output": "True", "is_sample": True},
                {"input": "s = \"(]\"", "expected_output": "False", "is_sample": True},
                {"input": "s = \"{[]}\"", "expected_output": "True", "is_sample": False}
            ]),
            json.dumps(["Google", "Atlassian", "Amazon", "Infosys DSE"])
        ),
        (
            "DSA",
            "Strings & Sliding Window",
            "Longest Substring Without Repeating Characters",
            "Medium",
            "coding",
            "Given a string `s`, find the length of the longest substring without duplicate characters.\n\n### Example 1:\n```\nInput: s = \"abcabcbb\"\nOutput: 3\nExplanation: The answer is \"abc\", with the length of 3.\n```\n\n### Example 2:\n```\nInput: s = \"bbbbb\"\nOutput: 1\nExplanation: The answer is \"b\", with the length of 1.\n```",
            None,
            "3",
            "Maintain a sliding window [left, right] and a map storing the last seen index of each character. When a duplicate is seen inside the current window, move the left pointer past that character's last seen index. Time: O(N), Space: O(min(N, alphabet_size)).",
            json.dumps({
                "python": "def lengthOfLongestSubstring(s: str) -> int:\n    # Write your solution here\n    char_index = {}\n    max_len = 0\n    left = 0\n    for right, char in enumerate(s):\n        if char in char_index and char_index[char] >= left:\n            left = char_index[char] + 1\n        char_index[char] = right\n        max_len = max(max_len, right - left + 1)\n    return max_len\n",
                "cpp": "#include <string>\n#include <unordered_map>\n#include <algorithm>\nusing namespace std;\n\nint lengthOfLongestSubstring(string s) {\n    unordered_map<char, int> charMap;\n    int left = 0, maxLen = 0;\n    for (int right = 0; right < s.length(); right++) {\n        if (charMap.count(s[right]) && charMap[s[right]] >= left) {\n            left = charMap[s[right]] + 1;\n        }\n        charMap[s[right]] = right;\n        maxLen = max(maxLen, right - left + 1);\n    }\n    return maxLen;\n}",
                "java": "import java.util.HashMap;\n\nclass Solution {\n    public int lengthOfLongestSubstring(String s) {\n        HashMap<Character, Integer> map = new HashMap<>();\n        int left = 0, maxLen = 0;\n        for (int right = 0; right < s.length(); right++) {\n            char c = s.charAt(right);\n            if (map.containsKey(c) && map.get(c) >= left) {\n                left = map.get(c) + 1;\n            }\n            map.put(c, right);\n            maxLen = Math.max(maxLen, right - left + 1);\n        }\n        return maxLen;\n    }\n}"
            }),
            json.dumps({
                "python": "def lengthOfLongestSubstring(s: str) -> int:\n    char_index = {}\n    max_len = 0\n    left = 0\n    for right, char in enumerate(s):\n        if char in char_index and char_index[char] >= left:\n            left = char_index[char] + 1\n        char_index[char] = right\n        max_len = max(max_len, right - left + 1)\n    return max_len\n"
            }),
            json.dumps([
                {"input": "s = \"abcabcbb\"", "expected_output": "3", "is_sample": True},
                {"input": "s = \"bbbbb\"", "expected_output": "1", "is_sample": True},
                {"input": "s = \"pwwkew\"", "expected_output": "3", "is_sample": False}
            ]),
            json.dumps(["Amazon", "Microsoft", "Adobe", "Swiggy"])
        ),

        # Technical Core Questions
        (
            "Technical",
            "DBMS",
            "Transaction Isolation Anomalies",
            "Medium",
            "mcq",
            "Which phenomenon occurs when Transaction T1 reads data modified by concurrent Transaction T2, but T2 later aborts and rolls back the change?",
            json.dumps(["Dirty Read", "Non-repeatable Read", "Phantom Read", "Lost Update"]),
            "Dirty Read",
            "A Dirty Read occurs when a transaction reads uncommitted changes made by another concurrent transaction that subsequently rolls back. This is prevented by the 'Read Committed' isolation level.",
            None,
            None,
            None,
            json.dumps(["Amazon", "Oracle", "Microsoft", "TCS Digital"])
        ),
        (
            "Technical",
            "Operating Systems",
            "Deadlock Necessary Condition Prevention",
            "Medium",
            "mcq",
            "Which of the following techniques is commonly used in OS design to break the 'Circular Wait' condition for deadlock prevention?",
            json.dumps([
                "Imposing a total linear ordering of all resource types and requiring processes to request resources in strictly increasing order",
                "Allowing resource preemption via kill signals",
                "Requiring all processes to request all resources at initialization",
                "Allocating multiple instances of every resource"
            ]),
            "Imposing a total linear ordering of all resource types and requiring processes to request resources in strictly increasing order",
            "Imposing a global numerical order on all resources (e.g., F(R_i) < F(R_j)) and requiring processes to request resources in strictly monotonically increasing order mathematically guarantees that a closed cyclic wait graph cannot form.",
            None,
            None,
            None,
            json.dumps(["Google", "Microsoft", "Qualcomm"])
        ),
        (
            "Technical",
            "Computer Networks",
            "TCP 3-Way Handshake Packet Sequence",
            "Easy",
            "mcq",
            "What is the exact sequence of packet flags exchanged between client and server to establish a standard TCP connection?",
            json.dumps([
                "SYN -> SYN-ACK -> ACK",
                "ACK -> SYN -> ACK",
                "SYN -> ACK -> DATA",
                "FIN -> ACK -> FIN-ACK"
            ]),
            "SYN -> SYN-ACK -> ACK",
            "The client initiates with SYN (Synchronize), the server responds with SYN-ACK (Synchronize-Acknowledge), and the client concludes the handshake with ACK (Acknowledge). Data transfer can then begin.",
            None,
            None,
            None,
            json.dumps(["Cisco", "Amazon", "Infosys", "TCS"])
        ),

        # HR Interview Scenarios
        (
            "HR",
            "Behavioral",
            "Handling Conflict with Senior Teammate",
            "Medium",
            "hr_prompt",
            "Scenario: You are working on a critical college capstone project or internship deliverable. A senior team member insists on using an outdated technology stack (e.g., legacy PHP or raw SQL strings) while you propose a modern, secure framework (e.g., FastAPI with ORM). How would you handle this disagreement?",
            json.dumps([
                "Prepare a neutral comparison matrix highlighting security, maintenance cost, and benchmark performance, then schedule a collaborative discussion to find common ground.",
                "Immediately escalate the issue to the department professor or project manager without discussing it with the senior member.",
                "Silently yield to avoid friction and work with the outdated tech stack even if it introduces security vulnerabilities.",
                "Refuse to work on the module until they agree to switch to your proposed stack."
            ]),
            "Prepare a neutral comparison matrix highlighting security, maintenance cost, and benchmark performance, then schedule a collaborative discussion to find common ground.",
            "In behavioral interviews, companies look for emotional intelligence, data-driven reasoning, and collaboration. Escalating early or confronting aggressively shows poor teamwork, while blind submission shows lack of ownership. Building a factual pros/cons matrix and seeking collaborative alignment demonstrates maturity.",
            None,
            None,
            None,
            json.dumps(["Amazon (Earns Trust)", "Google (Googliness)", "Atlassian", "Microsoft"])
        )
    ]

    cursor.executemany("""
    INSERT INTO prep_problems (
        category, subcategory, title, difficulty, problem_type, question_text,
        options, correct_answer, explanation, starter_code, solution_code,
        test_cases, companies_asked
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, problems_data)

    # --- 4. COMPANIES HIRING PROCESS SEED DATA ---
    companies_data = [
        # 1. TCS
        (
            "Tata Consultancy Services (TCS)",
            "tcs",
            "IT Services & Consulting",
            "#0F2537",
            "Building on belief — India's largest IT and consulting powerhouse.",
            "₹3.36 - ₹11.5 LPA (Ninja: 3.36L, Digital: 7.2L, Prime: 9-11.5L)",
            json.dumps(["Ninja (Assistant System Engineer)", "Digital (System Engineer)", "Prime (Senior System Engineer)"]),
            json.dumps({
                "min_cgpa": "60% or 6.0 CGPA throughout 10th, 12th, Diploma, and Graduation",
                "backlogs": "Maximum 1 active backlog permitted at the time of examination (must be cleared before joining)",
                "gap_allowed": "Maximum 24 months total academic break permitted with valid documentation",
                "eligible_degrees": "B.E. / B.Tech / M.E. / M.Tech / MCA / M.Sc (All streams)",
                "passing_years": "2024, 2025, 2026 Batch"
            }),
            json.dumps([
                {
                    "round_number": 1,
                    "round_name": "TCS National Qualifier Test (NQT)",
                    "platform": "TCS iON Test Centers",
                    "duration": "165 Minutes",
                    "negative_marking": "No negative marking",
                    "sections": [
                        {"name": "Part A: Foundation Section", "duration": "75 mins", "details": "Numerical Ability (20 Qs), Verbal Ability (25 Qs), Reasoning Ability (20 Qs)"},
                        {"name": "Part B: Advanced Cognitive Section", "duration": "35 mins", "details": "Advanced Quantitative (10 Qs), Advanced Reasoning (10 Qs)"},
                        {"name": "Part C: Advanced Coding Section", "duration": "55 mins", "details": "2 Coding Problems (1 Medium DSA, 1 Advanced DP/Graph/Greedy in C, C++, Java, or Python)"}
                    ]
                },
                {
                    "round_number": 2,
                    "round_name": "Technical Interview",
                    "platform": "Virtual / Campus In-person",
                    "duration": "30 - 45 Minutes",
                    "negative_marking": "N/A",
                    "sections": [
                        {"name": "Core CS Concepts", "duration": "15 mins", "details": "DBMS queries, Normalization, OOPs concepts, OS scheduling, and chosen programming language fundamentals"},
                        {"name": "Live Coding & Project Walkthrough", "duration": "20 mins", "details": "Explain resume projects, architecture, role played, and live dry-run of a problem solved in NQT"}
                    ]
                },
                {
                    "round_number": 3,
                    "round_name": "Managerial & HR Interview",
                    "platform": "Virtual / In-person",
                    "duration": "20 - 30 Minutes",
                    "negative_marking": "N/A",
                    "sections": [
                        {"name": "Work Readiness & Culture", "duration": "20 mins", "details": "Willingness to relocate, night shifts, handling work stress, bond/service agreement terms, and verification of academic records"}
                    ]
                }
            ]),
            json.dumps([
                {"section": "Numerical Ability", "topics": ["Number System", "Percentages", "Profit & Loss", "Time Speed Distance", "Ratio & Proportion", "Permutation & Combination", "Probability", "Mixtures & Alligation"]},
                {"section": "Reasoning Ability", "topics": ["Blood Relations", "Syllogisms", "Data Sufficiency", "Seating Arrangement (Linear & Circular)", "Coding-Decoding", "Visual Puzzles"]},
                {"section": "Verbal Ability", "topics": ["Reading Comprehension", "Para Jumbles", "Sentence Correction", "Idioms & Prepositions", "Vocabulary in Context"]},
                {"section": "Advanced Coding", "topics": ["Dynamic Programming (1D/2D)", "Two Pointers & Sliding Window", "Matrix Manipulations", "Strings & Hashing", "Graph Traversals (BFS/DFS)"]}
            ]),
            json.dumps([
                "Register on TCS NextStep portal & generate CT/DT reference ID.",
                "Appear for TCS NQT on assigned date at TCS iON center.",
                "Top scorers receive interview call for Digital & Prime bands; others interviewed for Ninja band.",
                "Combined Technical + Managerial + HR interview round.",
                "Offer Letter released with onboarding schedule."
            ]),
            json.dumps([
                "Focus heavily on the Advanced Coding section; clearing both coding test cases with zero syntax errors unlocks the Digital/Prime band.",
                "Prepare SQL queries thoroughly (Joins, GROUP BY, HAVING, and 2nd highest salary).",
                "Be ready to explain every single library and framework listed on your resume.",
                "Ensure your communication is clear and confident during the managerial situational questions."
            ]),
            json.dumps([
                "Write a program to find the largest sum of a contiguous subarray (Kadane's Algorithm).",
                "Explain the difference between primary key, unique key, and candidate key in DBMS.",
                "What happens when you type google.com in the browser? (Network protocol flow)",
                "How would you handle a scenario where your team member does not contribute to the sprint?"
            ]),
            "Moderate",
            "August - October & Off-Campus Cycles"
        ),

        # 2. Infosys
        (
            "Infosys",
            "infosys",
            "IT Services & Consulting",
            "#007CC3",
            "Navigate your next — Global leader in next-generation digital services and consulting.",
            "₹3.6 - ₹13.0 LPA (System Engineer: 3.6L, DSE: 6.5L, SP: 9.5-13L)",
            json.dumps(["System Engineer (SE)", "Digital Specialist Engineer (DSE)", "Specialist Programmer (SP)"]),
            json.dumps({
                "min_cgpa": "65% or 6.5 CGPA in 10th, 12th, and ongoing Graduation",
                "backlogs": "Zero active backlogs allowed at the time of online assessment and onboarding",
                "gap_allowed": "Maximum 2 years educational gap allowed",
                "eligible_degrees": "B.E. / B.Tech / M.E. / M.Tech / MCA / M.Sc in CS, IT, ECE, EEE, Mechanical, Civil",
                "passing_years": "2024, 2025, 2026 Batch"
            }),
            json.dumps([
                {
                    "round_number": 1,
                    "round_name": "Online Test / InfyTQ / HackWithInfy",
                    "platform": "Infosys Assessment Platform",
                    "duration": "100 - 180 Minutes (depending on track)",
                    "negative_marking": "No negative marking",
                    "sections": [
                        {"name": "Reasoning Ability", "duration": "25 mins", "details": "15 Questions on Data Interpretation, Syllogisms, and Critical Thinking"},
                        {"name": "Technical Ability (Pseudocode)", "duration": "10 mins", "details": "5 Questions on algorithmic pseudocode execution and loop time complexity"},
                        {"name": "Verbal Ability", "duration": "20 mins", "details": "20 Questions on sentence correction and reading comprehension"},
                        {"name": "Numerical Puzzle Solving", "duration": "10 mins", "details": "4 Mathematical puzzles and grid deductions"}
                    ]
                },
                {
                    "round_number": 2,
                    "round_name": "SP / DSE Coding Round (For High Packages)",
                    "platform": "HackerEarth Platform",
                    "duration": "180 Minutes",
                    "negative_marking": "Strict plagiarism checking",
                    "sections": [
                        {"name": "Problem 1 (Easy-Medium)", "duration": "45 mins", "details": "String manipulations, Hashing, or Greedy approach (50 marks)"},
                        {"name": "Problem 2 (Medium-Hard)", "duration": "60 mins", "details": "Trees / Graph traversal or Binary Search on answer (75 marks)"},
                        {"name": "Problem 3 (Hard)", "duration": "75 mins", "details": "Dynamic Programming with Bitmask or Segment Trees (100 marks)"}
                    ]
                },
                {
                    "round_number": 3,
                    "round_name": "Technical + HR Interview",
                    "platform": "Infosys Webex Platform",
                    "duration": "30 - 45 Minutes",
                    "negative_marking": "N/A",
                    "sections": [
                        {"name": "Technical Evaluation", "duration": "25 mins", "details": "DSA concepts, Database Normalization, OOPs 4 pillars, Cloud basics"},
                        {"name": "HR Fitment", "duration": "15 mins", "details": "Behavioral questions, adaptability, and Infosys core values"}
                    ]
                }
            ]),
            json.dumps([
                {"section": "Pseudocode", "topics": ["Recursion tracing", "Bitwise operators", "While loop edge cases", "Array pointers in C/C++"]},
                {"section": "Coding (SP/DSE)", "topics": ["Dynamic Programming (Knapsack, LCS, Matrix Chain)", "Disjoint Set Union (DSU)", "Dijkstra & BFS/DFS", "Monotonic Stacks"]},
                {"section": "Core Technical", "topics": ["OOPs in Java/Python", "DBMS Queries & ACID", "Software Engineering SDLC Models", "Operating Systems Paging & Semaphores"]}
            ]),
            json.dumps([
                "Application via Infosys Career Portal or HackWithInfy competition.",
                "Round 1 Proctored Online Assessment (Cognitive + Technical).",
                "HackWithInfy qualifiers advance directly to SP / DSE interview rounds.",
                "Comprehensive Technical Interview with senior architect.",
                "HR Discussion and Offer Letter rollout."
            ]),
            json.dumps([
                "Pseudocode section has high cut-off; trace loops carefully on paper with small input values.",
                "For SP (Specialist Programmer) role, practice LeetCode Medium/Hard DP and Graph questions.",
                "Know your final year project from database schema to deployment architecture.",
                "Maintain strong eye contact with camera and speak in structured points."
            ]),
            json.dumps([
                "Reverse a Linked List in groups of size K.",
                "Explain the difference between Abstract Class and Interface with real-world examples.",
                "How does garbage collection work in Java?",
                "Tell me about a time you had to learn a completely new tech stack in under two weeks."
            ]),
            "Medium to Hard",
            "September - December"
        ),

        # 3. Amazon
        (
            "Amazon",
            "amazon",
            "Product / Big Tech",
            "#FF9900",
            "Earth's most customer-centric company — Global e-commerce, cloud computing (AWS), and AI leader.",
            "₹28 - ₹48 LPA (Base ₹16-20L + RSUs + Relocation + Sign-on)",
            json.dumps(["Software Development Engineer I (SDE-1)", "SDE Intern", "Support Engineer"]),
            json.dumps({
                "min_cgpa": "6.5+ CGPA or 65% in B.Tech / M.Tech / MCA",
                "backlogs": "Zero active backlogs permitted",
                "gap_allowed": "Up to 1 year permitted with valid justification",
                "eligible_degrees": "CS, IT, Software Engineering, ECE, or related computing fields",
                "passing_years": "2024, 2025, 2026 Batch"
            }),
            json.dumps([
                {
                    "round_number": 1,
                    "round_name": "Online Assessment (OA)",
                    "platform": "HackerRank Proctored",
                    "duration": "105 Minutes",
                    "negative_marking": "No negative marking",
                    "sections": [
                        {"name": "Part 1: Code Debugging / Coding", "duration": "70 mins", "details": "2 algorithmic coding questions (LeetCode Medium-Hard level)"},
                        {"name": "Part 2: Work Style Assessment", "duration": "20 mins", "details": "Situational judgment questions testing Amazon's 16 Leadership Principles"},
                        {"name": "Part 3: Work Simulation", "duration": "15 mins", "details": "Simulated workday responding to teammate emails and prioritizing tasks"}
                    ]
                },
                {
                    "round_number": 2,
                    "round_name": "Technical Round 1 (Data Structures)",
                    "platform": "Amazon Chime + Live Code Editor",
                    "duration": "60 Minutes",
                    "negative_marking": "N/A",
                    "sections": [
                        {"name": "DSA Problem Solving", "duration": "45 mins", "details": "2 DSA problems on Trees, Heaps, Sliding Window, or Graphs with clean production code"},
                        {"name": "LP Behavioral Questions", "duration": "15 mins", "details": "1-2 STAR format questions on Customer Obsession and Bias for Action"}
                    ]
                },
                {
                    "round_number": 3,
                    "round_name": "Technical Round 2 (Algorithms & LLD)",
                    "platform": "Amazon Chime + Live Code Editor",
                    "duration": "60 Minutes",
                    "negative_marking": "N/A",
                    "sections": [
                        {"name": "Algorithms & Low-Level Design", "duration": "45 mins", "details": "Object-oriented design (e.g. Design Parking Lot, Chess Game, or Elevator) or Advanced DP"},
                        {"name": "LP Behavioral Questions", "duration": "15 mins", "details": "Frugality, Ownership, and Have Backbone; Disagree and Commit"}
                    ]
                },
                {
                    "round_number": 4,
                    "round_name": "Bar Raiser Round",
                    "platform": "Amazon Chime",
                    "duration": "60 Minutes",
                    "negative_marking": "N/A",
                    "sections": [
                        {"name": "Deep Dive & Core Values", "duration": "60 mins", "details": "Independent senior leader outside the hiring team evaluating if you raise the company's average talent bar across CS fundamentals and Leadership Principles"}
                    ]
                }
            ]),
            json.dumps([
                {"section": "Core DSA", "topics": ["Binary Trees & BST", "Priority Queues / Min-Max Heaps", "Breadth-First Search & Dijkstra", "Dynamic Programming", "Tries"]},
                {"section": "Low-Level Design (LLD)", "topics": ["SOLID Principles", "Singleton, Factory, Strategy Patterns", "Concurrency & Thread Safety", "Schema Design"]},
                {"section": "16 Leadership Principles", "topics": ["Customer Obsession", "Ownership", "Invent & Simplify", "Bias for Action", "Deliver Results", "Are Right, A Lot"]}
            ]),
            json.dumps([
                "Online Assessment via Amazon University Recruiting or Referral.",
                "Review of OA performance and resume review by recruiting team.",
                "3 to 4 rounds of virtual 1-on-1 interviews including Technical and Bar Raiser.",
                "Hiring Committee debrief where all interviewers vote.",
                "Job Offer release with RSUs and benefits package."
            ]),
            json.dumps([
                "50% of the interview score comes from the 16 Leadership Principles! Do NOT neglect them.",
                "Always communicate your thought process out loud before typing code.",
                "Start with a brute-force approach, calculate its time/space complexity, then optimize.",
                "Test your code manually with edge cases (empty array, single element, negative numbers, overflow) before saying you're done."
            ]),
            json.dumps([
                "Find Median from Data Stream using two heaps (Min-heap & Max-heap).",
                "Rotten Oranges / Multi-source BFS problem.",
                "Design a Locker Delivery System (Amazon Hub Locker).",
                "Tell me about a time you disagreed with a colleague or manager and how you resolved it."
            ]),
            "Hard",
            "August - November & Rolling"
        ),

        # 4. Google
        (
            "Google",
            "google",
            "Product / Big Tech",
            "#4285F4",
            "Organizing the world's information and making it universally accessible and useful.",
            "₹35 - ₹65 LPA (Base ₹18-24L + Huge Stock Grant + Bonus + Meals)",
            json.dumps(["Software Engineer (SWE)", "SWE Intern", "Associate Product Manager"]),
            json.dumps({
                "min_cgpa": "No strict CGPA cut-off, but 7.5+ recommended with strong academic standing",
                "backlogs": "No active backlogs allowed",
                "gap_allowed": "Permitted with valid explanation",
                "eligible_degrees": "B.Tech / M.Tech / Dual Degree / PhD in Computer Science, Math, or related STEM",
                "passing_years": "2024, 2025, 2026, 2027 Batch"
            }),
            json.dumps([
                {
                    "round_number": 1,
                    "round_name": "Google Online Challenge (GOC)",
                    "platform": "Google Assessment Platform",
                    "duration": "60 Minutes",
                    "negative_marking": "No negative marking",
                    "sections": [
                        {"name": "Algorithmic Challenges", "duration": "60 mins", "details": "2 Hard algorithmic problems focusing on Dynamic Programming, Trees, Graphs, or Combinatorics"}
                    ]
                },
                {
                    "round_number": 2,
                    "round_name": "Technical Screen (Phone / Virtual)",
                    "platform": "Google Meet + Google Docs",
                    "duration": "45 Minutes",
                    "negative_marking": "N/A",
                    "sections": [
                        {"name": "DSA & Problem Solving", "duration": "45 mins", "details": "Coding in a plain Google Doc (no syntax highlighting or autocompletion) to evaluate pure coding discipline"}
                    ]
                },
                {
                    "round_number": 3,
                    "round_name": "Onsite / Final Virtual Loop (3-4 Rounds)",
                    "platform": "Google Meet",
                    "duration": "4 x 45 Minutes",
                    "negative_marking": "N/A",
                    "sections": [
                        {"name": "Round 1: Advanced Algorithms", "duration": "45 mins", "details": "Graphs, DP, Segment Trees, Topological Sorting"},
                        {"name": "Round 2: Data Structures & System Scalability", "duration": "45 mins", "details": "Custom data structures, caching, Big-O efficiency"},
                        {"name": "Round 3: Complex Coding & Edge Cases", "duration": "45 mins", "details": "Writing bug-free, modular, clean code under time pressure"},
                        {"name": "Round 4: Googliness & Leadership", "duration": "45 mins", "details": "Collaboration, navigating ambiguity, ethical judgment, bias to help others"}
                    ]
                }
            ]),
            json.dumps([
                {"section": "Core Algorithms", "topics": ["Dynamic Programming (Bitmask, Tree DP)", "Graphs (Tarjan's, Dijkstra, Topological Sort)", "Segment Trees & Binary Indexed Trees", "Recursion & Backtracking"]},
                {"section": "Computer Science Foundations", "topics": ["Memory Management & Pointers", "Concurrency & Thread Safety", "Time & Space Complexity analysis"]},
                {"section": "Googliness", "topics": ["Doing the right thing", "Comfort with ambiguity", "Collaborative problem solving", "Intellectual humility"]}
            ]),
            json.dumps([
                "Apply via Google Careers portal or through an employee referral.",
                "Google Online Challenge (GOC) screening test.",
                "Recruiter phone screen and profile alignment.",
                "4 to 5 rigorous coding & Googliness rounds.",
                "Hiring Committee (HC) comprehensive review.",
                "Team matching phase and official offer packet."
            ]),
            json.dumps([
                "Practice coding on a blank text editor or Google Docs without syntax highlighting or auto-bracket closing.",
                "Ask clarifying questions before touching the keyboard: verify input constraints, negative numbers, duplicate values, and memory limits.",
                "Google interviewers evaluate how receptive you are to hints and feedback during the session.",
                "Show clean, modular function breakdown with descriptive variable names."
            ]),
            json.dumps([
                "Word Ladder II (Shortest transformation sequence using BFS + DFS backtracking).",
                "Count of Smaller Numbers After Self (using Merge Sort or Segment Tree).",
                "Design a distributed rate limiter for millions of QPS.",
                "Describe a situation where a project was failing or unclear. How did you navigate the ambiguity?"
            ]),
            "Very Hard",
            "July - October & Off-Campus Cycles"
        ),

        # 5. Microsoft
        (
            "Microsoft",
            "microsoft",
            "Product / Enterprise",
            "#00A4EF",
            "Empowering every person and every organization on the planet to achieve more.",
            "₹25 - ₹45 LPA (Base ₹15-18L + Stocks + Performance Bonus)",
            json.dumps(["Software Engineer", "Support Engineer", "Cloud Solution Architect"]),
            json.dumps({
                "min_cgpa": "7.0+ CGPA or 70% in 10th, 12th, and College",
                "backlogs": "Zero active backlogs allowed",
                "gap_allowed": "Maximum 1 year",
                "eligible_degrees": "B.E. / B.Tech / M.Tech in CS, IT, ECE, Data Science",
                "passing_years": "2024, 2025, 2026 Batch"
            }),
            json.dumps([
                {
                    "round_number": 1,
                    "round_name": "Online Assessment",
                    "platform": "Codility Platform",
                    "duration": "80 Minutes",
                    "negative_marking": "Evaluated on correctness and execution speed",
                    "sections": [
                        {"name": "Coding Problems", "duration": "80 mins", "details": "2-3 algorithmic problems (Array manipulation, String matching, Graph connectivity)"}
                    ]
                },
                {
                    "round_number": 2,
                    "round_name": "Technical Round 1 (Data Structures)",
                    "platform": "Microsoft Teams",
                    "duration": "45 - 60 Minutes",
                    "negative_marking": "N/A",
                    "sections": [
                        {"name": "DSA Coding", "duration": "45 mins", "details": "Linked lists, Trees, Stacks, Queues, Binary Search"}
                    ]
                },
                {
                    "round_number": 3,
                    "round_name": "Technical Round 2 (System & Low-Level Design)",
                    "platform": "Microsoft Teams",
                    "duration": "45 - 60 Minutes",
                    "negative_marking": "N/A",
                    "sections": [
                        {"name": "OOP & Design Patterns", "duration": "45 mins", "details": "Design a File System, In-memory Key-Value Store, or Elevator Controller"}
                    ]
                },
                {
                    "round_number": 4,
                    "round_name": "Partner / Director Round (AA Round)",
                    "platform": "Microsoft Teams",
                    "duration": "45 - 60 Minutes",
                    "negative_marking": "N/A",
                    "sections": [
                        {"name": "Engineering Philosophy & Fit", "duration": "45 mins", "details": "Growth mindset evaluation, past architecture decisions, and passion for Microsoft technologies"}
                    ]
                }
            ]),
            json.dumps([
                {"section": "Core Problem Solving", "topics": ["Binary Trees (LCA, Views, Zigzag)", "Linked Lists (Cycle, LRU Cache)", "Sorting & Searching", "Dynamic Programming"]},
                {"section": "Design & Fundamentals", "topics": ["OOPs 4 Pillars", "SOLID Principles", "Operating Systems (Threads, Semaphores)", "Database Indexing"]},
                {"section": "Culture & Mindset", "topics": ["Growth Mindset vs Fixed Mindset", "Learning from mistakes", "Customer empathy"]}
            ]),
            json.dumps([
                "Apply via Microsoft Engage / Microsoft Careers / Referrals.",
                "Codility Online Assessment.",
                "3 rounds of Technical Interviews on MS Teams.",
                "Final 'As-Appropriate' (AA) Leadership Interview.",
                "Offer roll out with relocation and benefits."
            ]),
            json.dumps([
                "Microsoft values clean, readable, object-oriented code with proper error handling and variable names.",
                "Demonstrate a 'Growth Mindset' — when you make a mistake, acknowledge it quickly and explain how you'd fix it.",
                "Revise Low-Level Design (LLD) and design patterns thoroughly.",
                "Be ready to explain the inner workings of memory, threads, and pointers."
            ]),
            json.dumps([
                "LRU Cache implementation with O(1) get and put operations.",
                "Lowest Common Ancestor in a Binary Tree.",
                "Design a distributed URL shortener service (like TinyURL).",
                "What is the difference between process and thread context switching overhead?"
            ]),
            "Hard",
            "August - November"
        ),

        # 6. Accenture
        (
            "Accenture",
            "accenture",
            "IT Services & Consulting",
            "#A100FF",
            "Let there be change — Global professional services company delivering 360-degree value.",
            "₹4.5 - ₹12.0 LPA (ASE: 4.5L, Advanced ASE: 6.5-12L)",
            json.dumps(["Associate Software Engineer (ASE)", "Advanced Associate Software Engineer (AASE)", "Cloud Engineer"]),
            json.dumps({
                "min_cgpa": "65% or 6.5 CGPA in Graduation, 10th, and 12th",
                "backlogs": "Zero active backlogs at the time of recruitment process",
                "gap_allowed": "Maximum 1 year educational gap",
                "eligible_degrees": "B.E. / B.Tech / M.E. / M.Tech / MCA / M.Sc (All streams)",
                "passing_years": "2024, 2025, 2026 Batch"
            }),
            json.dumps([
                {
                    "round_number": 1,
                    "round_name": "Cognitive & Technical Assessment",
                    "platform": "Wheebox / Aon CoCubes",
                    "duration": "90 Minutes",
                    "negative_marking": "No negative marking",
                    "sections": [
                        {"name": "Cognitive Ability (50 Qs)", "duration": "50 mins", "details": "English Ability (17 Qs), Critical Reasoning & Problem Solving (18 Qs), Abstract Reasoning (15 Qs)"},
                        {"name": "Technical Assessment (40 Qs)", "duration": "40 mins", "details": "Common Application & MS Office (12 Qs), Pseudocode (18 Qs), Networking & Security, Cloud (10 Qs)"}
                    ]
                },
                {
                    "round_number": 2,
                    "round_name": "Coding Assessment (Automated Elimination)",
                    "platform": "Wheebox Coding Platform",
                    "duration": "45 Minutes",
                    "negative_marking": "Evaluated on test cases passed",
                    "sections": [
                        {"name": "Coding Challenges", "duration": "45 mins", "details": "2 Coding problems (Easy to Medium level in C, C++, Java, or Python)"}
                    ]
                },
                {
                    "round_number": 3,
                    "round_name": "Communication Assessment",
                    "platform": "Automated Audio System",
                    "duration": "30 Minutes",
                    "negative_marking": "Scored on fluency, pronunciation, and vocabulary",
                    "sections": [
                        {"name": "Speaking & Listening Evaluation", "duration": "30 mins", "details": "Reading sentences, repeating audio phrases, answering short questions, story retelling"}
                    ]
                },
                {
                    "round_number": 4,
                    "round_name": "Virtual HR & Technical Interview",
                    "platform": "Accenture Interview Platform",
                    "duration": "20 - 30 Minutes",
                    "negative_marking": "N/A",
                    "sections": [
                        {"name": "Project & Culture Discussion", "duration": "25 mins", "details": "Discussion on academic projects, internships, leadership scenarios, and willingness to work across domains"}
                    ]
                }
            ]),
            json.dumps([
                {"section": "Cognitive", "topics": ["Abstract Reasoning", "Arrangements & Puzzles", "Sentence Completion", "Vocabulary"]},
                {"section": "Technical", "topics": ["Pseudocode loops & bitwise ops", "MS Excel & Office functions", "Network topologies & firewalls", "Cloud computing basics"]},
                {"section": "Coding", "topics": ["Array rotations & sums", "String anagrams & palindromes", "Number theory (Fibonacci, primes)"]}
            ]),
            json.dumps([
                "Registration on Accenture recruitment portal.",
                "Round 1: Cognitive + Technical Assessment.",
                "Round 2: Coding Assessment (Unlocks immediately upon passing Round 1).",
                "Round 3: Automated Communication Assessment.",
                "Round 4: Virtual Interview with Accenture Leader.",
                "Letter of Intent (LOI) and Onboarding documentation."
            ]),
            json.dumps([
                "Clear Round 1 cutoff to instantly unlock the coding round; if you fail the cognitive cutoff, the test ends immediately.",
                "The Communication Assessment is AI-evaluated: speak clearly, avoid background noise, and keep your voice cadence steady.",
                "Review basic MS Office shortcuts, formulas (VLOOKUP, SUMIF), and network security terms.",
                "Prepare a concise 1-minute introduction highlighting your strongest project."
            ]),
            json.dumps([
                "Find the sum of all elements in an array that are divisible by both 3 and 5.",
                "Write a function to check if two strings are anagrams of each other.",
                "Explain the difference between Symmetric and Asymmetric encryption.",
                "Tell me about a time you worked in a diverse group with conflicting opinions."
            ]),
            "Easy to Moderate",
            "August - November & March - May"
        )
    ]

    cursor.executemany("""
    INSERT INTO companies (
        name, slug, tier, logo_color, tagline, avg_package, roles_offered,
        eligibility, exam_pattern, syllabus, selection_process, interview_tips,
        frequent_questions, difficulty_rating, hiring_season
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, companies_data)

    conn.commit()
    conn.close()
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    init_db()
    seed_data_if_empty()
