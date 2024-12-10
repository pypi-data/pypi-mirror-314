import json
import re


def extract_plain_text_from_portable_text(portable_text_str: str) -> str:
    """
    Extract plain text from Sanity Portable Text format.

    Args:
        portable_text_str: JSON string in Portable Text format

    Returns:
        Plain text string with blocks separated by newlines
    """
    try:
        blocks = json.loads(portable_text_str)
        texts = []
        for block in blocks:
            if block.get("_type") == "block":
                block_texts = []
                for child in block.get("children", []):
                    if child.get("_type") == "span":
                        block_texts.append(child.get("text", ""))
                texts.append(" ".join(block_texts))
        return "\n".join(texts)
    except (json.JSONDecodeError, AttributeError, KeyError):
        # If parsing fails, return the original string
        return portable_text_str


def to_snake_case(name: str) -> str:
    """Convert a string to snake case."""
    # Replace any non-alphanumeric characters with underscore
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
    # Convert to lowercase and replace multiple underscores with single
    return re.sub("_+", "_", s2.lower())
