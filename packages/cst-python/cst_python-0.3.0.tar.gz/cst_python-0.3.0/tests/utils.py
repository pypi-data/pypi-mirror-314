import os
import pathlib


def get_repository_path():
    repository_path = pathlib.Path(__file__).parent.parent.resolve()
    return repository_path

def get_examples_path():
    examples_path = os.path.join(get_repository_path(), "examples")
    return examples_path