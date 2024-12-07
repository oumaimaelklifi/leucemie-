import requests
from PIL import Image, ImageTk
from io import BytesIO


def set_window_icon(root):
    url = "https://flagcdn.com/40x30/ma.png"
    try:
        response = requests.get(url)
        image_data = response.content
        image = Image.open(BytesIO(image_data))
        image = image.resize((32, 32))
        icon_image = ImageTk.PhotoImage(image)
        root.iconphoto(True, icon_image)
    except Exception as e:
        print(f"Erreur de téléchargement de l'image: {e}")

