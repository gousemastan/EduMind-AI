import sqlite3
from pathlib import Path


# ============================================================
# EDUMIND AI DATABASE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATA_DIR / "edumind.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def init_database():

    connection = get_connection()

    cursor = connection.cursor()

    # ========================================================
    # USERS TABLE
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    designation TEXT DEFAULT '',
    department TEXT DEFAULT '',
    job_role TEXT DEFAULT '',
    current_assignment TEXT DEFAULT '',
    education TEXT DEFAULT '',
    experience TEXT DEFAULT '',
    previous_training TEXT DEFAULT '[]',
    role TEXT DEFAULT 'learner',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
    """)

    # ========================================================
    # ADD EMPLOYEE PROFILE COLUMNS
    # ========================================================

    existing_columns = {
        row["name"]
        for row in cursor.execute(
            "PRAGMA table_info(users)"
        ).fetchall()
    }

    profile_columns = {
    "designation": "TEXT DEFAULT ''",
    "department": "TEXT DEFAULT ''",
    "job_role": "TEXT DEFAULT ''",
    "current_assignment": "TEXT DEFAULT ''",
    "education": "TEXT DEFAULT ''",
    "experience": "TEXT DEFAULT ''",
    "previous_training": "TEXT DEFAULT '[]'",
}

    for column_name, column_type in profile_columns.items():

        if column_name not in existing_columns:

            cursor.execute(
                f"""
                ALTER TABLE users
                ADD COLUMN {column_name} {column_type}
                """
            )

            print(
                f"✅ Added users column: {column_name}"
            )

    # ========================================================
    # LEARNING PROGRESS TABLE
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            topic TEXT NOT NULL,

            score INTEGER DEFAULT 0,

            completed INTEGER DEFAULT 0,

            updated_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id),

            UNIQUE(user_id, topic)
        )
    """)

    # ========================================================
    # QUIZ HISTORY TABLE
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            quiz_title TEXT
                DEFAULT 'Generated Quiz',

            topic TEXT
                DEFAULT 'General',

            score INTEGER
                DEFAULT 0,

            total_questions INTEGER
                DEFAULT 0,

            percentage REAL
                DEFAULT 0,

            result TEXT
                DEFAULT 'Completed',

            completed_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
        )
    """)
    
    
    
        # ========================================================
    # USER COMPETENCIES TABLE
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_competencies (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            category TEXT NOT NULL,

            skill TEXT NOT NULL,

            level TEXT NOT NULL DEFAULT 'Beginner',

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
            REFERENCES users(id),

            UNIQUE(user_id, category, skill)
        )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS competency_framework (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_role TEXT NOT NULL,
        category TEXT NOT NULL,
        skill TEXT NOT NULL,
        target_level TEXT NOT NULL DEFAULT 'Intermediate',
        UNIQUE(job_role, category, skill)
    )
""")
    
    
    framework_data = [

    # =========================================================
    # DATA ANALYST
    # =========================================================

    ("Data Analyst", "Statistical", "Sampling", "Intermediate"),
    ("Data Analyst", "Statistical", "Data Quality", "Advanced"),
    ("Data Analyst", "Statistical", "Descriptive Statistics", "Advanced"),
    ("Data Analyst", "Statistical", "Inferential Statistics", "Intermediate"),
    ("Data Analyst", "Statistical", "Survey Design", "Intermediate"),
    ("Data Analyst", "Statistical", "Statistical Analysis", "Advanced"),
    ("Data Analyst", "Statistical", "Data Visualization", "Advanced"),

    ("Data Analyst", "Technical", "Python", "Advanced"),
    ("Data Analyst", "Technical", "SQL", "Advanced"),
    ("Data Analyst", "Technical", "R", "Intermediate"),
    ("Data Analyst", "Technical", "Data Visualization Tools", "Advanced"),
    ("Data Analyst", "Technical", "AI / ML", "Intermediate"),
    ("Data Analyst", "Technical", "APIs", "Intermediate"),
    ("Data Analyst", "Technical", "Database Management", "Advanced"),

    ("Data Analyst", "Digital Governance", "Data Privacy", "Intermediate"),
    ("Data Analyst", "Digital Governance", "Cybersecurity", "Intermediate"),
    ("Data Analyst", "Digital Governance", "Open Data", "Intermediate"),
    ("Data Analyst", "Digital Governance", "Digital Public Infrastructure", "Intermediate"),

    ("Data Analyst", "Behavioural / Managerial", "Communication", "Intermediate"),
    ("Data Analyst", "Behavioural / Managerial", "Problem Solving", "Advanced"),
    ("Data Analyst", "Behavioural / Managerial", "Teamwork", "Intermediate"),


    # =========================================================
    # DATA SCIENTIST
    # =========================================================

    ("Data Scientist", "Statistical", "Sampling", "Advanced"),
    ("Data Scientist", "Statistical", "Data Quality", "Advanced"),
    ("Data Scientist", "Statistical", "Statistical Modelling", "Expert"),
    ("Data Scientist", "Statistical", "Inferential Statistics", "Advanced"),
    ("Data Scientist", "Statistical", "Experimental Design", "Advanced"),

    ("Data Scientist", "Technical", "Python", "Expert"),
    ("Data Scientist", "Technical", "SQL", "Advanced"),
    ("Data Scientist", "Technical", "R", "Advanced"),
    ("Data Scientist", "Technical", "AI / ML", "Expert"),
    ("Data Scientist", "Technical", "Data Visualization", "Advanced"),
    ("Data Scientist", "Technical", "Cloud Computing", "Advanced"),
    ("Data Scientist", "Technical", "APIs", "Intermediate"),
    ("Data Scientist", "Technical", "Big Data Analytics", "Advanced"),
    ("Data Scientist", "Technical", "Database Management", "Advanced"),

    ("Data Scientist", "Digital Governance", "Data Privacy", "Advanced"),
    ("Data Scientist", "Digital Governance", "Cybersecurity", "Advanced"),
    ("Data Scientist", "Digital Governance", "Open Data", "Advanced"),

    ("Data Scientist", "Behavioural / Managerial", "Communication", "Advanced"),
    ("Data Scientist", "Behavioural / Managerial", "Problem Solving", "Expert"),
    ("Data Scientist", "Behavioural / Managerial", "Research Skills", "Advanced"),


    # =========================================================
    # STATISTICAL OFFICER
    # =========================================================

    ("Statistical Officer", "Statistical", "Survey Design", "Advanced"),
    ("Statistical Officer", "Statistical", "Sampling", "Advanced"),
    ("Statistical Officer", "Statistical", "Data Quality", "Advanced"),
    ("Statistical Officer", "Statistical", "National Accounts", "Intermediate"),
    ("Statistical Officer", "Statistical", "Price Statistics", "Intermediate"),
    ("Statistical Officer", "Statistical", "Labour Statistics", "Intermediate"),
    ("Statistical Officer", "Statistical", "Agricultural Statistics", "Intermediate"),
    ("Statistical Officer", "Statistical", "Industrial Statistics", "Intermediate"),
    ("Statistical Officer", "Statistical", "SDG Indicators", "Intermediate"),
    ("Statistical Officer", "Statistical", "Data Visualization", "Intermediate"),
    ("Statistical Officer", "Statistical", "Statistical Analysis", "Advanced"),

    ("Statistical Officer", "Technical", "SQL", "Intermediate"),
    ("Statistical Officer", "Technical", "Python", "Intermediate"),
    ("Statistical Officer", "Technical", "R", "Intermediate"),
    ("Statistical Officer", "Technical", "Excel", "Advanced"),
    ("Statistical Officer", "Technical", "GIS", "Intermediate"),
    ("Statistical Officer", "Technical", "Statistical Software", "Intermediate"),

    ("Statistical Officer", "Digital Governance", "Data Privacy", "Intermediate"),
    ("Statistical Officer", "Digital Governance", "Cybersecurity", "Intermediate"),
    ("Statistical Officer", "Digital Governance", "Open Data", "Intermediate"),
    ("Statistical Officer", "Digital Governance", "Metadata Standards", "Intermediate"),
    ("Statistical Officer", "Digital Governance", "Digital Signatures", "Intermediate"),

    ("Statistical Officer", "Behavioural / Managerial", "Communication", "Advanced"),
    ("Statistical Officer", "Behavioural / Managerial", "Problem Solving", "Advanced"),
    ("Statistical Officer", "Behavioural / Managerial", "Teamwork", "Intermediate"),


    # =========================================================
    # IT / TECHNICAL OFFICER
    # =========================================================

    ("IT / Technical Officer", "Technical", "Python", "Advanced"),
    ("IT / Technical Officer", "Technical", "SQL", "Advanced"),
    ("IT / Technical Officer", "Technical", "APIs", "Advanced"),
    ("IT / Technical Officer", "Technical", "Cloud Computing", "Advanced"),
    ("IT / Technical Officer", "Technical", "Database Management", "Advanced"),
    ("IT / Technical Officer", "Technical", "System Administration", "Advanced"),
    ("IT / Technical Officer", "Technical", "Software Development", "Advanced"),

    ("IT / Technical Officer", "Digital Governance", "Cybersecurity", "Advanced"),
    ("IT / Technical Officer", "Digital Governance", "Data Privacy", "Advanced"),
    ("IT / Technical Officer", "Digital Governance", "Government Cloud", "Advanced"),
    ("IT / Technical Officer", "Digital Governance", "Digital Public Infrastructure", "Intermediate"),
    ("IT / Technical Officer", "Digital Governance", "Open Data", "Intermediate"),
    ("IT / Technical Officer", "Digital Governance", "Digital Signatures", "Intermediate"),

    ("IT / Technical Officer", "Behavioural / Managerial", "Communication", "Intermediate"),
    ("IT / Technical Officer", "Behavioural / Managerial", "Problem Solving", "Advanced"),
    ("IT / Technical Officer", "Behavioural / Managerial", "Teamwork", "Intermediate"),


    # =========================================================
    # MANAGER / TEAM LEAD
    # =========================================================

    ("Manager / Team Lead", "Statistical", "Data Interpretation", "Advanced"),
    ("Manager / Team Lead", "Statistical", "Data Quality", "Advanced"),
    ("Manager / Team Lead", "Statistical", "Statistical Analysis", "Intermediate"),

    ("Manager / Team Lead", "Technical", "Data Visualization", "Advanced"),
    ("Manager / Team Lead", "Technical", "Digital Tools", "Advanced"),
    ("Manager / Team Lead", "Technical", "AI / ML Awareness", "Intermediate"),

    ("Manager / Team Lead", "Digital Governance", "Data Privacy", "Advanced"),
    ("Manager / Team Lead", "Digital Governance", "Cybersecurity Awareness", "Advanced"),
    ("Manager / Team Lead", "Digital Governance", "Digital Governance", "Advanced"),

    ("Manager / Team Lead", "Behavioural / Managerial", "Leadership", "Expert"),
    ("Manager / Team Lead", "Behavioural / Managerial", "Communication", "Expert"),
    ("Manager / Team Lead", "Behavioural / Managerial", "Project Management", "Advanced"),
    ("Manager / Team Lead", "Behavioural / Managerial", "Decision Making", "Advanced"),
    ("Manager / Team Lead", "Behavioural / Managerial", "Change Management", "Advanced"),
    ("Manager / Team Lead", "Behavioural / Managerial", "Ethics", "Advanced"),
    ("Manager / Team Lead", "Behavioural / Managerial", "Team Building", "Advanced"),
]

    cursor.executemany("""
        INSERT OR IGNORE INTO competency_framework
        (
            job_role,
            category,
            skill,
            target_level
        )
        VALUES (?, ?, ?, ?)
    """, framework_data)
    
    
    # ========================================================
    # COMPETENCY ASSESSMENTS TABLE
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competency_assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            skill TEXT NOT NULL,
            score INTEGER NOT NULL DEFAULT 0,
            total_questions INTEGER NOT NULL DEFAULT 0,
            assessed_level TEXT NOT NULL DEFAULT 'Beginner',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
            REFERENCES users(id)
        )
    """)
        # ============================================================
    # iGoT ENROLLMENTS
    # ============================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS igot_enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            course_id TEXT NOT NULL,
            course_title TEXT NOT NULL,
            skill TEXT,
            duration TEXT,
            status TEXT DEFAULT 'enrolled',
            enrolled_at TEXT NOT NULL,
            completed_at TEXT,
            progress INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # ========================================================
    # SAVE DATABASE CHANGES
    # ========================================================

    connection.commit()

    connection.close()

    print("✅ SQLite database initialized.")
    print(f"📁 Database: {DATABASE_PATH}")