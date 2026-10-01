
import sqlite3
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# 1. CONNECT TO DATABASE
# ============================================================

from pathlib import Path

# Get the folder where career_engine.py is located
BASE_DIR = Path(__file__).resolve().parent

# Set the correct database path
DATABASE_PATH = BASE_DIR / "career_platform.db"

# Connect to the correct database
connection = sqlite3.connect(
    str(DATABASE_PATH),
    check_same_thread=False
)
# Connect Python to the existing SQLite database

# ============================================================
# 2. GET USER SKILLS
# ============================================================
def get_user_skills(user_name):
    # Get the skills belonging to a particular user

    cursor = connection.execute("""
        SELECT skills.skill_name
        FROM users
        JOIN user_skills
            ON users.id = user_skills.user_id
        JOIN skills
            ON user_skills.skill_id = skills.id
        WHERE users.name = ?
    """, (user_name,))

    rows = cursor.fetchall()

    user_skills = set()

    for row in rows:
        user_skills.add(row[0])

    return user_skills


# ============================================================
# 3. GET ALL AVAILABLE SKILLS
# ============================================================

def get_all_skills():
    # Retrieve all skills from the database

    cursor = connection.execute("""
        SELECT skill_name
        FROM skills
    """)

    rows = cursor.fetchall()

    all_skills = [row[0] for row in rows]

    return all_skills


# ============================================================
# 4. GET REQUIRED SKILLS
# ============================================================

def get_required_skills(job_role):
    # Get skills required for a particular job role

    cursor = connection.execute("""
        SELECT skills.skill_name
        FROM job_role_skills
        JOIN job_roles
            ON job_role_skills.job_role_id = job_roles.id
        JOIN skills
            ON job_role_skills.skill_id = skills.id
        WHERE job_roles.role_name = ?
    """, (job_role,))

    rows = cursor.fetchall()

    required_skills = set()

    for row in rows:
        required_skills.add(row[0])

    return required_skills


# ============================================================
# 5. GET ALL JOB ROLES
# ============================================================

def get_all_job_roles():
    # Retrieve all job roles from the database

    cursor = connection.execute("""
        SELECT role_name
        FROM job_roles
    """)

    rows = cursor.fetchall()

    job_roles = []

    for row in rows:
        job_roles.append(row[0])

    return job_roles


# ============================================================
# 6. CALCULATE MATCH USING SETS (DAY 3)
# ============================================================

def calculate_match(user_skills, required_skills):
    # Compare user skills with required skills

    matched = user_skills & required_skills

    missing = required_skills - user_skills

    if len(required_skills) == 0:
        return matched, missing, 0

    match_percentage = (
        len(matched) / len(required_skills)
    ) * 100

    return matched, missing, match_percentage


# ============================================================
# 7. RECOMMEND JOB ROLES (DAY 3)
# ============================================================

def recommend_roles(user_name):
    # Analyze the user against every job role

    user_skills = get_user_skills(user_name)

    job_roles = get_all_job_roles()

    recommendations = {}

    for role in job_roles:

        required_skills = get_required_skills(role)

        matched, missing, match_percentage = calculate_match(
            user_skills,
            required_skills
        )

        recommendations[role] = {
            "match_percentage": round(match_percentage, 2),
            "matched_skills": matched,
            "missing_skills": missing
        }

    return recommendations


# ============================================================
# 8. RECOMMEND MISSING SKILLS (DAY 3)
# ============================================================

def recommend_skills(user_name, job_role):
    # Find skills the user should learn

    user_skills = get_user_skills(user_name)

    required_skills = get_required_skills(job_role)

    missing_skills = required_skills - user_skills

    return missing_skills


# ============================================================
# DAY 4 - STEP 4.1: CREATE SKILL VECTORS
# ============================================================

def create_skill_vector(user_skills, all_skills):
    # Convert a set of skills into a binary vector

    vector = []

    for skill in all_skills:

        if skill in user_skills:
            vector.append(1)
            # 1 means the skill is present

        else:
            vector.append(0)
            # 0 means the skill is absent

    return vector


# ============================================================
# DAY 4 - STEP 4.2: CALCULATE COSINE SIMILARITY
# ============================================================

def calculate_cosine_match(user_skills, required_skills):
    # Get all available skills from the database

    all_skills = get_all_skills()

    # Create vectors using the same skill order

    user_vector = create_skill_vector(
        user_skills,
        all_skills
    )

    job_vector = create_skill_vector(
        required_skills,
        all_skills
    )

    # Convert vectors into NumPy arrays

    user_array = np.array(user_vector).reshape(1, -1)

    job_array = np.array(job_vector).reshape(1, -1)

    # Calculate cosine similarity using scikit-learn

    similarity = cosine_similarity(
        user_array,
        job_array
    )[0][0]

    # Convert similarity into a percentage

    similarity_percentage = similarity * 100

    return round(similarity_percentage, 2)

# DAY 8 - STEP 3: ROLE-RESTRICTED COSINE SIMILARITY

def calculate_role_cosine_match(user_skills, required_skills):

    # Handle roles with no required skills
    if not required_skills:
        return 0

    # Only consider skills required for this job role
    user_vector = [
        1 if skill in user_skills else 0
        for skill in sorted(required_skills)
    ]

    # The job role requires every skill in this vector
    job_vector = [1] * len(required_skills)

    # Convert lists into NumPy arrays
    user_array = np.array(user_vector).reshape(1, -1)
    job_array = np.array(job_vector).reshape(1, -1)

    # Calculate cosine similarity
    similarity = cosine_similarity(
        user_array,
        job_array
    )[0][0]

    return round(similarity * 100, 2)


# ============================================================
# DAY 4 - STEP 4.3: RECOMMEND ROLES USING COSINE SIMILARITY
# ============================================================

# ============================================================
# DAY 4 - STEP 6: SORT JOB ROLES BY SIMILARITY
# ============================================================

def recommend_roles_cosine(user_name):

    # Get the user's skills
    user_skills = get_user_skills(user_name)

    # Get all available job roles
    job_roles = get_all_job_roles()

    recommendations = {}

    # Calculate similarity for every job role
    for role in job_roles:

        required_skills = get_required_skills(role)

        similarity_percentage = calculate_role_cosine_match(
    user_skills,
    required_skills
)

        recommendations[role] = similarity_percentage

    # Sort roles from highest similarity to lowest
    sorted_recommendations = dict(
        sorted(
            recommendations.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )

    return sorted_recommendations


# ============================================================
# 9. TEST THE CAREER ENGINE
# ============================================================

if __name__ == "__main__":

    user_name = "Rambo"

    print("\n========================================")
    print("       AI CAREER ANALYSIS")
    print("========================================")

    # --------------------------------------------------------
    # USER SKILLS
    # --------------------------------------------------------

    user_skills = get_user_skills(user_name)

    print("\nUser:", user_name)
    print("Current Skills:", user_skills)

    # --------------------------------------------------------
    # DAY 3 - SET-BASED JOB RECOMMENDATIONS
    # --------------------------------------------------------

    recommendations = recommend_roles(user_name)

    print("\n===== DAY 3: SET-BASED RECOMMENDATIONS =====")

    for role, result in recommendations.items():

        print("\nRole:", role)

        print("Match:", result["match_percentage"], "%")

        print("Matched Skills:", result["matched_skills"])

        print("Missing Skills:", result["missing_skills"])

    # --------------------------------------------------------
    # DAY 3 - SKILLS TO LEARN
    # --------------------------------------------------------

    recommended_skills = recommend_skills(
        user_name,
        "Machine Learning Engineer"
    )

    print("\n===== SKILLS TO LEARN =====")

    for skill in recommended_skills:
        print("-", skill)

    # --------------------------------------------------------
    # DAY 4 - DATABASE SKILLS
    # --------------------------------------------------------

    all_skills = get_all_skills()

    print("\n===== DAY 4: DATABASE SKILLS =====")

    print("All Available Skills:", all_skills)

    # --------------------------------------------------------
    # DAY 4 - COSINE SIMILARITY RECOMMENDATIONS
    # --------------------------------------------------------

    cosine_recommendations = recommend_roles_cosine(user_name)

    print("\n===== DAY 4: COSINE SIMILARITY =====")

    for role, percentage in cosine_recommendations.items():

        print("\nRole:", role)

        print("Cosine Similarity:", percentage, "%")

    print("\n========================================")
    print("       ANALYSIS COMPLETE")
    print("========================================")


# ============================================================
# 10. CLOSE DATABASE
# ============================================================
# Close the connection only when running career_engine.py directly
if __name__ == "__main__":
    connection.close()
# Close the database after all testing is complete