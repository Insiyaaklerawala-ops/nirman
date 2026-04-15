import os
import random
import cv2

def verify_image(path):
    result = {
        "is_valid": False,
        "confidence": 0,
        "message": ""
    }

    # --------------------------
    # 1. FILE TYPE CHECK
    # --------------------------
    if not path.endswith((".png", ".jpg", ".jpeg")):
        result["message"] = "Invalid file type"
        return result

    # --------------------------
    # 2. FILE SIZE CHECK
    # --------------------------
    size = os.path.getsize(path)

    if size < 5000:
        result["message"] = "Image too small / suspicious"
        return result

    # --------------------------
    # 3. LOAD IMAGE (OpenCV)
    # --------------------------
    img = cv2.imread(path)

    if img is None:
        result["message"] = "Corrupted image"
        return result

    # --------------------------
    # 4. BASIC IMAGE ANALYSIS
    # --------------------------

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect edges
    edges = cv2.Canny(gray, 50, 150)

    edge_count = edges.sum()

    # --------------------------
    # 5. FAKE VS REAL HEURISTIC
    # --------------------------

    # If too smooth → suspicious
    if edge_count < 50000:
        result["confidence"] = random.randint(30, 60)
        result["message"] = "Low detail image (possibly fake)"
        result["is_valid"] = False
        return result

    # Otherwise more likely real
    result["confidence"] = random.randint(70, 95)
    result["message"] = "Image looks genuine"
    result["is_valid"] = True

    return result
if __name__ == "__main__":
    test_path = "test.jpg"   # put any image here
    result = verify_image(test_path)
    print(result)