import itertools
from collections import defaultdict

# 🔹 SKILL → FUTURE AI ROLE MAP (expandable to 200+)
SKILL_JOB_MAP = {
    # Frontend / Web
    ("html", "css", "js"): ["AI Frontend Developer", "AI UI/UX Designer", "AI MERN Stack Developer"],
    ("html", "css", "react"): ["AI Frontend Developer", "AI React Developer", "AI UI/UX Designer"],
    ("react", "nodejs", "js"): ["AI Fullstack Developer", "AI MERN Stack Developer", "AI Frontend Developer"],
    ("angular", "typescript", "js"): ["AI Frontend Developer", "AI UI/UX Designer"],

    # Backend / Fullstack
    ("python", "django"): ["AI Backend Developer", "AI Software Engineer", "AI ML Engineer"],
    ("nodejs", "express"): ["AI Backend Developer", "AI Fullstack Developer", "AI MERN Stack Developer"],
    ("java", "spring"): ["AI Backend Developer", "AI Software Developer"],

    # Data / Analytics
    ("python", "excel"): ["AI Data Analyst", "AI Software Developer", "AI Engineer"],
    ("python", "sql"): ["AI Data Engineer", "AI ML Engineer", "AI Business Analyst"],
    ("python", "pandas"): ["AI Data Analyst", "AI Data Scientist"],
    ("r", "statistics"): ["AI Data Analyst", "AI Data Scientist"],
    ("tableau", "excel"): ["AI Data Analyst", "AI Business Intelligence Specialist"],
    ("power bi", "excel"): ["AI BI Analyst", "AI Data Analyst"],

    # Machine Learning / AI
    ("python", "machine learning"): ["AI ML Engineer", "AI Data Scientist", "AI Software Developer"],
    ("python", "tensorflow"): ["AI ML Engineer", "AI Deep Learning Engineer"],
    ("python", "pytorch"): ["AI ML Engineer", "AI Deep Learning Engineer"],
    ("python", "nlp"): ["AI NLP Engineer", "AI ML Engineer", "AI Data Scientist"],
    ("python", "cv", "opencv"): ["AI Computer Vision Engineer", "AI ML Engineer"],

    # Cloud / DevOps
    ("aws", "docker"): ["AI Cloud Engineer", "AI DevOps Engineer"],
    ("azure", "kubernetes"): ["AI Cloud Engineer", "AI DevOps Engineer"],
    ("gcp", "ml"): ["AI Cloud ML Engineer", "AI Data Scientist"],

    # Security
    ("cybersecurity", "networking"): ["AI Security Engineer", "AI Cybersecurity Specialist"],

    # Mobile Development
    ("flutter", "dart"): ["AI Mobile Developer", "AI Fullstack Developer"],
    ("android", "java"): ["AI Mobile Developer", "AI Software Developer"],

    # UI/UX / Design
    ("ux", "design"): ["AI UI/UX Designer", "AI Product Designer"],
    ("figma", "ux"): ["AI UI/UX Designer", "AI Product Designer"],
    ("photoshop", "design"): ["AI UI/UX Designer", "AI Graphic AI Designer"],

    # ERP / BI
    ("sap", "finance"): ["AI ERP Consultant", "AI Business Analyst"],
    ("sql", "power bi"): ["AI BI Analyst", "AI Data Analyst"],
}

# 🔹 Job Descriptions (expandable to 200+ roles)
JOB_DESCRIPTIONS = {
    "AI Frontend Developer": "Build AI-enhanced user interfaces with modern frontend frameworks.",
    "AI React Developer": "Develop intelligent web applications using React with AI features.",
    "AI UI/UX Designer": "Design user experiences using AI insights to improve usability.",
    "AI MERN Stack Developer": "Fullstack developer for AI applications using MongoDB, Express, React, Node.js.",
    "AI Backend Developer": "Develop backend systems with AI integration, APIs, and database management.",
    "AI Software Engineer": "Build AI-adapted software solutions for enterprises.",
    "AI ML Engineer": "Design and implement machine learning models to solve real-world problems.",
    "AI Data Analyst": "Analyze data with AI-driven insights and visualizations.",
    "AI Data Scientist": "Build AI models and predictive analytics pipelines.",
    "AI Data Engineer": "Create pipelines and infrastructure for AI-ready data processing.",
    "AI Business Analyst": "Apply AI analytics to improve business processes.",
    "AI NLP Engineer": "Develop AI systems for NLP tasks like chatbots and sentiment analysis.",
    "AI Deep Learning Engineer": "Design deep learning models for image, audio, and text data.",
    "AI Cloud Engineer": "Build and maintain AI-driven cloud applications.",
    "AI DevOps Engineer": "Implement AI automation in CI/CD pipelines and cloud operations.",
    "AI Product Designer": "Design AI-enhanced products focusing on usability and intelligence.",
    "AI Cybersecurity Specialist": "Use AI to detect and mitigate cybersecurity threats in networks.",
    "AI Mobile Developer": "Develop AI-powered mobile apps for Android/iOS.",
    "AI ERP Consultant": "Implement AI-enhanced ERP solutions for businesses.",
    "AI BI Analyst": "Use AI to generate business intelligence reports from large datasets."
}

# 🔹 Normalize skills
def normalize_skills(skills_input):
    return [s.strip().lower() for s in skills_input]

# 🔹 Predict future AI roles
def predict_future_roles(user_skills):
    user_skills = normalize_skills(user_skills)
    role_scores = defaultdict(float)

    # Combination match (2–4 skills)
    for r in range(2, min(5, len(user_skills)+1)):
        for comb in itertools.combinations(user_skills, r):
            comb_sorted = tuple(sorted(comb))
            for skill_map in SKILL_JOB_MAP:
                if set(comb_sorted).issubset(skill_map):
                    for role in SKILL_JOB_MAP[skill_map]:
                        role_scores[role] += 2

    # Partial match (single skill)
    for skill in user_skills:
        for skill_map, roles in SKILL_JOB_MAP.items():
            if skill in skill_map:
                for role in roles:
                    role_scores[role] += 1

    if not role_scores:
        return [{"role": "No matching AI roles found", "confidence": 0, "adaptability": 0, "description": ""}]

    # Build predictions
    total_score = sum(role_scores.values())
    predictions = []
    for role, score in role_scores.items():
        confidence = round((score / total_score) * 100, 2)
        adaptability = round(min(score / len(user_skills), 1) * 100, 2)
        description = JOB_DESCRIPTIONS.get(role, "Description not available.")
        predictions.append({"role": role, "confidence": confidence, "adaptability": adaptability, "description": description})

    predictions = sorted(predictions, key=lambda x: x["confidence"], reverse=True)
    return predictions

# 🔹 CLI
if __name__ == "__main__":
    print("✅ AI Future IT Roles Predictor with Adaptability & Descriptions")
    skills_input = input("Enter your skills (comma separated), e.g., Python, Excel, SQL:\nSkills: ")
    skills_list = skills_input.split(",")
    results = predict_future_roles(skills_list)

    print("\n📌 Top Future IT Roles Predictions:")
    for idx, res in enumerate(results[:20], 1):
        print(f"{idx}. {res['role']} - Confidence: {res['confidence']}% | AI Adaptability: {res['adaptability']}%")
        print(f"   Description: {res['description']}\n")