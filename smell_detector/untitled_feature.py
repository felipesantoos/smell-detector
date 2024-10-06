import re
import csv
import os
from tabulate import tabulate

def find_untitled_features(filenames, feature_files, csv_filename=None):
    """
    Finds untitled features in a list of feature files. An untitled feature is defined as a line 
    containing "Feature:" followed by optional whitespace and nothing else until the end of the line.
    
    Args:
    - feature_files (list of str): The content of the feature files.
    - filenames (list of str): The names of the feature files.
    - csv_filename (str, optional): The name of the CSV file to save results.
    
    Returns:
    - None
    """
    pattern = r"Feature:\s*$"  # "Feature:" followed by whitespace, and end of line
    results = []

    for index, (feature_file, filename) in enumerate(zip(feature_files, filenames)):
        for line_number, line in enumerate(feature_file.splitlines(), start=1):
            match = re.search(pattern, line)
            if match:
                results.append((filename, line_number, line.lstrip()))  # Store filename, line number, and matched line
                break

    if results:
        # Print the table
        print(tabulate(results, headers=["Filename", "Line Number", "Matched Line"], tablefmt="grid"))

        # Generate CSV if filename is provided
        if csv_filename:
            file_exists = os.path.isfile(csv_filename)  # Check if file already exists
            with open(csv_filename, mode='a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                if not file_exists:  # Write header only if the file is new
                    csv_writer.writerow(["Filename", "Line Number", "Matched Line"])  # Write header
                csv_writer.writerows(results)  # Write data
            print(f"Results saved to {csv_filename}.")
    else:
        print("No untitled features found.")

# Example usage
def run_example():
    feature_file_names = [
        "file1.feature",
        "file2.feature",
        "file3.feature",
        "file4.feature"
    ]
    feature_file_contents = [
        """
        Feature:
            Scenario: Valid scenario
        """,
        """
        Feature: 
        """,
        """
        Feature: Some title
            Scenario: Another valid scenario
        """,
        """
        Feature:     
        """
    ]

    find_untitled_features(feature_file_names, feature_file_contents, "reports/untitled_feature.csv")

# run_example()
