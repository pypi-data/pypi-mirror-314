from dataclasses import dataclass

@dataclass
class About:
    """Represents a single entry in the DSL dictionary"""
    def __init__(self, about: str, definitions: list[str]):
        self.about = about
        self.definitions = definitions
