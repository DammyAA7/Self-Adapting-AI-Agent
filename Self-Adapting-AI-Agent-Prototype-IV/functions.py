

import csv
import re

def find_helping_todos(verbs, path=None):
    """
    Finds todo items whose task contains any of the given helper verbs as whole words, case-insensitive.
    Returns a list of matching todo dicts, an empty list if no matches or empty verbs, and False on invalid input or file errors.
    """
    if not isinstance(verbs, list):
        return False
    if not verbs:
        return []
    file_path = path if path else "/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/Self-Adapting-AI-Agent-Prototype-IV/todo.csv"
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            if not reader.fieldnames:
                return []
            patterns = [re.compile(r'\b' + re.escape(verb) + r'\b', re.IGNORECASE) for verb in verbs]
            matches = []
            for row in reader:
                task = row.get('task', '')
                for pat in patterns:
                    if pat.search(task):
                        matches.append(row)
                        break
            return matches
    except FileNotFoundError:
        return False
    except Exception:
        return False


if __name__ == "__main__":
    pass
