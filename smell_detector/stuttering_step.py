import re
from tabulate import tabulate

def find_stuttering_steps(feature_files):
    """
    Finds all the stuttering steps in the feature file.

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

    stuttering_registers = []
    total_stuttering_steps = 0

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

        total_stuttering_steps = stuttering_analysis(feature_index, backgrounds, step_pattern, stuttering_registers, total_stuttering_steps)
        total_stuttering_steps = stuttering_analysis(feature_index, scenarios, step_pattern, stuttering_registers, total_stuttering_steps)
        total_stuttering_steps = stuttering_analysis(feature_index, scenarios_outline, step_pattern, stuttering_registers, total_stuttering_steps)
        total_stuttering_steps = stuttering_analysis(feature_index, examples, step_pattern, stuttering_registers, total_stuttering_steps)

    if stuttering_registers:
        # Transforming stuttering_steps into a string
        for register in stuttering_registers:
            register["stuttering_steps"] = ', '.join(register["stuttering_steps"])

        report_data = [
            [stuttering_register["feature"], stuttering_register["scenario_type_position"], stuttering_register["stuttering_steps"], stuttering_register["register"]]
            for stuttering_register in stuttering_registers
        ]

        print(f"- Total number of stuttering steps: {total_stuttering_steps}")
        print(tabulate(report_data, headers=["Feature", "Position by Type", "Stuttering Steps", "Reference"], tablefmt="grid"))
    else:
        print("No registers with stuttering steps.")


# Verifying into background or scenario if it has some stuttering step
def stuttering_analysis(feature_index, registers, step_pattern, stuttering_registers, total_stuttering_steps):
    for register_index, register in enumerate(registers):
        register = register.strip()
        steps = re.findall(step_pattern, register)

        # Counting keywords duplication
        keyword_counts = stuttering_steps_counter(steps)

        # Organizing the result into a list
        total_stuttering_steps = stuttering_steps_structure(feature_index, keyword_counts, register, register_index,
                                                            stuttering_registers, total_stuttering_steps)
    return total_stuttering_steps


def stuttering_steps_counter(steps):
    keyword_counts = {"Given": 0, "When": 0, "Then": 0}
    for step in steps:
        if step.startswith("Given"):
            keyword_counts["Given"] += 1
        elif step.startswith("When"):
            keyword_counts["When"] += 1
        elif step.startswith("Then"):
            keyword_counts["Then"] += 1
    return keyword_counts


def stuttering_steps_structure(feature_index, keyword_counts, register, scenario_index, stuttering_registers,
                               total_stuttering_steps):
    stuttering_steps = []
    for keyword, count in keyword_counts.items():
        if count > 1:
            stuttering_steps.append(f"{keyword} appears {count} times")
            total_stuttering_steps += count

    if stuttering_steps:
        stuttering_registers.append({
            "feature": feature_index + 1,
            "scenario_type_position": scenario_index + 1,
            "stuttering_steps": stuttering_steps,
            "register": register
        })
    return total_stuttering_steps

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

# find_stuttering_steps(feature_files_example)
