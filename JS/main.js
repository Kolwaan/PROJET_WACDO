// Récupération du panier depuis le localStorage
let panier = JSON.parse(localStorage.getItem("panier")) || []

Promise.all([
    fetch("DATA/categories.json").then((r) => {
        if (!r.ok) {
            throw new Error(
                "Impossible de charger les données. Erreur HTTP : " + r.status
            )
        }
        return r.json()
    }),

    fetch("DATA/produits.json").then((r) => {
        if (!r.ok) {
            throw new Error(
                "Impossible de charger les données. Erreur HTTP : " + r.status
            )
        }
        return r.json()
    }),
])
    .then(([cat, prod]) => {
        // CHARGEMENT DES CATÉGORIES DU SLIDER
        const slider = document.querySelector(".nav_images_container")

        cat.forEach((catSlider) => {
            const modifCat = document.createElement("button")
            modifCat.classList.add(`slider_button${catSlider.id}`)
            modifCat.innerHTML = `<img src="ASSETS${catSlider.image}" alt="${catSlider.title}">${catSlider.title}`

            slider.append(modifCat)
        })

        // FONCTION DU SLIDER CATÉGORIES
        initSlider()

        // Numéro de commande aléatoire
        const numeroCommande = document.querySelector(".numero")
        numeroCommande.textContent = Math.floor(Math.random() * 999) + 1

        // Sur place ou à emporter
        const surPlaceOuAemporter = document.querySelector(
            ".commande_numero p:last-child"
        )
        const SPouAEstorage = localStorage.getItem("SPouAEstorage")

        if (SPouAEstorage) {
            surPlaceOuAemporter.innerHTML = SPouAEstorage
        }

        // AFFICHAGE DES MENUS À L'OUVERTURE DE LA PAGE
        const container = document.querySelector(".nos_menus_img")

        prod.menus.forEach((menu) => {
            const modifChoix = document.createElement("button")
            modifChoix.innerHTML = `<img src="ASSETS${menu.image}" alt="${
                menu.nom
            }">
            <div class="nos_menus_img--nomEtPrix">
            <p>${menu.nom}</p>
            <p>${menu.prix.toFixed(2)} €</p>
            </div>`

            container.append(modifChoix)
        })

        // AFFICHAGE DES CHOIX DE PRODUITS/MENUS EN CLIQUANT SUR LES CATÉGORIES DU SLIDER
        cat.forEach((catClick) => {
            // Sélection de chaque classe "slider_buttonNb" sur chaque bouton du slider
            const categories = document.querySelector(
                `.slider_button${catClick.id}`
            )

            categories.addEventListener("click", () => {
                // vidage de la div qui a la classe "nos_menus_img"
                // variable container créée à la ligne 25
                container.innerHTML = ""

                prod[catClick.title].forEach((menu) => {
                    const modifChoix = document.createElement("button")
                    modifChoix.innerHTML = `<img src="ASSETS${
                        menu.image
                    }" alt="${menu.nom}">
                    <div class="nos_menus_img--nomEtPrix">
                    <p>${menu.nom}</p>
                    <p>${menu.prix.toFixed(2)} €</p>
                    </div>`

                    container.append(modifChoix)
                    modifChoix.classList.add("buttonClick")
                })
            })
        })

        // Noms des catégories + descriptions
        document
            .querySelector(".slider_button1")
            .addEventListener("click", () => {
                document.querySelector(".nos_menus_txt h1").textContent =
                    "Nos menus"
                document.querySelector(".nos_menus_txt p").textContent =
                    "Un sandwich, une friture ou une salade et une boisson"
            })
        document
            .querySelector(".slider_button2")
            .addEventListener("click", () => {
                document.querySelector(".nos_menus_txt h1").textContent =
                    "Nos Boissons Fraîches"
                document.querySelector(".nos_menus_txt p").textContent =
                    "Une petite soif, sucrée, légère, rafraîchissante"
            })
        document
            .querySelector(".slider_button3")
            .addEventListener("click", () => {
                document.querySelector(".nos_menus_txt h1").textContent =
                    "Nos Burgers"
                document.querySelector(".nos_menus_txt p").textContent = ""
            })
        document
            .querySelector(".slider_button4")
            .addEventListener("click", () => {
                document.querySelector(".nos_menus_txt h1").textContent =
                    "Nos Frites et Potatoes"
                document.querySelector(".nos_menus_txt p").textContent = ""
            })
        document
            .querySelector(".slider_button5")
            .addEventListener("click", () => {
                document.querySelector(".nos_menus_txt h1").textContent =
                    "Nos Encas"
                document.querySelector(".nos_menus_txt p").textContent = ""
            })
        document
            .querySelector(".slider_button6")
            .addEventListener("click", () => {
                document.querySelector(".nos_menus_txt h1").textContent =
                    "Nos Wraps"
                document.querySelector(".nos_menus_txt p").textContent = ""
            })
        document
            .querySelector(".slider_button7")
            .addEventListener("click", () => {
                document.querySelector(".nos_menus_txt h1").textContent =
                    "Nos Salades"
                document.querySelector(".nos_menus_txt p").textContent = ""
            })
        document
            .querySelector(".slider_button8")
            .addEventListener("click", () => {
                document.querySelector(".nos_menus_txt h1").textContent =
                    "Nos Desserts"
                document.querySelector(".nos_menus_txt p").textContent = ""
            })
        document
            .querySelector(".slider_button9")
            .addEventListener("click", () => {
                document.querySelector(".nos_menus_txt h1").textContent =
                    "Nos Sauces"
                document.querySelector(".nos_menus_txt p").textContent = ""
            })

        // AFFICHAGE DES MODALES MENU ET TAILLE BOISSON
        const btn_container = document.querySelector(".nos_menus_img")
        const menuTxt = document.querySelector(".nos_menus_txt h1")

        // variables overlays
        const overlayMenu = document.querySelector(".overlay_menu")
        const overlayFrites = document.querySelector(".overlay_frites")
        const overlayBoissons = document.querySelector(".overlay_boissons")
        const overlayTailleBoisson = document.querySelector(
            ".overlay_tailleBoisson"
        )

        // variables modale menu 1 (Maxi / Best Of)
        const menu1 = document.querySelector(".modalButtonMenu1")
        const menu2 = document.querySelector(".modalButtonMenu2")
        const etapeSuivante1 = document.querySelector(".modale_button1")

        // variables modale menu 2 (frites / potatoes)
        const frites1 = document.querySelector(".modalButtonfrites1")
        const frites2 = document.querySelector(".modalButtonfrites2")
        const retour1 = document.querySelector(".retour1")
        const etapeSuivante2 = document.querySelector(".modale_button2")

        //  variable modale menu 3 (boissons)
        const boisson = document.querySelector(".slider_boisson")
        const retour2 = document.querySelector(".retour2")
        const ajouterLeMenu = document.querySelector(".ajouterLeMenu")

        // variables modale taille boisson
        const ajouter = document.querySelector(".bouton_tailleBoisson_ajouter")
        const annuler = document.querySelector(".bouton_tailleBoisson_annuler")
        const taille30cl = document.querySelector(".tailleBoisson1")
        const taille50cl = document.querySelector(".tailleBoisson2")

        // Affichage modales menu et taille boisson
        btn_container.addEventListener("click", (e) => {
            const bouton = e.target.closest("button")
            if (bouton && menuTxt.textContent === "Nos menus") {
                overlayMenu.classList.add("active")
            } else if (
                bouton &&
                menuTxt.innerHTML === "Nos Boissons Fraîches"
            ) {
                overlayTailleBoisson.classList.add("active")
            }
        })

        // Clics boutons modale menu
        let selectMenu = false

        menu1.addEventListener("click", () => {
            selectMenu = true
            menu1.classList.add("active")
            menu2.classList.remove("active")


        })
        menu2.addEventListener("click", () => {
            selectMenu = true
            menu2.classList.add("active")
            menu1.classList.remove("active")



        })

        etapeSuivante1.addEventListener("click", () => {
            if (selectMenu) {
                overlayMenu.classList.remove("active")
                overlayFrites.classList.add("active")
                selectMenu = false
            }
        })

        // Clics boutons modale frites / potatoes
        let selectFrites = false

        frites1.addEventListener("click", () => {
            selectFrites = true
            frites2.classList.remove("active")
            frites1.classList.add("active")
        })
        frites2.addEventListener("click", () => {
            selectFrites = true
            frites1.classList.remove("active")
            frites2.classList.add("active")

        })
        etapeSuivante2.addEventListener("click", () => {
            if (selectFrites) {
                overlayFrites.classList.remove("active")
                overlayBoissons.classList.add("active")
                selectMenu = false
            }
        })
        retour1.addEventListener("click", () => {
            selectMenu = false
            selectFrites = false
            overlayFrites.classList.remove("active")
            overlayMenu.classList.add("active")
            menu1.classList.remove("active")
            menu2.classList.remove("active")
            frites1.classList.remove("active")
            frites2.classList.remove("active")
        })

        // Clics boutons modale boisson
        let selectBoisson = false
        let boissonEnCours = ""

        boisson.addEventListener("click", (e) => {
            const drinkButton = e.target.closest("button")
            if (!drinkButton) return
            selectBoisson = true

            boissonEnCours = drinkButton.dataset.boisson
        })

        retour2.addEventListener("click", () => {
            selectFrites = false
            selectBoisson = false
            overlayBoissons.classList.remove("active")
            overlayFrites.classList.add("active")
            frites1.classList.remove("active")
            frites2.classList.remove("active")
        })

        ajouterLeMenu.addEventListener("click", () => {
            menu1.classList.remove("active")
            menu2.classList.remove("active")
            frites1.classList.remove("active")
            frites2.classList.remove("active")
            taille30cl.classList.remove("active")
            taille50cl.classList.remove("active")
        })

        // Clics boutons modale taille boisson
        let selectTailleBoisson = false

        taille30cl.addEventListener("click", () => {
            selectTailleBoisson = true
            tailleBoissonChoisie = "30 cl"
            taille50cl.classList.remove("active")
            taille30cl.classList.add("active")
        })

        taille50cl.addEventListener("click", () => {
            selectTailleBoisson = true
            tailleBoissonChoisie = "50 cl"
            taille30cl.classList.remove("active")
            taille50cl.classList.add("active")
        })

        ajouter.addEventListener("click", () => {
            if (selectTailleBoisson) {
                overlayTailleBoisson.classList.remove("active")

                // Si c'est une boisson individuelle (pas dans un menu)
                if (nomBoissonEnCours) {
                    let prixFinal = prixBoissonEnCours

                    // Ajouter 0.50 € si 50 cl
                    if (tailleBoissonChoisie === "50 cl") {
                        prixFinal += 0.5
                    }

                    // Récupérer la quantité
                    const quantite = Number(nbBoissons.textContent)

                    // Ajouter la boisson au panier avec la quantité
                    ajouterAuPanier(
                        nomBoissonEnCours,
                        prixFinal,
                        [tailleBoissonChoisie],
                        quantite
                    )

                    // Reset
                    nomBoissonEnCours = ""
                    prixBoissonEnCours = 0
                    tailleBoissonChoisie = ""
                    nbBoissons.textContent = 1
                }
            }
            selectTailleBoisson = false
            taille30cl.classList.remove("active")
            taille50cl.classList.remove("active")
        })

        annuler.addEventListener("click", () => {
            overlayTailleBoisson.classList.remove("active")
            taille30cl.classList.remove("active")
            taille50cl.classList.remove("active")

            nbBoissons.textContent = 1
            nomBoissonEnCours = ""
            prixBoissonEnCours = 0
            tailleBoissonChoisie = ""
            selectTailleBoisson = false
        })

        // COUNTER TAILLE BOISSON
        const moins = document.querySelector(".moins")
        const plus = document.querySelector(".plus")
        const nbBoissons = document.querySelector(".nbBoissons")

        moins.addEventListener("click", () => {
            if (nbBoissons.textContent > 1) {
                nbBoissons.textContent = Number(nbBoissons.textContent) - 1
            }
        })
        plus.addEventListener("click", () => {
            if (nbBoissons.textContent < 30) {
                nbBoissons.textContent = Number(nbBoissons.textContent) + 1
            }
        })
        annuler.addEventListener("click", () => {
            nbBoissons.textContent = 1
        })

        // FERMETURE À LA CROIX DES MODALES MENU + TAILLE BOISSON
        const closeModal = document.querySelectorAll(".croix img")

        closeModal.forEach((croix) => {
            croix.addEventListener("click", () => {
                selectMenu = false
                selectFrites = false
                selectBoisson = false
                selectTailleBoisson = false
                overlayMenu.classList.remove("active")
                overlayTailleBoisson.classList.remove("active")
                overlayFrites.classList.remove("active")
                overlayBoissons.classList.remove("active")
                menu1.classList.remove("active")
                menu2.classList.remove("active")
                frites1.classList.remove("active")
                frites2.classList.remove("active")
                taille30cl.classList.remove("active")
                taille50cl.classList.remove("active")
            })
        })

        // FERMETURE, AU CLIC SUR L'OVERLAY, DES MODALES MENU + TAILLE BOISSON
        const allOverlays = [
            overlayMenu,
            overlayFrites,
            overlayBoissons,
            overlayTailleBoisson,
        ]

        allOverlays.forEach((oneOverlay) => {
            oneOverlay.addEventListener("click", (e) => {
                if (e.target !== oneOverlay) return

                selectMenu = false
                selectFrites = false
                selectBoisson = false
                selectTailleBoisson = false
                overlayMenu.classList.remove("active")
                overlayTailleBoisson.classList.remove("active")
                overlayFrites.classList.remove("active")
                overlayBoissons.classList.remove("active")
                menu1.classList.remove("active")
                menu2.classList.remove("active")
                frites1.classList.remove("active")
                frites2.classList.remove("active")
                taille30cl.classList.remove("active")
                taille50cl.classList.remove("active")
            })
        })

        // CHARGEMENT DES BOISSONS DU SLIDER DE LA MODALE BOISSONS (menu)
        const slider2 = document.querySelector(".slider_boisson")

        prod.boissons.forEach((drinkSlide) => {
            const drinkChoice = document.createElement("button")

            drinkChoice.dataset.boisson = drinkSlide.nom
            drinkChoice.innerHTML = `
            <img src="ASSETS${drinkSlide.image}" alt="${drinkSlide.nom}">
            <span>${drinkSlide.nom}</span>
            `
            slider2.append(drinkChoice)
        })

        // FONCTION DU SLIDER BOISSONS
        initSliderBoissons()

        // *****************************
        // ----- GESTION DU PANIER -----
        // *****************************

        // Variables pour les menus
        let nomMenuEnCours = ""
        let prixMenuEnCours = 0
        let maxiOuBestOf = ""
        let fritesOuPotatoes = ""

        // Variables pour les boissons individuelles
        let nomBoissonEnCours = ""
        let prixBoissonEnCours = 0
        let tailleBoissonChoisie = ""

        const containerMenus = document.querySelector(".nos_menus_img")

        function categorieActuelle() {
            return document
                .querySelector(".nos_menus_txt h1")
                .textContent.toLowerCase()
        }

        function estUnMenu() {
            return categorieActuelle().includes("menu")
        }

        containerMenus.addEventListener("click", (event) => {
            const bouton = event.target.closest("button")
            if (!bouton) return

            const nom = bouton.querySelector(
                ".nos_menus_img--nomEtPrix p"
            ).textContent

            const prixTexte = bouton.querySelector(
                ".nos_menus_img--nomEtPrix p:last-child"
            ).textContent

            const prix = parseFloat(prixTexte.replace(",", "."))

            // Si c'est un menus
            if (estUnMenu()) {
                nomMenuEnCours = nom
                prixMenuEnCours = prix
                return
            }

            // Si c'est une boisson individuelle (modale taille boisson)
            if (categorieActuelle().includes("boisson")) {
                nomBoissonEnCours = nom
                prixBoissonEnCours = prix
                return
            }

            // Si c'est un produit simple → ajout direct
            ajouterAuPanier(nom, prix, (options = []))
        })

        // Ajout de "Maxi Best of" ou "Best Of" avant le nom du menu
        const boutonMaxiBestOf = document.querySelector(".modalButtonMenu1")
        const boutonBestOf = document.querySelector(".modalButtonMenu2")

        boutonMaxiBestOf.addEventListener("click", () => {
            if (maxiOuBestOf === "Menu Best Of") {
                maxiOuBestOf = "Menu Maxi Best Of"
            }
            maxiOuBestOf = "Menu Maxi Best Of"
        })

        boutonBestOf.addEventListener("click", () => {
            if (maxiOuBestOf === "Menu Maxi Best Of") {
                maxiOuBestOf = "Menu Best Of"
            }
            maxiOuBestOf = "Menu Best Of"
        })

        // Ajout de "Frites" ou "Potatoes"
        const boutonFrites = document.querySelector(".modalButtonfrites1")
        const boutonPotatoes = document.querySelector(".modalButtonfrites2")

        boutonFrites.addEventListener("click", () => {
            fritesOuPotatoes = "Frites"
        })

        boutonPotatoes.addEventListener("click", () => {
            fritesOuPotatoes = "Potatoes"
        })

        // Clic sur "Ajouter le menu à ma commande" (dans la modale choix boisson)
        ajouterLeMenu.addEventListener("click", () => {
            if (!selectBoisson) return

            overlayBoissons.classList.remove("active")

            // Ajout du menu COMPLET au panier avec toutes les options
            const nomSansMenu = nomMenuEnCours.replace(/^menu\s+/i, "")
            const nomComplet = `${maxiOuBestOf} ${nomSansMenu}`

            // Calcul du prix : + 1 € si Menu Maxi Best Of
            if (maxiOuBestOf === "Menu Maxi Best Of") {
                prixMenuEnCours += 1
            }

            // Récupération des options : frites + boisson
            const toutesLesOptions = []

            if (fritesOuPotatoes) {
                toutesLesOptions.push(fritesOuPotatoes)
            }

            if (boissonEnCours) {
                toutesLesOptions.push(boissonEnCours)
            }

            ajouterAuPanier(nomComplet, prixMenuEnCours, toutesLesOptions)

            // Reset pour le prochain menu
            selectBoisson = false
            nomMenuEnCours = ""
            prixMenuEnCours = 0
            maxiOuBestOf = ""
            fritesOuPotatoes = ""
            boissonEnCours = ""
        })

        // AJOUT AU PANIER
        function ajouterAuPanier(
            nom,
            prix,
            options = [],
            quantiteAAjouter = 1
        ) {
            // Convertion des options en string pour comparer facilement
            const optionsStr = JSON.stringify(options)

            // Chercher si un produit identique existe déjà dans le panier
            const produitExistant = panier.find(
                (item) =>
                    item.nom === nom &&
                    item.prix === prix &&
                    JSON.stringify(item.options) === optionsStr
            )

            if (produitExistant) {
                // Si le produit existe déjà, on augmente la quantité
                produitExistant.quantite += quantiteAAjouter
            } else {
                // Sinon on ajoute un nouveau produit
                panier.push({
                    id: Date.now(),
                    nom,
                    prix,
                    options,
                    quantite: quantiteAAjouter,
                })
            }

            afficherPanier()
            sauvegarderPanier() // Sauvegarde dans le localStorage
        }

        // AFFICHAGE DU PANIER
        function afficherPanier() {
            const ulMenus = document.querySelector(".ul_menus")
            ulMenus.innerHTML = ""

            panier.forEach((dicoPanier) => {
                const liMenu = document.createElement("li")

                liMenu.classList.add("liste_menu")

                liMenu.innerHTML = `
                <div class="choix_menu_item">
                    <strong>${dicoPanier.quantite} ${dicoPanier.nom}</strong>
                    <button class="trash" data-id="${dicoPanier.id}">
                    <img src="ASSETS/images/trash.png" alt="logo supprimer">
                    </button>
                </div>
                <ul class="detail_menu"></ul>
                `

                const ulOptions = liMenu.querySelector(".detail_menu")

                dicoPanier.options.forEach((option) => {
                    const liOption = document.createElement("li")
                    liOption.textContent = option
                    ulOptions.append(liOption)
                })

                ulMenus.append(liMenu)
            })

            MaJtotal()
        }

        // SUPPRIMER
        document
            .querySelector(".ul_menus")
            .addEventListener("click", (event) => {
                const cibleTrash = event.target.closest(".trash")
                if (!cibleTrash) return

                const dateNow = Number(cibleTrash.dataset.id)
                // dataset.id vient récupérer (dans le HTML) data-id = "Date.now()" qui est une chaîne de caractères
                // 1 date.now par trash
                panier = panier.filter(
                    (dicoPanier) => dicoPanier.id !== dateNow
                )

                afficherPanier()
                sauvegarderPanier() // Sauvegarde dans le localStorage
            })

        // TOTAL
        function MaJtotal() {
            const total = panier.reduce((sum, dicoPanier) => {
                return sum + dicoPanier.prix * dicoPanier.quantite
            }, 0)

            document.querySelector(".tarif").textContent =
                total.toFixed(2).replace(".", ",") + " €"
        }

        // SAUVEGARDE DU PANIER DANS LE LOCAL STORAGE
        function sauvegarderPanier() {
            localStorage.setItem("panier", JSON.stringify(panier))
        }

        // AFFICHAGE DU PANIER AU CHARGEMENT DE LA PAGE
        afficherPanier()

        // BOUTON ABANDON --> Vider le panier
        document.querySelector(".abandon").addEventListener("click", () => {
            panier = []

            // Réafficher le panier vide
            afficherPanier()
            sauvegarderPanier() // Sauvegarde dans le localStorage
        })

        // ***********
        // --- API ---
        // ***********

        const boutonPayer = document.querySelector(".payer")
        const fermerConf = document.querySelector(".fermer")
        const overlayConf = document.querySelector(".overlayConf")
        const messageConf = document.querySelector(".messageConf")
        
        function envoyerCommande() {
            const today = new Date()
            const totalApayer = document.querySelector(".tarif").textContent

            const orderData = {
                    orderNb: numeroCommande.textContent,
                    date: today.toLocaleDateString("fr-FR", {
                        day: "2-digit",
                        month: "2-digit",
                        year: "numeric",
                        hour: "2-digit",
                        minute: "2-digit"
                    }),
                    produits: panier,
                    total: totalApayer
                }


            fetch("data:application/json,{\"success\":true}", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(orderData)
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error("Erreur lors de l'envoi de la commande")
                    }
                    return response.json()
                })
                .then((data) => {
                    if (!data.success) {
                        throw new Error("Commande refusée")
                    }
                    panier = []
                    localStorage.removeItem("panier")
                    messageConf.innerHTML =
                        `Votre commande a bien<br>été prise en compte<br>✅`
                })
                .catch((error) => {
                    messageConf.innerHTML =
                        `❌ Une erreur est survenue.<br>Veuillez réessayer.`
                })
            }
            
            // Clic bouton payer
            boutonPayer.addEventListener("click", () => {
                if (panier.length > 0) {
                    envoyerCommande()
                    overlayConf.classList.remove("hidden")
                    fermerConf.focus()
            }
        })


        //  Clic bouton fermer (modale confirmation commande)
        fermerConf.addEventListener("click", () => {    
            if (messageConf.innerHTML === `Votre commande a bien<br>été prise en compte<br>✅`) {
                surPlaceOuAemporter.textContent === "À emporter" ? 
                (window.location.href = "merci.html") :
                (window.location.href = "chevalet.html") 
            }
            overlayConf.classList.add("hidden")
        })

        
    }) //fin du .then

    // GESTION DES ERREURS
    .catch((erreur) => {
        console.error(erreur.message)

        const messageDerreur1 = document.querySelector(".nos_menus_img")
        messageDerreur1.innerHTML = `
        <p class="error">
            ❌ Impossible de charger les données.<br>
            Veuillez réessayer plus tard.
        </p>
        `

        const messageDerreur2 = document.querySelector(".nav_images_container")
        messageDerreur2.innerHTML = `
        <p class="error">
            ❌ Impossible de charger les données.<br>
            Veuillez réessayer plus tard.
        </p>
        `
        const messageDerreur3 = document.querySelector(".slider_boisson")
        if (messageDerreur3) {
            messageDerreur3.innerHTML = `
                <p class="error">❌ Impossible de charger les données.</p>
                `
        }
    })
