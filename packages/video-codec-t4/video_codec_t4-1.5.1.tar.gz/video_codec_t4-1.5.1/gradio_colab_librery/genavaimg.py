import os
import requests
import json
import time
from tqdm.notebook import tqdm
import hashlib
from PIL import Image
import base64
import random
from IPython.display import display, HTML
import subprocess  # Importar subprocess
from registro import *

FOLDER_PATH_HED = None
IMAGE_PATH_HED = None
RUTA_VIDEO_HED = None
RATIO_HED = None
PROMPT_HED = None
SEED_INPUT_HED = None
SEED_HED = None
CONTINUE_FRAGMENT_HED = None

def video_to_base64(video_path):
    with open(video_path, "rb") as video_file:
        video_base64 = base64.b64encode(video_file.read()).decode('utf-8')
    return video_base64

def display_video_base64(video_path):
    video_base64 = video_to_base64(video_path)
    video_html = f"""
    <video width="512" height="512" controls>
      <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
      Your browser does not support the video tag.
    </video>
    """
    display(HTML(video_html))


def eliminar_proyecto(token, joob_ids):
    url = f"https://www.hedra.com/api/app/v1/app/projects/{joob_ids}"
    headers = {
        "Authorization": f"Bearer {token}",
        "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://www.hedra.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.hedra.com/app/characters",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    }

    response = requests.delete(url, headers=headers)

    # Imprime el código de estado de la respuesta y el contenido de la respuesta
    #print(f"Status Code: {response.status_code}")
    #print(f"Response: {response.text}")


def extract_last_frame(video_path, output_image):
    # Verificar si existe un archivo JPG y eliminarlo
    if os.path.exists(output_image):
        os.remove(output_image)
        print(f'Existing file {output_image} deleted.')

    # Primero obtenemos la duración del video
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", video_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    # Convertimos la duración a segundos
    duration = float(result.stdout)

    # Comando para extraer el fotograma en el último segundo
    command = [
        "ffmpeg",
        "-ss", str(duration - 0.1),  # Nos movemos al último segundo del video
        "-i", video_path,
        "-vframes", "1",             # Extraemos un solo fotograma
        "-q:v", "2",                 # Calidad de la imagen (2 es la mejor calidad)
        output_image
    ]

    # Ejecutar el comando
    subprocess.run(command)

    # Estirar la imagen 2 píxeles en altura
    with Image.open(output_image) as img:
        width, height = img.size
        new_height = height + 2
        resized_img = img.resize((width, new_height))
        resized_img.save(output_image)

    print(f"Last frame saved and stretched as {output_image}")





# Función para actualizar la barra de progreso y descargar el video si el progreso es 100%
def update_progress_bar(token, current_progress, file_name_without_ext, joob_ids, ruta_videos, ruta_ava_img, continue_fragment):
    total_steps = 100
    video_url = None
    while current_progress < 1.0:
        # Simula obtener el progreso actualizado
        response = obtener_avatar_sin_cookies(token)
        #print("Proceso:", response)
        project = response['projects'][0]
        current_progress = project['progress']
        video_url = project['videoUrl']  # Obtener la URL del video
        #print("Video URL:", video_url)
        
        # Calcular el contador de progreso
        step = int(current_progress * total_steps)

        os.environ["PROGRESS_HEDRA"] = str(step)

        # Imprimir el progreso en la misma línea
        print(f"\rProgreso: {step}%", end='', flush=True)
        
        time.sleep(2)  # Ajusta el intervalo de actualización aquí

    if video_url:  # Si se ha obtenido una URL del video, descarga el video
        download_video(token, video_url, file_name_without_ext, joob_ids, ruta_videos, ruta_ava_img, continue_fragment)


# Función para generar un nombre de archivo seguro a partir de una URL
def generate_safe_filename(url):
    # Usa un hash MD5 de la URL para generar un nombre de archivo único y seguro
    hash_object = hashlib.md5(url.encode())
    return hash_object.hexdigest() + '.mp4'

# Función para descargar el video desde una URL
def download_video(token, url, file_name_without_ext, joob_ids, ruta_videos, ruta_ava_img, continue_fragment):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        filename = generate_safe_filename(url)
        with open(f"{ruta_videos}{file_name_without_ext}.mp4", 'wb') as file:
        #with open(f"/tmp/videos/{file_name_without_ext}.mp4", 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        print(f" Video downloaded as {ruta_videos}{file_name_without_ext}.mp4")
        # Ejemplo de uso
        video_path = f"{ruta_videos}{file_name_without_ext}.mp4"

        # Reemplaza con la ruta de tu archivo
        display_video_base64(video_path)

        output_image = ruta_ava_img #"/tmp/avatar_img.jpg"
        if continue_fragment:
           extract_last_frame(video_path, output_image)
        # Ejecutar la función
        eliminar_proyecto(token, joob_ids)

        os.environ["VIDEO_PATH_HEDRA"] = f"{ruta_videos}{file_name_without_ext}.mp4"

    else:
        print("Error downloading video")

def obtener_avatar_sin_cookies(token):
    url = "https://www.hedra.com/api/app/v1/app/projects"
    headers = {
        "Authorization": f"Bearer {token}",
        "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.hedra.com/app/characters",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    }

    response = requests.get(url, headers=headers)
    return response.json()

# Convertir la imagen a base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string



def enviar_avatar_predict(token, img_base64, audio_link):
    url = "https://www.hedra.com/api/app/v1/app/avatars/predict-async"
    headers = {
        "Host": "www.hedra.com",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-mobile": "?0",
        "Authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://www.hedra.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.hedra.com/app/characters",
        "Accept-Language": "es-ES,es;q=0.9",
        #"Cookie": "__Host-next-auth.csrf-token=63291ebf55d36a72dc388dd71bff...",
        "Accept-Encoding": "gzip, deflate",
    }

    data = {
        "text": "",
        "avatar_image": f"{img_base64}",
        "avatar_image_input": {
            "prompt": "",
            "seed": 2373
        },
        "audio_source": "audio",
        "voice_url": f"{audio_link}"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Request successful!")
        #print(response.json())  # Imprimir respuesta si es JSON
        # Supongamos que tienes el siguiente diccionario
        responses = response.json()

        # Extraer el job_id
        job_id = responses['job_id']
        return job_id
    else:
        print(f"Request failed with status code {response.status_code}")
        #print(response.text)


def generar_avatar(
    authorization_token,  # Token de autorización que puede cambiar
    avatar_image,         # Imagen base64 del avatar
    aspect_ratio="16:9",  # Relación de aspecto, editable
    prompt="",            # Descripción del prompt, editable
    seed_input=True,      # Si es True, puedes proporcionar un seed; si es False, el seed es aleatorio
    seed=None,            # Semilla proporcionada si seed_input es True, sino se genera aleatoriamente
    voice_url="",         # URL del archivo de voz editable
):

    # Si seed_input es False, generamos una semilla aleatoria
    if not seed_input:
        seed = random.randint(1000000, 9999999)  # Genera un número aleatorio de 7 dígitos

    # Definir la URL de la API
    url = "https://www.hedra.com/api/app/v1/app/avatars/predict-async"

    # Cabeceras HTTP
    headers = {
        "Host": "www.hedra.com",
        "Connection": "keep-alive",
        "Authorization": f"Bearer {authorization_token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://www.hedra.com",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    }

    # Crear el cuerpo de la solicitud
    data = {
        "text": "",
        "avatar_image": avatar_image,
        "aspect_ratio": aspect_ratio,
        "avatar_image_input": {
            "prompt": prompt,
            "seed": seed
        },
        "audio_source": "audio",  # Usando TTS como la fuente de audio
        "voice_url": voice_url
    }

    # Realizar la solicitud POST
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Verificar la respuesta
    if response.status_code == 200:
        print("Solicitud enviada con éxito.")
        responses = response.json()

        # Extraer el job_id
        job_id = responses['job_id']
        return job_id
        #return response.json()  # Devuelve la respuesta en formato JSON
    else:
        proceso_completo()
        time.sleep(2)
        access = os.environ.get("ACCESS_TOKEN_HEDRA")
        #if access:
        process_audio_files(FOLDER_PATH_HED, IMAGE_PATH_HED, RUTA_VIDEO_HED, RATIO_HED, PROMPT_HED, SEED_INPUT_HED, SEED_HED, CONTINUE_FRAGMENT_HED)

        print(f"Error en la solicitud: {response.status_code}")
        return None



def upload_audio(file_path, token):
    url = "https://www.hedra.com/api/app/v1/app/avatars/audio"
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Origin": "https://www.hedra.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.hedra.com/app/characters",
        "Accept-Language": "es-ES,es;q=0.9",
        "Connection": "keep-alive",
    }

    with open(file_path, 'rb') as audio_file:
        files = {'file': (file_path.split('/')[-1], audio_file, 'audio/wav')}
        response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        print(f"Audio {file_path} uploaded successfully.")
        # Convertimos el texto a un diccionario
        response_dict = json.loads(response.text)

        # Extraemos la URL
        url = response_dict["url"]

        return url
    else:
        print(f"Error uploading audio {file_path}: {response.status_code}, {response.text}")

def process_audio_files(folder_path, image_path, ruta_videos, aspect_ratio, prompt, seed_input, seed, continue_fragment):
    global FOLDER_PATH_HED, IMAGE_PATH_HED, RUTA_VIDEO_HED, RATIO_HED, PROMPT_HED, SEED_INPUT_HED, SEED_HED, CONTINUE_FRAGMENT_HED

    # Asignar valores a las variables globales
    FOLDER_PATH_HED = folder_path
    IMAGE_PATH_HED = image_path
    RUTA_VIDEO_HED = ruta_videos
    RATIO_HED = aspect_ratio
    PROMPT_HED = prompt
    SEED_INPUT_HED = seed_input
    SEED_HED = seed
    CONTINUE_FRAGMENT_HED = continue_fragment

    access_token = os.environ.get("ACCESS_TOKEN_HEDRA")

    # Procesar los archivos de audio
    file_list = sorted([f for f in os.listdir(folder_path) if f.endswith('.mp3')])

    if not continue_fragment:
        file_list = file_list[:1]  # Procesar solo el primer archivo

    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        print(f"Processing audio: {file_path}")

        url_audio = upload_audio(file_path, access_token)

        file_name_without_extension = os.path.splitext(file_name)[0]

        # Convertir la imagen en base64
        base64_string = image_to_base64(image_path)

        # Generar el avatar y obtener el `joob_id`
        joob_id = generar_avatar(
            authorization_token=access_token,
            avatar_image=base64_string,
            aspect_ratio=aspect_ratio,
            prompt=prompt,
            seed_input=seed_input,
            seed=seed,
            voice_url=url_audio
        )

        # Obtener el progreso inicial del avatar
        resultado = obtener_avatar_sin_cookies(access_token)
        project = resultado['projects'][0]
        initial_progress = project['progress']

        # Actualizar la barra de progreso y descargar el video
        update_progress_bar(access_token, initial_progress, file_name_without_extension, joob_id, ruta_videos, image_path, continue_fragment)

        if not continue_fragment:
            break

        time.sleep(2)