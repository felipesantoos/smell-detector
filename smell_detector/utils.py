import colors

def smell_title(smell_title):
    # Calculate the length of the title and adjust the width
    title_length = len(smell_title)
    total_width = title_length + 2  # 2 spaces on each side and 2 for the vertical bars

    # Create the dashed line
    dashes = '-' * total_width

    # Print the formatted title
    print(f"{colors.BBlue}+{dashes}+{colors.Color_Off}")
    print(f"{colors.BBlue}| {smell_title.upper()} |{colors.Color_Off}")
    print(f"{colors.BBlue}+{dashes}+{colors.Color_Off}")

def start_test():
    print(f"{colors.BGreen}+---------------+{colors.Color_Off}")
    print(f"{colors.BGreen}| STARTING TEST |{colors.Color_Off}")
    print(f"{colors.BGreen}+---------------+{colors.Color_Off}")

def finish_test():
    print(f"{colors.BRed}+----------------+{colors.Color_Off}")
    print(f"{colors.BRed}| FINISHING TEST |{colors.Color_Off}")
    print(f"{colors.BRed}+----------------+{colors.Color_Off}")
