"""String utility functions"""

import string


def ct(
    s: str,
    remove_punctuation: bool = True,
    lower: bool = True,
    strip: bool = True,
    replace: str = "",
) -> str:
    """ct = cleantext

    Takes a utf-8 string and converts to ascii lower case without punctuation
    """
    if not s:
        return ""
    s = s.encode("utf-8").decode("ascii", "ignore")
    if remove_punctuation:
        s = s.translate(str.maketrans("", "", string.punctuation))
    if lower:
        s = s.lower()
    if strip:
        s = s.strip()
    if replace:
        for char in replace:
            s = s.replace(char, "")
    return s
