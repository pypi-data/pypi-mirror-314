import contextlib
import os
import shutil
import socket
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer, test
from pathlib import Path
from typing import Optional

from minicli import cli, run

from . import ROOT_DIR, VERSION
from .generator import generate_chapters, generate_homepage
from .indexes import generate_indexes
from .models import configure_book
from .statics import bundle_statics, sync_statics


@cli
def version():
    """Return the current version of pressoir."""
    print(f"Pressoir version: {VERSION}")


@cli
@cli("collection", choices=["pum", "sp", "blank"])
def init(repository_path: Path = Path(), collection: str = "blank"):
    """Initialize a new book to `repository_path` or current directory.

    :repository_path: Absolute or relative path to book’s sources (default: current).
    :collection: Name of the collection (default: blank).
    """
    print(
        f"Initializing a new book: `{repository_path}` for `{collection}` collection."
    )

    if not (repository_path / "presssoir").exists():
        shutil.copytree(
            ROOT_DIR / "init" / collection / "pressoir",
            repository_path / "pressoir",
            dirs_exist_ok=True,
        )

    if "textes" not in os.listdir(repository_path):
        shutil.copytree(
            ROOT_DIR / "init" / collection / "textes",
            repository_path / "textes",
            dirs_exist_ok=True,
        )

    if "doc" not in os.listdir(repository_path) and "doc" in os.listdir(
        ROOT_DIR / "init" / collection
    ):
        shutil.copytree(
            ROOT_DIR / "init" / collection / "doc",
            repository_path / "doc",
            dirs_exist_ok=True,
        )


@cli
def docs(target_path: Optional[Path] = None):
    """Generate documentation with pressoir itself. #SoMeta"""
    if target_path is None:
        target_path = Path(os.getenv("PWD")) / "public"
    else:
        target_path = Path(target_path)
    print(f"Generating documentation in `{target_path.resolve()}`.")
    build(ROOT_DIR / "docs", target_path)


@cli
def build(
    repository_path: Path = Path(),
    target_path: Optional[Path] = None,
    chapter: str = "",
    verbose: bool = False,
):
    """Build a book from `repository_path` or current directory.

    :repository_path: Absolute or relative path to book’s sources (default: current).
    :target_path: Where the book will be built (default: `repository_path`/public).
    :chapter: Specify a given chapter id (e.g. `chapter1`).
    :verbose: Display more informations during the build.
    """
    if target_path is None:
        target_path = repository_path / "public"
    target_path.mkdir(parents=True, exist_ok=True)
    print(
        f"Building a book from {repository_path.resolve()} to {target_path.resolve()}."
    )
    sync_statics(repository_path, target_path)
    css_filename, js_filename = bundle_statics(repository_path, target_path)
    book = configure_book(repository_path / "textes" / "garde" / "livre.yaml")
    if verbose:
        import pprint

        pprint.pprint(book)

    meta = {"css_filename": css_filename, "js_filename": js_filename}
    generate_homepage(repository_path, target_path, book, meta)
    generate_chapters(repository_path, target_path, book, meta, chapter)
    generate_indexes(repository_path, target_path, book)


@cli
def serve(repository_path: Path = Path(), port: int = 8000):
    """Serve an HTML book from `repository_path`/public or current directory/public.

    :repository_path: Absolute or relative path to book’s sources (default: current).
    :port: Port to serve the book from (default=8000)
    """
    print(
        f"Serving HTML book from `{repository_path}/public` to http://127.0.0.1:{port}"
    )

    # From https://github.com/python/cpython/blob/main/Lib/http/server.py#L1307-L1326
    class DirectoryServer(ThreadingHTTPServer):
        def server_bind(self):
            # suppress exception when protocol is IPv4
            with contextlib.suppress(Exception):
                self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            return super().server_bind()

        def finish_request(self, request, client_address):
            self.RequestHandlerClass(
                request, client_address, self, directory=str(repository_path / "public")
            )

    test(HandlerClass=SimpleHTTPRequestHandler, ServerClass=DirectoryServer, port=port)


def main():
    run()
