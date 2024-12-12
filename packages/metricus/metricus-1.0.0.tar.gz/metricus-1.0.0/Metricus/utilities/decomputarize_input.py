def decomputarize_input(message) -> str:
    """
    Converts underscores to spaces and adjusts the capitalization of the words.
    
    Args:
    - message: The input string with underscores.
    
    Returns:
    - A formatted string with spaces instead of underscores and adjusted capitalization.
    """
    message_with_spaces = message.replace("_", " ")
    
    return message_with_spaces.title()
