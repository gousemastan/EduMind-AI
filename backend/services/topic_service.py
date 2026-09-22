import re


# Topic keywords
TOPIC_KEYWORDS = {
    "Artificial Intelligence": [
        "artificial intelligence",
        "intelligent system",
        "intelligent agent",
        "ai",
    ],

    "Machine Learning": [
        "machine learning",
        "supervised learning",
        "unsupervised learning",
        "training data",
        "classification",
        "regression",
    ],

    "Problem Solving": [
        "problem solving",
        "search algorithm",
        "state space",
        "breadth first search",
        "depth first search",
        "heuristic",
    ],

    "Knowledge Representation": [
        "knowledge representation",
        "knowledge base",
        "predicate logic",
        "propositional logic",
        "inference",
    ],

    "Natural Language Processing": [
        "natural language processing",
        "natural language",
        "nlp",
        "language processing",
        "speech recognition",
    ],

    "Computer Vision": [
        "computer vision",
        "image processing",
        "object detection",
        "image recognition",
        "pattern recognition",
    ],
}


def detect_topics(text: str) -> list:
    """
    Detect important learning topics from extracted PDF text.
    """

    text_lower = text.lower()

    detected_topics = []

    for topic, keywords in TOPIC_KEYWORDS.items():

        matches = 0

        for keyword in keywords:
            matches += len(
                re.findall(
                    re.escape(keyword),
                    text_lower
                )
            )

        if matches > 0:
            detected_topics.append({
                "topic": topic,
                "matches": matches
            })

    # Most frequently detected topics first
    detected_topics.sort(
        key=lambda item: item["matches"],
        reverse=True
    )

    return detected_topics