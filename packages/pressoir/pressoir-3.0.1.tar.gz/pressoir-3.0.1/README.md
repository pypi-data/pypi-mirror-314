# Pressoir

Documentation complète : https://pressoir.org/

## Installation

Pré-requis : Python3.8+

Installer et activer un environnement virtuel :

    $ python3 -m venv venv
    $ source venv/bin/activate

Installer les dépendances :

    $ make install

## Initialiser un livre

Par exemple :

    $ pressoir init --repository-path=../fia --collection sp

ou

    $ pressoir init --repository-path=../12-editionscritiques --collection pum

Note : si la destination n’existe pas ou n’a pas de dossier `textes`,
une coquille complète du livre est créée.

Par exemple :

    $ mkdir livre-test
    $ cd livre-test
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install pressoir
    $ pressoir init --collection=sp

## Construire un livre

    $ pressoir build --repository-path=../fia-en

Avec `../fia-en` qui est le chemin vers le dépôt du livre.

En bonus, il est possible de passer un chapitre particulier pour ne reconstruire que lui :

    $ pressoir build --repository-path=../fia-en --chapter=chapter1

Si vous êtes en local / développement, il faut passer l’option `--local` 
pour que les liens de parcours du livre fonctionnent.


## Servir un livre

    $ pressoir serve --repository-path=../fia-en

Avec `../fia-en` qui est le chemin vers le dépôt du livre qui a été construit.


## Help

### Commands

<!-- [[[cog
import subprocess
import cog
output = subprocess.check_output("pressoir --help", shell=True)
help = output.decode().split("\n", 1)[1]  # Remove Pandoc version.
cog.out(f"```\n{help}\n```")
]]] -->
```
usage: pressoir [-h]  ...

optional arguments:
  -h, --help  Show this help message and exit

Available commands:
  
    version   Return the current version of pressoir.
    init      Initialize a new book to `repository_path` or current directory.
    docs      Generate documentation with pressoir itself. #SoMeta
    build     Build a book from `repository_path` or current directory.
    serve     Serve an HTML book from `repository_path`/public or current
              directory/public.

```
<!-- [[[end]]] -->

### Command: `init`

<!-- [[[cog
import subprocess
import cog
output = subprocess.check_output("pressoir init --help", shell=True)
help = output.decode().split("\n", 1)[1]  # Remove Pandoc version.
cog.out(f"```\n{help}\n```")
]]] -->
```
usage: pressoir init [-h] [--repository-path REPOSITORY_PATH]
                     [--collection {pum,sp,blank}]

optional arguments:
  -h, --help            show this help message and exit
  --repository-path REPOSITORY_PATH
                        Absolute or relative path to book’s sources (default:
                        current).
  --collection {pum,sp,blank}, -c {pum,sp,blank}
                        Name of the collection (default: blank).

```
<!-- [[[end]]] -->


### Command: `docs`

<!-- [[[cog
import subprocess
import cog
output = subprocess.check_output("pressoir docs --help", shell=True)
help = output.decode().split("\n", 1)[1]  # Remove Pandoc version.
cog.out(f"```\n{help}\n```")
]]] -->
```
usage: pressoir docs [-h] [--target-path TARGET_PATH]

optional arguments:
  -h, --help            show this help message and exit
  --target-path TARGET_PATH

```
<!-- [[[end]]] -->


### Command: `build`

<!-- [[[cog
import subprocess
import cog
output = subprocess.check_output("pressoir build --help", shell=True)
help = output.decode().split("\n", 1)[1]  # Remove Pandoc version.
cog.out(f"```\n{help}\n```")
]]] -->
```
usage: pressoir build [-h] [--repository-path REPOSITORY_PATH]
                      [--target-path TARGET_PATH] [--chapter CHAPTER]
                      [--verbose]

optional arguments:
  -h, --help            show this help message and exit
  --repository-path REPOSITORY_PATH
                        Absolute or relative path to book’s sources (default:
                        current).
  --target-path TARGET_PATH
                        Where the book will be built (default:
                        `repository_path`/public).
  --chapter CHAPTER, -c CHAPTER
                        Specify a given chapter id (e.g. `chapter1`).
  --verbose, -v         Display more informations during the build.

```
<!-- [[[end]]] -->


### Command: `serve`

<!-- [[[cog
import subprocess
import cog
output = subprocess.check_output("pressoir serve --help", shell=True)
help = output.decode().split("\n", 1)[1]  # Remove Pandoc version.
cog.out(f"```\n{help}\n```")
]]] -->
```
usage: pressoir serve [-h] [--repository-path REPOSITORY_PATH] [--port PORT]

optional arguments:
  -h, --help            show this help message and exit
  --repository-path REPOSITORY_PATH
                        Absolute or relative path to book’s sources (default:
                        current).
  --port PORT, -p PORT  Port to serve the book from (default=8000)

```
<!-- [[[end]]] -->
