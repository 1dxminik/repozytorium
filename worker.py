import pika
import json
import sqlite3
import requests
import os
import sys  # <--- Dodałem brakujący import
from ultralytics import YOLO
import cv2

# Ładowanie modelu
model = YOLO("yolov8n.pt")

RESULTS_DB = "results.db"
PROCESSED_DIR = "processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)


def update_db(task_id, status, count):
    try:
        conn = sqlite3.connect(RESULTS_DB)
        c = conn.cursor()
        c.execute("UPDATE tasks SET status=?, count=? WHERE id=?", (status, count, task_id))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f" [!] Database error: {e}")


def process_image(task_data):
    task_id = task_data['id']
    img_path = ""

    try:
        # 1. Pobieranie obrazu
        if task_data['type'] == 'url':
            img_path = f"temp_{task_id}.jpg"
            resp = requests.get(task_data['url'], timeout=5)  # Timeout żeby nie wisiało
            if resp.status_code != 200:
                raise Exception(f"Download failed: {resp.status_code}")
            with open(img_path, 'wb') as f:
                f.write(resp.content)
        else:
            img_path = task_data['path']

        # 2. Sprawdzenie czy plik jest poprawnym obrazem (To naprawia crash)
        img_check = cv2.imread(img_path)
        if img_check is None:
            raise Exception("Invalid image file or download blocked")

        # 3. ANALIZA AI
        results = model.predict(img_path, save=False, classes=[0], verbose=False)
        count = len(results[0].boxes)

        # 4. Rysowanie i zapis
        result_img = results[0].plot()
        save_path = f"{PROCESSED_DIR}/{task_id}_result.jpg"
        cv2.imwrite(save_path, result_img)

        # Sprzątanie
        if task_data['type'] == 'url' and os.path.exists(img_path):
            os.remove(img_path)

        print(f" [x] Task {task_id} DONE. People: {count}")
        update_db(task_id, "DONE", count)

    except Exception as e:
        # Teraz worker nie umrze, tylko wypisze błąd i pójdzie dalej!
        print(f" [!] Error processing {task_id}: {str(e)[:50]}...")
        update_db(task_id, "ERROR", 0)
        # Sprzątanie po błędzie
        if 'img_path' in locals() and task_data['type'] == 'url' and os.path.exists(img_path):
            try:
                os.remove(img_path)
            except:
                pass


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)

    def callback(ch, method, properties, body):
        data = json.loads(body)
        process_image(data)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    print(' [*] Workery gotowe. Czekam na zadania...')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Zamykanie workera...')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)