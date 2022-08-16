
import captcha as cap
import json, bypass, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def getConfig ():
    # read file config.json
    with open('config.json') as config:
        data = json.load(config)
        return data

def driver_create ():
    op = Options()
    # add extension
    op.add_extension("ads.crx")
    return webdriver.Chrome(options=op)

def driver_close (driver):
    driver.quit()

def resetTab (driver):
    child = driver.window_handles[0]
    driver.switch_to.window(child)

def closeTab (driver):
    driver.switch_to.window(driver.window_handles[1])
    driver.close()

def login (driver, wallet):
    if driver.page_source.find('Login') == -1:
        return False
    else:
        driver.find_element('name', 'address').send_keys(wallet)
        time.sleep(2)
        for x in range(2):
            try:
                driver.find_element('xpath', '//*[@id="faucet"]/div/form/input[2]').click()
                break
            except:
                time.sleep(1)
        for x in range(10):
            
            if driver.page_source.find('This faucet requires a') > -1:
                return None
            if driver.page_source.find('Logged In As:') == -1:
                time.sleep(1)
            else:
                return True
        return False
def clear (str):
    return str.replace('@','a').replace('!','i').replace('5','s').replace('3', 'e').replace('1','i').lower()

def claim (driver):
    if driver.page_source.find('Continue') == -1:
        return False
    else:
        time.sleep(2)
        driver.find_element('xpath', '//*[@id="faucet"]/div/form/button').click()
        time.sleep(2)
        # get image
        img = driver.execute_script('var content = document.querySelector("#antibot > div > div > div.modal-header.no-padding > div > img").src; return content;')
        cap.image = img.replace('data:image/png;base64,','')
        solve = cap.solve_captcha()
        if solve == False:
            return False
        else:
            sp = solve.lower().replace(', ', ' ').replace(';', ' ').split(' ')
            if len(sp) == 4:
                print('[+] Solve captcha: ' + str(sp))
                img1 = driver.execute_script('var content = document.querySelector("#antibot > div > div > div.modal-body > div.row.no-margin.no-padding > div:nth-child(1) > a > img").src; return content;')
                cap.image = img1.replace('data:image/png;base64,','')
                solve1 = cap.solve_captcha()
                if solve1 == False:
                    return False
                img2 = driver.execute_script('var content = document.querySelector("#antibot > div > div > div.modal-body > div.row.no-margin.no-padding > div:nth-child(2) > a > img").src; return content;')
                cap.image = img2.replace('data:image/png;base64,','')
                solve2 = cap.solve_captcha()
                if solve2 == False:
                    return False
                img3 = driver.execute_script('var content = document.querySelector("#antibot > div > div > div.modal-body > div:nth-child(7) > div:nth-child(1) > a > img").src; return content;')
                cap.image = img3.replace('data:image/png;base64,','')
                solve3 = cap.solve_captcha()
                if solve3 == False:
                    return False
                img4 = driver.execute_script('var content = document.querySelector("#antibot > div > div > div.modal-body > div:nth-child(7) > div:nth-child(2) > a > img").src; return content;')
                cap.image = img4.replace('data:image/png;base64,','')
                solve4 = cap.solve_captcha()
                if solve4 == False:
                    return False 
                print('[+] Solve captcha: ' + str(solve1) + ' ' + str(solve2) + ' ' + str(solve3) + ' ' + str(solve4))
                lImgs = [clear(solve1), clear(solve2), clear(solve3), clear(solve4)]
                lu = []
                for x in sp:
                    lis = {}
                    for y in lImgs:
                        i = 1
                        for u in y:
                            if u in x:
                                i += 1
                        lis[y] = i
                    ma = max(lis.values())
                    a = 1

                    for u in lis:
                        if lis[u] == ma:
                            lu.append(a)
                            break
                        a += 1
                print('[+] Solve captcha: ' + str(lu))
                action = []
                for a in lu:
                    if a == 1:
                        action.append('document.querySelector("#antibot > div > div > div.modal-body > div.row.no-margin.no-padding > div:nth-child(1) > a > img").click()')
                    elif a == 2:
                        action.append('document.querySelector("#antibot > div > div > div.modal-body > div.row.no-margin.no-padding > div:nth-child(2) > a > img").click()')
                    elif a == 3:
                        action.append('document.querySelector("#antibot > div > div > div.modal-body > div:nth-child(7) > div:nth-child(1) > a > img").click()')
                    elif a == 4:
                        action.append('document.querySelector("#antibot > div > div > div.modal-body > div:nth-child(7) > div:nth-child(2) > a > img").click()')
                if len(action) != len(set(action)):
                    return False
                for x in action:
                    driver.execute_script(x)
                    time.sleep(1)
                print(driver.current_url)
                id = bypass.solveCaptchaV2('6LfDD6sbAAAAAEs1Qjg_OBkWgU0TQ2esQpAm-SFP', driver.current_url)
                if id == False:
                    return False
                else:
                    for a in range(10):
                        solve = bypass.submit(id)
                        if solve == False:
                            time.sleep(10)
                        else:
                            break
                    if solve == False or solve == 'error' or solve == '':
                        return False
                    else:
                        driver.execute_script('document.querySelector("#g-recaptcha-response").value = "' + solve + '";')
                        time.sleep(2)
                        driver.find_element('xpath', '//*[@id="ncb"]/input').click()
                        time.sleep(5)
                        if driver.page_source.find('alert alert-success') == -1:
                            return False
                        else:
                            content = driver.execute_script('var x = document.querySelector("#faucet > div > div.form > div.alert.alert-success").innerHTML; return x;')
                            print(content)
                     
            else:
                return False

conf = getConfig()
print('lmao')
bypass.inputToken(conf['2captcha'])
wallet = conf['wallet']
ite = iter(wallet)
cols = color()
def resetIterConfig ():
    global ite
    ite = iter(wallet)


# get all wallet and print the screen
for x in ite:
    print(cols.GREEN + '[' + x + '] ' + cols.BLUE + ' = ' + cols.END + wallet[x])
resetIterConfig()

tags = {
    'btc' : '/free-bitcoin/',
    'doge' : '/free-dogecoin/',
    'ltc': '/free-litecoin/',
    'tron': '/free-tron/',
    'bnb' : '/free-binance/',
    'sql' : '/free-solana/',
    'dash' : '/free-dash/',
    'usdt' : '/free-tether/',
    'zec' : '/free-zcash/',
    'dgb' : '/free-digibyte/',
    'eth' : '/free-ethereum/',
    'btcs' : '/free-bitcoin-cash/',
    'fey' : '/free-feyorra/'
}

drivers = driver_create()
time.sleep(3)
closeTab(drivers)
resetTab(drivers)

while True:
    for x in tags:
        for y in wallet:
            if x == y:
                while True:
                    try:
                        drivers.get('https://claimfreecoins.io' + tags[x])
                        log = login(drivers, wallet[y])
                        if log:
                            print(cols.GREEN + '[' + y + '] Login thanh cong')
                        elif log == None:
                            print(cols.RED + '[' + y + '] Chặn tính năng')
                            driver_close(drivers)
                            drivers = driver_create()
                            time.sleep(3)
                            closeTab(drivers)
                            resetTab(drivers)
                            continue
                        if claim(drivers) == False:
                            print(cols.RED + '[' + y + '] Claim that bai')
                        else:
                            print(cols.GREEN + '[' + y + '] Claim thanh cong')
                            break
                    except:
                        driver_close(drivers)
                        drivers = driver_create()
                        time.sleep(3)
                        closeTab(drivers)
                        resetTab(drivers)
           
