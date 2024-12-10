def validate_location(location):
    # Simple validation for location (e.g., non-empty string)
    return isinstance(location, str) and len(location.strip()) > 0
