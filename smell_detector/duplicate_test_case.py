import re
import csv
import os
from tabulate import tabulate

def find_duplicate_test_cases(filenames, feature_files, csv_filename=None):
    """
    Finds duplicate test cases in a list of feature files by comparing only the body 
    (excluding the first line) of each test case.

    Args:
    - filenames (list of str): The names of the feature files.
    - feature_files (list of str): The content of the feature files.
    - csv_filename (str, optional): The name of the CSV file to save the report.

    Returns:
    - None
    """
    test_case_count = {}
    
    # Process each feature file
    for index, (filename, text) in enumerate(zip(filenames, feature_files)):
        lines = text.splitlines()
        
        # Use re.findall to capture "Scenario:", "Example:", and "Scenario Outline:"
        test_cases = re.finditer(r"(Scenario:[\s\S]*?|Example:[\s\S]*?|Scenario Outline:[\s\S]*?)(?=Scenario:|Example:|Scenario Outline:|$)", text)
        
        for match in test_cases:
            test_case = match.group(0).strip()
            line_number = text.count('\n', 0, match.start(0)) + 1  # Calculate line number
            
            # Exclude the first line (title) for comparison
            test_case_lines = test_case.splitlines()
            test_case_body = '\n'.join(test_case_lines[1:]).strip()

            if test_case_body not in test_case_count:
                test_case_count[test_case_body] = {'count': 0, 'titles_and_files': []}
            test_case_count[test_case_body]['count'] += 1
            test_case_count[test_case_body]['titles_and_files'].append(f"{filename}:{line_number} - {test_case_lines[0]}")

    # Prepare data for reporting duplicates
    report_data = []
    for test_case_body, data in test_case_count.items():
        if data['count'] > 1:
            report_data.append([data['count'], '\n'.join(data['titles_and_files']), test_case_body])

    # Print overall report
    total_test_cases = sum(len(re.findall(r"(Scenario:[\s\S]*?|Example:[\s\S]*?|Scenario Outline:[\s\S]*?)(?=Scenario:|Example:|Scenario Outline:|$)", text)) for text in feature_files)
    print(f"- Total number of test cases: {total_test_cases}")
    print(f"- Duplicate test cases:")
    
    if report_data:
        print(tabulate(report_data, headers=["Count", "Files And Scenario Titles", "Test Case Body"], tablefmt="grid"))

        # Generate CSV if filename is provided
        if csv_filename:
            report_dir = './reports'
            if not os.path.exists(report_dir):
                os.mkdir(report_dir)
            file_exists = os.path.isfile(csv_filename)  # Check if file already exists
            with open(csv_filename, mode='a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                if not file_exists:  # Write header only if the file is new
                    csv_writer.writerow(["Count", "Files And Scenario Titles", "Test Case Body"])  # Write header
                csv_writer.writerows(report_data)  # Write data
            print(f"Report saved to {csv_filename}.")
    else:
        print("No test cases appeared more than once.")

# Example usage
def run_example():
    feature_files_example = [
        # Scenario:
        """
        Feature: Example feature 1
            Scenario: First scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
                And step 6
            Scenario: First scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
                And step 6
        """,
        """
        Feature: Example feature 2
            Scenario: First scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
                And step 6
            Scenario: Second scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
                And step 6
        """,
        """
        Feature: Example feature 3
            Scenario: First scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
                And step 6
            Scenario: Second scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
                And step 6
            Scenario: First scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
                And step 6
        """,
        """
        Feature: Example feature 4
            Scenario: First scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
                And step 6
            Scenario: First scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
        """,
        # Example:
        """
        Feature: Example feature 1
            Example: First scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
                And step 6
            Example: First scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
                And step 6
        """,
        """
        Feature: Example feature 2
            Example: First scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
                And step 6
            Example: Second scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
                And step 6
        """,
        """
        Feature: Example feature 3
            Example: First scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
                And step 6
            Example: Second scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
                And step 6
            Example: First scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
                And step 6
        """,
        """
        Feature: Example feature 4
            Example: First scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
                And step 6
            Example: First scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
        """,
        # Scenario Outline:
        """
        Feature: Example feature 1
            Scenario Outline: First scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
                And step 6
            Scenario Outline: First scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
                And step 6
        """,
        """
        Feature: Example feature 2
            Scenario Outline: First scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
                And step 6
            Scenario Outline: Second scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
                And step 6
        """,
        """
        Feature: Example feature 3
            Scenario Outline: First scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
                And step 6
            Scenario Outline: Second scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
                And step 6
            Scenario Outline: First scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
                And step 6
        """,
        """
        Feature: Example feature 4
            Scenario Outline: First scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
                And step 6
            Scenario Outline: First scenario
                Given step 1
                And step 2
                When step 3
                And step 4
                Then step 5
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

    # Specify the CSV filename where the report should be saved
    find_duplicate_test_cases(filenames_example, feature_files_example, "reports/duplicate_test_case.csv")

# run_example()
