import re

_NON_BREAKING_SPACES_PATTERN = re.compile(r'[\u202f\u00a0]')
_ZERO_WIDTH_CHARS_PATTERN = re.compile(r'[\u200b-\u200d\uFEFF]')
_SPACE_PATTERN = re.compile(r'\s+')


def remove_redundant_whitespaces(text: str) -> str:
    """ INTERNAL FUNCTION! """
    text = _NON_BREAKING_SPACES_PATTERN.sub(' ', text)
    text = _ZERO_WIDTH_CHARS_PATTERN.sub('', text)
    text = _SPACE_PATTERN.sub(' ', text)
    return text.strip()
