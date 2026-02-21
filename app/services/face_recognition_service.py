import os
import json
import cv2
import numpy as np
import sys

# Windows isolation fix: If twilio is missing from system path, check User Roaming site-packages
try:
    import twilio
except ImportError:
    user_site = os.path.expanduser("~") + r"\AppData\Roaming\Python\Python310\site-packages"
    if user_site not in sys.path:
        sys.path.append(user_site)
    try:
        import twilio
    except ImportError:
        # Fallback for other potential python versions if needed
        pass

# Lazy load DeepFace to keep application startup fast
_deepface = None

def get_deepface():
    global _deepface
    if _deepface is None:
        from deepface import DeepFace
        _deepface = DeepFace
    return _deepface

# ── Configuration ─────────────────────────────────────────────────────────────
# opencv: ~2-5 sec (fast, good for live scan) | ssd: ~5-10 sec | retinaface: ~15-30 sec (most accurate)
MODEL_NAME = "ArcFace"
DETECTOR_BACKEND = os.getenv("DEEPFACE_DETECTOR", "opencv")
DISTANCE_METRIC = "cosine"
MATCH_THRESHOLD = 0.55   # Cosine distance; 0.55 is a good balance for ArcFace


def get_embedding(image_path: str) -> list:
    """
    Extract a face embedding from an image file.
    Ensures RGB conversion for consistency.
    """
    DeepFace = get_deepface()
    
    # Load image and convert to RGB (DeepFace needs RGB for consistent embeddings)
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image at {image_path}")
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    result = DeepFace.represent(
        img_path=img_rgb,
        model_name=MODEL_NAME,
        detector_backend=DETECTOR_BACKEND,
        align=True,
        enforce_detection=True,
    )
    # Pick the largest face if multiple are found (DeepFace returns them sorted by size usually, but let's be safe)
    best_face = result[0]
    return best_face["embedding"]


def embedding_from_frame(frame_bgr) -> list:
    """
    Extract a face embedding directly from an OpenCV BGR numpy array.
    Ensures RGB conversion before passing to DeepFace.
    """
    DeepFace = get_deepface()
    
    # CRITICAL: Convert BGR to RGB
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    
    result = DeepFace.represent(
        img_path=frame_rgb,
        model_name=MODEL_NAME,
        detector_backend=DETECTOR_BACKEND,
        align=True,
        enforce_detection=True,
    )
    return result[0]["embedding"]


def cosine_distance(emb1: list, emb2: list) -> float:
    """
    Calculate normalized cosine distance.
    Distance = 1 - Cosine Similarity
    """
    a = np.array(emb1)
    b = np.array(emb2)

    # Explicit normalization ensures magnitudes don't interfere
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)

    return float(1.0 - np.dot(a, b))


def match_against_cases(probe_embedding: list, cases: list) -> list:
    """
    Compare a probe embedding against all cases using consolidated logic.
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
