import read_file
from utils import smell_title, start_test, finish_test
from untitled_feature import find_untitled_features
from envious_title_scenario import find_envious_title_scenarios
from envious_title_feature import find_envious_title_features

fake_feature_files_dir = "fake_feature_files"
real_feature_files_dir = ".."

# Untitled Feature
smell_title("Untitled Feature")
start_test()
filenames = [f"{real_feature_files_dir}/thoughtbot_factory_bot_rails/fixture_replacement_config.feature"]
contents = read_file.read_files(filenames)
find_untitled_features(contents)
finish_test()

# Envious Title Feature
smell_title("Envious Title Feature")
start_test()
filenames = [
    f"{real_feature_files_dir}/inukshuk_jekyll-scholar/citation.feature",
    f"{real_feature_files_dir}/inukshuk_jekyll-scholar/cite_details.feature"
]
contents = read_file.read_files(filenames)
find_envious_title_features(contents)
finish_test()

# Envious Title Scenario
smell_title("Envious Title Scenario")
start_test()
filenames = [f"{real_feature_files_dir}/inukshuk_jekyll-scholar/filter.feature"]
contents = read_file.read_files(filenames)
find_envious_title_scenarios(contents)
finish_test()
