import requests
image = ''
def solve_captcha():
    global image
    json_data = {
        "requests": [
            {
                "image": {"content": image},
                "features": [{"type": "TEXT_DETECTION"}],
            }
        ]
    }

    req = requests.post(
        url="https://content-vision.googleapis.com/v1/images:annotate",
        headers={
            "x-origin": "https://explorer.apis.google.com",
        },
        params={
            "alt": "json",
            "key": "<key gg vision>",
        },
        json=json_data,
    )

    captcha_answer = req.json()["responses"][0]["textAnnotations"][0]["description"]
    if captcha_answer == "" or captcha_answer is None:
        return False
    else:
        return captcha_answer.split("\n")[0]
