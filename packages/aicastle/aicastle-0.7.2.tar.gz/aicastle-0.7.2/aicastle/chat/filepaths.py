import os
from pathspec import PathSpec

def get_all_filepaths(gitignore=True):
    gitignore_path='./.gitignore'
    if gitignore and os.path.exists(gitignore_path) :
        with open(gitignore_path, 'r') as f:
            patterns = f.readlines()
        patterns = [pattern.strip() for pattern in patterns if pattern.strip() and not pattern.startswith('#')]
    else :
        patterns = []

    spec = PathSpec.from_lines('gitwildmatch', patterns)
    all_filepaths = []
    for root, dirs, files in os.walk("./"):
        if '.git' in dirs:
            dirs.remove('.git')

        for name in files:
            filepath = os.path.relpath(os.path.join(root, name), start="./")
            all_filepaths.append(filepath)

    all_filepaths = [f for f in all_filepaths if not spec.match_file(f)]
    return sorted(all_filepaths)


def get_target_filepaths(patterns, ignore):
    all_filepaths = get_all_filepaths()
    patterns = [pattern.strip() for pattern in patterns if pattern.strip()]
    spec = PathSpec.from_lines('gitwildmatch', patterns)
    if ignore :
        return [f for f in all_filepaths if not spec.match_file(f)]
    else :
        return [f for f in all_filepaths if spec.match_file(f)]


def get_chat_filepaths(patterns):
    return get_target_filepaths(patterns, True)


def get_finetuning_filepaths(patterns):
    return get_target_filepaths(patterns, False)

