import csv
import os
import re
from tabulate import tabulate

def find_malformed_test(feature_filenames, feature_files, csv_filename=None):
    """
    Finds all the malformed tests in the feature file.

    Args:
    - feature_filenames (list of str): The names of the feature files.
    - feature_files (list of str): The content of the feature files.
    - csv_filename (str, optional): Name of the CSV file to save the report.

    Returns:
    - None
    """
    background_pattern = r"(Background:.*)([\s\S]*?)(?=(?:([@#]\S*?)?Scenario:)|(?:([@#]\S*?)?Scenario Outline:)|(?:([@#]\S*?)?Example:)|$)"
    scenario_pattern = r"(Scenario:.*)([\s\S]*?)(?=(?:([@#]\S*?)?Scenario:)|(?:([@#]\S*?)?Scenario Outline:)|(?:([@#]\S*?)?Example:)|$)"
    scenario_outline_pattern = r"(Scenario Outline:.*)([\s\S]*?)(?=(?:([@#]\S*?)?Scenario:)|(?:([@#]\S*?)?Scenario Outline:)|(?:([@#]\S*?)?Example:)|$)"
    example_pattern = r"(Example:.*)([\s\S]*?)(?=(?:([@#]\S*?)?Scenario:)|(?:([@#]\S*?)?Scenario Outline:)|(?:([@#]\S*?)?Example:)|$)"
    step_pattern = r"(Given.*|When.*|Then.*)"

    malformed_registers = []
    total_malformed_tests = 0
    for feature_index, (filename, feature_file) in enumerate(zip(feature_filenames, feature_files)):
        # Find background or scenarios into feature
        backgrounds = [(group.strip(), feature_file[:match.start()].count('\n') + 1)
                       for match in re.finditer(background_pattern, feature_file)
                       for group in match.groups()[1:] if group]
        scenarios = [(group.strip(), feature_file[:match.start()].count('\n') + 1)
                     for match in re.finditer(scenario_pattern, feature_file)
                     for group in match.groups()[1:] if group]
        scenarios_outline = [(group.strip(), feature_file[:match.start()].count('\n') + 1)
                             for match in re.finditer(scenario_outline_pattern, feature_file)
                             for group in match.groups()[1:] if group]
        examples = [(group.strip(), feature_file[:match.start()].count('\n') + 1)
                    for match in re.finditer(example_pattern, feature_file)
                    for group in match.groups()[1:] if group]

        total_registers = scenarios + scenarios_outline + examples

        if len(backgrounds) != 0:
            total_malformed_tests = malformed_analysis_backgrounds(filename, backgrounds, step_pattern, malformed_registers, total_malformed_tests)
        total_malformed_tests = malformed_analysis(filename, total_registers, step_pattern, malformed_registers, total_malformed_tests)

    if malformed_registers:
        # Transforming file_and_line and malformed_tests into a string
        for register in malformed_registers:
            register["file_and_line"] = '\n'.join(register["file_and_line"])
            register["justification"] = '\n'.join(register["justification"])

        report_data = [
            [malformed_register["file_and_line"], malformed_register["justification"], malformed_register["register"]]
            for malformed_register in malformed_registers
        ]

        print(f"- Total number of malformed tests by occurrence: {total_malformed_tests}")
        print(tabulate(report_data, headers=["File and Line Position", "Justification", "Reference"], tablefmt="grid"))

        # Generate CSV if filename is provided
        if csv_filename:
            report_dir = './reports'
            if not os.path.exists(report_dir):
                os.mkdir(report_dir)

            file_exists = os.path.isfile(csv_filename)  # Check if file already exists
            with open(csv_filename, mode='a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile, delimiter=';')
                if not file_exists:  # Write header only if the file is new
                    csv_writer.writerow(["File and Line Position", "Justification", "Reference"])  # Write header
                csv_writer.writerows(report_data)  # Write data
            print(f"Report saved to {csv_filename}.")
    else:
        print("No registers with malformed tests.")


# Verifying into background or scenario if it has some malformed test
def malformed_analysis_backgrounds(filename, registers, step_pattern, malformed_registers, total_malformed_tests):
    original_registers = [register_content for register_content, _ in registers]

    for register_index, (register, register_line) in enumerate(registers):
        registers[register_index] = re.sub("\n\n", "\n", register)
        register = register.strip()
        steps = re.findall(step_pattern, register)

        # Counting malformed test
        keyword_counts = malformed_tests_counter(steps)

        # Organizing the result into a list
        total_malformed_tests = malformed_tests_structure_backgrounds(filename, register_line, keyword_counts, original_registers[register_index],
                                                          malformed_registers, total_malformed_tests)
    return total_malformed_tests


# Verifying into background or scenario if it has some malformed test
def malformed_analysis(filename, registers, step_pattern, malformed_registers, total_malformed_tests):
    original_registers = [register_content for register_content, _ in registers]

    for register_index, (register, register_line) in enumerate(registers):
        registers[register_index] = re.sub("\n\n", "\n", register)
        register = register.strip()
        steps = re.findall(step_pattern, register)

        # Counting malformed test
        keyword_counts = malformed_tests_counter(steps)

        # Organizing the result into a list
        total_malformed_tests = malformed_tests_structure(filename, register_line, keyword_counts, original_registers[register_index],
                                                                  malformed_registers, total_malformed_tests)
    return total_malformed_tests


def malformed_tests_counter(steps):
    keyword_counts = {"Given": 0, "When": 0, "Then": 0}
    for step in steps:
        if step.startswith("Given"):
            keyword_counts["Given"] += 1
        elif step.startswith("When"):
            keyword_counts["When"] += 1
        elif step.startswith("Then"):
            keyword_counts["Then"] += 1
    return keyword_counts


def malformed_tests_structure_backgrounds(filename, register_line, keyword_counts, register, malformed_registers,
                              total_malformed_tests):
    malformed_keywords = []
    file_and_line = []
    for keyword, count in keyword_counts.items():
        if count > 1:
            step_line = 0
            lines = register.split("\n")
            for line_index, line in enumerate(lines):
                if re.search(re.escape(keyword), line):
                    step_line = register_line + line_index + 1
                    break

            file_and_line.append(f"{filename}:{step_line}")
            malformed_keywords.append(f"{keyword} appears {count} times")
            total_malformed_tests += count

    if malformed_keywords:
        malformed_registers.append({
            "file_and_line": file_and_line,
            "justification": malformed_keywords,
            "register": register
        })
    return total_malformed_tests


def malformed_tests_structure(filename, register_line, keyword_counts, register, malformed_registers,
                              total_malformed_tests):
    malformed_keywords = []
    file_and_line = []
    for keyword, count in keyword_counts.items():
        if count > 1:
            step_line = 0
            lines = register.split("\n")
            for line_index, line in enumerate(lines):
                if re.search(re.escape(keyword), line):
                    step_line = register_line + line_index + 1
                    break

            file_and_line.append(f"{filename}:{step_line}")
            malformed_keywords.append(f"{keyword} appears {count} times")
            total_malformed_tests += count

        if count == 0 and keyword != "Given":
            file_and_line.append(f"{filename}:{register_line}")
            malformed_keywords.append(f"{keyword} appears zero times")
            total_malformed_tests += 1

    if malformed_keywords:
        malformed_registers.append({
            "file_and_line": file_and_line,
            "justification": malformed_keywords,
            "register": register
        })
    return total_malformed_tests

# Example usage
feature_files_example = [
    """
    Feature: Example feature 1
        Scenario: First scenario
            Given step 1
            Given step 2
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
            When step 4
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
            Then step 6
    """,
    """
    Feature: Example feature 4
        Scenario: First scenario
            Given step 1
            
        Scenario: Second scenario
            Given step 1
            When step 2
        
        Scenario: Third scenario
    """,
]

filenames_example = [
    "file1.feature",
    "file2.feature",
    "file3.feature",
    "file4.feature"
]

# find_malformed_test(filenames_example, feature_files_example)
