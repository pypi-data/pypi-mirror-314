import requests
import urllib3
from urllib.parse import urlencode
import re
import time
import json
import os

def get_session_info():
    url = "https://www.hedra.com/api/auth/csrf"
    headers = {
        "Host": "www.hedra.com",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "Content-Type": "application/json",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "sec-ch-ua-platform": '"Windows"',
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.hedra.com/login?redirectUrl=%2F&ref=nav",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        cookies = response.cookies
        formatted_cookies = "; ".join([f"{cookie.name}={cookie.value}" for cookie in cookies])
        csrf_token = response.json().get('csrfToken')
        return csrf_token, formatted_cookies
    except requests.exceptions.RequestException:
        return None, None


def get_session_info2(formatted_cookies):
    url = "https://www.hedra.com/api/auth/session"
    headers = {
        "Host": "www.hedra.com",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "Content-Type": "application/json",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "sec-ch-ua-platform": '"Windows"',
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.hedra.com/login?redirectUrl=%2F&ref=nav",
        "Accept-Language": "es-ES,es;q=0.9",
        "Cookie": f"{formatted_cookies}",
        "Accept-Encoding": "gzip, deflate"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        cookies = response.cookies
        csrf_token = None
        for cookie in cookies:
            if cookie.name == "__Secure-next-auth.session-token":
                csrf_token = cookie.value
                break
        return csrf_token
    except requests.exceptions.RequestException:
        return None


def post_sign_in(txtCorreo, txtContra, formatted_cookies, session_token, csrf_token):
    url = "https://www.hedra.com/api/auth/callback/credentials"
    headers = {
        "Host": "www.hedra.com",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "Content-Type": "application/x-www-form-urlencoded",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "sec-ch-ua-platform": '"Windows"',
        "Accept": "*/*",
        "Origin": "https://www.hedra.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.hedra.com/login?redirectUrl=%2F&ref=nav",
        "Accept-Language": "es-ES,es;q=0.9",
        "Cookie": f"{formatted_cookies}; __Secure-next-auth.session-token={session_token}",
        "Accept-Encoding": "gzip, deflate"
    }

    data = {
        "email": txtCorreo,
        "password": txtContra,
        "action": "signIn",
        "redirect": "false",
        "csrfToken": csrf_token,
        "callbackUrl": "https://www.hedra.com/login?redirectUrl=%2F&ref=nav",
        "json": "true"
    }

    encoded_data = urlencode(data)

    http = urllib3.PoolManager()
    try:
        response = http.request('POST', url, body=encoded_data, headers=headers)
        if response.status == 200 and 'set-cookie' in response.headers:
            cookies = response.headers['set-cookie']
            match_0 = re.search(r'__Secure-next-auth.session-token.0=([^;]+)', cookies)
            match_1 = re.search(r'__Secure-next-auth.session-token.1=([^;]+)', cookies)
            session_token_0 = match_0.group(1) if match_0 else None
            session_token_1 = match_1.group(1) if match_1 else None
            return session_token_0, session_token_1
    except Exception:
        pass
    return None, None


def obtener_session(url, token_0, token_1, csrf_Cookies):
    headers = {
        'Host': 'www.hedra.com',
        'Connection': 'keep-alive',
        'sec-ch-ua-platform': '"Windows"',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="127", "Chromium";v="127", "Not_A Brand";v="99"',
        'Content-Type': 'application/json',
        'sec-ch-ua-mobile': '?0',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.hedra.com/login?redirectUrl=%2Fapp%2Fcharacters&ref=nav',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Cookie': f'__Host-next-auth.csrf-token={csrf_Cookies}; __Secure-next-auth.session-token.0={token_0}; __Secure-next-auth.session-token.1={token_1}',
        'Accept-Encoding': 'gzip, deflate',
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('user', {}).get('accessToken', None)
    except Exception:
        pass
    return None


def ejecutar_proceso_completo(email, password):
    try:
        csrf_token, formatted_cookies = get_session_info()
        session_token = get_session_info2(formatted_cookies)
        token_0, token_1 = post_sign_in(email, password, formatted_cookies, session_token, csrf_token)
        api_url = 'https://www.hedra.com/api/auth/session'
        access_token = obtener_session(api_url, token_0, token_1, formatted_cookies)
        if access_token:
            os.environ["ACCESS_TOKEN_HEDRA"] = access_token

        return "access_token"
    except Exception:
        return None