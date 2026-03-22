import sys
from pathlib import Path

# добавляем корень проекта (parent папки tests) в начало sys.path
root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
