import re
from typing import Optional


class Filter:
    @classmethod
    def generate_format(cls, min_length: Optional[int | None] = 3, max_length: Optional[int | None] = 70, artifacts: Optional[bool | None] = False, max_repeat: Optional[int | None] = 2):
        repeat_rule = rf"(?!.*([A-Za-z_])\1{{{max_repeat},}})" if not artifacts else ""
        symbols_rule = "[A-Za-z]" if not artifacts else r"."
        regexp = rf"^{repeat_rule}{symbols_rule}{{{min_length},{max_length}}}$"
        return regexp


    @classmethod
    def compile_word_list(cls, word_list: list[str], red_flags: Optional[set | None] = set(), format: Optional[str | None] = r"\w"):
        pattern = re.compile(format)
        compiled_word_list = [word for word in word_list if pattern.match(word) and word not in red_flags]
        return compiled_word_list
