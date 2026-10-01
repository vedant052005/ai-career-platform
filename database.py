import sqlite3
# sqlite3 = Python's built-in SQLite database library


# ============================================================
# 1. CONNECT TO DATABASE
# ============================================================

connection = sqlite3.connect("career_platform.db")
# Connect to the database
# If the file does not exist, SQLite creates it


# ============================================================
# 2. CREATE USERS TABLE
# ============================================================

connection.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    education TEXT NOT NULL
)
""")
# Create the users table
# id = unique ID for each user
# name = user's name
# education = user's education


# ============================================================
# 3. CREATE SKILLS TABLE
# ============================================================

connection.execute("""
CREATE TABLE skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_name TEXT NOT NULL
)
""")
# Create the skills table
# id = unique ID for each skill
# skill_name = name of the skill


# ============================================================
# 4. CREATE USER_SKILLS TABLE
# ============================================================

connection.execute("""
CREATE TABLE user_skills (
    user_id INTEGER,
    skill_id INTEGER,

    PRIMARY KEY (user_id, skill_id),

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (skill_id) REFERENCES skills(id)
)
""")
# Connect users with their skills
# user_id = ID of the user
# skill_id = ID of the skill
# PRIMARY KEY prevents duplicate user-skill combinations
# FOREIGN KEY connects this table to users and skills


# ============================================================
# 5. CREATE JOB_ROLES TABLE
# ============================================================

connection.execute("""
CREATE TABLE job_roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT NOT NULL UNIQUE
)
""")
# Create the job_roles table
# id = unique ID for each job role
# role_name = name of the career role
# UNIQUE = prevents duplicate job roles


# ============================================================
# 6. CREATE JOB_ROLE_SKILLS TABLE
# ============================================================

connection.execute("""
CREATE TABLE job_role_skills (
    job_role_id INTEGER,
    skill_id INTEGER,

    PRIMARY KEY (job_role_id, skill_id),

    FOREIGN KEY (job_role_id) REFERENCES job_roles(id),
    FOREIGN KEY (skill_id) REFERENCES skills(id)
)
""")
# Connect job roles with their required skills
# job_role_id = ID of the job role
# skill_id = ID of the required skill
# PRIMARY KEY prevents duplicate role-skill combinations
# FOREIGN KEY connects this table to job_roles and skills


# ============================================================
# 7. INSERT SKILLS
# ============================================================

skills = [
    "python",
    "sql",
    "git",
    "oop",
    "django",
    "apis",
    "pandas",
    "statistics",
    "excel",
    "power bi",
    "machine learning",
    "numpy",
    "scikit-learn",
    "deep learning",
    "html",
    "css",
    "javascript",
    "react"
]
# List of all unique skills used in our project


for skill in skills:
    connection.execute(
        "INSERT INTO skills (skill_name) VALUES (?)",
        (skill,)
    )
# Insert each skill into the skills table
# ? = placeholder for the skill value


# ============================================================
# 8. VERIFY SKILLS
# ============================================================

cursor = connection.execute(
    "SELECT id, skill_name FROM skills"
)
# Get all skill records from the skills table

skills_data = cursor.fetchall()
# Fetch all records returned by the query


print("\n===== SKILLS IN DATABASE =====")

for skill in skills_data:
    print(skill)
# Print every skill stored in the database


# ============================================================
# 9. INSERT JOB ROLES
# ============================================================

job_roles = [
    "Python Developer",
    "Data Analyst",
    "Machine Learning Engineer",
    "Frontend Developer"
]
# List of job roles available in our career platform


for role in job_roles:
    connection.execute(
        "INSERT INTO job_roles (role_name) VALUES (?)",
        (role,)
    )
# Insert each job role into the database


# ============================================================
# 10. VERIFY JOB ROLES
# ============================================================

cursor = connection.execute(
    "SELECT id, role_name FROM job_roles"
)
# Get all job roles from the database

roles_data = cursor.fetchall()
# Fetch all returned records


print("\n===== JOB ROLES IN DATABASE =====")

for role in roles_data:
    print(role)
# Display every job role


# Save the changes
connection.commit()


# ============================================================
# 11. DEFINE JOB ROLE REQUIREMENTS
# ============================================================

job_role_requirements = {
    "Python Developer": [
        "python",
        "sql",
        "git",
        "oop",
        "django",
        "apis"
    ],

    "Data Analyst": [
        "python",
        "sql",
        "pandas",
        "statistics",
        "excel",
        "power bi"
    ],

    "Machine Learning Engineer": [
        "python",
        "sql",
        "machine learning",
        "statistics",
        "pandas",
        "numpy",
        "scikit-learn",
        "git",
        "deep learning"
    ],

    "Frontend Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "git"
    ]
}
# Store required skills for each job role


# ============================================================
# 12. CONNECT JOB ROLES WITH REQUIRED SKILLS
# ============================================================

for role, required_skills in job_role_requirements.items():
    # Take one job role at a time

    role_result = connection.execute(
        "SELECT id FROM job_roles WHERE role_name = ?",
        (role,)
    ).fetchone()
    # Find the ID of the job role

    role_id = role_result[0]
    # Get the actual role ID


    for skill in required_skills:
        # Take one required skill at a time

        skill_result = connection.execute(
            "SELECT id FROM skills WHERE skill_name = ?",
            (skill,)
        ).fetchone()
        # Find the ID of the skill

        skill_id = skill_result[0]
        # Get the actual skill ID


        connection.execute(
            """
            INSERT INTO job_role_skills (job_role_id, skill_id)
            VALUES (?, ?)
            """,
            (role_id, skill_id)
        )
        # Connect the job role with its required skill


# ============================================================
# 13. VERIFY JOB ROLE → REQUIRED SKILLS
# ============================================================

cursor = connection.execute("""
SELECT
    job_roles.role_name,
    skills.skill_name
FROM job_role_skills
JOIN job_roles
    ON job_role_skills.job_role_id = job_roles.id
JOIN skills
    ON job_role_skills.skill_id = skills.id
ORDER BY job_roles.id
""")
# JOIN the related tables
# Get each job role and its required skills


role_skills = cursor.fetchall()
# Get all results from the query


print("\n===== JOB ROLE → REQUIRED SKILLS =====")

for role, skill in role_skills:
    print(role, "→", skill)
# Display each job role with its required skill


# ============================================================
# 14. INSERT TEST USER
# ============================================================

connection.execute(
    """
    INSERT INTO users (name, education)
    VALUES (?, ?)
    """,
    ("Rambo", "BCA")
)
# Add a test user to the users table


# ============================================================
# 15. VERIFY USER
# ============================================================

cursor = connection.execute(
    "SELECT id, name, education FROM users"
)
# Get users from the database

users_data = cursor.fetchall()
# Fetch all users


print("\n===== USERS =====")

for user in users_data:
    print(user)
# Display each user


# ============================================================
# 16. CONNECT USER WITH SKILLS
# ============================================================

user_skills = [
    "python",
    "sql",
    "machine learning",
    "html",
    "css"
]
# Skills that our test user has


user_result = connection.execute(
    "SELECT id FROM users WHERE name = ?",
    ("Rambo",)
).fetchone()
# Find Rambo's user ID


user_id = user_result[0]
# Get the actual user ID


for skill in user_skills:
    # Take one user skill at a time

    skill_result = connection.execute(
        "SELECT id FROM skills WHERE skill_name = ?",
        (skill,)
    ).fetchone()
    # Find the ID of this skill

    skill_id = skill_result[0]
    # Get the actual skill ID


    connection.execute(
        """
        INSERT INTO user_skills (user_id, skill_id)
        VALUES (?, ?)
        """,
        (user_id, skill_id)
    )
    # Connect the user with the skill


# ============================================================
# 17. VERIFY USER → SKILLS
# ============================================================

cursor = connection.execute("""
SELECT
    users.name,
    skills.skill_name
FROM user_skills
JOIN users
    ON user_skills.user_id = users.id
JOIN skills
    ON user_skills.skill_id = skills.id
WHERE users.name = ?
""", ("Rambo",))
# Get Rambo's skills by joining the tables


user_skill_data = cursor.fetchall()
# Get all matching records


print("\n===== USER SKILLS =====")

for name, skill in user_skill_data:
    print(name, "→", skill)
# Display the user's skills


# ============================================================
# 18. FINAL MATCHING TEST
# ============================================================

cursor = connection.execute("""
SELECT
    skills.skill_name
FROM user_skills
JOIN skills
    ON user_skills.skill_id = skills.id
JOIN job_role_skills
    ON skills.id = job_role_skills.skill_id
JOIN job_roles
    ON job_role_skills.job_role_id = job_roles.id
JOIN users
    ON user_skills.user_id = users.id
WHERE users.name = ?
AND job_roles.role_name = ?
""", ("Rambo", "Machine Learning Engineer"))
# Find skills that Rambo has
# and that are also required by the
# Machine Learning Engineer role


matching_skills = cursor.fetchall()
# Get all matching skills


print("\n===== MATCHING SKILLS =====")

for skill in matching_skills:
    print("-", skill[0])
# Display the matching skills


# ============================================================
# 19. SAVE AND CLOSE DATABASE
# ============================================================

print("User skills inserted successfully!")
print("Job role skills inserted successfully!")


connection.commit()
# Save all database changes


connection.close()
# Close the database connection