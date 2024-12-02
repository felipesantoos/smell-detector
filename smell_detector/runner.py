import read_file
import os
from utils import title, start_test, finish_test
from untitled_feature import find_untitled_features
from duplicate_scenario_title import find_duplicate_scenario_titles
from duplicate_feature_title import find_duplicate_feature_titles
from duplicate_test_case import find_duplicate_test_cases
from absence_background import find_absence_background
from vicious_tag import find_vicious_tags
from duplicate_step import find_duplicate_steps
from starting_with_the_left_foot import find_starting_with_the_left_foot
from malformed_test import find_malformed_test

feature_files_dir = "../"

def execute_project(project):
    # Catch all features in a specific project
    path = f"{feature_files_dir}{project}/"
    project_features = os.listdir(path)

    # filenames structuration and contents construction
    filenames = []
    for feature in project_features:
        filenames.append(f"{path}{feature}")
    contents = read_file.read_files(filenames)

    # Untitled Feature
    title("Untitled Feature", "blue")
    start_test()
    find_untitled_features([str(filename).removeprefix(feature_files_dir) for filename in filenames], contents, "reports/untitled_feature.csv")
    finish_test()

    # Duplicate Feature Title
    title("Duplicate Feature Title", "blue")
    start_test()
    find_duplicate_feature_titles([str(filename).removeprefix(feature_files_dir) for filename in filenames], contents, "reports/duplicate_feature_title.csv")
    finish_test()

    # Duplicate Scenario Title
    title("Duplicate Title Scenario", "blue")
    start_test()
    find_duplicate_scenario_titles([str(filename).removeprefix(feature_files_dir) for filename in filenames], contents, "reports/duplicate_scenario_title.csv")
    finish_test()

    # Duplicate Scenario
    title("Duplicate Scenario", "blue")
    start_test()
    find_duplicate_test_cases([str(filename).removeprefix(feature_files_dir) for filename in filenames], contents, "reports/duplicate_test_case.csv")
    finish_test()

    # Absence of Background
    title("Absence of Background", "blue")
    start_test()
    find_absence_background([str(filename).removeprefix(feature_files_dir) for filename in filenames], contents, "reports/absence_background.csv")
    finish_test()

    # Vicious Tag
    title("Vicious Tag", "blue")
    start_test()
    find_vicious_tags([str(filename).removeprefix(feature_files_dir) for filename in filenames], contents, "reports/vicious_tag.csv")
    finish_test()

    # Duplicate Step
    title("Duplicate Step", "blue")
    start_test()
    find_duplicate_steps([str(filename).removeprefix(feature_files_dir) for filename in filenames], contents, "reports/duplicate_step.csv")
    finish_test()

    # Starting With The Left Foot
    title("Starting With The Left Foot", "blue")
    start_test()
    find_starting_with_the_left_foot([str(filename).removeprefix(feature_files_dir) for filename in filenames], contents, "reports/starting_with_the_left_foot.csv")
    finish_test()

    # Malformed Test
    title("Malformed Test", "blue")
    start_test()
    find_malformed_test([str(filename).removeprefix(feature_files_dir) for filename in filenames], contents, "reports/malformed_test.csv")
    finish_test()

def execute_projects(projects):
    for project in projects:
        execute_project(project)
