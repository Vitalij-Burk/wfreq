import json
import os
import re

import requests
from bs4 import BeautifulSoup

pattern = re.compile(r"\w+")


word_list = []


class Finder:
    @classmethod
    def _source_determinant(cls, path: str) -> str | None:
        if os.path.isdir(path):
            return "folder"
        elif os.path.isfile(path):
            return "file"
        elif content := requests.get(path).text.strip():
            if content.startswith("{") or content.startswith("["):
                return "json"
            elif content.startswith("<html") or content.startswith("<!DOCTYPE"):
                return "html"
        else:
            return None


    @classmethod
    def _find_words_by_local_path(cls, path: str):
        path = os.path.expanduser(path)
        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    cls._find_words_by_local_path(os.path.join(root, file))
        elif os.path.isfile(path):
            with open(path, encoding="utf-8", errors="ignore") as file:
                text = file.read()
            for word in pattern.findall(text):
                word_list.append(word.lower())
        else:
            return []
        return word_list


    @classmethod
    def _find_words_by_API(cls, path: str):
        response = requests.get(path)
        content = response.text.strip()
        formatted_data = json.loads(content)
        if isinstance(formatted_data, list):
            for obj in formatted_data:
                for k, v in obj.items():
                    print(k, v)
                    for word in pattern.findall(k if isinstance(k, str) else str(k)):
                        word_list.append(word.lower())
                    for word in pattern.findall(v if isinstance(v, str) else str(v)):
                        word_list.append(word.lower())
        else:
            for k, v in formatted_data.items():
                for word in pattern.findall(k):
                    word_list.append(k.lower())
                for word in pattern.findall(v):
                    word_list.append(v.lower())
        return word_list


    @classmethod
    def _find_words_by_web_scraping(cls, path: str):
        response = requests.get(path)
        content = response.text.strip()
        soup = BeautifulSoup(content, "html.parser")
        parsed = soup.get_text()
        for word in pattern.findall(parsed):
            word_list.append(word.lower())
        return word_list


    @classmethod
    def find_words(cls, path: str):
        format = cls._source_determinant(path)
        print(format)
        if format == "folder" or format == "file":
            cls._find_words_by_local_path(path)
        elif format == "json":
            cls._find_words_by_API(path)
        elif format == "html":
            cls._find_words_by_web_scraping(path)
        return word_list
