def read_file(filename):
    file = open(filename, "r")
    content = file.read()
    file.close()
    return content

def read_files(filenames):
    contents = []
    for filename in filenames:
        contents.append(read_file(filename))
    return contents
