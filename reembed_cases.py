"""
Re-generate embeddings for all cases that have empty embeddings.
Uses a fallback chain of detectors: ssd → opencv → retinaface → enforce_detection=False
Run: python reembed_cases.py
"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.models.database import get_connection
from app.config import config

print("Loading DeepFace (first run may download models, ~1 min)...")
from deepface import DeepFace
print("DeepFace loaded.\n")

DETECTORS = ["ssd", "opencv", "retinaface"]

def get_embedding_with_fallback(image_path):
    """Try multiple detectors; last resort: enforce_detection=False."""
    for backend in DETECTORS:
        try:
            results = DeepFace.represent(
                img_path=image_path,
                model_name="ArcFace",
                detector_backend=backend,
                enforce_detection=True,
            )
            print(f"    ✅ Succeeded with detector: {backend}")
            return results[0]["embedding"]
        except Exception as e:
            print(f"    ⚠️  {backend} failed: {e}")

    # Final fallback – no detection enforcement (whole-image embedding)
    try:
        results = DeepFace.represent(
            img_path=image_path,
            model_name="ArcFace",
            detector_backend="opencv",
            enforce_detection=False,
        )
        print("    ✅ Succeeded with enforce_detection=False (fallback).")
        return results[0]["embedding"]
    except Exception as e:
        raise RuntimeError(f"All detectors failed: {e}")


conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT id, missing_full_name, image_path FROM cases WHERE embedding = '' OR embedding IS NULL")
cases = cursor.fetchall()

if not cases:
    print("All cases already have embeddings. Nothing to do.")
    conn.close()
    sys.exit(0)

print(f"Found {len(cases)} case(s) with missing embeddings.\n")

success = 0
failed = 0

for case in cases:
    image_path = os.path.join(config.UPLOAD_FOLDER, case["image_path"])
    print(f"Case {case['id']}: {case['missing_full_name']}  ({case['image_path']})")

    if not os.path.exists(image_path):
        print(f"    ❌ Image file not found at: {image_path}\n")
        failed += 1
        continue

    try:
        embedding = get_embedding_with_fallback(image_path)
        embedding_json = json.dumps(embedding)

        update_cursor = conn.cursor()
        update_cursor.execute(
            "UPDATE cases SET embedding = ? WHERE id = ?",
            (embedding_json, case["id"])
        )
        conn.commit()
        print(f"    💾 Saved embedding ({len(embedding)} dims).\n")
        success += 1
    except Exception as e:
        print(f"    ❌ All detectors failed: {e}\n")
        failed += 1

conn.close()
print(f"Done. ✅ {success} succeeded  ❌ {failed} failed.")
