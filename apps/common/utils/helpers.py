from rest_framework.exceptions import ValidationError

def extract_error_message(error):
    """
    Recursively extract the first human-readable error message 
    from the Validation Error.
    """
    if isinstance(error, ValidationError):
        detail = error.detail
    else:
        detail = error

    # Dict: go into the first value
    if isinstance(detail, dict):
        for value in detail.values():
            return extract_error_message(value)

    # List: go into the first item
    if isinstance(detail, list) and detail:
        return extract_error_message(detail[0])

    # ErrorDetail or string
    return str(detail)
