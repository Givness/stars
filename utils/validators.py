def is_number(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def to_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None