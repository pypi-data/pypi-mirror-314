from flask import Flask, render_template, request, jsonify
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
import os
import base64
import argparse
import pyfiglet
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)


app = Flask(__name__)

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
csrf = CSRFProtect(app)  # Correctly initialize CSRFProtect

# Configuration for file uploads
UPLOAD_FOLDER = os.path.join(app.root_path , "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Handle resampling filter compatibility
try:
    # For Pillow >=9.1.0
    resample_filter = Image.Resampling.LANCZOS
except AttributeError:
    # For older versions of Pillow
    resample_filter = Image.LANCZOS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    embed_type = request.form.get('embed_type')
    data = request.form.get('data')
    file = request.files.get('file')
    custom_image = None

    # Handle custom image upload
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        custom_image = Image.open(filepath)
        # Optimize custom image
        custom_image = optimize_image(custom_image)
        # Check if the file exists before trying to delete it
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"The file {filepath} has been deleted.")
        else:
            print(f"The file {filepath} does not exist.")

    elif file and not allowed_file(file.filename):
        return jsonify({'error': "Invalid file type. Please upload an image file."})

    if data:
        qr_img = generate_stylish_qr(data, custom_image)
        if qr_img:
            img_io = io.BytesIO()
            qr_img.save(img_io, 'PNG')
            img_io.seek(0)
            qr_code_data = base64.b64encode(img_io.getvalue()).decode('ascii')
            return jsonify({'qr_code_data': qr_code_data})
        else:
            return jsonify({'error': "Failed to generate QR code. Please try again with different data. Make sure the data is within qr range."})
    else:
        return jsonify({'error': "Please enter the data to embed in the QR code."})

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def optimize_image(image):
    # Resize the image to a maximum dimension
    max_size = (150, 150)
    image.thumbnail(max_size, resample=resample_filter)
    return image

def generate_stylish_qr(data, custom_image=None):
    try:
        # Create QR code instance with optimized settings
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=2,
        )

        qr.add_data(data)
        qr.make(fit=True)

        # Create an image from the QR Code instance with enhanced graphics
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=SquareModuleDrawer(),
            color_mask=SolidFillColorMask(back_color=(255, 255, 255), front_color=(54, 162, 235))
        ).convert('RGBA')

        # Add frame to the QR code if frame image exists
        frame_path = 'frame.png'
        if os.path.exists(frame_path):
            frame = Image.open(frame_path).convert('RGBA')
            frame = frame.resize(img.size)
            img = Image.alpha_composite(frame, img)

        if custom_image:
            # Calculate position for the custom image
            img_w, img_h = img.size
            custom_image = custom_image.convert('RGBA')
            # Resize custom image to fit in the center of the QR code
            factor = 3.5
            size_w = int(img_w / factor)
            size_h = int(img_h / factor)
            custom_image = custom_image.resize((size_w, size_h), resample=resample_filter)
            # Create a circular mask for the custom image
            custom_image = make_round_image(custom_image)
            pos = ((img_w - size_w) // 2, (img_h - size_h) // 2)

            # Paste the custom image onto the QR code with adjusted opacity
            custom_image.putalpha(200)
            img.paste(custom_image, pos, mask=custom_image)
        
        return img
    except Exception as e:
        print(f"Error generating QR code: {e}")
        return None

def make_round_image(image):
    # Create a circular mask for the image
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + image.size, fill=255)
    image.putalpha(mask)
    return image

def custom_figlet_text(text, font="slant", color=Fore.CYAN):
    ascii_art = pyfiglet.figlet_format(text, font=font)
    colored_art = f"{color}{ascii_art}{Style.RESET_ALL}"
    return colored_art


def start():
    parser = argparse.ArgumentParser(description="Open QR Code Generator")
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to run the server on')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
    args = parser.parse_args()

    if not isinstance(args.host, str):
        raise ValueError("Host must be a string.")
    if not isinstance(args.port, int):
        raise ValueError("Port must be an integer.")
    print(custom_figlet_text(text="Open QR Plus"))
    print("version 1.0.0")



    app.run(host=args.host, port=args.port)


