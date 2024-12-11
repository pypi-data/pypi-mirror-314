from dictionary_analyser.models.constants import *
from dictionary_analyser.models.card import Card
from dictionary_analyser.models.about import About
from dictionary_analyser.models.dictionary import Dictionary
def format_line(line:str):
    # remove all tag, it's a temporary solution.
    for color_tag in COLORS:
        line = line.replace(color_tag, '')
    for common_tag in COMMON:
        line = line.replace(common_tag, '')
    for margin_tag in MARGINS:
        line = line.replace(margin_tag, '')
    return line.strip()


def analyser(data: list[str]) -> Dictionary:
    dictionary:Dictionary
    words: list[Card] = []
    index = 0
    metadata = {}
    for line_index, line in enumerate(data):
        starts_with = line[0]
        # Skip empty lines.
        if line == "":
            continue
        # Skip metadata & empty lines.
        if starts_with == "#":
            
            key, value = line[1:].split('\t', 1)
            metadata[key.strip()] = value.strip()
            continue

        # Tab/Space means it is definition of previous word.
        if starts_with in STARTING_CHARACTERS:
            definition = format_line(line)
            words[index - 1].definitions.append(definition)

            continue

        if len(words) > 0:
            if len(words[index - 1].definitions) == 0:
                not_found = True
                new_index = line_index

                while not_found:
                    new_index += 1

                    if data[new_index][0] in STARTING_CHARACTERS:
                        found_definition = format_line(data[new_index])
                        words[index - 1].definitions.append(found_definition)
                        not_found = False

        # The line is a headword, start new entry.
        words.append(Card(word=format_line(line),definitions=[]))
        index += 1
    return Dictionary(name=metadata['NAME'], 
                      index_language=metadata['INDEX_LANGUAGE'], 
                      contents_language=metadata['CONTENTS_LANGUAGE'], 
                      about=None, 
                      cards=words
            )

