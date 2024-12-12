
import requests
import json
import base64
from PIL import Image
from io import BytesIO
import IPython.display as display
import random
import os

def guardar_imagen_base64(base64_string):
    ruta_archivo = '/tmp/avatar_img.jpg'
    with open(ruta_archivo, 'wb') as archivo_imagen:
        archivo_imagen.write(base64.b64decode(base64_string))
    print(f'Imagen guardada en {ruta_archivo}')

def generar_numero_aleatorio():
    return random.randint(1000000, 9999999)

def enviar_solicitud(prompt="Andrés male, Activista de Derechos Humanos", aspect_ratio="16:9",
                     controlnet_scale=0.7,
                     steps=30,
                     eta=0.8,
                     guidance_scale=0,
                     use_manual_seed=False,
                     seed_number=0,
                     authorization_token="",
                     negative_prompt=False,  # Cambié el valor por defecto a False
                     negative_prompt_txt=""):
    # Decide el valor de la semilla
    seed = seed_number if use_manual_seed else generar_numero_aleatorio()

    # Decide el valor del negative_prompt
    negative_prompt_value = negative_prompt_txt if negative_prompt else ""

    print(f"Usando seed: {seed}")
    print(f"Usando negative_prompt: {negative_prompt_value}")

    url = "https://www.hedra.com/api/diffusion/v1/models/t2a/predict"
    headers = {
        "Host": "www.hedra.com",
        "Connection": "keep-alive",
        "Enable-Canary": "False",
        "sec-ch-ua-platform": "\"Windows\"",
        "Authorization": f"Bearer {authorization_token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "Content-Type": "application/json",
        "sec-ch-ua-mobile": "?0",
        "Accept": "*/*",
        "Origin": "https://www.hedra.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.hedra.com/app/characters",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate"
    }
    data = {
        "data": {
            "prompt": prompt,
            "negative_prompt": negative_prompt_value,
            "mvp_matrix": "1.3025840520858765,-0.005124199669808149,0.031128384172916412,0.031122159212827682,5.651839231275624e-19,1.29294753074646,0.12536752223968506,0.1253424435853958,0.040881600230932236,0.1632690578699112,-0.9918236136436462,-0.9916252493858337,0.000049583341024117544,-0.000011476542567834258,19.803979873657227,20",
            "aspect_ratio": aspect_ratio,
            "controlnet_scale": controlnet_scale,
            "steps": steps,
            "eta": eta,
            "guidance_scale": guidance_scale,
            "seed": seed,
            "model": "sdxl" #sdxl
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("Request successful.")
        try:
            # Convertir la imagen base64 en un objeto de imagen
            image_base64 = response.text  # Aquí asumimos que la respuesta es una imagen en base64
            image_data = base64.b64decode(image_base64)
            image = Image.open(BytesIO(image_data))

            # Redimensionar la imagen
            new_size = (image.width // 2, image.height // 2)  # Reducir al 50%
            resized_image = image.resize(new_size)

            # Visualizar la imagen redimensionada en Colab
            display.display(resized_image)
            return image_base64, seed

        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return f"Error processing image: {str(e)}", None
    else:
        print(f"Error: {response.status_code}")
        return f"Error: {response.status_code}", None

def ejecutar_todo(aspect_ratio, prompt_txt, negative_prompt_txt, use_manual_seed, seed_number, negative_prompt):
    access_token = os.environ.get("ACCESS_TOKEN_HEDRA")
    
    # Ejecutar la solicitud
    base64_string, seed_used = enviar_solicitud(
        prompt=prompt_txt,
        aspect_ratio=aspect_ratio,
        controlnet_scale=0.8,
        steps=15,
        eta=0.7,
        guidance_scale=5.0,
        use_manual_seed=use_manual_seed,
        seed_number=seed_number,
        authorization_token=access_token,
        negative_prompt=negative_prompt,
        negative_prompt_txt=negative_prompt_txt
    )
    
    # Guardar la imagen
    guardar_imagen_base64(base64_string)