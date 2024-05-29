import requests
import time
import json
import sys
import base64
import warnings
import urllib.parse
import capsolver

capsolver.api_key = "CAP-B736BC4D3F522CE5F855A6FF3C01B586"

MAX_RETRIES_WITH_SAME_SOLUTION = 5
MAX_TOTAL_RETRIES = 3


def getPlan(rq):

    h = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}

    grabPlanRq = rq.get(
        "https://www.spotify.com/api/account/v1/datalayer/", headers=h)
    planObj = json.loads(grabPlanRq.text)
    return planObj["currentPlan"]


def getUsername(rq):
    h = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}

    grabUsernameRq = rq.get(
        "https://www.spotify.com/api/account-settings/v1/profile", headers=h)
    profileObj = json.loads(grabUsernameRq.text)
    return profileObj["profile"]["username"]


def login(u, p):
    print("[@] Logging in to: " + u + ":" + p)

    retries_with_same_solution = 0
    total_retries = 0

    # catpcha
    solution = capsolver.solve({"type": "ReCaptchaV3EnterpriseTaskProxyLess","websiteURL": "https://accounts.spotify.com/","websiteKey": "6LfCVLAUAAAAALFwwRnnCJ12DalriUGbj8FW_J39","pageAction":"accounts/login","minScore":0.3})
    while total_retries < MAX_TOTAL_RETRIES:
        rq = requests.Session()

        h = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36','Pragma': 'no-cache',
'Accept': '*/*',
'Accept-Language': 'en-US,en;q=0.8'}

        getRq = rq.get(
            "https://accounts.spotify.com/login?continue=https%3A%2F%2Fopen.spotify.com%2F%3F", headers=h)
        soup = BeautifulSoup(getRq.text, 'html.parser')
        meta_element = soup.find('meta', id='bootstrap-data')
        bootstrap_data = meta_element['sp-bootstrap-data']
        data = json.loads(bootstrap_data)  
        flow = data.get('flowCtx')
        flow = urllib.parse.quote(flow)
        csrf = rq.cookies.get_dict()["sp_sso_csrf_token"]
        payload = {"username": u,"password": p,"remember": "true","recaptchaToken": solution['gRecaptchaResponse'],"continue": f"https://open.spotify.com/?flow_ctx={flow}","flowCtx": flow}
        h = {
    'Host': 'accounts.spotify.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-GB,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://accounts.spotify.com/en-GB/login?continue=https%3A%2F%2Fopen.spotify.com%2F%3F',
    'X-CSRF-Token': csrf,
    'Origin': 'https://accounts.spotify.com',
    'DNT': '1',
    'Connection': 'close',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}

        loginReq = rq.post(
            "https://accounts.spotify.com/login/password", data=payload, headers=h)
        print(loginReq.text)
        if(loginReq.status_code == 200):
            cookie = rq.cookies.get_dict()["sp_dc"]
            parsed_username = getUsername(rq)
            plan = getPlan(rq)
            if plan == 'free':
                print("USERNAME:", parsed_username)
                return "COOKIE: " + cookie
            elif plan == 'premium':
                return "Already Premium"
            elif plan == 'student_premium':
                return "Already Premium"
        elif "errorInvalidCredentials" in loginReq.text:
            return "Invalid Login"
        else:
            if retries_with_same_solution < MAX_RETRIES_WITH_SAME_SOLUTION:
                retries_with_same_solution += 1
                print(f"Retrying with the same solution ({retries_with_same_solution}/{MAX_RETRIES_WITH_SAME_SOLUTION})...")
                time.sleep(1)
            else:
                retries_with_same_solution = 0
                total_retries += 1
                print(f"Requesting a new captcha solution ({total_retries}/{MAX_TOTAL_RETRIES})...")
                captcha = solve()
    
    return f"Unknown Error"

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Please provide 'usnm' and 'pass' args in the command.")
    else:
        u = sys.argv[1]
        p = sys.argv[2]

        print(login(u, p))

#u = input("Enter username: ")
#p = input("Enter password: ")


#print(login(u, p))