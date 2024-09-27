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
    step_pattern = r"(?:Given|When|Then|And|But)\s+(.*)"

    stuttering_steps = []
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

        total_stuttering_steps = stuttering_analysis(feature_index, backgrounds, step_pattern, stuttering_steps, total_stuttering_steps)
        total_stuttering_steps = stuttering_analysis(feature_index, scenarios, step_pattern, stuttering_steps, total_stuttering_steps)
        total_stuttering_steps = stuttering_analysis(feature_index, scenarios_outline, step_pattern, stuttering_steps, total_stuttering_steps)
        total_stuttering_steps = stuttering_analysis(feature_index, examples, step_pattern, stuttering_steps, total_stuttering_steps)

    if stuttering_steps:
        # Transforming stuttering_step into a string
        for register in stuttering_steps:
            register["stuttering_step"] = ', '.join(register["stuttering_step"])

        report_data = [
            [stuttering_step["feature"], stuttering_step["scenario_type_position"], stuttering_step["stuttering_step"], stuttering_step["register"]]
            for stuttering_step in stuttering_steps
        ]

        print(f"- Total number of stuttering steps: {total_stuttering_steps}")
        print(tabulate(report_data, headers=["Feature", "Position by Type", "Stuttering Step", "Reference"], tablefmt="grid"))
    else:
        print("No registers with stuttering steps.")


# Verifying into background or scenario if it has some stuttering step
def stuttering_analysis(feature_index, registers, step_pattern, stuttering_steps, total_stuttering_steps):
    for register_index, register in enumerate(registers):
        register = register.strip()
        steps = re.findall(step_pattern, register)

        # Counting stuttering steps
        stuttering_counts = stuttering_counter(steps)

        # Organizing the result into a list
        total_stuttering_steps = stuttering_steps_structure(feature_index, stuttering_counts, register, register_index,
                                                            stuttering_steps, total_stuttering_steps)
    return total_stuttering_steps


def stuttering_counter(steps):
    step_counts = {}
    for step in steps:
        step = step.strip()
        step_counts[step] = step_counts.get(step, 0) + 1
    return step_counts


def stuttering_steps_structure(feature_index, stuttering_counts, register, scenario_index, stuttering_steps,
                               total_stuttering_steps):
    stuttering_step = []
    for step, count in stuttering_counts.items():
        if count > 1:
            stuttering_step.append(f"'{step}' appears {count} times")
            total_stuttering_steps += count

    if stuttering_step:
        stuttering_steps.append({
            "feature": feature_index + 1,
            "scenario_type_position": scenario_index + 1,
            "stuttering_step": stuttering_step,
            "register": register
        })
    return total_stuttering_steps

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

# find_stuttering_steps(feature_files_example)
