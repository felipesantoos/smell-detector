import read_file
import os
from utils import title, start_test, finish_test, feature_glossary
from untitled_feature import find_untitled_features
from envious_title_scenario import find_envious_title_scenarios
from envious_title_feature import find_envious_title_features
from time import sleep

fake_feature_files_dir = "fake_feature_files"
real_feature_files_dir = ".."

def execute_project(project):
    # Catch all features in a specific project
    path = f"{real_feature_files_dir}/{project}""/"
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

    sleep(10)

def execute_projects(projects):
    for project in projects:
        execute_project(project)
