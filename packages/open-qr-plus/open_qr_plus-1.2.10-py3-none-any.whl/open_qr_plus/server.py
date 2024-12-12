from flask import Flask, render_template, request, jsonify, send_file
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import SquareModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
import io
from flask_wtf.csrf import CSRFProtect
import base64
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import argparse
import pyfiglet
from colorama import init, Fore, Style
from pyzbar.pyzbar import decode
import platform
import subprocess

# Initialize colorama
init(autoreset=True)

app = Flask(__name__)

def install_zbar():
    system = platform.system()  # Detect the OS type
    try:
        if system == "Linux":
            print("Detected Linux. Installing libzbar...")
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "libzbar0"], check=True)
        elif system == "Darwin":
            print("Detected macOS. Installing zbar via Homebrew...")
            subprocess.run(["brew", "update"], check=True)
            subprocess.run(["brew", "install", "zbar"], check=True)
        elif system == "Windows":
            print("Detected Windows. Please ensure zbar is installed manually.")
            print("Download from: https://zbar.sourceforge.net/")
        else:
            print(f"Unsupported operating system: {system}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while installing zbar: {e}")
    else:
        print("zbar installation completed successfully.")


def generate_unique_key(length=400):
    # Create a random salt
    salt = os.urandom(16)
    
    # Define the key derivation function
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=length,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    
    # Derive a key
    key = base64.urlsafe_b64encode(kdf.derive(os.urandom(32)))
    
    # Ensure the key length is exactly 400 characters
    while len(key) < length:
        key += base64.urlsafe_b64encode(kdf.derive(os.urandom(32)))
    return key[:length].decode('utf-8')

app.config['SECRET_KEY'] = generate_unique_key()
csrf = CSRFProtect(app)

# Configuration for file uploads
UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
QR_FOLDER = os.path.join(UPLOAD_FOLDER, "qrcodes")
os.makedirs(QR_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Handle resampling filter compatibility
try:
    resample_filter = Image.Resampling.LANCZOS
except AttributeError:
    resample_filter = Image.LANCZOS

def clear_qr_directory():
    for filename in os.listdir(QR_FOLDER):
        file_path = os.path.join(QR_FOLDER, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    embed_type = request.form.get('embed_type')
    data = request.form.get('data')
    file = request.files.get('file')
    custom_image = None
    qr_id = os.urandom(8).hex()  # Generate a unique ID for each QR

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        custom_image = Image.open(filepath)
        custom_image = optimize_image(custom_image)
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"Failed to delete {filepath}. Reason: {e}")

    elif file and not allowed_file(file.filename):
        return jsonify({'error': "Invalid file type. Please upload an image file."})

    if data:
        qr_img, opacity = generate_stylish_qr(data, custom_image)
        if qr_img:
            qr_path = os.path.join(QR_FOLDER, f"{qr_id}.png")
            qr_img.save(qr_path, 'PNG')
            # Check if QR code can be decoded correctly
            if not verify_qr_code(qr_path, data):
                # Adjust opacity until QR code is readable or max attempts reached
                for attempt in range(10):  # Max 10 attempts
                    opacity -= 10 if opacity > 10 else 0
                    new_qr_img, _ = generate_stylish_qr(data, custom_image, opacity)
                    new_qr_path = os.path.join(QR_FOLDER, f"{qr_id}_temp.png")
                    new_qr_img.save(new_qr_path, 'PNG')
                    if verify_qr_code(new_qr_path, data):
                        os.rename(new_qr_path, qr_path)
                        break
                    else:
                        os.remove(new_qr_path)
                else:
                    return jsonify({'error': "Failed to generate a scannable QR code."})
            
            with open(qr_path, "rb") as image_file:
                qr_code_data = base64.b64encode(image_file.read()).decode('ascii')
            return jsonify({'qr_code_data': qr_code_data, 'qr_id': qr_id})
        else:
            return jsonify({'error': "Failed to generate QR code."})
    else:
        return jsonify({'error': "Please enter the data to embed in the QR code."})
@app.route('/scan_qr', methods=['POST'])
def scan_qr():
    data = request.json.get('data')
    if data:
        try:
            # Convert base64 to image
            img_data = base64.b64decode(data.split(',')[1])
            img = Image.open(io.BytesIO(img_data))
            barcodes = decode(img)
            if barcodes:
                return jsonify({'decoded': barcodes[0].data.decode('utf-8')})
            else:
                return jsonify({'error': 'No QR code found in the image.'})
        except Exception as e:
            return jsonify({'error': f'Error scanning QR code: {str(e)}'})
    return jsonify({'error': 'No data provided to scan.'})
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def optimize_image(image):
    max_size = (150, 150)
    image.thumbnail(max_size, resample=resample_filter)
    return image

def generate_stylish_qr(data, custom_image=None, opacity=200):
    try:
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )

        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=SquareModuleDrawer(),
            color_mask=SolidFillColorMask(back_color=(255, 255, 255), front_color=(54, 162, 235))
        ).convert('RGBA')

        frame_path = 'frame.png'
        if os.path.exists(frame_path):
            frame = Image.open(frame_path).convert('RGBA')
            frame = frame.resize(img.size)
            img = Image.alpha_composite(frame, img)

        if custom_image:
            img_w, img_h = img.size
            custom_image = custom_image.convert('RGBA')
            factor = 3.5
            size_w, size_h = int(img_w / factor), int(img_h / factor)
            custom_image = custom_image.resize((size_w, size_h), resample=resample_filter)
            custom_image = make_round_image(custom_image)
            pos = ((img_w - size_w) // 2, (img_h - size_h) // 2)
            custom_image.putalpha(opacity)
            img.paste(custom_image, pos, mask=custom_image)
        
        return img, opacity
    except Exception as e:
        print(f"Error generating QR code: {e}")
        return None, None

def make_round_image(image):
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + image.size, fill=255)
    image.putalpha(mask)
    return image


def verify_qr_code(path, expected_data):
    try:
        with Image.open(path) as img:
            barcodes = decode(img)
            if barcodes:
                # Decode the first barcode found
                decoded_data = barcodes[0].data.decode('utf-8')
                return decoded_data == expected_data
    except Exception as e:
        print(f"Error reading QR code: {e}")
    return False

@app.route('/download_qr/<qr_id>')
def download_qr(qr_id):
    qr_path = os.path.join(QR_FOLDER, f"{qr_id}.png")
    if os.path.exists(qr_path):
        return send_file(qr_path, as_attachment=True)
    return "QR Code not found", 404

def custom_figlet_text(text, font="slant", color=Fore.CYAN):
    ascii_art = pyfiglet.figlet_format(text, font=font)
    colored_art = f"{color}{ascii_art}{Style.RESET_ALL}"
    return colored_art

def start():
    parser = argparse.ArgumentParser(description="Open QR Code Generator")
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to run the server on')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
    args = parser.parse_args()
    install_zbar()

    if not isinstance(args.host, str):
        raise ValueError("Host must be a string.")
    if not isinstance(args.port, int):
        raise ValueError("Port must be an integer.")
    print(custom_figlet_text(text="Open QR Plus"))
    print("version 1.2.10")

    # Clear all QR codes when the server starts
    clear_qr_directory()

    app.run(host=args.host, port=args.port)

