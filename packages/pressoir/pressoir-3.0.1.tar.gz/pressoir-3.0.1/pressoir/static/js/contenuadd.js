document.addEventListener('DOMContentLoaded', () => {
    const contenuaddTitles = document.querySelectorAll('.contenuadd.lowpriority > h3')
    /* Expand contenuadd with lowpriority on title click. */
    Array.from(contenuaddTitles).forEach((contenuaddTitle) => {
        contenuaddTitle.addEventListener('click', (e) => {
            const section = e.target.closest('section')
            section.classList.toggle('expanded')
            e.preventDefault()
        })
    })
})
