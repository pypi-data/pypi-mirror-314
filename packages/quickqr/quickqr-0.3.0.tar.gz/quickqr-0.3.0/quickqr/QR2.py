import os
import qrcode
from PIL import Image
import re
import asyncio

# Function to generate a basic QR code with customizable settings
def generate_qr_code(data, filename="qr_code.png", color="black", bgcolor="white", border_size=4, box_size=10):
    try:
        qr = qrcode.QRCode(
            version=1, 
            error_correction=qrcode.constants.ERROR_CORRECT_L, 
            box_size=box_size, 
            border=border_size
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill=color, back_color=bgcolor)
        img.save(filename)
        print(f"QR code generated: {filename}")
    except Exception as e:
        print(f"Error generating QR code: {e}")

# Function to add a logo in the center of the QR code
def generate_qr_with_logo(data, logo_path, filename="qr_code_with_logo.png", color="black", bgcolor="white", border_size=4, box_size=10):
    try:
        qr = qrcode.QRCode(
            version=1, 
            error_correction=qrcode.constants.ERROR_CORRECT_L, 
            box_size=box_size, 
            border=border_size
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill=color, back_color=bgcolor)
        
        # Open logo image and resize it
        logo = Image.open(logo_path)
        logo = logo.resize((img.size[0] // 4, img.size[1] // 4))  # Resize logo to fit in center
        logo_position = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)

        img.paste(logo, logo_position, logo)
        img.save(filename)
        print(f"QR code with logo generated: {filename}")
    except Exception as e:
        print(f"Error adding logo: {e}")

# Function to validate URL format
def is_valid_url(url):
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    return re.match(pattern, url) is not None

# Function to generate QR code with validation
def generate_qr_with_validation(data, filename="qr_code.png"):
    try:
        if not is_valid_url(data):
            raise ValueError("Invalid URL or data format.")
        
        generate_qr_code(data, filename)
    except Exception as e:
        print(f"Error: {e}")

# Function to generate QR code with error correction
def generate_qr_with_error_correction(data, error_correction=qrcode.constants.ERROR_CORRECT_L, filename="qr_code.png"):
    try:
        qr = qrcode.QRCode(
            version=1, 
            error_correction=error_correction, 
            box_size=10, 
            border=4
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill="black", back_color="white")
        img.save(filename)
        print(f"QR code with error correction generated: {filename}")
    except Exception as e:
        print(f"Error generating QR with error correction: {e}")

# Function to generate QR codes in batch asynchronously
async def generate_batch_qr_codes_async(data_list, filenames=None):
    if not filenames:
        filenames = [f"qr_code_{i}.png" for i in range(len(data_list))]

    tasks = []
    for data, filename in zip(data_list, filenames):
        tasks.append(asyncio.to_thread(generate_qr_code, data, filename))

    await asyncio.gather(*tasks)
    print(f"Batch QR codes generated: {', '.join(filenames)}")

# Function to generate QR code in SVG format
def generate_qr_as_svg(data, filename="qr_code.svg"):
    try:
        qr = qrcode.QRCode(
            version=1, 
            error_correction=qrcode.constants.ERROR_CORRECT_L, 
            box_size=10, 
            border=4
        )
        qr.add_data(data)
        qr.make(fit=True)

        svg_img = qr.make_image(fill="black", back_color="white").convert("RGB")
        svg_img.save(filename, format="SVG")
        print(f"SVG QR code generated: {filename}")
    except Exception as e:
        print(f"Error generating QR as SVG: {e}")

# Function to generate QR code with customizable borders
def generate_qr_with_custom_border(data, border_size=4, filename="qr_code.png"):
    try:
        qr = qrcode.QRCode(
            version=1, 
            error_correction=qrcode.constants.ERROR_CORRECT_L, 
            box_size=10, 
            border=border_size
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill="black", back_color="white")
        img.save(filename)
        print(f"QR code with custom border generated: {filename}")
    except Exception as e:
        print(f"Error generating QR with custom border: {e}")

# Function to generate QR codes for different data types (URL, email, phone)
def generate_qr_for_type(data, data_type="url", filename="qr_code.png"):
    try:
        if data_type == "url":
            data = f"http://{data}"
        elif data_type == "email":
            data = f"mailto:{data}"
        elif data_type == "phone":
            data = f"tel:{data}"
        
        generate_qr_code(data, filename)
    except Exception as e:
        print(f"Error generating QR for type {data_type}: {e}")
