import os
import argparse

def analyze_directory(directory_path):
    """Analyzes the contents of a directory and provides statistics."""
    if not os.path.exists(directory_path):
        return f"Error: The directory '{directory_path}' does not exist."

    if not os.path.isdir(directory_path):
        return f"Error: The path '{directory_path}' is not a directory."

    stats = []
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isdir(item_path):
            stats.append(f"{item} - directory")
        elif os.path.isfile(item_path):
            size = os.path.getsize(item_path)
            stats.append(f"{item} - {size} B file")
    return stats

def read_from_file(file_path):
    """Reads a list of directory paths from a file."""
    try:
        with open(file_path, 'r') as f:
            directories = [line.strip() for line in f if line.strip()]
    except Exception as e:
        return f"Error: Unable to read from file '{file_path}'. Details: {str(e)}"
    return directories

def write_to_file(file_path, content):
    """Writes content to a file."""
    try:
        with open(file_path, 'w') as f:
            for line in content:
                f.write(line + '\n')
    except Exception as e:
        return f"Error: Unable to write to file '{file_path}'. Details: {str(e)}"
    return f"Results successfully written to '{file_path}'"

def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Analyze the contents of a directory.")
    parser.add_argument(
        "directory",
        type=str,
        nargs="?",
        help="The path to the directory to analyze."
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="The file to write the analysis results to."
    )
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help="The file containing directory paths to analyze."
    )
    return parser.parse_args()

def main():
    args = parse_arguments()

    if args.input:
        directories = read_from_file(args.input)
        if isinstance(directories, str):  # Handle errors
            print(directories)
            return
        results = []
        for directory in directories:
            analysis = analyze_directory(directory)
            if isinstance(analysis, str):  # Handle errors for each directory
                results.append(analysis)
            else:
                results.extend(analysis)
        if args.output:
            result = write_to_file(args.output, results)
            print(result)
        else:
            print("\n".join(results))
    elif args.directory:
        analysis = analyze_directory(args.directory)
        if isinstance(analysis, str):
            print(analysis)
        elif args.output:
            result = write_to_file(args.output, analysis)
            print(result)
        else:
            print("\n".join(analysis))
    else:
        print("Error: Please provide either a directory to analyze or an input file with directories.")

if __name__ == "__main__":
    main()
