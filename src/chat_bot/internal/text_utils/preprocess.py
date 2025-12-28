from .symbols import replace_yo_with_e
from .whitespaces import remove_redundant_whitespaces


def preprocess_text(text: str) -> str:
    """ INTERNAL FUNCTION! """
    text = remove_redundant_whitespaces(text)
    text = replace_yo_with_e(text)
    return text
