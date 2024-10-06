import re
import csv
import os
from tabulate import tabulate

def find_duplicate_scenario_titles(feature_filenames, feature_files, csv_filename=None):
    """
    Finds duplicate scenario titles in a list of feature files. A duplicate title scenario is defined 
    as a scenario that appears more than once.
    
    Args:
    - feature_files (list of str): The content of the feature files.
    - feature_filenames (list of str): The names of the feature files.
    - csv_filename (str, optional): Name of the CSV file to save the report.
    
    Returns:
    - None
    """
    all_report_data = []
    total_scenarios = 0
    total_distinct_scenarios = 0
    total_occurrences = 0

    for index, (filename, feature_file) in enumerate(zip(feature_filenames, feature_files)):
        # Find all scenarios in the current feature file
        pattern = r"Scenario:.*"
        matches = re.findall(pattern, feature_file)

        total_scenarios += len(matches)
        distinct_values = list(set(matches))
        total_distinct_scenarios += len(distinct_values)
        number_of_occurrences_of_this_smell_in_this_file = 0

        # Prepare data for tabulation
        report_data = []
        for value in distinct_values:
            number_of_times_the_value_appeared = matches.count(value)
            if number_of_times_the_value_appeared > 1:
                # Get indexes of the value in the matches
                scenario_indexes = [i + 1 for i, match in enumerate(matches) if match == value]
                scenario_lines = [i + 1 for i, line in enumerate(feature_file.splitlines()) if value in line]
                report_data.append([filename, value, number_of_times_the_value_appeared, scenario_indexes, scenario_lines])
                number_of_occurrences_of_this_smell_in_this_file += 1

        # Sort the report data by scenario name
        report_data.sort(key=lambda x: x[1])  # Sort by scenario name

        # Store the report data for the current feature file
        if report_data:
            all_report_data.extend(report_data)

        total_occurrences += number_of_occurrences_of_this_smell_in_this_file

    # Print overall report
    print(f"- Total number of scenarios across all files: {total_scenarios}")
    print(f"- Total number of distinct scenarios across all files: {total_distinct_scenarios}")
    print("- Scenarios that appeared more than once:")
    
    if all_report_data:
        indexed_report_data = [[item[0], item[1], item[2], ', '.join(map(str, item[3])), ', '.join(map(str, item[4]))] for item in all_report_data]
        print(tabulate(indexed_report_data, headers=["Feature File", "Scenario", "Count", "Indexes", "Lines"], tablefmt="pretty"))
        
        # Generate CSV if filename is provided
        if csv_filename:
            file_exists = os.path.isfile(csv_filename)  # Check if file already exists
            with open(csv_filename, mode='a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                if not file_exists:  # Write header only if the file is new
                    csv_writer.writerow(["Feature File", "Scenario", "Count", "Indexes", "Lines"])  # Write header
                csv_writer.writerows(indexed_report_data)  # Write data
            print(f"Report saved to {csv_filename}.")
    else:
        print("No scenarios appeared more than once.")

    print(f"- Total number of occurrences of this smell across all files: {total_occurrences}")

# Example usage
feature_files_example = [
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
    """
]

feature_filenames_example = [
    "file1.feature",
    "file2.feature",
    "file3.feature",
    "file4.feature"
]

find_duplicate_scenario_titles(feature_filenames_example, feature_files_example, "reports/duplicate_scenario_title.csv")
