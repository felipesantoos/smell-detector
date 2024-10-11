import colors
from tabulate import tabulate

def title(title, color):
    # Calculate the length of the title and adjust the width
    title_length = len(title)
    total_width = title_length + 2  # 2 spaces on each side and 2 for the vertical bars

    # Create the dashed line
    dashes = '-' * total_width

    # Print the formatted title
    if color == 'black':
        print(f"{colors.BBlack}+{dashes}+{colors.Color_Off}")
        print(f"{colors.BBlack}| {title.upper()} |{colors.Color_Off}")
        print(f"{colors.BBlack}+{dashes}+{colors.Color_Off}")
    if color == 'red':
        print(f"{colors.BRed}+{dashes}+{colors.Color_Off}")
        print(f"{colors.BRed}| {title.upper()} |{colors.Color_Off}")
        print(f"{colors.BRed}+{dashes}+{colors.Color_Off}")
    if color == 'green':
        print(f"{colors.BGreen}+{dashes}+{colors.Color_Off}")
        print(f"{colors.BGreen}| {title.upper()} |{colors.Color_Off}")
        print(f"{colors.BGreen}+{dashes}+{colors.Color_Off}")
    if color == 'yellow':
        print(f"{colors.BYellow}+{dashes}+{colors.Color_Off}")
        print(f"{colors.BYellow}| {title.upper()} |{colors.Color_Off}")
        print(f"{colors.BYellow}+{dashes}+{colors.Color_Off}")
    if color == 'blue':
        print(f"{colors.BBlue}+{dashes}+{colors.Color_Off}")
        print(f"{colors.BBlue}| {title.upper()} |{colors.Color_Off}")
        print(f"{colors.BBlue}+{dashes}+{colors.Color_Off}")
    if color == 'purple':
        print(f"{colors.BPurple}+{dashes}+{colors.Color_Off}")
        print(f"{colors.BPurple}| {title.upper()} |{colors.Color_Off}")
        print(f"{colors.BPurple}+{dashes}+{colors.Color_Off}")
    if color == 'cyan':
        print(f"{colors.BCyan}+{dashes}+{colors.Color_Off}")
        print(f"{colors.BCyan}| {title.upper()} |{colors.Color_Off}")
        print(f"{colors.BCyan}+{dashes}+{colors.Color_Off}")
    if color == 'white':
        print(f"{colors.BWhite}+{dashes}+{colors.Color_Off}")
        print(f"{colors.BWhite}| {title.upper()} |{colors.Color_Off}")
        print(f"{colors.BWhite}+{dashes}+{colors.Color_Off}")

def start_test():
    print(f"{colors.BGreen}+---------------+{colors.Color_Off}")
    print(f"{colors.BGreen}| STARTING TEST |{colors.Color_Off}")
    print(f"{colors.BGreen}+---------------+{colors.Color_Off}")

def finish_test():
    print(f"{colors.BRed}+----------------+{colors.Color_Off}")
    print(f"{colors.BRed}| FINISHING TEST |{colors.Color_Off}")
    print(f"{colors.BRed}+----------------+{colors.Color_Off}")