import argparse
import json

from .worker import grade_problem


def main():
    parser = argparse.ArgumentParser(description="Run grader locally")
    parser.add_argument("problem", help="Problem ID to grade")
    args = parser.parse_args()
    results = grade_problem(args.problem)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
