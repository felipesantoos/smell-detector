import csv
import os
import re
from tabulate import tabulate

def find_vicious_tags(feature_filenames, feature_files, csv_filename=None):
    """
    Finds all the vicious tags in the feature file.

    Args:
    - feature_filenames (list of str): The names of the feature files.
    - feature_files (list of str): The content of the feature files.
    - csv_filename (str, optional): Name of the CSV file to save the report.

    Returns:
    - None
    """
    rule_tag_pattern = r"((?:@\w+\s*)+)(?=\s*Rule:)"
    scenario_tag_pattern = r"((?:@\w+\s*)+)(?=\s*Scenario:)"
    scenario_outline_tag_pattern = r"((?:@\w+\s*)+)(?=\s*Scenario Outline:)"
    example_tag_pattern = r"((?:@\w+\s*)+)(?=\s*Example:)"
    # TODO: Implement for examples in the same Scenario Outline

    vicious_tags = []
    total_vicious_tags = 0
    total_scenarios = 0

    for feature_index, (filename, feature_file) in enumerate(zip(feature_filenames, feature_files)):
        # Find tags into feature
        rules = re.findall(rule_tag_pattern, feature_file)
        scenarios = re.findall(scenario_tag_pattern, feature_file)
        scenarios_outline = re.findall(scenario_outline_tag_pattern, feature_file)
        examples = re.findall(example_tag_pattern, feature_file)

        rules = [t.strip() for t in rules if t.strip()]
        scenarios = [t.strip() for t in scenarios if t.strip()]
        scenarios_outline = [t.strip() for t in scenarios_outline if t.strip()]
        examples = [t.strip() for t in examples if t.strip()]

        # Calculating all scenarios into feature
        total_scenarios = len(scenarios) + len(scenarios_outline) + len(examples)

        total_vicious_tags = vicious_analysis(filename, rules, vicious_tags, len(rules), total_vicious_tags, 'Rule')
        total_vicious_tags = vicious_analysis(filename, scenarios, vicious_tags, total_scenarios, total_vicious_tags, 'Scenario')
        total_vicious_tags = vicious_analysis(filename, scenarios_outline, vicious_tags, total_scenarios, total_vicious_tags, 'Scenario')
        total_vicious_tags = vicious_analysis(filename, examples, vicious_tags, total_scenarios, total_vicious_tags, 'Scenario')

    if vicious_tags:
        # Transforming vicious_tags into a string
        for register in vicious_tags:
            register["vicious_tag"] = '\n'.join(register["vicious_tag"])

        report_data = [
            [vicious_tag["filename"], vicious_tag["vicious_tag"], vicious_tag["scenarios"], vicious_tag["type"]]
            for vicious_tag in vicious_tags
        ]

        print(f"- Total number of vicious tags: {total_vicious_tags}")
        print(tabulate(report_data, headers=["Filename", "Vicious Tag", "Scenarios", "Type"], tablefmt="grid"))

        # Generate CSV if filename is provided
        if csv_filename:
            report_dir = './reports'
            if not os.path.exists(report_dir):
                os.mkdir(report_dir)

            file_exists = os.path.isfile(csv_filename)  # Check if file already exists
            with open(csv_filename, mode='a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile, delimiter=';')
                if not file_exists:  # Write header only if the file is new
                    csv_writer.writerow(["Filename", "Vicious Tags", "Scenarios", "Type"])  # Write header
                csv_writer.writerows(report_data)  # Write data
            print(f"Report saved to {csv_filename}.")
    else:
        print("No registers with vicious tags.")


def vicious_analysis(filename, registers, vicious_tags, total_scenarios, total_vicious_tags, type):
    tags_scenarios_feature = []

    for register_index, register in enumerate(registers):
        register = register.strip()
        tags = re.findall(r'@\w+', register)

        tags_scenarios_feature.append(tags)

    vicious_counts = vicious_counter(tags_scenarios_feature)

    total_vicious_tags = vicious_structure(filename, vicious_counts, tags_scenarios_feature,
                                           vicious_tags, total_scenarios, total_vicious_tags, type)
    return total_vicious_tags


def vicious_counter(tags_scenarios_feature):
    tag_counts = {}
    for tags_scenario in tags_scenarios_feature:
        for tag in tags_scenario:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    return tag_counts


def vicious_structure(filename, vicious_counts, tags_scenarios_feature, vicious_tags, total_scenarios, total_vicious_tags, type):
    vicious_tag = []
    for tag, count in vicious_counts.items():
        if count >= total_scenarios > 1:
            vicious_tag.append(f"'{tag}' appears {count} times")
            total_vicious_tags += count

    if vicious_tag:
        vicious_tags.append({
            "filename": filename,
            "vicious_tag": vicious_tag,
            "scenarios": total_scenarios,
            "type": type
        })
    return total_vicious_tags


# Example usage
feature_files_example = [
    """
    Feature: Example feature 1
    
        @viciousTag0
        Rule: Test Rule
        
        @viciousTag1 @viciousTag2 @viciousTag3
        Scenario: First scenario
            Given step 1 @notTag1 @notTag1
            And step 2
            When step 3
            @notTag2
            And step 4
            Then step 5
            And step 6
            
        @viciousTag4 @viciousTag2
        @viciousTag5 @viciousTag1
        @viciousTag6
        Scenario: Second scenario
            Given step 1
            When step 2
            Then step 3
    """,
    """
    Feature: Example feature 2
    
        @viciousTag1
        Scenario: First scenario
            Given step 1 @notTag1
            And step 2
            When step 3
            @notTag2
            @notTag2
            And step 4
            Then step 5
            And step 6
            
        @viciousTag1 @viciousTag2
        Scenario: Second scenario
            Given step 1
            When step 2
            Then step 3
    """,
]

filenames_example = [
    "file1.feature",
    "file2.feature"
]

#find_vicious_tags(filenames_example, feature_files_example)
