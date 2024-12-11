function transformCitation(citation) {
    const cites = citation.dataset.cites
    const content = citation.textContent
    if (!content) {
        return
    }
    // We remove initial parentheses.
    const innerContent = content.slice(1, -1)
    if (cites === '') {
        return
    }
    if (cites.indexOf(' ') > -1) {
        const [cite1, cite2] = cites.split(' ', 2)
        if (innerContent.indexOf(';') === -1) {
            return
        }
        const [innerContent1, innerContent2] = innerContent.split(';', 2)
        const linkCitation1 = document.createElement('a')
        linkCitation1.setAttribute('href', `#ref-${cite1}`)
        linkCitation1.textContent = innerContent1.trim()
        const linkCitation2 = document.createElement('a')
        linkCitation2.setAttribute('href', `#ref-${cite2}`)
        linkCitation2.textContent = innerContent2.trim()
        citation.innerHTML = `(${linkCitation1.outerHTML}, ${linkCitation2.outerHTML})`
    } else {
        const linkCitation = document.createElement('a')
        linkCitation.setAttribute('href', `#ref-${cites}`)
        linkCitation.textContent = innerContent.trim()
        citation.innerHTML = `(${linkCitation.outerHTML})`
    }
}

function capitalize(string) {
    return string.replace(/\b\w/g, (c) => c.toUpperCase())
}

function handleReference(referenceLink, reference, fromBibliography) {
    const content = reference.textContent
        .trim()
        .replace(/(?:https?|ftp):\/\/[\n\S]+/g, '') // Remove links.
    let onelinerContent = content
        .split('\n')
        .map((fragment) => fragment.trim()) // Remove new lines.
        .join(' ')
    if (onelinerContent.startsWith('———.')) {
        const [refauthor, book] = referenceLink.hash.split('_', 2)
        const [ref, author] = refauthor.split('-', 2)
        onelinerContent = onelinerContent.replace('———.', `${capitalize(author)}.`)
    }
    if (fromBibliography) {
        referenceLink.href = `bibliographie.html${referenceLink.hash}`
    }
    referenceLink.setAttribute('aria-label', onelinerContent)
    const balloonLength = window.screen.width < 760 ? 'medium' : 'xlarge'
    referenceLink.dataset.balloonLength = balloonLength

    /* Open references on click. */
    referenceLink.addEventListener('click', (e) => {
        references.parentElement.setAttribute('open', 'open')
        // Waiting to reach the bottom of the page then scroll up a bit
        // to avoid the fixed header. Fragile.
        setTimeout(() => {
            window.scrollTo({
                top: window.scrollY - 130,
                behavior: 'smooth',
            })
        }, 10)
    })
}

function tooltipReference(referenceLink) {
    /* Put attributes for balloon.css to render tooltips. */
    const reference = document.querySelector(referenceLink.hash)
    if (reference) {
        handleReference(referenceLink, reference)
    } else {
        fetch('bibliographie.html')
            .then((response) => response.text())
            .then((body) => {
                const tempDiv = document.createElement('div')
                tempDiv.innerHTML = body
                return tempDiv.querySelector(referenceLink.hash)
            })
            .then((reference) => handleReference(referenceLink, reference, true))
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const references = document.querySelector('#references')
    const chapter = document.body.dataset.chapitre
    if (!chapter || !references) {
        return
    }

    /* Transform citations from contenuadd (converted as <span>s by Pandoc
     because we set `suppress-bibliography` to true). */
    Array.from(document.querySelectorAll('[data-cites]')).forEach(transformCitation)

    /* Setup balloons tooltips for references. */
    Array.from(document.querySelectorAll('[href^="#ref-"]')).forEach(tooltipReference)
})
