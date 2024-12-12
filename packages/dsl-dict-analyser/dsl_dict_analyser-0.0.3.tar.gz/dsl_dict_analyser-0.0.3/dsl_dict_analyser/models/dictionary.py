from dataclasses import dataclass
from dsl_dict_analyser.models.about import About
from dsl_dict_analyser.models.card import Card
@dataclass
class Dictionary:
    """Represents a single entry in the DSL dictionary"""
    def __init__(self, name: str, index_language: str, contents_language: str, about:About, cards: list[Card]):
        self.name :str = name
        self.index_language:str = index_language
        self.contents_language:str =contents_language
        self.about:About|None = about
        self.cards:list[Card] = cards

