import getpass

def get_secure_input(prompt):
    # Prompt the user for sensitive information (e.g., passwords, API keys) securely
    return getpass.getpass(prompt)
