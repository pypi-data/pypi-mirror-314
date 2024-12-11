import argparse
import re
from pathlib import Path
from shutil import which
from typing import Generator

from haystack.find_plus_context import find_plus_context
from haystack.types import SearchResult

assert which(
    "rg"
), "ripgrep (rg) is required to run this script. Please install it and ensure it is in your PATH."


def parse_args():
    parser = argparse.ArgumentParser(
        description="Refined Search Tool with ripgrep and fzf"
    )
    parser.add_argument("directory", nargs="?", help="Directory to search")
    parser.add_argument("--term1", help="First search term")
    parser.add_argument("--term2", help="Second search term")
    parser.add_argument(
        "--lines",
        type=int,
        default=20,
        help="Number of context lines to show (default: 20)",
    )
    return parser.parse_args()


def double_search(
    q1: str, q2: str, start_dir: Path = Path.cwd(), context_lines: int = 20
) -> Generator[SearchResult, None, None]:
    if not q1:
        print("Error: First search term (--term1) is required.")
        return None

    second_regex = re.compile(q2)
    for result in find_plus_context(q1, start_dir, context_lines=context_lines):
        # print(result)
        if q2:
            term_in_at_least_one_line = any(
                second_regex.search(line) for line in result.lines
            )
            if term_in_at_least_one_line:
                yield result
        else:
            yield result

    for result in find_plus_context(q2, start_dir, context_lines=context_lines):
        # print(result)
        if q1:
            term_in_at_least_one_line = any(line for line in result.lines if q1 in line)
            if term_in_at_least_one_line:
                yield result
        else:
            yield result

    return None


def promptYn(msg) -> bool:
    while True:
        response = input(msg).strip().lower()
        if response in ["y", "n"]:
            return response == "y"
        print("Please enter 'y' or 'n'.")
        continue


def main() -> None:
    # Simulate command-line arguments for testing
    args = parse_args()
    directory = args.directory or Path.cwd()
    if not args.term1:
        args.term1 = input("1st Search term: ").strip()
    if not args.term2:
        args.term2 = input("2nd Search term: ").strip()
    for result in double_search(
        args.term1, args.term2, start_dir=directory, context_lines=args.lines
    ):
        print(result)


if __name__ == "__main__":
    main()
