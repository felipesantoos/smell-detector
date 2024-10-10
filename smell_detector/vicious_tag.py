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
    tag_pattern = r"(@\S+)(?=(?:\s*(@\S+|Rule:|Background:|Scenario:|Scenario Outline:|Example:|Examples:)))"
    rule_pattern = r"(Rule:)"
    scenarios_pattern = r"(Scenario:|Scenario Outline:|Example:)"
    # TODO: Implement for examples in the same Scenario Outline
    examples_pattern = r"(Examples:)"

    captured_tag = []

    rules_tags = []
    scenarios_tags = []
    examples_tags = []

    features_scenarios_tags = []
    features_rules_tags = []
    tag_counter = {}
    final_results = []

    for feature_index, (filename, feature_file) in enumerate(zip(feature_filenames, feature_files)):
        # Find tags into feature
        tags = re.findall(tag_pattern, feature_file)

        # Ordered tags into a list
        list_tags(filename, captured_tag, examples_pattern, examples_tags, rule_pattern, rules_tags,
                  scenarios_pattern, scenarios_tags, tags)

        # Feature tags processed
        features_rules_tags.append(rules_tags.copy())
        features_scenarios_tags.append(scenarios_tags.copy())
        rules_tags.clear()
        scenarios_tags.clear()

    # Counting tags in scenarios per feature
    counting_tags(features_rules_tags, final_results, tag_counter)
    counting_tags(features_scenarios_tags, final_results, tag_counter)

    if final_results:
        # Transforming tags into a string
        report_data = [
            [final_result["Filename"], ", ".join(tag for tag in final_result if tag.startswith('@')), final_result["Type"], final_result["Type Counts"]]
            for final_result in final_results
        ]

        # Counting vicious tags
        total_vicious_tags = sum(1 for final_result in final_results for tag in final_result if tag.startswith('@'))

        print(f'- Total number of features with vicious tags: {len(final_results)}')
        print(f'- Total number of vicious tags: {total_vicious_tags}')
        print(tabulate(report_data, headers=["Filename", "Tags", "Type", "Type Counts"], tablefmt="pretty"))

        # Generate CSV if filename is provided
        if csv_filename:
            report_dir = './reports'
            if not os.path.exists(report_dir):
                os.mkdir(report_dir)

            file_exists = os.path.isfile(csv_filename)  # Check if file already exists
            with open(csv_filename, mode='a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile, delimiter=';')
                if not file_exists:  # Write header only if the file is new
                    csv_writer.writerow(["Filename", "Tags", "Type", "Type Counts"])  # Write header
                csv_writer.writerows(report_data)  # Write data
            print(f"Report saved to {csv_filename}.")
    else:
        print("No registers with vicious tags.")


def list_tags(filename, captured_tag, examples_pattern, examples_tags, rule_pattern, rules_tags, scenarios_pattern,
              scenarios_tags, tags):
    for pair_tag_index, pair_tag in enumerate(tags):
        for tag in pair_tag:
            if tag not in captured_tag:
                captured_tag.append(tag)

        # Tags organization
        tags_organization(filename, captured_tag, pair_tag, rule_pattern, rules_tags)
        tags_organization(filename, captured_tag, pair_tag, scenarios_pattern, scenarios_tags)
        tags_organization(filename, captured_tag, pair_tag, examples_pattern, examples_tags)


def tags_organization(filename, captured_tag, pair_tag, pattern, tags):
    if re.search(pattern, pair_tag[1]) is not None:
        captured_tag.append(filename)
        tags.append(captured_tag.copy())
        captured_tag.clear()


def counting_tags(features_keywords_tags, final_results, tag_counter):
    for feature_index, feature_keywords_tags in enumerate(features_keywords_tags):
        # Tag Counting
        for scenario_tag in feature_keywords_tags:
            for tag in scenario_tag[:-2]:
                tag = tag.strip()
                tag_counter[tag] = tag_counter.get(tag, 0) + 1

        # Tag verification
        tag_counter_aux = tag_counter.copy()
        for tag, count in tag_counter_aux.items():
            if count < len(features_keywords_tags):
                tag_counter.pop(tag)

        if tag_counter != {}:
            tag_counter["Filename"] = feature_keywords_tags[feature_index][-1]
            tag_counter["Type"] = feature_keywords_tags[feature_index][-2][:-1]
            tag_counter["Type Counts"] = len(feature_keywords_tags)
            final_results.append(tag_counter.copy())
            tag_counter.clear()

# Example usage
feature_files_example = [
    """
    Feature: Example feature 1
    
        @viciousTag1
        Rule: Some random rule
        
        @viciousTag1 @viciousTag2 @viciousTag3
        Scenario: First scenario
            Given step 1 @notTag1 @notTag1
            And step 2
            And step 2
            When step 3
            @notTag2
            And step 4
            Then step 5
            And step 6
        
        @viciousTag1
        Rule: Another random rule
            
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
