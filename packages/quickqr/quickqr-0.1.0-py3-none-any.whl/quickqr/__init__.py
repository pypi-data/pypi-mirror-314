import qrcode
from PIL import Image
import os

def generate_qr_code(data: str, filename: str = None, size: int = 10, image_input: bool = False) -> Image:
    """
    Generate a QR Code from the provided data (URL, text, or image path).

    Args:
        data (str): The data to encode in the QR code (URL or text).
        filename (str, optional): If provided, saves the generated QR code to this file. Defaults to None.
        size (int, optional): Size of the QR code. Defaults to 10.
        image_input (bool, optional): If True, treats the input as an image path to encode. Defaults to False.

    Returns:
        Image: The generated QR code as an image object.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=4,
    )
    
    if image_input:
        # If the input is an image path, load it into QR
        if os.path.exists(data):
            with open(data, 'rb') as img_file:
                qr.add_data(img_file.read())
        else:
            raise FileNotFoundError(f"Image not found at path: {data}")
    else:
        # Otherwise, treat the data as URL/text
        qr.add_data(data)

    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    if filename:
        img.save(filename)

    return img

def save_qr_code(data: str, filename: str, size: int = 10, image_input: bool = False) -> None:
    """
    Generate and save a QR Code to a file.

    Args:
        data (str): The data to encode in the QR code (URL or text).
        filename (str): The path to save the QR code image.
        size (int, optional): Size of the QR code. Defaults to 10.
        image_input (bool, optional): If True, treats the input as an image path to encode. Defaults to False.
    """
    generate_qr_code(data, filename, size, image_input)
