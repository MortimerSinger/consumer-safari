"""
briefing_schema.py — JSON Schema for Consumer Safari briefing DATA.

The cron MUST validate against this schema before writing to Supabase.
Validation failures abort the write — bad data never reaches the live site.

Run standalone to validate any candidate briefing JSON:
    python3 briefing_schema.py path/to/data.json
"""
import json
import sys
from pathlib import Path

SCHEMA_VERSION = 1

# Reusable sub-schemas
_STORY = {
    "type": "object",
    "required": ["headline", "source", "url"],
    "properties": {
        "headline": {"type": "string", "minLength": 1},
        "source": {"type": "string", "minLength": 1},
        "url": {"type": "string", "minLength": 1, "pattern": "^https?://"},
        "blurb": {"type": "string"},
        "tag": {"type": "string"},
        "feedType": {"type": "string", "enum": ["consumer", "ai"]},
    },
    "additionalProperties": True,
}

_CATEGORY_GROUP = {
    "type": "object",
    "required": ["category", "stories"],
    "properties": {
        "category": {"type": "string", "minLength": 1},
        "stories": {
            "type": "array",
            "items": _STORY,
            "minItems": 0,
        },
    },
    "additionalProperties": False,
}

_KEY_NUMBER = {
    "type": "object",
    "required": ["label", "value", "change"],
    "properties": {
        "label": {"type": "string", "minLength": 1},
        "value": {"type": "string", "minLength": 1},
        "change": {"type": "string", "minLength": 1},  # NEVER empty/null
        "direction": {"type": "string", "enum": ["up", "down", "neutral"]},
    },
    "additionalProperties": True,
}

_PATTERN = {
    "oneOf": [
        {"type": "string", "minLength": 1},
        {
            "type": "object",
            "required": ["title"],
            "properties": {
                "title": {"type": "string", "minLength": 1},
                "detail": {"type": "string"},
            },
            "additionalProperties": True,
        },
    ]
}

BRIEFING_SCHEMA = {
    "$schema": "https://json-schema.org/draft-07/schema#",
    "title": "Consumer Safari Briefing DATA",
    "type": "object",
    "required": ["date", "todayNews", "aiTodayNews", "todayForMe"],
    "properties": {
        "date": {"type": "string", "minLength": 1},
        "greeting": {"type": "string"},

        # Core feeds — MUST be category-grouped, not flat
        "todayNews": {"type": "array", "items": _CATEGORY_GROUP, "minItems": 1},
        "aiTodayNews": {"type": "array", "items": _CATEGORY_GROUP, "minItems": 1},
        "weekNews": {"type": "array", "items": _CATEGORY_GROUP},
        "aiWeekNews": {"type": "array", "items": _CATEGORY_GROUP},
        "monthNews": {"type": "array", "items": _CATEGORY_GROUP},
        "aiMonthNews": {"type": "array", "items": _CATEGORY_GROUP},

        # todayForMe — MUST be an object with summary + keyNumbers + patterns
        "todayForMe": {
            "type": "object",
            "required": ["summary", "keyNumbers", "patterns"],
            "properties": {
                "summary": {"type": "string", "minLength": 1},
                "keyNumbers": {
                    "type": "array",
                    "items": _KEY_NUMBER,
                    "minItems": 1,
                    "maxItems": 6,
                },
                "patterns": {
                    "type": "array",
                    "items": _PATTERN,
                    "minItems": 0,
                },
                "recommendations": {"type": "array"},
            },
            "additionalProperties": True,
        },

        # Long-form
        "deepRead": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["title", "source", "url"],
                "properties": {
                    "title": {"type": "string", "minLength": 1},
                    "source": {"type": "string"},
                    "url": {"type": "string", "pattern": "^https?://"},
                    "readTime": {"type": "string"},
                    "summary": {"type": "string"},
                    "takeaway": {"type": "string"},
                },
                "additionalProperties": True,
            },
        },
        "aiDeepRead": {"type": "array"},

        # Audio
        "toListen": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["title", "url"],
                "properties": {
                    "title": {"type": "string", "minLength": 1},
                    "show": {"type": "string"},
                    "url": {"type": "string", "pattern": "^https?://"},
                    "duration": {"type": "string"},
                    "why": {"type": "string"},
                },
                "additionalProperties": True,
            },
        },
        "aiListen": {"type": "array"},

        # Voices
        "voices": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["author", "url"],
                "properties": {
                    "author": {"type": "string", "minLength": 1},
                    "handle": {"type": "string"},
                    "platform": {"type": "string"},
                    "title": {"type": "string"},
                    "url": {"type": "string", "pattern": "^https?://"},
                    "date": {"type": "string"},
                    "feedType": {"type": "string", "enum": ["consumer", "ai"]},
                },
                "additionalProperties": True,
            },
        },

        # Other tabs
        "dealTracker": {"type": "array"},
        "calendarEvents": {"type": "array"},
        "whitePapers": {"type": "array"},

        # Schema metadata
        "schema_version": {"type": "integer"},
    },
    "additionalProperties": True,  # Be permissive about extra keys
}


def validate(data: dict) -> tuple[bool, list[str]]:
    """Return (is_valid, list_of_errors). Empty errors list when valid.
    Uses jsonschema if available, else hand-rolled validator covering the critical fields."""
    errors = []

    try:
        import jsonschema
        validator = jsonschema.Draft7Validator(BRIEFING_SCHEMA)
        for err in validator.iter_errors(data):
            path = ".".join(str(p) for p in err.absolute_path) or "(root)"
            errors.append(f"{path}: {err.message}")
        return (len(errors) == 0, errors)
    except ImportError:
        pass

    # Hand-rolled fallback: enforce only the bugs we've actually hit
    if not isinstance(data, dict):
        return (False, ["DATA must be an object"])

    if not data.get("date"):
        errors.append("date: required, non-empty string")

    # The two shape bugs from 2026-04-25
    for key in ("todayNews", "aiTodayNews", "weekNews", "aiWeekNews", "monthNews", "aiMonthNews"):
        v = data.get(key)
        if v is None:
            continue
        if not isinstance(v, list):
            errors.append(f"{key}: must be an array")
            continue
        for i, group in enumerate(v):
            if not isinstance(group, dict):
                errors.append(f"{key}[{i}]: each item must be an object")
                continue
            if "category" not in group:
                errors.append(f"{key}[{i}]: missing required field 'category'")
            if "stories" not in group:
                errors.append(f"{key}[{i}]: missing required field 'stories'")
            if "items" in group and "stories" not in group:
                errors.append(f"{key}[{i}]: uses 'items' but renderer expects 'stories' (this was the 2026-04-25 bug)")
            if isinstance(group.get("stories"), list):
                for j, s in enumerate(group["stories"]):
                    if not isinstance(s, dict):
                        errors.append(f"{key}[{i}].stories[{j}]: must be an object")
                        continue
                    if not s.get("headline") and not s.get("title"):
                        errors.append(f"{key}[{i}].stories[{j}]: missing 'headline'")
                    if not s.get("url"):
                        errors.append(f"{key}[{i}].stories[{j}]: missing 'url'")

    # todayForMe shape — was flattened to a list of strings on 2026-04-25
    tfm = data.get("todayForMe")
    if tfm is None:
        errors.append("todayForMe: required")
    elif not isinstance(tfm, dict):
        errors.append("todayForMe: MUST be an object with {summary, keyNumbers, patterns}, not a list (this was the 2026-04-25 bug)")
    else:
        if not tfm.get("summary"):
            errors.append("todayForMe.summary: required, non-empty string")
        kn = tfm.get("keyNumbers")
        if not isinstance(kn, list) or len(kn) == 0:
            errors.append("todayForMe.keyNumbers: required, non-empty array")
        else:
            for i, n in enumerate(kn):
                if not isinstance(n, dict):
                    errors.append(f"todayForMe.keyNumbers[{i}]: must be an object")
                    continue
                if not n.get("change"):
                    errors.append(f"todayForMe.keyNumbers[{i}].change: must be non-empty string (NEVER undefined/null)")
                if not n.get("label"):
                    errors.append(f"todayForMe.keyNumbers[{i}].label: required")
                if not n.get("value"):
                    errors.append(f"todayForMe.keyNumbers[{i}].value: required")
        if "patterns" in tfm and not isinstance(tfm["patterns"], list):
            errors.append("todayForMe.patterns: must be an array")

    return (len(errors) == 0, errors)


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 briefing_schema.py path/to/data.json")
        sys.exit(2)
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"ERROR: {path} not found")
        sys.exit(2)
    data = json.loads(path.read_text())
    ok, errors = validate(data)
    if ok:
        print(f"VALID: {path}")
        sys.exit(0)
    print(f"INVALID: {path}")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)


if __name__ == "__main__":
    main()
