import re
import csv
import os
from tabulate import tabulate

def extract_features(filenames, feature_files):
    """
    Extracts features from a list of feature files along with their filenames.
    
    Args:
    - filenames (list of str): The names of the feature files.
    - feature_files (list of str): The content of the feature files.
    
    Returns:
    - list of tuples: List of extracted feature titles with corresponding filenames.
    """
    pattern = r"Feature:.*"
    features = []

    for feature_file, filename in zip(feature_files, filenames):
        match = re.search(pattern, feature_file, re.MULTILINE)
        if match:
            features.append((match.group(), filename))
    
    return features

def analyze_features(features):
    """
    Analyzes the features to find duplicates and their occurrences.
    
    Args:
    - features (list of tuples): List of extracted feature titles with filenames.
    
    Returns:
    - tuple: Total features, total distinct features, report data.
    """
    total_features = len(features)
    distinct_features = {}
    
    for feature, filename in features:
        if feature in distinct_features:
            distinct_features[feature].append(filename)
        else:
            distinct_features[feature] = [filename]

    total_distinct_features = len(distinct_features)

    report_data = []
    for feature, files in distinct_features.items():
        count = len(files)
        if count > 1:
            report_data.append([feature, count, ', '.join(files)])
    
    report_data.sort(key=lambda x: x[0])  # Sort by feature name

    return total_features, total_distinct_features, report_data

def print_report(total_features, total_distinct_features, report_data, csv_filename=None):
    """
    Prints the analysis report and optionally saves it to a CSV file.
    
    Args:
    - total_features (int): Total number of features.
    - total_distinct_features (int): Total number of distinct features.
    - report_data (list): Data for the report.
    - csv_filename (str, optional): Name of the CSV file to save the report.
    
    Returns:
    - None
    """
    print(f"- Total number of features across all files: {total_features}")
    print(f"- Total number of distinct features across all files: {total_distinct_features}")
    print("- Features that appeared more than once:")
    
    if report_data:
        indexed_report_data = [
            [item[0], item[1], item[2]] 
            for i, item in enumerate(report_data)
        ]
        print(tabulate(indexed_report_data, headers=["Feature", "Count", "Filenames"], tablefmt="pretty"))
        
        # Generate CSV if filename is provided
        report_dir = './reports'
        if not os.path.exists(report_dir):
            os.mkdir(report_dir)

        if csv_filename:
            file_exists = os.path.isfile(csv_filename)  # Check if file already exists
            with open(csv_filename, mode='a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                if not file_exists:  # Write header only if the file is new
                    csv_writer.writerow(["Feature", "Count", "Filenames"])  # Write header
                csv_writer.writerows(indexed_report_data)  # Write data
            print(f"Report saved to {csv_filename}.")
    else:
        print("No features appeared more than once.")

def find_duplicate_feature_titles(feature_files, filenames, csv_filename=None):
    """
    Main function to find and report duplicate feature titles.
    
    Args:
    - feature_files (list of str): The content of the feature files.
    - filenames (list of str): The names of the feature files.
    - csv_filename (str, optional): Name of the CSV file to save the report.
    
    Returns:
    - None
    """
    features = extract_features(feature_files, filenames)
    total_features, total_distinct_features, report_data = analyze_features(features)
    print_report(total_features, total_distinct_features, report_data, csv_filename)

# Example usage
def run_example():
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
    feature_filenames = [
        "file1.feature",
        "file2.feature",
        "file3.feature",
        "file4.feature",
        "file5.feature",
        "file6.feature"
    ]

    find_duplicate_feature_titles(feature_filenames, feature_files_example, "reports/duplicate_feature_title.csv")

# run_example()