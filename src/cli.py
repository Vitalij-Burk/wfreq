import argparse
import os
import time

import yaml
from rich.console import Console
from rich.table import Table

from src.core.filter import Filter
from src.core.formatter import Formatter
from src.in_out.finder import Finder


class CLI:
    def init_emulator(self, argv=None):
        parser = argparse.ArgumentParser(
            prog="wfreq",
            description="A tool for text analyzing",
            epilog="Here you can see some statistics about your texts",
        )


        parser.add_argument("-p", "--path")
        parser.add_argument("-c", "--config")
        parser.add_argument("-f", "--frequent")
        parser.add_argument("-r", "--rare")
        parser.add_argument("-minl", "--min_length")
        parser.add_argument("-maxl", "--max_length")
        parser.add_argument("-rf", "--red_flags")
        parser.add_argument("-a", "--artifacts")
        parser.add_argument("-maxr", "--max_repeat")
        parser.add_argument("-nt", "--no_tags")


        self.args = parser.parse_args(argv)
        return self.args


    def parse_params(self):
        if self.args.config:
            path = os.path.expanduser(self.args.config)
            with open(path, "r") as file:
                params = yaml.safe_load(file)
            config = params["wfreq_config"]
            self.path = config["path"]
            self.artifacts = config["artifacts"]
            self.min_length = config["min_length"]
            self.max_length = config["max_length"]
            self.rare = config["rare"]
            self.frequent = config["frequent"]
            self.red_flags = config["red_flags"]
            self.max_repeat = config["max_repeat"]
        elif self.args.path:
            self.path = self.args.path
            self.frequent = int(self.args.frequent) if isinstance(self.args.frequent, str) else 10
            self.rare = int(self.args.rare) if isinstance(self.args.rare, str) else 0
            self.min_length = int(self.args.min_length) if isinstance(self.args.min_length, str) else 3
            self.max_length = int(self.args.max_length) if isinstance(self.args.max_length, str) else 70
            self.red_flags = set(self.args.red_flags.split(",")) if self.args.red_flags else set()
            self.artifacts = True if self.args.artifacts else False
            self.max_repeat = int(self.args.max_repeat) if isinstance(self.args.max_repeat, str) else 2


    def process(self):
        red_flags_copy = self.red_flags.copy()
        for red_flag in self.red_flags:
            if words := Finder.find_words_by_local_path(red_flag):
                for word in words:
                    red_flags_copy.add(word)
                red_flags_copy.remove(red_flag)
            else:
                continue
        red_flags = red_flags_copy
        start = time.perf_counter_ns()
        word_list = Finder.find_words(self.path)
        format = Filter.generate_format(self.min_length, self.max_length, self.artifacts, self.max_repeat)
        formatted_word_list = Filter.compile_word_list(word_list, red_flags, format)
        result = Formatter.format_word_list(formatted_word_list, self.frequent, self.rare)
        end = time.perf_counter_ns()
        print("Time: ", end - start)
        self.counts = result
        return result


    def output(self):
        frequent_table = Table(title="Frequent words", expand=True)
        rare_table = Table(title="Rare words", expand=True)
        frequent_table.add_column("Place")
        frequent_table.add_column("Word")
        frequent_table.add_column("Count")
        rare_table.add_column("Place")
        rare_table.add_column("Word")
        rare_table.add_column("Count")

        console = Console()

        if "frequent" in self.counts:
            index = 1
            for key, value in self.counts["frequent"].items():
                frequent_table.add_row(str(index), key, str(value))
                index += 1
            console.print(frequent_table)
        if "rare" in self.counts:
            index = 1
            for key, value in self.counts["rare"].items():
                rare_table.add_row(str(index), key, str(value))
                index += 1
            console.print(rare_table)


def main():
    cli = CLI()
    cli.init_emulator()
    cli.parse_params()
    cli.process()

    cli.output()


if __name__ == "__main__":
    main()
