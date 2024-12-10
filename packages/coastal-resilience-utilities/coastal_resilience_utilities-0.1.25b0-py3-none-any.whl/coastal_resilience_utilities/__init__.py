# Ugly hack to allow absolute import from the root folder
# whatever its name is. Please forgive the heresy.
import sys, os
sys.path.insert(0, os.path.abspath('.'))


def get_project_root():
    return os.path.dirname(__file__)
