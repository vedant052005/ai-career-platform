
/* ==========================================================
   CAREERAI - DAY 6
   JAVASCRIPT + FLASK API INTEGRATION
========================================================== */

// Get HTML elements
const careerForm = document.getElementById("careerForm");
const userNameInput = document.getElementById("userName");
const analyzeButton = document.getElementById("analyzeButton");

const statusMessage = document.getElementById("statusMessage");
const resultsSection = document.getElementById("results");

const currentSkillsContainer = document.getElementById("currentSkills");
const recommendationsContainer = document.getElementById("recommendations");


// ==========================================================
// FORM SUBMISSION
// ==========================================================

careerForm.addEventListener("submit", async function (event) {

    // Prevent the browser from reloading the page
    event.preventDefault();

    // Get the user's name
    const userName = userNameInput.value.trim();

    // Validate the input
    if (!userName) {
        showStatus("Please enter your registered name.", "error");
        return;
    }

    // Show loading message
    showStatus("Analyzing your career profile...", "success");

    // Disable button during analysis
    analyzeButton.disabled = true;
    analyzeButton.textContent = "Analyzing...";

    // Hide previous results
    resultsSection.classList.add("hidden");

    try {

        // Send POST request to Flask
        const response = await fetch("/api/career", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                user_name: userName
            })

        });

        // Convert Flask response to JSON
        const data = await response.json();

        // Handle unsuccessful responses
        if (!response.ok) {

            showStatus(
                data.message || "Unable to analyze your career.",
                "error"
            );

            return;
        }

        // Display career results
        displayCareerResults(data);

        showStatus(
            "Career analysis completed successfully!",
            "success"
        );

    } catch (error) {

        // Handle network or server errors
        console.error("Career analysis error:", error);

        showStatus(
            "Unable to connect to the server. Please check Flask.",
            "error"
        );

    } finally {

        // Restore button
        analyzeButton.disabled = false;
        analyzeButton.textContent = "Analyze My Career";

    }

});


// ==========================================================
// DISPLAY CAREER RESULTS
// ==========================================================

function displayCareerResults(data) {

    // Clear previous results
    currentSkillsContainer.replaceChildren();
    recommendationsContainer.replaceChildren();

    // Display current skills
    data.current_skills.forEach(function (skill) {

        const skillTag = document.createElement("span");

        skillTag.className = "skill-tag";

        skillTag.textContent = skill;

        currentSkillsContainer.appendChild(skillTag);

    });


    // Display recommended job roles
    data.recommendations.forEach(function (role) {

        // Create a recommendation card
        const card = document.createElement("div");

        card.className = "role-card";


        // Job role title
        const title = document.createElement("h4");

        title.textContent = role.job_role;

        card.appendChild(title);


        // Match percentage
        const matchText = document.createElement("p");

        matchText.textContent =
            "Skill Match: " + role.match_percentage + "%";

        card.appendChild(matchText);


        // Progress bar container
        const progressContainer = document.createElement("div");

        progressContainer.className = "progress-container";

        const progressBar = document.createElement("div");

        progressBar.className = "progress-bar";

        // Keep the visual width between 0 and 100
        const matchValue = Number(role.match_percentage) || 0;

        progressBar.style.width =
            Math.min(100, Math.max(0, matchValue)) + "%";

        progressContainer.appendChild(progressBar);

        card.appendChild(progressContainer);


        // Cosine similarity
        const similarityText = document.createElement("p");

        similarityText.textContent =
            "Cosine Similarity: " +
            (Number(role.cosine_similarity)).toFixed(2) +
            "%";

        card.appendChild(similarityText);


        // Matched skills
        const matchedText = document.createElement("p");

        const matchedLabel = document.createElement("strong");

        matchedLabel.textContent = "Matched Skills: ";

        matchedText.appendChild(matchedLabel);

        matchedText.appendChild(
            document.createTextNode(
                role.matched_skills.length
                    ? role.matched_skills.join(", ")
                    : "None"
            )
        );

        card.appendChild(matchedText);


        // Missing skills
        const missingContainer = document.createElement("div");

        missingContainer.className = "missing-skills";

        const missingLabel = document.createElement("strong");

        missingLabel.textContent = "Skills to Learn: ";

        missingContainer.appendChild(missingLabel);

        missingContainer.appendChild(
            document.createTextNode(
                role.missing_skills.length
                    ? role.missing_skills.join(", ")
                    : "You have all the listed required skills!"
            )
        );

        card.appendChild(missingContainer);


        // Add card to recommendations
        recommendationsContainer.appendChild(card);

    });


    // Reveal results section
    resultsSection.classList.remove("hidden");

    // Scroll to results
    resultsSection.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });

}


// ==========================================================
// STATUS MESSAGES
// ==========================================================

function showStatus(message, type) {

    statusMessage.textContent = message;

    statusMessage.className = "";

    if (type === "error") {

        statusMessage.classList.add("status-error");

    } else {

        statusMessage.classList.add("status-success");

    }

}