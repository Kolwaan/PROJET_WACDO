// ==========================
// SLIDER CATÉGORIES
// ==========================
function initSlider() {
    const container = document.querySelector(".nav_images_container")
    const flecheGauche = document.querySelector(".fleche_slider")
    const flecheDroite = document.querySelector(".fleche_slider_reverse")

    if (!container || !flecheGauche || !flecheDroite) {
        console.warn("Slider catégories introuvable !")
        return
    }

    let position = 0
    let scrollContinu = { interval: null } // objet pour éviter les collisions
    let isBelow600px = window.innerWidth <= 600

    window.addEventListener("resize", () => {
        const wasBelow600px = isBelow600px
        isBelow600px = window.innerWidth <= 600

        if (wasBelow600px !== isBelow600px) {
            container.scrollLeft = 0
            position = 0
        }
    })

    function getScrollDistance() {
        return isBelow600px ? container.offsetWidth + 3 : 3
    }

    function scroll(direction) {
        const distance = getScrollDistance()
        const maxScroll = container.scrollWidth - container.offsetWidth

        if (direction === "left") position = Math.max(0, position - distance)
        else position = Math.min(maxScroll, position + distance)

        container.scrollTo({
            left: position,
            behavior: isBelow600px ? "smooth" : "auto",
        })
    }

    function startContinuousScroll(direction) {
        scroll(direction) // scroll immédiat

        if (!isBelow600px) {
            scrollContinu.interval = setInterval(() => scroll(direction), 4)
        }
    }

    function stopContinuousScroll() {
        if (scrollContinu.interval) {
            clearInterval(scrollContinu.interval)
            scrollContinu.interval = null
        }
    }

    // événements flèche gauche
    flecheGauche.parentElement.addEventListener("mousedown", (e) => {
        e.preventDefault()
        startContinuousScroll("left")
    })
    flecheGauche.parentElement.addEventListener(
        "touchstart",
        (e) => {
            e.preventDefault()
            startContinuousScroll("left")
        },
        { passive: false }
    )

    // événements flèche droite
    flecheDroite.parentElement.addEventListener("mousedown", (e) => {
        e.preventDefault()
        startContinuousScroll("right")
    })
    flecheDroite.parentElement.addEventListener(
        "touchstart",
        (e) => {
            e.preventDefault()
            startContinuousScroll("right")
        },
        { passive: false }
    )

    // arrêt global du scroll continu pour ce slider seulement
    document.addEventListener("mouseup", stopContinuousScroll)
    document.addEventListener("touchend", stopContinuousScroll)

    // synchroniser position scroll manuel
    container.addEventListener("scroll", () => {
        position = container.scrollLeft
    })
}





// ==========================
// SLIDER BOISSONS
// ==========================
function initSliderBoissons() {
    const container = document.querySelector(".slider_boisson")
    const fleches = document.querySelectorAll(".flechesSliderBoissons")

    if (!container || fleches.length < 2) {
        console.warn("Slider boissons introuvable !")
        return
    }

    const flecheGauche = fleches[0]
    const flecheDroite = fleches[1]

    let position = 0
    let scrollContinu = { interval: null } // objet pour éviter collisions
    let isBelow800px = window.innerWidth <= 800

    window.addEventListener("resize", () => {
        const wasBelow800px = isBelow800px
        isBelow800px = window.innerWidth <= 800

        if (wasBelow800px !== isBelow800px) {
            container.scrollLeft = 0
            position = 0
        }
    })

    function getScrollDistance() {
        return isBelow800px ? container.offsetWidth + 3 : 3
    }

    function scroll(direction) {
        const distance = getScrollDistance()
        const maxScroll = container.scrollWidth - container.offsetWidth

        if (direction === "left") position = Math.max(0, position - distance)
        else position = Math.min(maxScroll, position + distance)

        container.scrollTo({
            left: position,
            behavior: isBelow800px ? "smooth" : "auto",
        })
    }

    function startContinuousScroll(direction) {
        scroll(direction) // scroll immédiat

        if (!isBelow800px) {
            scrollContinu.interval = setInterval(() => scroll(direction), 4)
        }
    }

    function stopContinuousScroll() {
        if (scrollContinu.interval) {
            clearInterval(scrollContinu.interval)
            scrollContinu.interval = null
        }
    }

    // événements flèche gauche
    flecheGauche.addEventListener("mousedown", (e) => {
        e.preventDefault()
        startContinuousScroll("left")
    })
    flecheGauche.addEventListener(
        "touchstart",
        (e) => {
            e.preventDefault()
            startContinuousScroll("left")
        },
        { passive: false }
    )

    // événements flèche droite
    flecheDroite.addEventListener("mousedown", (e) => {
        e.preventDefault()
        startContinuousScroll("right")
    })
    flecheDroite.addEventListener(
        "touchstart",
        (e) => {
            e.preventDefault()
            startContinuousScroll("right")
        },
        { passive: false }
    )

    // arrêt global du scroll continu pour ce slider seulement
    document.addEventListener("mouseup", stopContinuousScroll)
    document.addEventListener("touchend", stopContinuousScroll)

    // synchroniser position scroll manuel
    container.addEventListener("scroll", () => {
        position = container.scrollLeft
    })
}