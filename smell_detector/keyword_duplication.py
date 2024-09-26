import re
from tabulate import tabulate

def find_keyword_duplication(feature_files):
    """
    Finds all the keyword duplications in the feature file.

    Args:
    - feature_files (list of str): The content of the feature files.

    Returns:
    - None
    """
    background_pattern = r"(Background:[\s\S]*?)(?=Scenario:|Scenario Outline:|Example:|$)"
    scenario_pattern = r"(Scenario:[\s\S]*?)(?=Scenario:|Scenario Outline:|Example:|$)"
    scenario_outline_pattern = r"(Scenario Outline:[\s\S]*?)(?=Scenario:|Scenario Outline:|Example:|$)"
    example_pattern = r"(Example:[\s\S]*?)(?=Scenario:|Scenario Outline:|Example:|$)"
    step_pattern = r"(Given.*|When.*|Then.*)"

    duplicated_registers = []
    total_duplicated_keywords = 0

    for feature_index, feature_file in enumerate(feature_files):
        # Find background or scenarios into feature
        backgrounds = re.findall(background_pattern, feature_file)
        scenarios = re.findall(scenario_pattern, feature_file)
        scenarios_outline = re.findall(scenario_outline_pattern, feature_file)
        examples = re.findall(example_pattern, feature_file)

        backgrounds = [b.strip() for b in backgrounds if b.strip()]
        scenarios = [s.strip() for s in scenarios if s.strip()]
        scenarios_outline = [so.strip() for so in scenarios_outline if so.strip()]
        examples = [e.strip() for e in examples if e.strip()]

        total_duplicated_keywords = duplicated_analysis(feature_index, backgrounds, step_pattern, duplicated_registers, total_duplicated_keywords)
        total_duplicated_keywords = duplicated_analysis(feature_index, scenarios, step_pattern, duplicated_registers, total_duplicated_keywords)
        total_duplicated_keywords = duplicated_analysis(feature_index, scenarios_outline, step_pattern, duplicated_registers, total_duplicated_keywords)
        total_duplicated_keywords = duplicated_analysis(feature_index, examples, step_pattern, duplicated_registers, total_duplicated_keywords)

    if duplicated_registers:
        # Transforming duplicated_keywords into a string
        for register in duplicated_registers:
            register["duplicated_keywords"] = ', '.join(register["duplicated_keywords"])

        report_data = [
            [duplicated_register["feature"], duplicated_register["scenario_type_position"], duplicated_register["duplicated_keywords"], duplicated_register["register"]]
            for duplicated_register in duplicated_registers
        ]

        print(f"- Total number of duplicated keywords: {total_duplicated_keywords}")
        print(tabulate(report_data, headers=["Feature", "Position by Type", "Duplicated Keyword", "Reference"], tablefmt="grid"))
    else:
        print("No registers with duplicated keywords.")


# Verifying into background or scenario if it has some duplicated keyword
def duplicated_analysis(feature_index, registers, step_pattern, duplicated_registers, total_duplicated_keywords):
    for register_index, register in enumerate(registers):
        register = register.strip()
        steps = re.findall(step_pattern, register)

        # Counting keywords duplication
        keyword_counts = duplicated_keywords_counter(steps)

        # Organizing the result into a list
        total_duplicated_keywords = duplicated_keywords_structure(feature_index, keyword_counts, register, register_index,
                                                            duplicated_registers, total_duplicated_keywords)
    return total_duplicated_keywords


def duplicated_keywords_counter(steps):
    keyword_counts = {"Given": 0, "When": 0, "Then": 0}
    for step in steps:
        if step.startswith("Given"):
            keyword_counts["Given"] += 1
        elif step.startswith("When"):
            keyword_counts["When"] += 1
        elif step.startswith("Then"):
            keyword_counts["Then"] += 1
    return keyword_counts


def duplicated_keywords_structure(feature_index, keyword_counts, register, scenario_index, duplicated_registers,
                               total_duplicated_keywords):
    duplicated_keywords = []
    for keyword, count in keyword_counts.items():
        if count > 1:
            duplicated_keywords.append(f"{keyword} appears {count} times")
            total_duplicated_keywords += count

    if duplicated_keywords:
        duplicated_registers.append({
            "feature": feature_index + 1,
            "scenario_type_position": scenario_index + 1,
            "duplicated_keywords": duplicated_keywords,
            "register": register
        })
    return total_duplicated_keywords

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
]

# find_keyword_duplication(feature_files_example)
