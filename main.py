import cv2
import numpy as np
import uuid
import os
import requests
import uvicorn
from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from pydantic import BaseModel


PROTO_PATH = "deploy.prototxt"
MODEL_PATH = "mobilenet_iter_73000.caffemodel"
MIN_CONFIDENCE = 0.5
CLASS_ID_PERSON = 15

app = FastAPI(title="System Detekcji Osób", version="1.0")
results_storage = {}


try:
    dnn_net = cv2.dnn.readNetFromCaffe(PROTO_PATH, MODEL_PATH)
    print("Model załadowany")
except cv2.error:
    print(f"Nie znaleziono plików: '{PROTO_PATH}' lub '{MODEL_PATH}'")

    dnn_net = None


class DetectionResponse(BaseModel):
    id: str
    detected_count: int
    status: str


def process_image(image_data, request_id: str) -> int:
    if dnn_net is None:
        return 0

    (h, w) = image_data.shape[:2]


    blob = cv2.dnn.blobFromImage(
        cv2.resize(image_data, (300, 300)),
        0.007843, (300, 300), 127.5
    )

    dnn_net.setInput(blob)
    detections = dnn_net.forward()

    people_count = 0

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > MIN_CONFIDENCE:
            idx = int(detections[0, 0, i, 1])

            if idx == CLASS_ID_PERSON:
                people_count += 1


                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (start_x, start_y, end_x, end_y) = box.astype("int")


                cv2.rectangle(image_data, (start_x, start_y),
                              (end_x, end_y), (0, 255, 0), 2)


                label = f"Person: {confidence:.2f}"
                text_y = start_y - 10 if start_y - 10 > 10 else start_y + 10
                cv2.putText(image_data, label, (start_x, text_y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)


    output_filename = f"result_{request_id}.jpg"
    cv2.imwrite(output_filename, image_data)

    return people_count



@app.get("/analyze/local_file", response_model=DetectionResponse)
async def analyze_local(path: str):

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Plik nie istnieje.")

    req_id = str(uuid.uuid4())
    img = cv2.imread(path)

    if img is None:
        raise HTTPException(status_code=400, detail="Błąd odczytu obrazu.")

    count = process_image(img, req_id)

    response = {"id": req_id, "detected_count": count, "status": "completed"}
    results_storage[req_id] = response
    return response


@app.get("/analyze/from_url", response_model=DetectionResponse)
async def analyze_url(url: str = Query(...)):
    req_id = str(uuid.uuid4())
    try:

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.124 Safari/537.36"
        }


        r = requests.get(url, headers=headers, timeout=10)


        if r.status_code != 200:
            raise ValueError(f"Serwer odrzucił połączenie. Kod: {r.status_code}")

        arr = np.asarray(bytearray(r.content), dtype="uint8")
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Niepoprawny format obrazu (pobrano dane, ale to nie zdjęcie)")

        count = process_image(img, req_id)

        response = {"id": req_id, "detected_count": count, "status": "completed"}
        results_storage[req_id] = response
        return response

    except Exception as e:
        #
        print(f"Błąd przetwarzania URL: {e}")
        raise HTTPException(status_code=400, detail=f"Błąd URL: {str(e)}")


@app.post("/analyze/upload", response_model=DetectionResponse)
async def analyze_upload(file: UploadFile = File(...)):

    req_id = str(uuid.uuid4())

    content = await file.read()
    nparr = np.frombuffer(content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    count = process_image(img, req_id)

    response = {"id": req_id, "detected_count": count, "status": "completed"}
    results_storage[req_id] = response
    return response


@app.get("/results/{request_id}")
async def get_result(request_id: str):

    if request_id not in results_storage:
        raise HTTPException(status_code=404, detail="Zadanie nieznane.")
    return results_storage[request_id]


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)