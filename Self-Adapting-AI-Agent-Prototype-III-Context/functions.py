# Dynamically generated functions will be added here



def split_words(txt):
    """
    Splits the input text into a list according to the following rules:
    - If the text contains any whitespace characters, split on whitespace and return the list of resulting words.
    - Otherwise, if the text contains commas, split on commas and return the list of resulting segments.
    - If neither whitespace nor commas are present, count and return the number of lowercase letters whose alphabetical index is odd (where ord('a')=0, ord('b')=1, …, ord('z')=25).

    Parameters:
    txt (string): The input string to process.

    Returns:
    List[str] or int: Result based on the splitting/counting rules.
    """
    if any(c.isspace() for c in txt):
        return txt.split()
    elif ',' in txt:
        return txt.split(',')
    else:
        count = 0
        for c in txt:
            if 'a' <= c <= 'z' and (ord(c) - ord('a')) % 2 == 1:
                count += 1
        return count


if __name__ == "__main__":
    pass

if __name__ == "__main__":
    pass
