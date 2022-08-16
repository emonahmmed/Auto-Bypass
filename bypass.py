import requests
token = ''

def inputToken (tokens):
    global token
    token = tokens

def solveNormalCaptcha (img):
    global token

    data = {
        'key': token,
        'method': 'post',
    }

    files = {
        'file': (img, open(img, 'rb'), 'image/png')
    }

    rq = requests.post('http://2captcha.com/in.php', data=data, files=files)
    if 'OK' in rq.text:
        return rq.text.split('|')[1]
    else:
        return False

def solveCaptchaV2 (key, url):
    global token
    url = "https://2captcha.com/in.php?key=" + token + "&method=userrecaptcha&googlekey=" + key + "&pageurl=" + url
    rq = requests.get(url)
    print(rq.text)
    if 'OK' in rq.text:
        return rq.text.split('|')[1]
    else:
        return False

def submit(id, action = 'get'):
    global token
    data = {
        'key': token,
        'action': action,
        'id': id
    }
    rq = requests.post('http://2captcha.com/res.php', data=data)
    if 'OK' in rq.text:
        if rq.text == 'ERROR_CAPTCHA_UNSOLVABLE':
            return None
        return rq.text.split('|')[1]
    else:
        return False
