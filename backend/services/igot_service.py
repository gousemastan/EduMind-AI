# ============================================================
# iGoT Karmayogi Course Integration Service
# ============================================================

import os
import requests
from dotenv import load_dotenv

load_dotenv()


# ============================================================
# Configuration
# ============================================================

KARMAYOGI_API_KEY = os.getenv("KARMAYOGI_API_KEY", "").strip()

KARMAYOGI_BASE_URL = os.getenv(
    "KARMAYOGI_BASE_URL",
    "https://igot.gov.in"
).rstrip("/")


# ============================================================
# Demo / Fallback Course Catalog
# ============================================================

COURSE_CATALOG = [
    {
        "id": "igot-python-001",
        "title": "Python for Data Analysis",
        "skill": "Python",
        "category": "Technical",
        "level": "Intermediate",
        "provider": "iGoT Karmayogi",
        "duration": "6 Hours",
        "description": "Build practical Python skills for data analysis and statistical work.",
        "url": "https://www.igotkarmayogi.gov.in/"
    },
    {
        "id": "igot-sql-001",
        "title": "SQL for Data Management",
        "skill": "SQL",
        "category": "Technical",
        "level": "Intermediate",
        "provider": "iGoT Karmayogi",
        "duration": "5 Hours",
        "description": "Learn SQL fundamentals for querying and managing structured data.",
        "url": "https://www.igotkarmayogi.gov.in/"
    },
    {
        "id": "igot-ai-001",
        "title": "Artificial Intelligence Fundamentals",
        "skill": "AI / ML",
        "category": "Technical",
        "level": "Intermediate",
        "provider": "iGoT Karmayogi",
        "duration": "7 Hours",
        "description": "Understand fundamental AI and machine learning concepts.",
        "url": "https://www.igotkarmayogi.gov.in/"
    },
    {
        "id": "igot-dv-001",
        "title": "Data Visualization Fundamentals",
        "skill": "Data Visualization",
        "category": "Technical",
        "level": "Intermediate",
        "provider": "iGoT Karmayogi",
        "duration": "4 Hours",
        "description": "Learn effective techniques for presenting statistical data visually.",
        "url": "https://www.igotkarmayogi.gov.in/"
    },
    {
        "id": "igot-survey-001",
        "title": "Survey Design Fundamentals",
        "skill": "Survey Design",
        "category": "Statistical",
        "level": "Intermediate",
        "provider": "iGoT Karmayogi",
        "duration": "5 Hours",
        "description": "Strengthen knowledge of survey planning, design and implementation.",
        "url": "https://www.igotkarmayogi.gov.in/"
    },
    {
        "id": "igot-sampling-001",
        "title": "Sampling Methods",
        "skill": "Sampling",
        "category": "Statistical",
        "level": "Intermediate",
        "provider": "iGoT Karmayogi",
        "duration": "5 Hours",
        "description": "Develop practical understanding of statistical sampling methods.",
        "url": "https://www.igotkarmayogi.gov.in/"
    },
    {
        "id": "igot-dq-001",
        "title": "Data Quality Management",
        "skill": "Data Quality",
        "category": "Statistical",
        "level": "Intermediate",
        "provider": "iGoT Karmayogi",
        "duration": "4 Hours",
        "description": "Learn methods for maintaining and improving data quality.",
        "url": "https://www.igotkarmayogi.gov.in/"
    },
    {
        "id": "igot-cyber-001",
        "title": "Cybersecurity Awareness",
        "skill": "Cybersecurity",
        "category": "Digital Governance",
        "level": "Beginner",
        "provider": "iGoT Karmayogi",
        "duration": "3 Hours",
        "description": "Understand essential cybersecurity practices for government workplaces.",
        "url": "https://www.igotkarmayogi.gov.in/"
    },
    {
        "id": "igot-privacy-001",
        "title": "Data Privacy and Protection",
        "skill": "Data Privacy",
        "category": "Digital Governance",
        "level": "Intermediate",
        "provider": "iGoT Karmayogi",
        "duration": "4 Hours",
        "description": "Build awareness of responsible data handling and privacy practices.",
        "url": "https://www.igotkarmayogi.gov.in/"
    },
    {
        "id": "igot-leadership-001",
        "title": "Leadership and Team Management",
        "skill": "Leadership",
        "category": "Behavioural / Managerial",
        "level": "Intermediate",
        "provider": "iGoT Karmayogi",
        "duration": "5 Hours",
        "description": "Develop leadership and team-management capabilities.",
        "url": "https://www.igotkarmayogi.gov.in/"
    },
]


# ============================================================
# Helper: API Headers
# ============================================================

def get_karmayogi_headers():
    """
    Build authentication headers for Karmayogi/iGoT API.
    """

    if not KARMAYOGI_API_KEY:
        return {}

    return {
        "Authorization": f"Bearer {KARMAYOGI_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


# ============================================================
# Check Real iGoT Configuration
# ============================================================

def is_real_igot_configured():
    """
    Return True when an iGoT/Karmayogi API key is configured.
    """

    return bool(KARMAYOGI_API_KEY)


# ============================================================
# Real iGoT API Request Helper
# ============================================================

def karmayogi_request(
    method,
    endpoint,
    params=None,
    json_data=None,
    timeout=20,
):
    """
    Send a server-side request to the Karmayogi/iGoT API.

    Returns:
        dict/list from API on success
        None on failure
    """

    if not is_real_igot_configured():
        return None

    url = f"{KARMAYOGI_BASE_URL}{endpoint}"

    try:
        response = requests.request(
            method=method,
            url=url,
            headers=get_karmayogi_headers(),
            params=params,
            json=json_data,
            timeout=timeout,
        )

        response.raise_for_status()

        if not response.content:
            return {}

        return response.json()

    except requests.RequestException as error:
        print(
            f"⚠️ Karmayogi API request failed: {error}"
        )
        return None

    except ValueError as error:
        print(
            f"⚠️ Karmayogi API returned invalid JSON: {error}"
        )
        return None


# ============================================================
# Real iGoT Course Catalogue
# ============================================================

def get_real_igot_courses():
    """
    Attempt to retrieve course/enrolment information
    from the real Karmayogi platform.

    NOTE:
    The exact catalogue endpoint may require additional
    government-side authentication/contract configuration.
    """

    # This is intentionally kept separate from the
    # existing demo catalogue until the official API
    # contract/credentials are available.

    if not is_real_igot_configured():
        return None

    # Placeholder for the officially provided course
    # catalogue endpoint.

    return None


# ============================================================
# Public Course Function
# ============================================================

def get_igot_courses():
    """
    Return iGoT courses.

    Priority:
        1. Real iGoT API
        2. Local demo catalogue fallback
    """

    real_courses = get_real_igot_courses()

    if real_courses is not None:
        return real_courses

    return COURSE_CATALOG


# ============================================================
# Personalized iGoT Recommendations
# ============================================================

def recommend_igot_courses(skill_gaps):
    """
    Match detected skill gaps with relevant iGoT courses.

    Uses the currently available iGoT catalogue.
    """

    recommendations = []

    if not skill_gaps:
        return recommendations

    courses = get_igot_courses()

    if not courses:
        return recommendations

    for gap in skill_gaps:

        # ----------------------------------------------------
        # Handle string gap
        # ----------------------------------------------------

        if isinstance(gap, str):

            skill_name = gap
            gap_level = "Needs Practice"

        # ----------------------------------------------------
        # Handle dictionary gap
        # ----------------------------------------------------

        elif isinstance(gap, dict):

            skill_name = (
                gap.get("skill")
                or gap.get("topic")
                or gap.get("name")
                or ""
            )

            gap_level = (
                gap.get("level")
                or gap.get("gap_level")
                or "Needs Practice"
            )

        else:
            continue

        if not skill_name:
            continue

        skill_name_lower = (
            skill_name.strip().lower()
        )

        for course in courses:

            course_skill = str(
                course.get("skill", "")
            ).strip().lower()

            if course_skill == skill_name_lower:

                recommendation = {
                    **course,
                    "skill_gap": gap_level,
                    "reason": (
                        f"This course is recommended because "
                        f"{skill_name} was identified as an area "
                        f"requiring additional learning."
                    ),
                }

                recommendations.append(
                    recommendation
                )

    return recommendations