import read_file
import os
from utils import title, start_test, finish_test, feature_glossary
from untitled_feature import find_untitled_features
from envious_title_scenario import find_envious_title_scenarios
from envious_title_feature import find_envious_title_features
from duplicate_scenario import find_duplicate_scenarios
from keyword_duplication import find_keyword_duplication
from time import sleep

feature_files_dir = ".."

def execute_project(project):
    # Catch all features in a specific project
    path = f"{feature_files_dir}/{project}""/"
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
    find_untitled_features(contents)
    finish_test()

    # Envious Title Feature
    title("Envious Title Feature", "blue")
    start_test()
    find_envious_title_features(contents)
    finish_test()

    # Envious Title Scenario
    title("Envious Title Scenario", "blue")
    start_test()
    find_envious_title_scenarios(contents)
    finish_test()

    # Duplicate Scenario
    title("Duplicate Scenario", "blue")
    start_test()
    find_duplicate_scenarios(contents)
    finish_test()

    # Keyword Duplication
    title("Keyword Duplication", "blue")
    start_test()
    find_keyword_duplication(contents)
    finish_test()

    sleep(10)

def execute_projects(projects):
    for project in projects:
        execute_project(project)
