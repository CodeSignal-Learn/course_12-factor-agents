def request_clarification(question: str) -> str:
    """
    Ask the user for clarification or additional information.
    
    Args:
        question (str): The question or prompt to ask the user
        
    Returns:
        str: The user's response
        
    Raises:
        EOFError: If input is not available (non-interactive environment)
    """
    try:
        response = input(f"\n🤔 {question}\n> ")
        return response
    except EOFError:
        raise EOFError("Cannot request clarification in non-interactive environment")

