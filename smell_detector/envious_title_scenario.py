import re
from tabulate import tabulate

def find_envious_title_scenarios(feature_files):
    """
    Finds envious title scenarios in a list of feature files. An envious title scenario is defined 
    as a scenario that appears more than once.
    
    Args:
    - feature_files (list of str): The content of the feature files.
    
    Returns:
    - None
    """
    all_report_data = []
    total_scenarios = 0
    total_distinct_scenarios = 0
    total_occurrences = 0

    for index, feature_file in enumerate(feature_files):
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
                report_data.append([value, number_of_times_the_value_appeared, scenario_indexes])
                number_of_occurrences_of_this_smell_in_this_file += 1

        # Sort the report data by scenario name
        report_data.sort(key=lambda x: x[0])

        # Store the report data for the current feature file
        if report_data:
            indexed_report_data = [[index + 1, item[0], item[1], ', '.join(map(str, item[2]))] for item in report_data]
            all_report_data.extend(indexed_report_data)

        total_occurrences += number_of_occurrences_of_this_smell_in_this_file

    # Print overall report
    print(f"- Total number of scenarios across all files: {total_scenarios}")
    print(f"- Total number of distinct scenarios across all files: {total_distinct_scenarios}")
    print("- Scenarios that appeared more than once:")
    
    if all_report_data:
        print(tabulate(all_report_data, headers=["File Index", "Scenario", "Count", "Indexes"], tablefmt="pretty"))
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

# find_envious_title_scenarios(feature_files_example)
