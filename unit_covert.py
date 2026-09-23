def convertir_unite(valeur, type_conversion):
    """Effectue la conversion demandée et retourne le résultat et l'unité."""
    table_conversions = {
        "km_vers_miles": (lambda v: v * 0.621371, "mi"),
        "miles_vers_km": (lambda v: v * 1.60934, "km"),
        "kg_vers_livres": (lambda v: v * 2.20462, "lb"),
        "livres_vers_kg": (lambda v: v * 0.453592, "kg"),
        "celsius_vers_fahrenheit": (lambda v: (v * 9 / 5) + 32, "°F"),
        "fahrenheit_vers_celsius": (lambda v: (v - 32) * 5 / 9, "°C"),
    }

    regle = table_conversions.get(type_conversion)
    if regle:
        fonction_calcul, symbole_unite = regle
        return fonction_calcul(valeur), symbole_unite

    return None, None


def afficher_menu():
    """Affiche l'interface du menu principal."""
    print("\n" + "=" * 50)
    print("      CONVERTISSEUR D'UNITÉS INTELLIGENT")
    print("=" * 50)
    print("1. Kilomètres (km) → Miles (mi)")
    print("2. Miles (mi)      → Kilomètres (km)")
    print("3. Kilogrammes (kg) → Livres (lb)")
    print("4. Livres (lb)     → Kilogrammes (kg)")
    print("5. Celsius (°C)    → Fahrenheit (°F)")
    print("6. Fahrenheit (°F) → Celsius (°C)")
    print("Q. Quitter le programme")
    print("=" * 50)


def executer_convertisseur():
    """Gère la boucle d'interaction avec l'utilisateur."""
    correspondance_menu = {
        "1": "km_vers_miles",
        "2": "miles_vers_km",
        "3": "kg_vers_livres",
        "4": "livres_vers_kg",
        "5": "celsius_vers_fahrenheit",
        "6": "fahrenheit_vers_celsius",
    }

    while True:
        afficher_menu()
        choix_utilisateur = (
            input("\nChoisissez une option (1-6 ou Q) : ").strip().lower()
        )

        # Condition de sortie de la boucle
        if choix_utilisateur == "q":
            print("\nMerci d'avoir utilisé le convertisseur. À bientôt !")
            break

        type_conversion = correspondance_menu.get(choix_utilisateur)

        if not type_conversion:
            print("\n[Erreur] Choix invalide. Veuillez réessayer.")
            continue

        # Saisie sécurisée de la valeur numérique
        try:
            valeur_saisie = float(
                input("Entrez la valeur à convertir : ").replace(",", ".")
            )
        except ValueError:
            print(
                "\n[Erreur] Saisie incorrecte. Veuillez entrer un nombre valide."
            )
            continue

        # Calcul et affichage du résultat
        resultat, symbole = convertir_unite(valeur_saisie, type_conversion)

        print("\n" + "-" * 50)
        print(f"Résultat : {valeur_saisie} -> {resultat:.2f} {symbole}")
        print("-" * 50)


if __name__ == "__main__":
    executer_convertisseur()
