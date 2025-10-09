# Dynamically generated functions will be added here

computation_cache = {}



def filter_by_substring(strings, substring):
    """Filters a list of strings, returning those that contain the given substring.

    Args:
        strings (list): List of strings to filter.
        substring (str): Substring to search for.

    Returns:
        list: List of strings containing the substring.

    Raises:
        TypeError: If 'strings' is not a list or 'substring' is not a string.
    """
    if not isinstance(strings, list):
        raise TypeError("'strings' must be a list")
    if not isinstance(substring, str):
        raise TypeError("'substring' must be a string")
    return [s for s in strings if substring in s]


if __name__ == "__main__":
    pass
