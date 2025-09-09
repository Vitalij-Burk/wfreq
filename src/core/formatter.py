from collections import Counter
from typing import Optional


class Formatter:
    @classmethod
    def format_word_list(cls, word_list: list[str], frequent: Optional[int | None] = 10, rare: Optional[int | None] = None):
        counter = Counter(word_list)
        results = {}
        if frequent:
            results["frequent"] = {}
            for word, count in counter.most_common(frequent):
                results["frequent"][word] = count
        if rare:
            results["rare"] = {}
            for word, count in sorted(counter.items(), key=lambda x: x[1])[:rare]:
                results["rare"][word] = count
        return results
        
