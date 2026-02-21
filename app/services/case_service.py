import os
import json
import uuid
import shutil
import numpy as np
from app.models.database import get_connection
from app.config import config

def save_case(data: dict, image_file):
    """
    Saves a missing person case to the database, including image and embedding.
    """
    # 1. Save the image file
    os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
    ext = image_file.filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    image_path = os.path.join(config.UPLOAD_FOLDER, filename)
    
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image_file.file, buffer)

    # 2. Generate Face Embedding using DeepFace (with detector fallback chain)
    embedding_json = ""
    try:
        from deepface import DeepFace  # lazy import to avoid blocking server startup

        _detectors = ["opencv", "ssd", "retinaface"]
        _embedding = None

        for _backend in _detectors:
            try:
                _res = DeepFace.represent(
                    img_path=image_path,
                    model_name="ArcFace",
                    detector_backend=_backend,
                    enforce_detection=True,
                )
                _embedding = _res[0]["embedding"]
                break  # stop on first success
            except Exception:
                continue

        if _embedding is None:
            # Last resort: skip enforcement so we still get an embedding
            _res = DeepFace.represent(
                img_path=image_path,
                model_name="ArcFace",
                detector_backend="opencv",
                enforce_detection=False,
            )
            _embedding = _res[0]["embedding"]

        if _embedding:
            embedding_json = json.dumps(_embedding)
    except Exception as e:
        print(f"Embedding error: {e}")

    # 3. Save to Database
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO cases (
            missing_full_name, gender, age, missing_state, missing_city, 
            pin_code, missing_date, missing_time, description, image_path, embedding,
            complainant_name, relationship, complainant_phone, address_line1
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("missing_full_name"),
        data.get("gender"),
        data.get("age"),
        data.get("missing_state"),
        data.get("missing_city"),
        data.get("pin_code"),
        data.get("missing_date"),
        data.get("missing_time"),
        data.get("description"),
        filename, # store relative path/filename
        embedding_json,
        data.get("complainant_name"),
        data.get("relationship"),
        data.get("complainant_phone"),
        data.get("address_line1")
    ))
    
    case_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return case_id

def get_recent_cases(limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cases ORDER BY created_at DESC LIMIT ?", (limit,))
    cases = cursor.fetchall()
    conn.close()
    return cases

def get_case_by_id(case_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cases WHERE id = ?", (case_id,))
    case = cursor.fetchone()
    conn.close()
    return case
