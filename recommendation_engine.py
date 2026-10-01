
# ---------------- USER SKILLS ----------------

user_skills = {
    "python",
    "sql",
    "pandas",
    "statistics",
    "excel"
}


# ---------------- JOB REQUIREMENTS ----------------

required_skills = {
    "python",
    "sql",
    "machine learning",
    "statistics",
    "pandas",
    "numpy",
    "scikit-learn",
    "git",
    "deep learning"
}

# ---------------- JOB ROLES ----------------

job_roles = {

    "Python Developer": {
        "python",
        "sql",
        "git",
        "oop",
        "django",
        "apis"
    },

    "Data Analyst": {
        "python",
        "sql",
        "pandas",
        "statistics",
        "excel",
        "power bi"
    },

    "Machine Learning Engineer": {
        "python",
        "sql",
        "machine learning",
        "statistics",
        "pandas",
        "numpy",
        "scikit-learn",
        "git",
        "deep learning"
    },

    "Frontend Developer": {
        "html",
        "css",
        "javascript",
        "react",
        "git"
    }
}


# ---------------- MATCHING FUNCTION ----------------

def calculate_match(user_skills, required_skills):

    matched = user_skills & required_skills
    # & = intersection → skills present in BOTH sets

    missing = required_skills - user_skills
    # - = difference → required skills the user DOES NOT have

    match_percentage = (len(matched) / len(required_skills)) * 100
    # len() = number of items
    # Formula = matched / total required × 100

    return matched, missing, match_percentage
    # return = send the results back to the caller


# ---------------- FUNCTION CALL ----------------

matched, missing, match_percentage = calculate_match(
    user_skills,
    required_skills
)
# Calls the function and stores its 3 results

def recommend_roles(user_skills, job_roles):
    # Compare the user's skills with every available job role

    recommendations = {}
    # Empty dictionary to store complete results for each role

    for role, required_skills in job_roles.items():
        # Take one job role at a time

        matched, missing, match_percentage = calculate_match(
            user_skills,
            required_skills
        )
        # Calculate match information for this role

        recommendations[role] = {
            "match_percentage": round(match_percentage, 2),
            "matched_skills": matched,
            "missing_skills": missing
        }
        # Store all information about this role

    return recommendations
    # Return all role recommendations

def recommend_skills(user_skills, required_skills):
    # Find skills required by the role that the user does not have

    missing_skills = required_skills - user_skills
    # - = difference → finds missing skills

    return missing_skills
    # Return the missing skills as recommendations

# ---------------- DISPLAY RESULTS ----------------

print("Matched Skills:", matched)
# print() = display information in terminal

print("Missing Skills:", missing)

print("Match Percentage:", round(match_percentage,2))

recommendations = recommend_roles(user_skills, job_roles)
# Compare the user with all available job roles

print("\n===== JOB ROLE RECOMMENDATIONS =====")

for role, result in recommendations.items():
    # Go through each recommended role

    print("\nRole:", role)

    print("Match:", result["match_percentage"], "%")

    print("Matched Skills:", result["matched_skills"])

    print("Missing Skills:", result["missing_skills"])

recommended_skills = recommend_skills(
    user_skills,
    job_roles["Machine Learning Engineer"]
)

print("\n===== RECOMMENDED SKILLS =====")

for skill in recommended_skills:
    # Go through each recommended skill

    print("-", skill)