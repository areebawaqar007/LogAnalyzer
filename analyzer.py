import sys
from parser import parse_line
from stats import Stats


def main(file_path):
    stats = Stats()

    with open(file_path, "r", errors="ignore") as f:
        for line in f:
            parsed, error = parse_line(line)

            if error:
                stats.add(None)
            else:
                stats.add(parsed)

    stats.report()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <logfile>")
        sys.exit(1)

    main(sys.argv[1])