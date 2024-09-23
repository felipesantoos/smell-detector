import re

def find_untitled_features(feature_files):
    """
    Finds untitled features in a list of feature files. An untitled feature is defined as a line 
    containing "Feature:" followed by optional whitespace and nothing else until the end of the line.
    
    Args:
    - feature_files (list of str): The content of the feature files.
    
    Returns:
    - None
    """
    # Regex pattern
    pattern = r"Feature:\s*$"  # "Feature:" followed by whitespace, and end of line

    for index, feature_file in enumerate(feature_files):
        match = re.search(pattern, feature_file, re.MULTILINE)  # Use search since there's only one "Feature:"
        
        # Report results
        if match:
            print(f"File {index + 1}: Untitled feature found.")
        else:
            print(f"File {index + 1}: No untitled feature found.")

# Example usage
feature_files_example = [
    """
    Feature:
    Scenario: Valid scenario
    """,
    """
    Feature: 
    """,
    """
    Feature:     
    """,
    """
    Feature: Some title
    Scenario: Another valid scenario
    """
]

# find_untitled_features(feature_files_example)
