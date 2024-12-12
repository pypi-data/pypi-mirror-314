def humanize_input(message) -> str:
    """
    Converts a given string into a 'humanized' format by converting it to lowercase 
    and replacing spaces with underscores.

    This function is useful for standardizing input strings, especially when preparing 
    data for use in file names, identifiers, or URLs where spaces are not allowed.

    Parameters:
    message (str): The input string that needs to be transformed.

    Returns:
    str: The transformed string in lowercase with spaces replaced by underscores.

    Examples:
    1. "Meter Per Second Squared" -> "meter_per_second_squared"
    2. "Nautical Mile" -> "nautical_mile"
    """
    return message.lower().replace(" ", "_")
