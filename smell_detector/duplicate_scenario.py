import re
from tabulate import tabulate

def find_duplicate_scenarios(feature_files):
    """
    Finds duplicate scenarios in a list of feature files. A duplicate scenario is defined 
    as a scenario that appears more than once.
    
    Args:
    - feature_files (list of str): The content of the feature files.
    
    Returns:
    - None
    """
    scenario_count = {}
    
    # Process each feature file
    for index, text in enumerate(feature_files):
        # Use re.findall to capture "Scenario:" and the following text
        scenarios = re.findall(r"(Scenario:[\s\S]*?)(?=Scenario:|$)", text)
        scenarios = [s.strip() for s in scenarios if s.strip()]

        # Count occurrences of each scenario
        for scenario in scenarios:
            scenario = scenario.strip()
            scenario_count[scenario] = scenario_count.get(scenario, 0) + 1

    # Prepare data for reporting duplicates
    report_data = []
    for title, count in scenario_count.items():
        if count > 1:
            report_data.append([title, count])

    # Print overall report
    total_scenarios = sum(len(re.findall(r"(Scenario:[\s\S]*?)(?=Scenario:|$)", text)) for text in feature_files)
    print(f"- Total number of scenarios: {total_scenarios}")
    print(f"- Duplicate scenarios:")
    
    if report_data:
        print(tabulate(report_data, headers=["Scenario", "Count"], tablefmt="pretty"))
    else:
        print("No scenarios appeared more than once.")

# Example usage
feature_files_example = [
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
        Scenario: First scenario
            Given step 1
            And step 2
            When step 3
            And step 4
            Then step 5
            And step 6
    """,
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
    """,
]

# find_duplicate_scenarios(feature_files_example)
