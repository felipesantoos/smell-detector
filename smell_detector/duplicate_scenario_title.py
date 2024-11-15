import re
import csv
import os
from tabulate import tabulate

def find_duplicate_scenario_titles(filenames, feature_files, csv_filename=None):
    """
    Finds duplicate scenario titles in a list of feature files, ignoring prefixes like "Scenario:", "Example:", 
    and "Scenario Outline:" when comparing titles. It also sorts the locations alphabetically.

    Args:
    - filenames (list of str): The names of the feature files.
    - feature_files (list of str): The content of the feature files.
    - csv_filename (str, optional): The name of the CSV file to save the report.

    Returns:
    - None
    """
    title_count = {}

    # Process each feature file
    for filename, text in zip(filenames, feature_files):
        lines = text.splitlines()
        for idx, line in enumerate(lines, start=1):  # Enumerate lines with 1-based index
            # Match Scenario, Example, and Scenario Outline titles
            match = re.match(r"^\s*(Scenario:|Example:|Scenario Outline:)\s*(.+)$", line)
            if match:
                _, title_name = match.groups()  # Extract the title part after the colon
                normalized_title = title_name.strip()  # Normalize by trimming whitespace

                if normalized_title not in title_count:
                    title_count[normalized_title] = {'count': 0, 'locations': []}
                title_count[normalized_title]['count'] += 1
                title_count[normalized_title]['locations'].append(f"{filename}:{idx}")

    # Prepare data for reporting duplicates
    report_data = []
    for title, data in title_count.items():
        if data['count'] > 1:
            # Sort the locations alphabetically
            sorted_locations = sorted(set(data['locations']))
            report_data.append([title, data['count'], '\n'.join(sorted_locations)])

    # Print overall report
    total_titles = sum(
        len(re.findall(r"^\s*(Scenario:|Example:|Scenario Outline:)", text, re.MULTILINE))
        for text in feature_files
    )
    print(f"- Total number of scenario titles: {total_titles}")
    print(f"- Duplicate scenario titles:")

    if report_data:
        print(tabulate(report_data, headers=["Title", "Count", "Files And Line Numbers"], tablefmt="grid"))

        # Generate CSV if filename is provided
        if csv_filename:
            report_dir = os.path.dirname(csv_filename)
            if report_dir and not os.path.exists(report_dir):
                os.makedirs(report_dir)
            with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["Title", "Count", "Files And Line Numbers"])  # Write header
                csv_writer.writerows(report_data)  # Write data
            print(f"Report saved to {csv_filename}.")
    else:
        print("No scenario titles appeared more than once.")

# Example usage
def run_example():
    feature_files_example = [
        # Feature:
        """
        Feature: Example feature 1
            Scenario: First scenario
            Scenario: Second scenario
            Scenario: First scenario
        """,
        """
        Feature: Example feature 2
            Scenario: First scenario
            Scenario: Second scenario
            Scenario: First scenario
            Scenario: Second scenario
            Scenario: First scenario
        """,
        """
        Feature: Example feature 3
            Scenario: First scenario
            Scenario: Third scenario
            Scenario: Second scenario
        """,
        """
        Feature: Example feature 4
            Scenario: Fourth scenario
        """,
        # Example:
        """
        Feature: Example feature 1
            Example: First scenario
            Example: Second scenario
            Example: First scenario
        """,
        """
        Feature: Example feature 2
            Example: First scenario
            Example: Second scenario
            Example: First scenario
            Example: Second scenario
            Example: First scenario
        """,
        """
        Feature: Example feature 3
            Example: First scenario
            Example: Third scenario
            Example: Second scenario
        """,
        """
        Feature: Example feature 4
            Example: Fourth scenario
        """,
        # Scenario Outline:
        """
        Feature: Example feature 1
            Scenario Outline: First scenario
            Scenario Outline: Second scenario
            Scenario Outline: First scenario
        """,
        """
        Feature: Example feature 2
            Scenario Outline: First scenario
            Scenario Outline: Second scenario
            Scenario Outline: First scenario
            Scenario Outline: Second scenario
            Scenario Outline: First scenario
        """,
        """
        Feature: Example feature 3
            Scenario Outline: First scenario
            Scenario Outline: Third scenario
            Scenario Outline: Second scenario
        """,
        """
        Feature: Example feature 4
            Scenario Outline: Fourth scenario
        """
    ]

    filenames_example = [
        "file1.feature",
        "file2.feature",
        "file3.feature",
        "file4.feature",
        "file5.feature",
        "file6.feature",
        "file7.feature",
        "file8.feature",
        "file9.feature",
        "file10.feature",
        "file11.feature",
        "file12.feature"
    ]

    find_duplicate_scenario_titles(filenames_example, feature_files_example, "reports/duplicate_scenario_title.csv")

# run_example()
