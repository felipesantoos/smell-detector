import re
from tabulate import tabulate

def extract_features(feature_files):
    """
    Extracts features from a list of feature files.
    
    Args:
    - feature_files (list of str): The content of the feature files.
    
    Returns:
    - list of str: List of extracted feature titles.
    """
    pattern = r"Feature:.*"
    features = []

    for feature_file in feature_files:
        match = re.search(pattern, feature_file, re.MULTILINE)
        if match:
            features.append(match.group())
    
    return features

def analyze_features(features):
    """
    Analyzes the features to find duplicates and their occurrences.
    
    Args:
    - features (list of str): List of extracted feature titles.
    
    Returns:
    - tuple: Total features, total distinct features, report data.
    """
    total_features = len(features)
    distinct_features = list(set(features))
    total_distinct_features = len(distinct_features)

    report_data = []
    for feature in distinct_features:
        count = features.count(feature)
        if count > 1:
            indexes = [i + 1 for i, f in enumerate(features) if f == feature]
            report_data.append([feature, count, indexes])
    
    report_data.sort(key=lambda x: x[0])  # Sort by feature name

    return total_features, total_distinct_features, report_data

def print_report(total_features, total_distinct_features, report_data):
    """
    Prints the analysis report.
    
    Args:
    - total_features (int): Total number of features.
    - total_distinct_features (int): Total number of distinct features.
    - report_data (list): Data for the report.
    
    Returns:
    - None
    """
    print(f"- Total number of features across all files: {total_features}")
    print(f"- Total number of distinct features across all files: {total_distinct_features}")
    print("- Features that appeared more than once:")
    
    if report_data:
        indexed_report_data = [
            [i + 1, item[0], item[1], ', '.join(map(str, item[2]))] 
            for i, item in enumerate(report_data)
        ]
        print(tabulate(indexed_report_data, headers=["Index", "Feature", "Count", "File Indexes"], tablefmt="pretty"))
    else:
        print("No features appeared more than once.")

def find_envious_title_features(feature_files):
    """
    Main function to find and report envious title features.
    
    Args:
    - feature_files (list of str): The content of the feature files.
    
    Returns:
    - None
    """
    features = extract_features(feature_files)
    total_features, total_distinct_features, report_data = analyze_features(features)
    print_report(total_features, total_distinct_features, report_data)

# Example usage
feature_files_example = [
    """
    Feature: Example feature 1
    """,
    """
    Feature: Example feature 1
    """,
    """
    Feature: Example feature 2
    """,
    """
    Feature: Example feature 1
    """,
    """
    Feature: Example feature 2
    """,
    """
    Feature: Example feature 3
    """
]

# find_envious_title_features(feature_files_example)
