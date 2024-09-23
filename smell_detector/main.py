import runner
from utils import title
from tabulate import tabulate

projects = [
    "inukshuk_jekyll-scholar",
    "keygen-sh_keygen-api",
    "opencypher_openCypher",
    "scality_Zenko",
    "sdkman_sdkman-cli",
    "serverlessworkflow_specification",
    "thoughtbot_factory_bot_rails",
    "RUN ALL PROJECTS",
    "EXIT"
]

title("Select Project", "white")
if projects:
    options = [
        [i + 1, item]
        for i, item in enumerate(projects)
    ]
    print(tabulate(options, headers=["Project Index", "Description"], tablefmt="pretty"))
else:
    print("No content available")

try:
    choice = int(input("Choice: "))
    choice -= 1

    if -1 < choice < 7:
        runner.execute_project(projects[choice])
    elif choice == 7:
        runner.execute_projects(projects[:-2])
    elif choice == 8:
        print("goodbye...")
    else:
        print("choice doesn't exist")
except Exception as e:
    print("ERROR: ", e)