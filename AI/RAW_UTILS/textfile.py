def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_text(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def read_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip("
") for line in f]


def write_lines(path, lines):
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(str(line) + "
")
