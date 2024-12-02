import csv
import os
import re
from tabulate import tabulate

def find_starting_with_the_left_foot(feature_filenames, feature_files, csv_filename=None):
    """
    Finds all the starting with the left foot in the feature file.

    Args:
    - feature_filenames (list of str): The names of the feature files.
    - feature_files (list of str): The content of the feature files.
    - csv_filename (str, optional): Name of the CSV file to save the report.

    Returns:
    - None
    """
    scenario_pattern = r"(Scenario:[\s\S]*?)(?=(?:([@#]\S*?)?Scenario:)|(?:([@#]\S*?)?Scenario Outline:)|(?:([@#]\S*?)?Example:)|(?:([@#]\S*?)?Rule:)|$)"
    scenario_outline_pattern = r"(Scenario Outline:[\s\S]*?)(?=(?:([@#]\S*?)?Scenario:)|(?:([@#]\S*?)?Scenario Outline:)|(?:([@#]\S*?)?Example:)|(?:([@#]\S*?)?Rule:)|$)"
    example_pattern = r"(Example:[\s\S]*?)(?=(?:([@#]\S*?)?Scenario:)|(?:([@#]\S*?)?Scenario Outline:)|(?:([@#]\S*?)?Example:)|(?:([@#]\S*?)?Rule:)|$)"
    step_pattern = r"(?:Scenario:|Scenario Outline:|Example:)[\s\S]*?(?:(Given[\s\S]*?|And[\s\S]*?|When[\s\S]*?|Then[\s\S]*?))(?=When|Then|Scenario:|Scenario Outline:|Example:|Examples:|Rule:|$)"
    partition_pattern = r"(Given[\s\S]*?|And[\s\S]*?|But[\s\S]*?|Then[\s\S]*?)(?=Given|And|But|When|Then|Scenario:|Scenario Outline:|Example:|Examples:|Rule:|$)"

    left_foots = []
    total_left_foots = 0
    for feature_index, (filename, feature_file) in enumerate(zip(feature_filenames, feature_files)):
        # Find scenarios into feature
        scenarios = [(group.strip(), feature_file[:match.start()].count('\n') + 1)
                     for match in re.finditer(scenario_pattern, feature_file)
                     for group in match.groups() if group]
        scenarios_outline = [(group.strip(), feature_file[:match.start()].count('\n') + 1)
                             for match in re.finditer(scenario_outline_pattern, feature_file)
                             for group in match.groups() if group]
        examples = [(group.strip(), feature_file[:match.start()].count('\n') + 1)
                    for match in re.finditer(example_pattern, feature_file)
                    for group in match.groups() if group]

        # Calculating all feature scenarios
        total_scenarios_feature = scenarios + scenarios_outline + examples

        total_left_foots = left_foot_analysis(filename, total_scenarios_feature, step_pattern, partition_pattern,
                                                     left_foots, total_left_foots)

    if left_foots:
        report_data = [
            [left_foot["filename"], left_foot["left_foot"]]
            for left_foot in left_foots
        ]

        print(f"- Total number of left foots: {total_left_foots}")
        print(tabulate(report_data, headers=["Filename", "Left Foot"], tablefmt="grid"))

        # Generate CSV if filename is provided
        if csv_filename:
            report_dir = './reports'
            if not os.path.exists(report_dir):
                os.mkdir(report_dir)

            file_exists = os.path.isfile(csv_filename)  # Check if file already exists
            with open(csv_filename, mode='a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile, delimiter=';')
                if not file_exists:  # Write header only if the file is new
                    csv_writer.writerow(["Filename", "Left Foot"])  # Write header
                csv_writer.writerows(report_data)  # Write data
            print(f"Report saved to {csv_filename}.")
    else:
        print("No registers with left foots.")


def left_foot_analysis(filename, registers, step_pattern, partition_pattern, left_foots, total_left_foots):
    untreated_left_foots = []
    for register_index, (register, register_line) in enumerate(registers):
        registers[register_index] = re.sub("\n\n", "\n", register)
        register = register.strip()
        untreated_steps_scenarios = re.findall(step_pattern, register)

        for untreated_steps_scenario in untreated_steps_scenarios:
            untreated_steps_scenario = untreated_steps_scenario.strip()
            steps_scenario = [step.strip() for step in re.split(partition_pattern, untreated_steps_scenario) if step.strip()]

            if not re.match(r"(Given|When)", steps_scenario[0]):
                total_left_foots = left_foot_structure(filename, left_foots, register, register_line, total_left_foots)
                total_left_foots += 1


    return total_left_foots


def left_foot_structure(filename, left_foots, scenario, line, total_left_foots):
    left_foots.append({
        "filename": f"{filename}:{line}",
        "left_foot": scenario
    })
    return total_left_foots


# Example usage
feature_files_example = [
    """
    Feature: Example feature 1
        
        Scenario: First scenario
            And step 1
            And step 1.1
            When step 2
            And step 3
            Then step 4
            And step 5
            
        Scenario: Second scenario
            Given step 1
            And step 2
            \"\"\"
            test
            \"\"\"
            When step 3
            Then step 4
            
        Scenario: Third scenario
            And step 1
            When step 2
            Then step 3
            
        Scenario: Fourth scenario
            Then step 1
    """,
    """
Feature: Example feature 2

    Example: First scenario
        And step 1
        But step 2
        When step 3
        And step 4
        Then step 5
        And step 6
        
    Example: Second scenario
        When step 1
        And step 2
        When step 3
        Then step 4
    """,
]

filenames_example = [
    "file1.feature",
    "file2.feature"
]

# find_starting_with_the_left_foot(filenames_example, feature_files_example)
