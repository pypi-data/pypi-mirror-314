import subprocess
import sys
import tomllib
import os

with open("../pyproject.toml", "rb") as file:
    data = tomllib.load(file)

packages = data["project"]["optional-dependencies"]["doc_generation"]

subprocess.check_call([sys.executable, "-m", "pip", "install"]+packages)