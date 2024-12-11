## verificationYaml

---
title: >-
    Vérifier la validité des yaml
credits:
keywords: yaml,métadonnées,vérification,validité
lang: fr
type: texte
link:
link-archive:
embed:
zotero:
date: 2024-09-20
date-publication: 2024-09-20
source: auteur
priority: lowpriority
positon: main
---

Il est possible de vérifier (en partie) la validité des yaml&nbsp;:

- avec des outils disponibles en ligne (par exemple&nbsp;: [YAML Lint](https://www.yamllint.com/){link-archive="https://web.archive.org/web/20240920194116/https://www.yamllint.com/"}).
- dans le terminal, `yq r localisation du fichier` (ex&nbsp;: textes/introduction/introduction.yaml) champ (ex&nbsp;: title). Si le contenu du champ apparaît, il est correctement rempli. Autrement, c'est qu'il y a un problème dans le champ.


## exempleArborescence

---
title: >-
   Exemple d'arborescence du dossier `MonLivre`
credits:
keywords: arborescence,dossier,livre
lang: fr
type: texte
link:
link-archive:
embed:
zotero:
date: 2024-09-20
date-publication: 2024-09-20
source: auteur
priority: lowpriority
positon: main

---


```
MonLivre
  |_textes
    |_garde
        |__homepage.md
        |__livre.yaml
    |_introduction
        |__introduction.bib
        |__introduction.md
        |__introduction.yaml
    |_chapitre1
        |__chapitre1.bib
        |__chapitre1.md
        |__chapitre1.yaml
        |__additionnels.md     
    |_chapitre2
        |__chapitre2.bib
        |__chapitre2.md
        |__chapitre2.yaml
    |_conclusion
        |__conclusion.bib
        |__conclusion.md
        |__conclusion.yaml
    |_bibliographie
        |__bibliographie.bib
        |__bibliographie.md
        |__bibliographie.yaml
    |_media
```


## yamldulivrevide

---
title: >-
   Modèle yaml du livre vide&nbsp;: `textes/garde/livre.yaml`
credits:
keywords: yaml,métadonnées,exemple,garde,vide
lang: fr
type: texte
link:
link-archive:
embed:
zotero:
date: 2024-09-20
date-publication: 2024-09-20
source: auteur
priority: lowpriority
positon: main

---


```
version:
title:
subtitle:
lang:
date:
rights:
url:
collective:
authors:
  - forname:
    surname:
    orcidurl:
    presentation:
coverurl:
abstract_fr:
abstract_en:
description:
nbpages:
isbnprint:
isbnepub:
isbnpdf:
isbnnum:
prixprint:
prixepub:
prixpdf:
prixnum:
luluurl:
amazonurl:
epuburl:
pdfurl:
backlinksp:
urlsp:
keyword_fr:
keyword_en:
toc:
  - id:
  - parttitle:
    content:
      - id:
  - parttitle:
    content:
      - id:
  - parttitle:
    content:
      - id:
  - id:
  - id:
referenceCitation:
  - key:
publisher:
place:
url_traduction:
```


## yamldulivrecommente

---
title: >-
   Modèle yaml du livre rempli et commenté
credits:
keywords: yaml,métadonnées,exemple,garde,commenté,rempli
lang: fr
type: texte
link:
link-archive:
embed:
zotero:
date: 2024-09-20
date-publication: 2024-09-20
source: auteur
priority: lowpriority
positon: main

---


```
version: 0
title: >-
   titre du livre
subtitle: >-
   sous-titre
lang: fr
# langue du chapitre en ISO 639 : en, it...
date: AAAA/MM/JJ
# date de publication
rights: |-

  Creative Commons Attribution-ShareAlike 4.0 International (CC
  BY-SA 4.0)
# licence attribuée à l'ouvrage
url: 'http://urlDuLivre'
# url du livre
collective:
# _true_ ou _false_, selon si le livre est un collectif ou non
authors:
  - forname: Prénom Auteur 1
    surname: Nom Auteur 1
    orcidurl: https://orcid.org/XXX
    # url du profil ORCID Auteur 1
    presentation: >-
         Courte biographie de l'auteur.rice
  - forname: Prénom Auteur 2
    surname: Nom Auteur 2
    orcidurl: https://orcid.org/XXX
    # url du profil ORCID Auteur 2
    presentation: >-
         Courte biographie de l'auteur.rice
coverurl:
# lien vers la 1ere de couverture dans media/couv.jpg
abstract_fr: >-
    Résumé en français
abstract_en: >-
    Résumé en anglais
description: >-
    Titre du livre | Maison d'édition
    nbpages: XXX pages
# nombre de pages de la version papier (ou pdf)
isbnprint: 978-X-XXXXXX-XX-X
# isbn de la version papier imprimée - POD
isbnepub: 978-X-XXXXXX-XX-X
# isbn de la version epub
isbnpdf: 978-X-XXXXXX-XX-X
# isbn de la version pdf
isbnnum: 978-X-XXXXXX-XX-X
# isbn de la version html
prixprint: XX$ CAD
# prix de la version papier
prixepub: Gratuit
# prix de la version epub
prixpdf: Gratuit
# prix de la version pdf
prixnum: Gratuit
# prix de la version html
luluurl:
# url du projet sur Lulu
epuburl: media/livre.epub
# lien vers le livre format epub dans media
pdfurl: media/livre.pdf
# lien vers le livre format epub dans media
keyword_fr: >-
       mot clé fr 1, mot clé fr 2, mot clé fr 3
# mots clés en français à séparer par des virgules
keyword_en: >-
       mot clé en 1, mot clé en 2, mot clé en 3
# mots clés en anglais à séparer par des virgules
toc:
# sommaire du livre avec tous les chapitres dans l'ordre où ils doivent apparaître
  - id: introduction
    # indiquer ici le nom donné au fichier.md du chapitre
  - id: chapitre1
  - parttitle: titre de la Partie I
    # si pas de partie, indiquer le titre du chapitre suivant
    content:
      - id: chapitre2
      - id: chapitre3
  - parttitle: titre de la Partie II
    content:
      - id: chapitre4
      - id: chapitre5
  - id: conclusion
  - id: bibliographie
referenceCitation:
  - key: >-
       @
# clé bibtex de l'ouvrage
publisher: XX Éditions
# nom de la maison d'édition
place: XXX
# lieu de la maison d'édition
url_traduction:
# ajouter éventuellement ici un lien vers le livre dans une autre langue

```


## yamlduchapitrevide

---
title: >-
   Modèle du yaml de chapitre vide
credits:
keywords: yaml,métadonnées,exemple,chapitre
lang: fr
type: article
link:
link-archive:
embed:
zotero:
date: 2024-09-20
date-publication: 2024-09-20
source: auteur
priority: lowpriority
positon: main

---


```
title:
subtitle:
blockcitation:
authors:
  - forname:
    surname:
    institution:
    orcidurl:
    display:
    presentation:
abstract_fr:
abstract_en:
keyword_fr:
keyword_en:
nocite:
url_traduction:

```

## yamlduchapitrecommente

---
title: >-
   Modèle du yaml de chapitre rempli et commenté
credits:
keywords: yaml,métadonnées,exemple,chapitre,commenté
lang: fr
type: article
link:
link-archive:
embed:
zotero:
date: 2024-09-20
date-publication: 2024-09-20
source: auteur
priority: lowpriority
positon: main

---


```
title: >-
   titre du chapitre
subtitle: >-
   sous-titre du chapitre
blockcitation:
# indiquer _true_ si on souhaite afficher le bloc de citation sur le chapitre, autrement laisser vide
authors:
# indiquer les noms des auteur.rice.s du chapitre
  - forname: Prénom Auteur 1
    surname: Nom Auteur 1
    orcidurl: https://orcid.org/XXX
    # url du profil ORCID Auteur 1
    presentation: >-
         Courte biographie de l'auteur.rice qui apparaîtra en fin de chapitre si elle est renseignée
  - forname: Prénom Auteur 2
    surname: Nom Auteur 2
    orcidurl: https://orcid.org/XXX
    # url du profil ORCID Auteur 2
    presentation: >-
         Courte biographie de l'auteur.rice qui apparaîtra en fin de chapitre si elle est renseignée
abstract_fr: >-
   Résumé en français du chapitre
abstract_en: >-
   Résumé en anglais du chapitre
keyword_fr: >-
   mot clé 1, mot clé 2, mot clé 3
# mots clés en français à séparer par des virgules
keyword_en: >-
   mot clé 1, mot clé 2, mot clé 3
# mots clés en anglais à séparer par des virgules
nocite: ''
# Quand nocite: '' = toutes les références du fichier .bib s'affichent, même celles qui ne sont pas citées dans le chapitre.
# Quand nocite: '@*' = seules les références citées s'affichent
url_traduction: >-
      [Texte](url)
# Permet ici de faire un lien vers le chapitre dans une autre langue : mettre le texte du bouton + l'url (ex : [English version](url))

```
