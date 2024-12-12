from dsl_dict_analyser.analyser import analyser
from dsl_dict_analyser.models.dictionary import Dictionary
def read(file_path: str) -> Dictionary:
    with open(file_path,"r",encoding='utf-8') as file:
        lines = []
        for line in file.readlines():
            lines.append(line)
    return analyser(lines)