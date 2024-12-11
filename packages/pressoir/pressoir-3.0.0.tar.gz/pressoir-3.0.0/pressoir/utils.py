import fnmatch
import hashlib
import os
import re

from . import ROOT_DIR

html_comments_re = re.compile(r"<!--.*?-->")
html_tags_re = re.compile(r"<[^>]*>")


def strip_html_comments(value):
    if not value:
        return ""
    return html_comments_re.sub("", value)


def strip_html_tags(value):
    if not value:
        return ""
    return html_tags_re.sub("", value)


def get_template_path(repository_path, name):
    """Try to find it within the book folder, fallback on pressoir one."""
    template_path = repository_path / "templates" / name
    if not template_path.exists():
        template_path = ROOT_DIR / "templates" / name
    return template_path


def each_file_from(source_dir, pattern="*.html"):
    """Walk across the `source_dir` and return file paths matching `pattern`."""
    for filename in fnmatch.filter(os.listdir(source_dir), pattern):
        yield source_dir / filename


def generate_md5(content):
    return hashlib.md5(content.encode()).hexdigest()


def neighborhood(iterable, first=None, last=None):
    """
    Yield the (index, previous, current, next) items given an iterable.

    You can specify a `first` and/or `last` item for bounds.
    """
    index = 1
    iterator = iter(iterable)
    previous = first
    current = next(iterator)  # Throws StopIteration if empty.
    for next_ in iterator:
        yield (index, previous, current, next_)
        previous = current
        index += 1
        current = next_
    yield (index, previous, current, last)
