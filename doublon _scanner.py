import hashlib
import os
from tqdm import tqdm

SDCARD = "/sdcard"

# Dossiers système à ignorer
EXCLUDED_PATHS = [
    "/sdcard/Android",
]


def get_file_hash(filepath, block_size=65536):
    """Calcule le hash MD5 d'un fichier."""
    hasher = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            buf = f.read(block_size)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(block_size)
        return hasher.hexdigest()
    except (PermissionError, FileNotFoundError, OSError):
        return None


def collect_all_files(root_path):
    """Indexe tous les fichiers valides du stockage."""
    all_files = []
    print(" Indexation des fichiers en cours...")

    for root, dirs, files in os.walk(root_path, onerror=lambda e: None):
        if any(root.startswith(excluded) for excluded in EXCLUDED_PATHS):
            continue

        for filename in files:
            filepath = os.path.join(root, filename)
            if not os.path.islink(filepath):
                all_files.append(filepath)

    return all_files


def find_duplicates(root_path):
    all_files = collect_all_files(root_path)

    # Étape 1 : Filtrage par taille
    files_by_size = {}
    print("\n[1/2] Analyse de la taille des fichiers...")

    for filepath in tqdm(all_files, desc="Taille", unit="fichiers"):
        try:
            size = os.path.getsize(filepath)
            if size > 0:
                files_by_size.setdefault(size, []).append(filepath)
        except (PermissionError, FileNotFoundError, OSError):
            continue

    potential_duplicates = [
        paths for paths in files_by_size.values() if len(paths) > 1
    ]
    total_candidates = sum(len(paths) for paths in potential_duplicates)

    if not potential_duplicates:
        return {}

    # Étape 2 : Calcul des signatures MD5
    duplicates = {}
    print(
        f"\n[2/2] Vérification du contenu MD5 ({total_candidates} fichiers suspects)..."
    )

    with tqdm(
        total=total_candidates, desc="Calcul MD5", unit="fichiers"
    ) as pbar:
        for paths in potential_duplicates:
            files_by_hash = {}
            for filepath in paths:
                file_hash = get_file_hash(filepath)
                if file_hash:
                    files_by_hash.setdefault(file_hash, []).append(filepath)
                pbar.update(1)

            for file_hash, confirmed_paths in files_by_hash.items():
                if len(confirmed_paths) > 1:
                    duplicates[file_hash] = confirmed_paths

    return duplicates


def interactive_delete(duplicates):
    """Interface interactive pour lister et choisir les doublons à supprimer."""
    total_deleted = 0
    bytes_freed = 0
    total_groups = len(duplicates)

    print("\n" + "=" * 60)
    print(" SELECTION INTERACTIVE DES DOUBLONS A SUPPRIMER")
    print("=" * 60)

    for idx, (file_hash, paths) in enumerate(duplicates.items(), start=1):
        try:
            file_size = os.path.getsize(paths[0]) / (1024 * 1024)
        except OSError:
            file_size = 0.0

        print(f"\n--- Groupe {idx}/{total_groups} (Taille : {file_size:.2f} Mo) ---")

        # Affichage de tous les fichiers du groupe avec un numéro
        for i, filepath in enumerate(paths, start=1):
            tag = " [Par défaut conservé]" if i == 1 else ""
            print(f"  [{i}]{tag} : {filepath}")

        print("\nOptions :")
        print(" - Entrez les numéros à SUPPRIMER séparés par un espace (ex: 2 3)")
        print(" - Entrez 'a' pour supprimer TOUS les doublons (sauf le [1])")
        print(" - Appuyez sur ENTRÉE pour ignorer ce groupe")

        choice = input("\nVotre choix : ").strip().lower()

        if not choice or choice == "0":
            print(" -> Aucun fichier supprimé dans ce groupe.")
            continue

        to_delete_indices = []

        if choice == "a":
            # Supprimer tous sauf le premier
            to_delete_indices = list(range(2, len(paths) + 1))
        else:
            # Traiter les numéros entrés par l'utilisateur
            raw_inputs = choice.replace(",", " ").split()
            for item in raw_inputs:
                if item.isdigit():
                    num = int(item)
                    if 1 <= num <= len(paths):
                        to_delete_indices.append(num)
                    else:
                        print(f" -> Numéro {num} invalide (ignoré).")

        # Suppression des fichiers sélectionnés
        for num in set(to_delete_indices):
            target_path = paths[num - 1]
            try:
                size = os.path.getsize(target_path)
                os.remove(target_path)
                print(f" -> Supprimé [{num}] : {target_path}")
                total_deleted += 1
                bytes_freed += size
            except Exception as e:
                print(f" -> Erreur lors de la suppression de [{num}] : {e}")

    megabytes = bytes_freed / (1024 * 1024)
    print("\n" + "=" * 60)
    print(
        f" FIN DU NETTOYAGE : {total_deleted} fichier(s) supprimé(s). {megabytes:.2f} Mo libérés."
    )
    print("=" * 60)


if __name__ == "__main__":
    if os.path.exists(SDCARD):
        dupes = find_duplicates(SDCARD)
        if dupes:
            print(f"\n {len(dupes)} groupe(s) de doublons identifié(s).")
            interactive_delete(dupes)
        else:
            print("\nAucun doublon trouvé !")
    else:
        print("Erreur : Impossible d'accéder au stockage de l'appareil.")
