import os
import json
import numpy as np

MODEL_NAME = "ArcFace"
DETECTOR_BACKEND = "retinaface"   # more reliable than opencv
DISTANCE_METRIC = "cosine"
MATCH_THRESHOLD = 0.55   # cosine distance; real-world webcam needs a little slack


def get_embedding(image_path: str) -> list:
    """
    Extract a face embedding from an image file.
    Returns a flat list of floats, or raises an exception if no face is found.
    """
    from deepface import DeepFace  # lazy import — avoids blocking startup with TF init
    result = DeepFace.represent(
        img_path=image_path,
        model_name=MODEL_NAME,
        detector_backend=DETECTOR_BACKEND,
        align=True,              # align face before embedding — critical for ArcFace
        enforce_detection=True,
    )
    # result is a list of dicts; take the first detected face
    return result[0]["embedding"]


def embedding_from_frame(frame_bgr) -> list:
    """
    Extract a face embedding directly from an OpenCV BGR numpy array.
    """
    from deepface import DeepFace  # lazy import — avoids blocking startup with TF init
    result = DeepFace.represent(
        img_path=frame_bgr,
        model_name=MODEL_NAME,
        detector_backend=DETECTOR_BACKEND,
        align=True,              # align face before embedding — critical for ArcFace
        enforce_detection=True,
    )
    return result[0]["embedding"]


def cosine_distance(emb1: list, emb2: list) -> float:
    a = np.array(emb1)
    b = np.array(emb2)
    return 1.0 - np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def match_against_cases(probe_embedding: list, cases: list) -> list:
    """
    Compare a probe embedding against all cases.

    Args:
        probe_embedding : embedding from the webcam frame
        cases           : list of sqlite3.Row objects with 'id', 'missing_full_name',
                          'image_path', 'embedding' columns

    Returns:
        List of matched cases sorted by distance (closest first).
        Each item: { 'case': row, 'distance': float, 'matched': bool }
    """
    results = []
    for case in cases:
        try:
            stored_emb = json.loads(case["embedding"])
        except (json.JSONDecodeError, TypeError):
            continue

        dist = cosine_distance(probe_embedding, stored_emb)
        results.append({
            "case": case,
            "distance": round(dist, 4),
            "matched": dist <= MATCH_THRESHOLD,
        })

    results.sort(key=lambda x: x["distance"])
    return results
