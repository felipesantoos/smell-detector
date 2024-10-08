import read_file
import os
from utils import title, start_test, finish_test, feature_glossary
from untitled_feature import find_untitled_features
from duplicate_scenario_title import find_duplicate_scenario_titles
from duplicate_feature_title import find_duplicate_feature_titles
from duplicate_scenario import find_duplicate_scenarios
from stuttering_step import find_stuttering_steps
from keyword_duplication import find_keyword_duplication

feature_files_dir = "../"

def execute_project(project):
    # Catch all features in a specific project
    path = f"{feature_files_dir}{project}/"
    project_features = os.listdir(path)

    # Feature glossary
    feature_glossary(project, project_features)

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
    find_duplicate_scenarios([str(filename).removeprefix(feature_files_dir) for filename in filenames], contents, "reports/duplicate_scenario.csv")
    finish_test()

    # Stuttering Step
    title("Stuttering Step", "blue")
    start_test()
    find_stuttering_steps(contents)
    finish_test()

    # Keyword Duplication
    title("Keyword Duplication", "blue")
    start_test()
    find_keyword_duplication(contents)
    finish_test()

def execute_projects(projects):
    for project in projects:
        execute_project(project)
