import requests
import re
from bs4 import BeautifulSoup
import time
import urllib3
from urllib.parse import urlencode
import re
import json
import ipywidgets as widgets
import random
import string
from datetime import datetime
import os
import random
import string

def generar_contrasena():
    # Definir los conjuntos de caracteres
    minusculas = string.ascii_lowercase
    mayusculas = string.ascii_uppercase
    numeros = string.digits
    caracteres_especiales = string.punctuation

    # Asegurarse de que la contraseña contiene al menos uno de cada tipo
    contrasena = [
        random.choice(minusculas),
        random.choice(mayusculas),
        random.choice(numeros),
        random.choice(caracteres_especiales)
    ]

    # Completar la contraseña hasta tener al menos 8 caracteres
    todos_caracteres = minusculas + mayusculas + numeros + caracteres_especiales
    contrasena += random.choices(todos_caracteres, k=8 - len(contrasena))

    # Mezclar los caracteres para que el orden sea aleatorio
    random.shuffle(contrasena)

    # Convertir la lista en una cadena
    return ''.join(contrasena)

    
def obtener_fecha_actual():
    return datetime.now().strftime("%b-%d-%Y").lower()  # Formato 'mmm-dd-yyyy', ejemplo: 'nov-20-2024'

def registrar_usuario(token):
    # Obtener la fecha actual para tos_version
    tos_version = obtener_fecha_actual()

    # Variables constantes (no editables)
    tos_accepted = True
    residence_status = "ALLOW"
    marketing_email_consent = "ALLOW"

    api_url = "https://api.dev.dream-ai.com/register"

    # Headers de la solicitud
    headers = {
        'Host': 'api.dev.dream-ai.com',
        'Connection': 'keep-alive',
        'sec-ch-ua-platform': '"Windows"',
        'Authorization': f'Bearer {token}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'Content-Type': 'application/json',
        'sec-ch-ua-mobile': '?0',
        'Accept': '*/*',
        'Origin': 'https://www.hedra.com',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.hedra.com/',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Accept-Encoding': 'gzip, deflate'
    }

    # Cuerpo de la solicitud
    payload = {
        "tos_version": tos_version,
        "tos_accepted": tos_accepted,
        "residence_not_blocked": residence_status,
        "marketing_email_consent": marketing_email_consent
    }

    try:
        # Realizar la solicitud POST
        response = requests.post(api_url, headers=headers, json=payload)

        # Verificar el estado de la respuesta
        if response.status_code == 200:
            return "Respuesta exitosa"
        else:
            return {"error": f"Error en la solicitud: {response.status_code}", "detalle": response.text}
    except Exception as e:
        return {"error": f"Error al realizar la solicitud: {str(e)}"}


def generar_nombre_completo():
  """Genera un nombre completo con un número aleatorio de 3 dígitos."""

  nombres = ["Juan", "Pedro", "Maria", "Ana", "Luis", "Sofia", "Diego", "Laura", "Javier", "Isabel",
            "Pablo", "Marta", "David", "Elena", "Sergio", "Irene", "Daniel", "Alicia", "Carlos", "Sandra",
            "Antonio", "Lucia", "Miguel", "Sara", "Jose", "Cristina", "Alberto", "Blanca", "Alejandro", "Marta",
            "Francisco", "Esther", "Roberto", "Silvia", "Manuel", "Patricia", "Marcos", "Victoria", "Fernando", "Rosa"]
  apellidos = ["Garcia", "Rodriguez", "Gonzalez", "Fernandez", "Lopez", "Martinez", "Sanchez", "Perez", "Alonso", "Diaz",
            "Martin", "Ruiz", "Hernandez", "Jimenez", "Torres", "Moreno", "Gomez", "Romero", "Alvarez", "Vazquez",
            "Gil", "Lopez", "Ramirez", "Santos", "Castro", "Suarez", "Munoz", "Gomez", "Gonzalez", "Navarro",
            "Dominguez", "Lopez", "Rodriguez", "Sanchez", "Perez", "Garcia", "Gonzalez", "Martinez", "Fernandez", "Lopez"]

  nombre = random.choice(nombres)
  apellido = random.choice(apellidos)
  numero = random.randint(100, 999)

  nombre_completo = f"{nombre}_{apellido}_{numero}"
  return nombre_completo

def enviar_formulario():
    """Envía una solicitud POST a un formulario web."""
    url = 'https://email-fake.com/'
    datos = {'campo_correo': 'ejemplo@dominio.com'}
    response = requests.post(url, data=datos)
    return response

def extraer_dominios(response_text):
    """Extrae dominios de un texto utilizando expresiones regulares."""
    dominios = re.findall(r'id="([^"]+\.[^"]+)"', response_text)
    return dominios

def obtener_sitio_web_aleatorio(response_text):
    """Obtiene un sitio web aleatorio de los dominios extraídos."""
    dominios = extraer_dominios(response_text)
    sitio_web_aleatorio = random.choice(dominios)
    return sitio_web_aleatorio

"""def extract_verification_code(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Buscar el texto que contiene el código de verificación
    code_element = soup.find('div', class_='fem mess_bodiyy').find('p')

    if code_element:
        # Extraer y devolver solo el número
        verification_code = code_element.get_text().strip()
        return verification_code
    else:
        return None"""

def extract_verification_code(html_content):
    try:
        # Crear el objeto BeautifulSoup para analizar el contenido HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Intentar buscar el div y el párrafo que contiene el código
        code_element = soup.find('div', class_='fem mess_bodiyy')
        
        # Verificar que el div y el párrafo existen antes de intentar acceder a ellos
        if code_element:
            p_element = code_element.find('p')
            if p_element:
                # Extraer y devolver el texto del párrafo
                verification_code = p_element.get_text().strip()
                return verification_code
        
        # Si no se encontró el código, devolver un mensaje claro
        return "No Exit"

    except Exception as e:
        # Manejar errores inesperados y devolver un mensaje
        return f"Error procesando el HTML: {e}"

def post_register(token):
    url = "https://api.dev.dream-ai.com/register"
    headers = {
        "Host": "api.dev.dream-ai.com",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-mobile": "?0",
        "Authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://www.hedra.com",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.hedra.com/",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate"
    }
    payload = {
        "tos_version": "may-21-2023",
        "tos_accepted": True,
        "residence_not_blocked": "ALLOW",
        "marketing_email_consent": "NONE"
    }

    # Initialize the HTTP client
    http = urllib3.PoolManager()

    # Send the POST request
    response = http.request(
        'POST',
        url,
        body=json.dumps(payload),
        headers=headers
    )

    # Decode the response
    response_data = json.loads(response.data.decode('utf-8'))
    #print(response_data)

    if response.status == 200:
        print("Registro exitoso!")
        return response_data
    else:
        print(f"Error en el registro: {response.status}")
        return None



def get_session( formatted_cookies, token_0, token_1):
    # Crear un administrador de conexiones
    http = urllib3.PoolManager()

    api_url = 'https://www.hedra.com/api/auth/session'

    # Realizar la solicitud GET sin enviar cookies
    response = http.request(
        'GET',
        api_url,
        headers={
            'Host': 'www.hedra.com',
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'Content-Type': 'application/json',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.hedra.com/login?redirectUrl=%2F&ref=nav',
            'Accept-Language': 'es-ES,es;q=0.9',
            "Cookie": f"{formatted_cookies}; __Secure-next-auth.session-token.0={token_0}; __Secure-next-auth.session-token.1={token_1}",
            "Accept-Encoding": "gzip, deflate"
        }
    )

    data = json.loads(response.data.decode('utf-8'))
    #print(data)

    # Extraer el access_token
    access_token = data.get('user', {}).get('accessToken', None)

    return response.status, access_token



def post_sign_in(txtEmail, txtPass, formatted_cookies, session_token, csrf_token):
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
        "Cookie": f"{formatted_cookies}; ph_phc_LPkfNqgrjYQMX7vjw63IAdpzDFpLNUz4fSq3dgbMRgS_posthog=%7B%22distinct_id%22%3A%22d8712390-0001-7079-897e-1eb6d2aa371d%22%2C%22%24sesid%22%3A%5B1723321702013%2C%2201913dfa-5168-7dea-8e61-d31f9f65d4ca%22%2C1723321700712%5D%2C%22%24epp%22%3Atrue%7D; __Secure-next-auth.session-token={session_token}",
        "Accept-Encoding": "gzip, deflate"
    }

    data = {
        "email": f"{txtEmail}",
        "password": f"{txtPass}",
        "action": "signIn",
        "redirect": "false",
        "csrfToken": f"{csrf_token}",
        "callbackUrl": "https://www.hedra.com/login?redirectUrl=%2F&ref=nav",
        "json": "true"
    }

    encoded_data = urlencode(data)

    http = urllib3.PoolManager()
    try:
        response = http.request(
            'POST',
            url,
            body=encoded_data,
            headers=headers
        )
    except Exception as e:
        print(f"Error during request: {e}")
        return None, None

    if response.status == 200:
        if 'set-cookie' in response.headers:
            cookies = response.headers['set-cookie']
            #print("Cookies recibidas:")
            #print(cookies)

            # Extracción de los valores de las cookies específicas
            session_token_0 = None
            session_token_1 = None

            # Buscar los tokens específicos en las cookies
            match_0 = re.search(r'__Secure-next-auth.session-token.0=([^;]+)', cookies)
            match_1 = re.search(r'__Secure-next-auth.session-token.1=([^;]+)', cookies)

            if match_0:
                session_token_0 = match_0.group(1)
            if match_1:
                session_token_1 = match_1.group(1)

            # Imprimir los valores extraídos
            #if session_token_0:
             #   print(f"__Secure-next-auth.session-token.0: {session_token_0}")
            #if session_token_1:
            #    print(f"__Secure-next-auth.session-token.1: {session_token_1}")

            # Retornar los tokens extraídos
            return session_token_0, session_token_1
        else:
            print("No se encontraron cookies en la respuesta.")
            return None, None
    else:
        print(f"Failed to post credentials. Status code: {response.status}")
        return None, None



def get_session_info2(txtEmail, txtPass, formatted_cookies, session_token):
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
        "Cookie": f"{formatted_cookies}; ph_phc_LPkfNqgrjYQMX7vjw63IAdpzDFpLNUz4fSq3dgbMRgS_posthog=%7B%22distinct_id%22%3A%22d8712390-0001-7079-897e-1eb6d2aa371d%22%2C%22%24sesid%22%3A%5B1723321702013%2C%2201913dfa-5168-7dea-8e61-d31f9f65d4ca%22%2C1723321700712%5D%2C%22%24epp%22%3Atrue%7D; __Secure-next-auth.session-token={session_token}",
        "Accept-Encoding": "gzip, deflate"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lanza una excepción para códigos de error HTTP
        print("Response received:")
        #print(response.text)

        # Extraer y formatear las cookies
        cookies = response.cookies
        print("Extraer y formatear las cookies...")

        # Buscar la cookie `__Host-next-auth.csrf-token`
        csrf_token = None
        for cookie in cookies:
            if cookie.name == "__Secure-next-auth.session-token":
                csrf_token = cookie.value
                break

        """if csrf_token:
            print(f"__Secure-next-auth.session-token: correct")
        else:
            print("__Secure-next-auth.session-token not found")"""

        return csrf_token

    except requests.exceptions.RequestException as e:
        print(f"Failed to get session info. Error: {e}")
        return None





def post_credentials_with_code(txtEmail, txtPass, codigoverificado, formatted_cookies, session_token, csrf_token):
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
        "Cookie": f"{formatted_cookies}; ph_phc_LPkfNqgrjYQMX7vjw63IAdpzDFpLNUz4fSq3dgbMRgS_posthog=%7B%22distinct_id%22%3A%22d8712390-0001-7079-897e-1eb6d2aa371d%22%2C%22%24sesid%22%3A%5B1723321702013%2C%2201913dfa-5168-7dea-8e61-d31f9f65d4ca%22%2C1723321700712%5D%2C%22%24epp%22%3Atrue%7D; __Secure-next-auth.session-token={session_token}",
        "Accept-Encoding": "gzip, deflate"
    }

    data = {
        "email": txtEmail,
        "password": txtPass,
        "action": "confirm",
        "code": codigoverificado,
        "redirect": "false",
        "csrfToken": csrf_token,
        "callbackUrl": "https://www.hedra.com/login?redirectUrl=%2F&ref=nav",
        "json": "true"
    }

    try:
        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            print("Response received:")
            if 'set-cookie' in response.headers:
                cookies = response.headers['set-cookie']
                print("Cookies received:")
                return cookies
        else:
            print(f"Failed to post credentials. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def post_credentials(txtEmail, txtPass, formatted_cookies, csrf_token):
    url = "https://www.hedra.com/api/auth/callback/credentials"
    headers = {
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
        "Cookie": formatted_cookies,
        "Accept-Encoding": "gzip, deflate"
    }

    data = {
        "email": txtEmail,
        "password": txtPass,
        "action": "signUp",
        "redirect": "true",
        "csrfToken": csrf_token,
        "callbackUrl": "https://www.hedra.com/login?redirectUrl=%2F&ref=nav",
        "json": "true"
    }

    try:
        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            print("Response received:")

            if 'set-cookie' in response.headers:
                cookies = response.headers['set-cookie']
                print("Cookies received:")

                match = re.search(r'__Secure-next-auth\.session-token=([^;]+)', cookies)
                if match:
                    session_token = match.group(1)
                    return session_token
                else:
                    print("Session Token not found.")
                    return None
        else:
            print("Failed to post credentials. Retrying...")
            configurar_credenciales()

            print("Obteniendo información de la sesión2...")
            csrf_token1, formatted_cookies1 = get_session_info()

            os.environ["CSRF_TOKEN"] = csrf_token1
            os.environ["FORMATTED_COOKIE"] = formatted_cookies1

            print("Enviando credenciales2...")
            correo = os.environ.get("EMAIL_HEDRA")
            contrasena = os.environ.get("PASS_HEDRA")
            session_token = post_credentials(correo, contrasena, formatted_cookies1, csrf_token1)
            if session_token:
                os.environ["SESSION_TOKEN"] = session_token
                print("Credenciales aceptadas2.")
            return session_token
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None



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
        response.raise_for_status()  # Lanza una excepción para códigos de error HTTP
        print("Response received:")
        #print(response.json())  # Cambia a response.text si no es JSON

        # Extraer y formatear las cookies
        cookies = response.cookies
        formatted_cookies = "; ".join([f"{cookie.name}={cookie.value}" for cookie in cookies])

        print("Formatted Cookies:")
        #print(formatted_cookies)

        # Retornar el csrfToken y las cookies formateadas si deseas utilizarlas después
        csrf_token = response.json().get('csrfToken')
        return csrf_token, formatted_cookies

    except requests.exceptions.RequestException as e:
        print(f"Failed to get session info. Error: {e}")



def extract_confirmation_code(text):
    # Utilizar una expresión regular para buscar el número en el texto
    match = re.search(r'\b\d{6}\b', text)
    if match:
        return match.group(0)  # Devolver el número encontrado
    else:
        return None


def enviar_dell_post(id_dell, usuarios, dominios):
    url = 'https://email-fake.com/del_mail.php'#{dominios}%2F{usuario}
    headers = {
       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
       'X-Requested-With': 'XMLHttpRequest',
       'Cookie': f'embx=%5B%22{usuarios}%40{dominios}; surl={dominios}/{usuarios}/',
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
       'Accept': '*/*',
       'Origin': 'https://email-fake.com',
       'Sec-Fetch-Site': 'same-origin',
       'Sec-Fetch-Mode': 'cors',
       'Sec-Fetch-Dest': 'empty',
       'Accept-Language': 'es-ES,es;q=0.9'
    }

    data = {
       'delll': f'{id_dell}'
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error en la solicitud POST: {str(e)}"

def extract_codes_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Encuentra la celda <td> con el estilo y clase específicos
    td_tag = soup.find('td', {'class': 'inner-td', 'style': 'border-radius: 6px; font-size: 16px; text-align: center; background-color: inherit'})

    if td_tag:
        # Encuentra la etiqueta <a> dentro de la celda <td>
        a_tag = td_tag.find('a', href=True)

        if a_tag:
            # Obtén el valor del atributo href
            href = a_tag['href']

            # Encuentra el valor de internalCode y oobCode en el href
            internal_code = None
            oob_code = None

            if 'internalCode=' in href:
                internal_code = href.split('internalCode=')[1].split('&')[0]

            if 'oobCode=' in href:
                oob_code = href.split('oobCode=')[1].split('&')[0]

            return internal_code, oob_code
    return None, None

def execute_get_request(usuario, dominios):
    url = "https://email-fake.com/"
    headers = {
        "Host": "email-fake.com",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "Accept-Language": "es-ES,es;q=0.9",
        "Cookie": f'surl={dominios}%2F{usuario}',
        "Accept-Encoding": "gzip, deflate"
    }

    response = requests.get(url, headers=headers)

    # Uso de la función
    internal_code, oob_code = extract_codes_from_html(response.text)

    #print(response.text)

    # Extraer el código de verificación del contenido HTML
    verification_code = extract_verification_code(response.text)

    #if verification_code=="No Exit":
    #  proceso_completo()

    # Definir el patrón de búsqueda para delll
    patron = r"delll:\s*\"([^\"]+)\""

    # Aplicar la búsqueda utilizando regex
    resultado = re.search(patron, response.text)

    # Verificar si se encontró delll y obtener su valor
    if resultado:
        valor_delll = resultado.group(1)

    else:
        print("No se encontró delll en el código JavaScript.")


    return internal_code, str(verification_code).replace("Your confirmation code is ",""), valor_delll

    #return response.text




def proceso_completo():
    configurar_credenciales()
    email = os.environ.get("EMAIL_HEDRA")
    passwords = os.environ.get("PASS_HEDRA")
    # Paso 2: Obtener información de la sesión
    print("Obteniendo información de la sesión...")
    csrf_token, formatted_cookies = get_session_info()
    os.environ["CSRF_TOKEN"] = csrf_token
    os.environ["FORMATTED_COOKIE"] = formatted_cookies
    time.sleep(1)


    # Paso 3: Postear credenciales y obtener token de sesión
    print("Enviando credenciales...")
    session_token = post_credentials(email, passwords, formatted_cookies, csrf_token)
    if session_token:
        os.environ["SESSION_TOKEN"] = session_token
        print("Credenciales aceptadas.")

    time.sleep(5)

    usuario = os.environ.get("USER_HEDRA")
    dominio = os.environ.get("DOMAIN_HEDRA")

    # Paso 4: Buscar código interno
    print("Buscando código interno...")
    internal_code, oob_code, valor_delll = execute_get_request(usuario, dominio)


    time.sleep(5)
    email = os.environ.get("EMAIL_HEDRA")
    passwords = os.environ.get("PASS_HEDRA")
    session_token2 = os.environ.get("SESSION_TOKEN")
    # Paso 5: Verificar credenciales con el código
    print("Verificando credenciales con el código...")

    csrf_token1 = os.environ.get("CSRF_TOKEN")
    formatted_cookies1 = os.environ.get("FORMATTED_COOKIE")

    cookies = post_credentials_with_code(email, passwords, oob_code, formatted_cookies1, session_token2, csrf_token1)
    if cookies:
        print("Credenciales verificadas.")


    time.sleep(2)
    email = os.environ.get("EMAIL_HEDRA")
    passwords = os.environ.get("PASS_HEDRA")
    session_token2 = os.environ.get("SESSION_TOKEN")
    csrf_token1 = os.environ.get("CSRF_TOKEN")
    formatted_cookies1 = os.environ.get("FORMATTED_COOKIE")
    # Paso 6: Obtener nueva información de sesión
    print("Actualizando sesión...")
    session_token3 = get_session_info2(email, passwords, formatted_cookies1, session_token2)
    if session_token3:
        print("Sesión actualizada.")


    time.sleep(2)
    email = os.environ.get("EMAIL_HEDRA")
    passwords = os.environ.get("PASS_HEDRA")
    session_token2 = os.environ.get("SESSION_TOKEN")
    csrf_token1 = os.environ.get("CSRF_TOKEN")
    formatted_cookies1 = os.environ.get("FORMATTED_COOKIE")
    # Paso 7: Loguearse con los tokens obtenidos
    print("Iniciando sesión...")
    token_0, token_1 = post_sign_in(email, passwords, formatted_cookies1, session_token2, csrf_token1)
    if token_0 and token_1:
        print("Inicio de sesión exitoso.")


    # Paso 8: Obtener sesión con la URL deseada
    print("Obteniendo sesión...")
    formatted_cookies1 = os.environ.get("FORMATTED_COOKIE")
    status_code, access_token = get_session(formatted_cookies1, token_0, token_1)
    if access_token:
        os.environ["ACCESS_TOKEN_HEDRA"] = access_token


    print("Sesión establecida correctamente.")
    time.sleep(2)

    # Paso 9: Registrar usuario con el token de acceso
    print("Registrando usuario...")
    registrar_usuario(access_token)
    print("Proceso completo.")




def configurar_credenciales():
    print("Generando datos iniciales...")
    
    password_segug = generar_contrasena()
    response = enviar_formulario()
    sitio_domain = obtener_sitio_web_aleatorio(response.text)
    
    nombre_completo = generar_nombre_completo()
    email = f'{nombre_completo}@{sitio_domain}'
    passwords = password_segug

    usuario, dominio = email.split('@')

    os.environ["USER_HEDRA"] = usuario
    os.environ["DOMAIN_HEDRA"] = dominio

    os.environ["EMAIL_HEDRA"] = email
    os.environ["PASS_HEDRA"] = passwords
