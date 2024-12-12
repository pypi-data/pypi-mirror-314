from dataclasses import dataclass

@dataclass
class Card:
    """Represents a single entry in the DSL dictionary"""
    def __init__(self, word: str, definitions: list[str]):
        self.word = word
        self.definitions = definitions
