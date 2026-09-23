from pathlib import Path
 # Extensions considérées comme potentiellement suspectes

EXTENSIONS_SUSPECTES = { ".exe", ".bat",".cmd"
".scr",".vbs",".ps1",".jar",
".msi"
 }
# Demander le chemin du dossier à analyser
dossier = Path(input("Entrez le chemin du dossier: ").strip())
# Vérifier si le dossier existe
if not dossier.is_dir():
    print("Dossier introuvable !")
    exit()

fichiers_suspects = []
 # Parcourir tous les fichiers dans le dossier et ses sous-dossiers
for fichier in dossier.rglob("*"):
    if not fichier.is_file():
        continue 

extension = fichier.suffix.lower()
 # Si l'extension est dans la liste des extensions suspectes
if extension in EXTENSIONS_SUSPECTES:
    fichiers_suspects.append(fichier)

# Affichage des résultats
    print("\n" + "==" * 60)
    print("SCAN DES FICHIERS SUSPECTS")

    print("==" * 60)

if not fichiers_suspects:
    print("\n Aucun fichier suspect trouvé.")
else:
    print(f"\nA {len (fichiers_suspects)} fichier (s) suspect(s) trouvé(s):\n")

for fichier in fichierers_suspects:
     print(f" - {fichier}")
     print("\n" + "==" * 60)