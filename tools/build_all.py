"""Rebuild both editions in dependency order, from any working directory."""
from pathlib import Path
import subprocess
import sys


def main():
    tools = Path(__file__).resolve().parent
    for script in ('build_course.py', 'extend_atlas.py', 'build_course_en.py', 'extend_atlas_en.py'):
        subprocess.run([sys.executable, str(tools / script)], check=True, cwd=tools.parent)


if __name__ == '__main__':
    main()
