try:
    from deepface import DeepFace
    print("Found deepface")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
