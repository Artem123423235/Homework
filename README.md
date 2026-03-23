Описание
Проект демонстрирует простую модель для товаров и категорий, показывает работу с классами, счётчиками и тестированием. Хорош для обучения формированию пакета, настройки тестов, CI и линтинга.

Рекомендуемая структура проекта
Используем подход "src layout":

project_root/
├─ .github/
│  └─ workflows/
│     └─ ci.yml
├─ .gitignore
├─ .flake8
├─ pytest.ini
├─ .coveragerc
├─ pyproject.toml / setup.cfg  (опционально)
├─ src/
│  └─ python_products/
│     ├─ __init__.py
│     └─ models.py
├─ tests/
│  ├─ __init__.py
│  └─ test_models.py
├─ README.md
└─ .venv/ (локально)
Ключевые моменты:

Код пакета хранится в src/python_products/.
Тесты — в tests/ (папка должна быть пакетом при необходимости).
Файлы .idea не должны попадать в репозиторий.
Быстрый старт (локально)
Клонировать репозиторий:
git clone https://github.com/USERNAME/REPO_NAME.git
cd REPO_NAME
Создать и активировать виртуальное окружение:
Unix / macOS:
python -m venv .venv
source .venv/bin/activate
Windows (PowerShell):
python -m venv .venv
.venv\Scripts\Activate.ps1
Установить dev-зависимости:
pip install --upgrade pip
pip install -r dev-requirements.txt
Примеры dev-зависимостей: black isort flake8 pytest pytest-cov coverage

Установить пакет в editable-режиме (рекомендуется):
pip install -e .
Это позволяет в тестах импортировать как from python_products.models import Product, Category.

Запуск demo
(Если есть main.py — пример использования)

python main.py
Тесты и покрытие
Запуск pytest с покрытием:

# Запуск тестов с выводом покрытия в консоль и созданием xml/html отчётов
pytest --cov=python_products --cov-report=term --cov-report=xml --cov-report=html
Проверка порога покрытия (локально):

coverage run -m pytest
coverage report --fail-under=75
В CI можно автоматически проваливать билд, если покрытие ниже 75%.

Линтинг и автоформатирование
Рекомендуемые инструменты:

black (автоформатирование)
isort (сортировка импортов)
flake8 (статический анализ/PEP8)
Примеры команд:

black .
isort .
flake8
CI (GitHub Actions)
CI должен запускать: black/isort в режиме проверки, flake8, pytest с coverage и проверку порога покрытия. В .github/workflows/ci.yml можно прописать шаги:

checkout
install deps
black --check .
isort --check-only .
flake8
pytest --cov=python_products --cov-report=xml
проверка покрытия >= 75% (например, разбор coverage.xml или использование coverage report --fail-under=75)
Примеры конфигов
.gitignore (минимальный, обязательно включает .idea)

# Byte-compiled / caches
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
.venv/
venv/
env/
ENV/

# IDE
.idea/
.vscode/

# pytest / coverage
.pytest_cache/
.coverage
coverage.xml
htmlcov/

# Build artifacts
build/
dist/
*.egg-info/

# OS
.DS_Store
Thumbs.db
.flake8

[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude =
    .git,
    __pycache__,
    .venv,
    build,
    dist,
    .mypy_cache,
    .idea
pytest.ini

[pytest]
testpaths = tests
python_files = test_*.py
.coveragerc

[run]
branch = True
omit =
    tests/*
    .venv/*
    */__init__.py

[report]
exclude_lines =
    pragma: no cover
    if __name__ == .__main__.:
Частые проблемы и решения
Ошибка "No module named 'models'":
Причина: запускаете тесты не из корня или не установили пакет.
Решение: ставьте пакет pip install -e . и используйте импорт from python_products.models import ..., либо запускайте pytest из корня и используйте sys.path в conftest.py (менее предпочтительно).
Ошибка "import file mismatch" при pytest (например два одинаковых test_models.py):
Найдите дубликаты:
Unix: find . -name "test_models.py"
Windows PowerShell: Get-ChildItem -Path . -Filter "test_models.py" -Recurse
Удалите/переименуйте лишнюю копию, очистите кэш:
Unix: find . -name "__pycache__" -type d -exec rm -rf {} + && find . -name "*.pyc" -delete
PowerShell: команды удаления pycache/ .pyc (см. выше)
Убедитесь, что pytest.ini ограничивает testpaths = tests.
.idea закоммичена в репозиторий:
git rm -r --cached .idea
echo ".idea/" >> .gitignore
git add .gitignore
git commit -m "Remove .idea and add to .gitignore"
git push
Удалять .idea из истории (если нужно) — особая операция (BFG / filter-branch), выполняется осторожно.

flake8 жалуется:
Исправьте сообщения flake8 (E*, W*). Используйте black для автоматического форматирования, затем flake8 для оставшихся проблем