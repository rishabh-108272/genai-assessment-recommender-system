
TEST_TYPE_GROUPS = {
    "Technical": {
        "Ability", "Automata", "Coding", "Skill", 
        "Knowledge", "Simulation", "Language"
    },
    "Behavioral": {
        "Personality", "Behavioral", "Competency", 
        "SJT", "Motivation", "Video Interview"
    }
}

JOB_TO_ASSESSMENT_DOMAIN = {
    "Sales": ["Behavioral", "Technical"],
    "Marketing": ["Behavioral", "Technical"],
    "Leadership": ["Behavioral"],
    "Management": ["Behavioral"],
    "HR": ["Behavioral"],
    "Finance": ["Technical", "Behavioral"],
    "Engineering": ["Technical"],
    "Tech": ["Technical"],
    "Technical": ["Technical"],
    "Behavioral": ["Behavioral"],
    "Culture": ["Behavioral"]
}

def belongs_to_domain(assessment, domain):
    """Checks if an assessment's test types match the required domain."""
    # Ensure we are looking at the 'test_type' list from your Pinecone metadata
    test_types = set(assessment.get("test_type", []))
    group = TEST_TYPE_GROUPS.get(domain, set())
    return len(test_types & group) > 0

def normalize_domains(domains: list) -> list:
    normalized = set()
    for d in domains:
        if d in JOB_TO_ASSESSMENT_DOMAIN:
            normalized.update(JOB_TO_ASSESSMENT_DOMAIN[d])
        elif d in ("Technical", "Behavioral"):
            normalized.add(d)
    return list(normalized) if normalized else ["Technical"]