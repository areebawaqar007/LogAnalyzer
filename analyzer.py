import sys
from parser import parse_line
from stats import Stats


def main(file_path):
    stats = Stats()

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                parsed, error = parse_line(line)

                # Always record stats safely
                stats.add(parsed)

    except FileNotFoundError:
        print(f"Error: File not found -> {file_path}")
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected error while processing file: {e}")
        sys.exit(1)

    stats.report()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <logfile>")
        sys.exit(1)

    main(sys.argv[1])