import shutil
import os


for path in ["_examples", "auto_doc"]:
    try:
        shutil.rmtree(path)
    except Exception:
        pass

for path in ["README.md", "Examples.md"]:
    try:
        os.remove(path)
    except Exception:
        pass