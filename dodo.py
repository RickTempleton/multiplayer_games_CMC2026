from pathlib import Path
import shutil

from doit.task import clean_targets


DOIT_CONFIG = {"default_tasks": ["html"]}


def task_pot():
    """Построение переводов."""
    py_files = list(Path("src").glob("**/*.py"))
    return {
        "file_dep": py_files + [Path("babel.cfg")],
        "actions": [
            "python3 -m babel.messages.frontend extract "
            "-F babel.cfg -k tr -o src/lib/locale/messages.pot src",
        ],
        "targets": ["src/lib/locale/messages.pot"],
        "clean": [clean_targets],
    }


def task_po():
    """Обновление переводов."""
    return {
        "file_dep": ["src/lib/locale/messages.pot"],
        "actions": [
            "python3 -m babel.messages.frontend update "
            "-D messages -i src/lib/locale/messages.pot "
            "-d src/lib/locale -l ru --init-missing",
            "python3 -m babel.messages.frontend update "
            "-D messages -i src/lib/locale/messages.pot "
            "-d src/lib/locale -l en --init-missing",
        ],
        "targets": [
            "src/lib/locale/ru/LC_MESSAGES/messages.po",
            "src/lib/locale/en/LC_MESSAGES/messages.po",
        ],
        "task_dep": ["pot"],
        "clean": [clean_targets],
    }


def task_mo():
    """Компиляция переводов."""
    po_files = [
        "src/lib/locale/ru/LC_MESSAGES/messages.po",
        "src/lib/locale/en/LC_MESSAGES/messages.po",
    ]
    return {
        "file_dep": po_files,
        "actions": [
            "python3 -m babel.messages.frontend compile "
            "-D messages -d src/lib/locale",
        ],
        "targets": [
            "src/lib/locale/ru/LC_MESSAGES/messages.mo",
            "src/lib/locale/en/LC_MESSAGES/messages.mo",
        ],
        "task_dep": ["po"],
        "clean": [clean_targets],
    }


def task_i18n():
    """Создание i18n."""
    return {
        "actions": ["touch .i18n"],
        "targets": [".i18n"],
        "task_dep": ["pot", "po", "mo"],
        "clean": [clean_targets],
    }


def task_html():
    """Создание html документации."""
    rstpy = (
        list(Path("docs").glob("**/*.rst"))
        + list(Path("src").glob("**/*.py"))
        + [Path("docs/conf.py")]
    )
    return {
        "actions": ["sphinx-build -M html docs docs/_build"],
        "targets": ["docs/_build/html/index.html"],
        "file_dep": rstpy,
        "clean": [(shutil.rmtree, ["docs/_build"], {"ignore_errors": True})],
    }


def task_test():
    """Прогон тестов."""
    test_files = list(Path("tests").glob("test_*.py"))
    py_files = list(Path("src").glob("**/*.py"))
    return {
        "file_dep": [
            "src/lib/locale/ru/LC_MESSAGES/messages.mo",
            "src/lib/locale/en/LC_MESSAGES/messages.mo",
        ] + test_files + py_files,
        "actions": [
            "PYTHONPATH=src python3 -m unittest discover -s tests",
            "touch .test",
        ],
        "targets": [".test"],
        "task_dep": ["i18n"],
        "clean": [clean_targets],
    }
