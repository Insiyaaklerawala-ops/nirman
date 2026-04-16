import requests

API_KEY = "+NgfqvH/wjmqI9jUPDeQA=="

def verify_image(path):
    try:
        url = "https://api.thehive.ai/api/v2/task/sync"

        files = {"image": open(path, "rb")}
        headers = {"Authorization": f"Token {API_KEY}"}

        response = requests.post(url, files=files, headers=headers)
        result = response.json()

        score = result["status"][0]["response"]["output"][0]["classes"][0]["score"]

        if score < 0.5:
            return {
                "status": "success",
                "is_valid": True,
                "confidence": int((1 - score) * 100),
                "message": "✅ Real image detected"
            }
        else:
            return {
                "status": "success",
                "is_valid": False,
                "confidence": int(score * 100),
                "message": "❌ AI-generated / fake image"
            }

    except Exception as e:
        print(e)
        return {
            "status": "error",
            "confidence": 0,
            "message": "AI detection failed"
        }