import re


KEYWORDS = {
    "termination": ["termination", "terminate", "expired"],
    "indemnity": ["indemnify", "indemnification", "indemnity"],
    "liability": ["liability", "limitation of liability", "damages"],
    "non_compete": ["non-compete", "non compete", "restrict competition"]
}


def split_into_sections(text: str):
    # Split by numbered headings like 1., 2., 3.
    sections = re.split(r"\n\s*\d+\.\s+", text)
    return sections


def find_relevant_sections(text: str):
    sections = split_into_sections(text)

    relevant_chunks = []

    for section in sections:
        section_lower = section.lower()

        for keyword_list in KEYWORDS.values():
            if any(keyword in section_lower for keyword in keyword_list):
                relevant_chunks.append(section)
                break

    # Join relevant sections into a single context
    return "\n\n".join(relevant_chunks)