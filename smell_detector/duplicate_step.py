import csv
import os
import re
from tabulate import tabulate

def find_duplicate_steps(feature_filenames, feature_files, csv_filename=None):
    """
    Finds all the duplicate steps in the feature file.

    Args:
    - feature_filenames (list of str): The names of the feature files.
    - feature_files (list of str): The content of the feature files.
    - csv_filename (str, optional): Name of the CSV file to save the report.

    Returns:
    - None
    """
    background_pattern = r"(Background:.*)([\s\S]*?)(?=(?:([@#][\s\S]*?)?Scenario:)|(?:([@#][\s\S]*?)?Scenario Outline:)|(?:([@#][\s\S]*?)?Example:)|(?:([@#][\s\S]*?)?Rule:)|$)"
    scenario_pattern = r"(Scenario:.*)([\s\S]*?)(?=(?:([@#][\s\S]*?)?Scenario:)|(?:([@#][\s\S]*?)?Scenario Outline:)|(?:([@#][\s\S]*?)?Example:)|(?:([@#][\s\S]*?)?Rule:)|$)"
    scenario_outline_pattern = r"(Scenario Outline:.*)([\s\S]*?)(?=(?:([@#][\s\S]*?)?Scenario:)|(?:([@#][\s\S]*?)?Scenario Outline:)|(?:([@#][\s\S]*?)?Example:)|(?:([@#][\s\S]*?)?Rule:)|$)"
    example_pattern = r"(Example:.*)([\s\S]*?)(?=(?:([@#][\s\S]*?)?Scenario:)|(?:([@#][\s\S]*?)?Scenario Outline:)|(?:([@#][\s\S]*?)?Example:)|(?:([@#][\s\S]*?)?Rule:)|$)"
    step_pattern = r"(?:Given|When|Then|And|But)([\s\S]*?)(?=Given|When|Then|And|But|Scenario:|Scenario Outline:|Example:|Examples:|Rule:|$)"

    duplicate_steps = []
    total_duplicate_steps = 0

    for feature_index, (filename, feature_file) in enumerate(zip(feature_filenames, feature_files)):
        # Find background or scenarios into feature
        backgrounds = [(match.group().strip(), feature_file[:match.start()].count('\n') + 1)
                       for match in re.finditer(background_pattern, feature_file)]
        scenarios = [(match.group().strip(), feature_file[:match.start()].count('\n') + 1)
                     for match in re.finditer(scenario_pattern, feature_file)]
        scenarios_outline = [(match.group().strip(), feature_file[:match.start()].count('\n') + 1)
                             for match in re.finditer(scenario_outline_pattern, feature_file)]
        examples = [(match.group().strip(), feature_file[:match.start()].count('\n') + 1)
                    for match in re.finditer(example_pattern, feature_file)]

        total_registers = backgrounds + scenarios + scenarios_outline + examples

        total_duplicate_steps = stuttering_analysis(filename, total_registers, step_pattern, duplicate_steps, total_duplicate_steps)

    if duplicate_steps:
        # Transforming file_and_line and duplicate_step into a string
        for register in duplicate_steps:
            register["file_and_line"] = '\n'.join(register["file_and_line"])
            register["duplicate_step"] = '\n'.join(register["duplicate_step"])

        report_data = [
            [duplicate_step["file_and_line"], duplicate_step["duplicate_step"], duplicate_step["register"]]
            for duplicate_step in duplicate_steps
        ]

        print(f"- Total number of duplicate steps: {total_duplicate_steps}")
        print(tabulate(report_data, headers=["File and Line Position", "Duplicate Step", "Reference"], tablefmt="grid"))

        # Generate CSV if filename is provided
        if csv_filename:
            report_dir = './reports'
            if not os.path.exists(report_dir):
                os.mkdir(report_dir)

            file_exists = os.path.isfile(csv_filename)  # Check if file already exists
            with open(csv_filename, mode='a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile, delimiter=';')
                if not file_exists:  # Write header only if the file is new
                    csv_writer.writerow(["File and Line Position", "Duplicate Step", "Reference"])  # Write header
                csv_writer.writerows(report_data)  # Write data
            print(f"Report saved to {csv_filename}.")
    else:
        print("No registers with duplicate steps.")


# Verifying into background or scenario if it has some duplicate step
def stuttering_analysis(filename, registers, step_pattern, duplicate_steps, total_duplicate_steps):
    original_registers = [register_content for register_content, _ in registers]

    for register_index, (register, register_line) in enumerate(registers):
        registers[register_index] = re.sub("\n\n", "\n", register)
        register = register.strip()
        steps = re.findall(step_pattern, register)

        # Counting duplicate steps
        stuttering_counts = stuttering_counter(steps)

        # Organizing the result into a list
        total_duplicate_steps = duplicate_steps_structure(filename, register_line, stuttering_counts, original_registers[register_index],
                                                            duplicate_steps, total_duplicate_steps)
    return total_duplicate_steps


def stuttering_counter(steps):
    step_counts = {}
    for step in steps:
        step = step.strip()
        step_counts[step] = step_counts.get(step, 0) + 1
    return step_counts


def duplicate_steps_structure(filename, register_line, stuttering_counts, register, duplicate_steps,
                               total_duplicate_steps):
    duplicate_step = []
    file_and_line = []
    for step, count in stuttering_counts.items():
        if count > 1:
            step_line = 0
            lines = register.split("\n")
            for line_index, line in enumerate(lines):
                if re.search(re.escape(step), line):
                    step_line = register_line + line_index
                    break

            file_and_line.append(f"{filename}:{step_line}")
            duplicate_step.append(f"'{step}' appears {count} times")
            total_duplicate_steps += count

    if duplicate_step:
        duplicate_steps.append({
            "file_and_line": file_and_line,
            "duplicate_step": duplicate_step,
            "register": register
        })
    return total_duplicate_steps

# Example usage
feature_files_example = [
    """
    Feature: Example feature 1
        Scenario: First scenario
            Given step 1
            And step 2
            And step 2
            When step 3
            And step 4
            Then step 5
            And step 6
            
        Scenario: Second scenario
            Given step 1
            Given step 1
            When step 2
            When step 2
            Then step 3
    """,
    """
    Feature: Example feature 2
        Scenario: First scenario
            Given step 1
            And step 2
            When step 3
            When step 3
            Then step 4
            And step 5
    """,
    """
    Feature: Example feature 3
        Scenario: First scenario
            Given step 1
            And step 2
            When step 3
            And step 4
            Then step 5
            Then step 5
    """,
]

filenames_example = [
    "file1.feature",
    "file2.feature",
    "file3.feature"
]

# find_duplicate_steps(filenames_example, feature_files_example)
