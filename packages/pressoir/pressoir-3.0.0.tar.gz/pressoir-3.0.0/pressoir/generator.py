import tempfile

import pypandoc
import yaml
from dataclass_wizard.dumpers import asdict

from .additionals import include_additional_contents
from .sidenotes import convert_sidenotes, rewrite_global_sidenotes
from .utils import get_template_path, neighborhood

try:
    print(f"Pandoc version: {pypandoc.get_pandoc_version()}")
except OSError:
    pypandoc.download_pandoc()
    print(f"Pandoc version: {pypandoc.get_pandoc_version()}")

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


def generate_chapters(repository_path, target_path, book, meta, chapter_id):
    print("  Generating chapters:")
    book_settings = tomllib.loads(
        (repository_path / "pressoir" / "book.toml").read_text()
    )

    indexes_ids = book_settings.get("indexes", {}).get("ids")
    meta["indexes"] = indexes_ids
    glossaire = book_settings.get("glossaire", {})
    meta["glossaire"] = {
        "button": {
            "label": glossaire.get("button-label", "Voir dans le glossaire"),
            "title": glossaire.get(
                "button-title", "Consulter la référence dans le glossaire de l’ouvrage"
            ),
        }
    }
    meta["nb_of_chapters"] = len(book.chapters)

    for index, previous_chapter, current_chapter, next_chapter in neighborhood(
        book.chapters
    ):
        meta["index"] = index
        if not chapter_id or chapter_id == current_chapter.id:
            generate_chapter(
                repository_path,
                target_path,
                book,
                current_chapter,
                previous_chapter,
                next_chapter,
                meta,
            )


def generate_chapter(
    repository_path,
    target_path,
    book,
    current_chapter,
    previous_chapter,
    next_chapter,
    meta,
):
    print(
        f"    {current_chapter.id}: {current_chapter.title_h} "
        + f"({meta['index']}/{meta['nb_of_chapters']})"
    )
    dict_content = {
        "book": asdict(book),
        "chapter": asdict(current_chapter),
        "prev": previous_chapter and asdict(previous_chapter) or "",
        "next": next_chapter and asdict(next_chapter) or "",
        "meta": meta,
    }
    yaml_content = yaml.dump(dict_content)
    yaml_content += "nocite: '[@*]'\n"
    with tempfile.NamedTemporaryFile() as metadata_file:
        metadata_file.write(yaml_content.encode("utf-8"))
        metadata_file.read()  # Required to be readable by Pandoc.
        html_content = generate_html_content(
            repository_path, book, current_chapter, metadata_file
        )
    html_content = rewrite_global_sidenotes(html_content)
    html_content = include_additional_contents(
        repository_path, current_chapter, html_content
    )
    html_content = convert_sidenotes(html_content)
    (target_path / f"{current_chapter.id}.html").write_text(html_content)


def generate_html_content(repository_path, book, current_chapter, metadata_file):
    textes_path = repository_path / "textes"
    chapter_id = current_chapter.id
    md_content = (textes_path / chapter_id / f"{chapter_id}.md").read_text()
    bib_file = textes_path / chapter_id / f"{chapter_id}.bib"
    md_content = md_content.replace(
        "## Références",
        """
<section>
<details class="references" open>
<summary id="references">Références</summary>

:::{#refs}
:::

</details>
</section>""",
    )

    template_path = get_template_path(repository_path, "chapitre.html")
    extra_args = [
        "--ascii",
        "--citeproc",
        f"--bibliography={bib_file}",
        f"--template={template_path}",
        f"--metadata=title:{current_chapter.title_f}",
        f"--metadata-file={metadata_file.name}",
    ]
    html_content = pypandoc.convert_text(
        md_content, "html", format="md", extra_args=extra_args
    )

    return html_content


def generate_homepage(repository_path, target_path, book, meta):
    print(f"Rendering {target_path}:")
    print("  Generating homepage")

    source = repository_path / "textes" / "garde" / "homepage.md"
    if not source.exists():
        print("    Homepage not generated (missing homepage.md file)")
        return
    dict_content = {
        "book": asdict(book),
        "meta": meta,
    }
    yaml_content = yaml.dump(dict_content)
    yaml_content += "nocite: '[@*]'\n"
    with tempfile.NamedTemporaryFile() as metadata_file:
        metadata_file.write(yaml_content.encode("utf-8"))
        metadata_file.read()  # Required to be readable by Pandoc.
        md_content = (repository_path / "textes" / "garde" / "homepage.md").read_text()
        template_path = get_template_path(repository_path, "homepage.html")
        extra_args = [
            "--ascii",
            "--citeproc",
            f"--template={template_path}",
            f"--metadata=title:{book.title_f}",
            f"--metadata-file={metadata_file.name}",
        ]
        html_content = pypandoc.convert_text(
            md_content, "html", format="md", extra_args=extra_args
        )

    (target_path / "index.html").write_text(html_content)
