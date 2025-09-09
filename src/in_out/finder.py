import os
import re

word_list = []


class Finder:
    @classmethod
    def find_words_by_local_path(cls, path: str):
        pattern = re.compile(r"\w+")
        path = os.path.expanduser(path)
        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    cls.find_words_by_local_path(os.path.join(root, file))
        elif os.path.isfile(path):
            with open(path, encoding="utf-8", errors="ignore") as file:
                text = file.read().lower()
            for word in pattern.findall(text):
                word_list.append(word)
        else:
            return []
        return word_list
