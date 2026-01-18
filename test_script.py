import requests
import time
import os
import glob
from concurrent.futures import ThreadPoolExecutor

# Adres API
API_URL = "http://127.0.0.1:8000/detect/local"
DATASET_DIR = "dataset_photos"

# Pobieramy listę plików
files = [os.path.abspath(p) for p in glob.glob(f"{DATASET_DIR}/*.jpg")]


def send_request(file_path):
    try:
        # Timeout ważny, żeby nie wisiało w nieskończoność
        response = requests.get(API_URL, params={"path": file_path}, timeout=5)
        if response.status_code == 200:
            print(f"[OK] Wysłano: {os.path.basename(file_path)}")
        else:
            print(f"[ERROR] Kod {response.status_code} dla {file_path}")
    except Exception as e:
        print(f"[CRITICAL] Błąd połączenia: {e}")


def main():
    if not files:
        print("Folder pusty! Uruchom generate_dataset.py")
        return

    print(f"Kolejkuję {len(files)} zdjęć używając puli wątków...")
    start = time.time()

    # Używamy max_workers=50. To wystarczająco dużo, żeby kolejka rosła błyskawicznie,
    # ale wystarczająco mało, żeby nie zawiesić Windowsa (błąd 10061).
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(send_request, files)

    end = time.time()
    print(f"\nSUKCES: Przetworzono {len(files)} plików w {end - start:.2f} s.")


if __name__ == "__main__":
    main()