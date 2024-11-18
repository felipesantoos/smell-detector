import csv
import os
import re
from tabulate import tabulate

def find_absence_background(feature_filenames, feature_files, csv_filename=None):
    """
    Finds all the absence of background in the feature file.

    Args:
    - feature_filenames (list of str): The names of the feature files.
    - feature_files (list of str): The content of the feature files.
    - csv_filename (str, optional): Name of the CSV file to save the report.

    Returns:
    - None
    """
    scenario_pattern = r"(Scenario:[\s\S]*?)(?=\n(?:\n\s*)*[@#]|Scenario:|Scenario Outline:|Example:|$)"
    scenario_outline_pattern = r"(Scenario Outline:[\s\S]*?)(?=\n(?:\n\s*)*[@#]|Scenario:|Scenario Outline:|Example:|$)"
    example_pattern = r"(Example:[\s\S]*?)(?=\n(?:\n\s*)*[@#]|Scenario:|Scenario Outline:|Example:|$)"
    step_pattern = r"(Given[\s\S]*?)(?=Given|When|Then|Scenario:|Scenario Outline:|Example:|Examples:|$)"
    partition_pattern = r"(?:Given\s|And\s|But\s)"

    absences_backgrounds = []
    total_absence_backgrounds = 0
    total_scenarios = 0

    for feature_index, (filename, feature_file) in enumerate(zip(feature_filenames, feature_files)):
        # Find scenarios into feature
        scenarios = re.findall(scenario_pattern, feature_file)
        scenarios_outline = re.findall(scenario_outline_pattern, feature_file)
        examples = re.findall(example_pattern, feature_file)

        scenarios = [s.strip() for s in scenarios if s.strip()]
        scenarios_outline = [so.strip() for so in scenarios_outline if so.strip()]
        examples = [e.strip() for e in examples if e.strip()]

        # Calculating all feature scenarios
        total_scenarios_feature = scenarios + scenarios_outline + examples
        total_scenarios = len(scenarios) + len(scenarios_outline) + len(examples)

        total_absence_backgrounds = absence_analysis(filename, total_scenarios_feature, step_pattern, partition_pattern,
                                                     absences_backgrounds, total_scenarios, total_absence_backgrounds)

    if absences_backgrounds:
        # Transforming absences_backgrounds into a string
        for register in absences_backgrounds:
            register["absence_background"] = '\n'.join(register["absence_background"])

        report_data = [
            [absence_background["filename"], absence_background["absence_background"], absence_background["scenarios"]]
            for absence_background in absences_backgrounds
        ]

        print(f"- Total number of absence backgrounds: {total_absence_backgrounds}")
        print(tabulate(report_data, headers=["Filename", "Absence Background", "Scenarios"], tablefmt="grid"))

        # Generate CSV if filename is provided
        if csv_filename:
            report_dir = './reports'
            if not os.path.exists(report_dir):
                os.mkdir(report_dir)

            file_exists = os.path.isfile(csv_filename)  # Check if file already exists
            with open(csv_filename, mode='a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile, delimiter=';')
                if not file_exists:  # Write header only if the file is new
                    csv_writer.writerow(["Filename", "Absence Background", "Scenarios"])  # Write header
                csv_writer.writerows(report_data)  # Write data
            print(f"Report saved to {csv_filename}.")
    else:
        print("No registers with absence of background.")


def absence_analysis(filename, registers, step_pattern, partition_pattern, absences_backgrounds, total_scenarios, total_absence_backgrounds):
    steps_scenarios_feature = []

    for register_index, register in enumerate(registers):
        registers[register_index] = re.sub("\n\n", "\n", register)

    for register_index, register in enumerate(registers):
        register = register.strip()
        untreated_steps_scenarios = re.findall(step_pattern, register)

        for untreated_steps_scenario in untreated_steps_scenarios:
            untreated_steps_scenario = untreated_steps_scenario.strip()
            steps_scenario = [step.strip() for step in re.split(partition_pattern, untreated_steps_scenario) if step.strip()]

            steps_scenarios_feature.append(steps_scenario)

    absence_counts = absence_counter(steps_scenarios_feature)

    total_absence_backgrounds = absence_structure(filename, absence_counts, absences_backgrounds,
                                                  total_scenarios, total_absence_backgrounds)
    return total_absence_backgrounds


def absence_counter(steps_scenarios_feature):
    # Using the biggest scenario to increment
    biggest_scenario = max(steps_scenarios_feature, key=len, default=[])

    # Going through the list by largest size and reducing loops
    step_counts = {}
    for size in range(len(biggest_scenario), 0, -1):
        # Counting occurrences
        step_counts.clear()
        for steps_scenario in steps_scenarios_feature:
            key = tuple(steps_scenario[:size])
            if key in step_counts:
                step_counts[key] += 1
            else:
                step_counts[key] = 1

        # Checking if step_counts meets criteria
        if max(step_counts.values(), default=0) >= len(steps_scenarios_feature):
            return step_counts

    return step_counts


def absence_structure(filename, absence_counts, absences_backgrounds, total_scenarios, total_absence_backgrounds):
    absence_background = []
    for step, count in absence_counts.items():
        if count >= total_scenarios > 1:
            formatted_step = "\n ".join(line.strip() for line in step)
            absence_background.append(f"'{formatted_step}' appears {count} times")
            total_absence_backgrounds += count

    if absence_background:
        absences_backgrounds.append({
            "filename": filename,
            "absence_background": absence_background,
            "scenarios": total_scenarios
        })
    return total_absence_backgrounds


# Example usage
feature_files_example = [
    """
    Feature: Example feature 1
        
        Scenario: First scenario
            Given step 1
            And step 2
            \"\"\"
            test
            \"\"\"
            When step 3
            And step 4
            Then step 5
            And step 6
            
        Scenario: Second scenario
            Given step 1
            And step 2
            \"\"\"
            test
            \"\"\"
            When step 3
            Then step 4
            
        Scenario: Third scenario
            Given step 1
            When step 2
            Then step 3
            
        Scenario: Fourth scenario
            Given step 1
            When step 2
            Then step 3
    """,
    """
Feature: Example feature 2

    Scenario: First scenario
        Given step 1
        But step 2
        When step 3
        And step 4
        Then step 5
        And step 6
        
    Scenario: Second scenario
        Given step 1
        And step 2
        When step 3
        Then step 4
    """,
]

filenames_example = [
    "file1.feature",
    "file2.feature"
]

# find_absence_background(filenames_example, feature_files_example)
