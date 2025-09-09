import argparse
import time

from rich.console import Console
from rich.table import Table

from src.core.filter import Filter
from src.core.formatter import Formatter
from src.in_out.finder import Finder


def main():
    parser = argparse.ArgumentParser(
        prog="wfreq",
        description="Program for text analyzing",
        epilog="Here you can see some statistics about your texts",
    )


    parser.add_argument("path")
    parser.add_argument("-f", "--frequent")
    parser.add_argument("-r", "--rare")
    parser.add_argument("-minl", "--min_length")
    parser.add_argument("-maxl", "--max_length")
    parser.add_argument("-rf", "--red_flags")
    parser.add_argument("-a", "--artifacts")
    parser.add_argument("-maxr", "--max_repeat")


    args = parser.parse_args()


    def wfreq(path: str, frequent: int, rare: int, min_length: int, max_length: int, red_flags: set, artifacts: bool, max_repeat: int):
        red_flags_copy = red_flags.copy()
        for red_flag in red_flags:
            if words := Finder.find_words_by_local_path(red_flag):
                for word in words:
                    red_flags_copy.add(word)
                red_flags_copy.remove(red_flag)
            else:
                continue
        red_flags = red_flags_copy
        start = time.perf_counter_ns()
        word_list = Finder.find_words_by_local_path(path)
        format = Filter.generate_format(min_length, max_length, artifacts, max_repeat)
        formatted_word_list = Filter.compile_word_list(word_list, red_flags, format)
        result = Formatter.format_word_list(formatted_word_list, frequent, rare)
        end = time.perf_counter_ns()
        print("Time: ", end - start)
        return result


    counts = wfreq(
        path=args.path,
        frequent=int(args.frequent) if isinstance(args.frequent, str) else 10,
        rare=int(args.rare) if isinstance(args.rare, str) else 0,
        min_length=int(args.min_length) if isinstance(args.min_length, str) else 3,
        max_length=int(args.max_length) if isinstance(args.max_length, str) else 70,
        red_flags=set(args.red_flags.split(",")) if args.red_flags else set(),
        artifacts=True if args.artifacts else False,
        max_repeat=int(args.max_repeat) if isinstance(args.max_repeat, str) else 2,
    )


    frequent_table = Table(title="Frequent words", expand=True)
    rare_table = Table(title="Rare words", expand=True)
    frequent_table.add_column("Place")
    frequent_table.add_column("Word")
    frequent_table.add_column("Count")
    rare_table.add_column("Place")
    rare_table.add_column("Word")
    rare_table.add_column("Count")


    console = Console()


    if "frequent" in counts:
        index = 1
        for key, value in counts["frequent"].items():
            frequent_table.add_row(str(index), key, str(value))
            index += 1
        console.print(frequent_table)
    if "rare" in counts:
        index = 1
        for key, value in counts["rare"].items():
            rare_table.add_row(str(index), key, str(value))
            index += 1
        console.print(rare_table)


if __name__ == "__main__":
    main()
