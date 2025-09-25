from src.in_out.finder import Finder


def test_source_determinant_folder():
    finder = Finder()
    format = finder._source_determinant("/")
    assert format == "folder"


def test_source_determinant_file():
    finder = Finder()
    format = finder._source_determinant("/bin/mkfs.btrfs")
    assert format == "file"


def test_source_determinant_html():
    finder = Finder()
    format = finder._source_determinant("https://www.youtube.com/")
    assert format == "html"


def test_source_determinant_json():
    finder = Finder()
    format = finder._source_determinant("https://jsonplaceholder.typicode.com/todos")
    assert format == "json"
