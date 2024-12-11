from dataclasses import dataclass


@dataclass
class SearchResult:
    filename: str
    lines: list[str]

    def __str__(self):
        return f"{self.filename}:\n" + "\n".join(self.lines)
