import re
import csv
import os
from tabulate import tabulate

def find_duplicate_scenarios(filenames, feature_files, csv_filename=None):
    """
    Finds duplicate scenarios in a list of feature files. A duplicate scenario is defined 
    as a scenario that appears more than once.
    
    Args:
    - filenames (list of str): The names of the feature files.
    - feature_files (list of str): The content of the feature files.
    - csv_filename (str, optional): The name of the CSV file to save the report.
    
    Returns:
    - None
    """
    scenario_count = {}
    
    # Process each feature file
    for index, (filename, text) in enumerate(zip(filenames, feature_files)):
        # Use re.findall to capture "Scenario:" and the following text
        scenarios = re.findall(r"(Scenario:[\s\S]*?|Example:[\s\S]*?|Scenario Outline:[\s\S]*?)(?=Scenario:|Example:|Scenario Outline:|$)", text)
        scenarios = [s.strip() for s in scenarios if s.strip()]

        # Count occurrences of each scenario
        for scenario in scenarios:
            scenario = scenario.strip()
            if scenario not in scenario_count:
                scenario_count[scenario] = {'count': 0, 'files': []}
            scenario_count[scenario]['count'] += 1
            if filename not in scenario_count[scenario]['files']:
                scenario_count[scenario]['files'].append(filename)

    # Prepare data for reporting duplicates
    report_data = []
    for scenario, data in scenario_count.items():
        if data['count'] > 1:
            report_data.append([scenario.splitlines()[0], data['count'], ', '.join(data['files'])])

    # Print overall report
    total_scenarios = sum(len(re.findall(r"(Scenario:[\s\S]*?)(?=Scenario:|$)", text)) for text in feature_files)
    print(f"- Total number of scenarios: {total_scenarios}")
    print(f"- Duplicate scenarios:")
    
    if report_data:
        print(tabulate(report_data, headers=["Scenario Title", "Count", "Files"], tablefmt="pretty"))

        # Generate CSV if filename is provided
        if csv_filename:
            report_dir = './reports'
            if not os.path.exists(report_dir):
                os.mkdir(report_dir)
            file_exists = os.path.isfile(csv_filename)  # Check if file already exists
            with open(csv_filename, mode='a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                if not file_exists:  # Write header only if the file is new
                    csv_writer.writerow(["Scenario Title", "Count", "Files"])  # Write header
                csv_writer.writerows(report_data)  # Write data
            print(f"Report saved to {csv_filename}.")
    else:
        print("No scenarios appeared more than once.")

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
    find_duplicate_scenarios(filenames_example, feature_files_example, "reports/duplicate_scenario.csv")

# run_example()
