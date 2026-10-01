
# ============================================================
# AI CAREER & SKILL INTELLIGENCE PLATFORM
# DAY 5 - FLASK BACKEND
# ============================================================

# Import Flask tools
from flask import Flask, jsonify, request, render_template

# Import recommendation engine functions
from career_engine import (
    get_user_skills,
    get_all_skills,
    get_all_job_roles,
    recommend_roles,
    recommend_roles_cosine
)

# Create Flask application
app = Flask(__name__)


# ============================================================
# ROUTE 1: HOME PAGE
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")

# ============================================================
# ROUTE 2: HEALTH CHECK
# ============================================================

@app.route("/api/health")
def health_check():

    return jsonify({
        "status": "success",
        "message": "Flask backend is running"
    })


# ============================================================
# ROUTE 3: GET ALL AVAILABLE SKILLS
# ============================================================

@app.route("/api/skills")
def get_skills():

    skills = get_all_skills()

    return jsonify({
        "status": "success",
        "total_skills": len(skills),
        "skills": skills
    })


# ============================================================
# ROUTE 4: GET ALL JOB ROLES
# ============================================================

@app.route("/api/roles")
def get_roles():

    roles = get_all_job_roles()

    return jsonify({
        "status": "success",
        "total_roles": len(roles),
        "job_roles": roles
    })


# ============================================================
# ROUTE 5: CAREER ANALYSIS (GET)
# ============================================================

@app.route("/api/career/<user_name>", methods=["GET"])
def career_analysis(user_name):

    # Retrieve user's skills
    user_skills = get_user_skills(user_name)

    # Validate user
    if not user_skills:

        return jsonify({
            "status": "error",
            "message": "User not found or no skills assigned",
            "user": user_name
        }), 404

    # Get recommendations from existing engine
    basic_recommendations = recommend_roles(user_name)

    cosine_recommendations = recommend_roles_cosine(user_name)

    results = []

    # Prepare recommendations for API
    for role, similarity in cosine_recommendations.items():

        basic_result = basic_recommendations.get(role, {})

        results.append({
            "job_role": role,
            "cosine_similarity": similarity,
            "match_percentage": basic_result.get(
                "match_percentage", 0
            ),
            "matched_skills": sorted(
                basic_result.get("matched_skills", set())
            ),
            "missing_skills": sorted(
                basic_result.get("missing_skills", set())
            )
        })

    # Return career analysis
    return jsonify({
        "status": "success",
        "user": user_name,
        "current_skills": sorted(user_skills),
        "total_roles_analyzed": len(results),
        "recommendations": results
    })


# ============================================================
# ROUTE 6: CAREER ANALYSIS (POST)
# ============================================================

@app.route("/api/career", methods=["POST"])
def career_analysis_post():

    # Read JSON data from request
    data = request.get_json(silent=True)

    # Validate JSON data
    if not isinstance(data, dict):

        return jsonify({
            "status": "error",
            "message": "Please provide valid JSON data"
        }), 400

    # Retrieve and validate user name
    user_name = data.get("user_name")

    if not isinstance(user_name, str) or not user_name.strip():

        return jsonify({
            "status": "error",
            "message": "A valid user_name is required"
        }), 400

    user_name = user_name.strip()

    # Retrieve user's skills
    user_skills = get_user_skills(user_name)

    # Check user existence and skills
    if not user_skills:

        return jsonify({
            "status": "error",
            "message": "User not found or no skills assigned",
            "user": user_name
        }), 404

    # Get recommendations
    basic_recommendations = recommend_roles(user_name)

    cosine_recommendations = recommend_roles_cosine(user_name)

    results = []

    # Process recommendations
    for role, similarity in cosine_recommendations.items():

        basic_result = basic_recommendations.get(role, {})

                # Get matched and missing skills
        matched_skills = basic_result.get(
            "matched_skills", set()
        )

        missing_skills = basic_result.get(
            "missing_skills", set()
        )

        # Calculate skill counts
        matched_count = len(matched_skills)

        missing_count = len(missing_skills)

        required_count = matched_count + missing_count

        # Calculate skill coverage
        if required_count > 0:
            skill_coverage = round(
                (matched_count / required_count) * 100,
                2
            )
        else:
            skill_coverage = 0

        # Prepare recommendation result
        results.append({
            "job_role": role,

            "cosine_similarity": similarity,

            "match_percentage": basic_result.get(
                "match_percentage", 0
            ),

            "skill_coverage": skill_coverage,

            "matched_count": matched_count,

            "required_count": required_count,

            "missing_count": missing_count,

            "matched_skills": sorted(matched_skills),

            "missing_skills": sorted(missing_skills)
        })

    # Return JSON response
    return jsonify({
        "status": "success",
        "user": user_name,
        "current_skills": sorted(user_skills),
        "total_roles_analyzed": len(results),
        "recommendations": results
    })


# ============================================================
# GLOBAL ERROR HANDLERS
# ============================================================

# Handle invalid URLs
@app.errorhandler(404)
def page_not_found(error):

    return jsonify({
        "status": "error",
        "message": "The requested API endpoint was not found"
    }), 404


# Handle unexpected server errors
@app.errorhandler(500)
def internal_server_error(error):

    return jsonify({
        "status": "error",
        "message": "An internal server error occurred"
    }), 500


# ============================================================
# START FLASK SERVER
# ============================================================

if __name__ == "__main__":

    app.run(debug=True)