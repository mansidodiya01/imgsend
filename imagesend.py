### Raspberry Pi Code: Sending the Image
import serial
import time
from PIL import Image

# Configure serial connection to Arduino
SERIAL_PORT = '/dev/cu.usbserial-130'
BAUD_RATE = 115200  # Increased baud rate
CHUNK_SIZE = 16000  # Increased chunk size significantly

def connect_to_arduino(port, baud_rate):
    """Establishes a serial connection to the Arduino."""
    try:
        arduino = serial.Serial(port, baud_rate)
        time.sleep(2)  # Allow time for Arduino to reset
        print(f"Connected to Arduino on {port} at {baud_rate} baud.")
        return arduino
    except serial.SerialException as e:
        print(f"Error: Unable to connect to Arduino on {port}: {e}")
        return None

# Establish connection
arduino = connect_to_arduino(SERIAL_PORT, BAUD_RATE)
if not arduino:
    exit("Exiting: Could not establish connection to Arduino.")

def compress_image(input_path, output_path, quality=15):
    """Compress the image to reduce its size."""
    try:
        with Image.open(input_path) as img:
            img.save(output_path, "JPEG", quality=quality)
        print(f"Image compressed and saved to {output_path}.")
    except Exception as e:
        exit(f"Error: Unable to compress the image - {e}")

# Compress the image
input_image_path = "img1.jpg"
compressed_image_path = "compressed_img1.jpg"
compress_image(input_image_path, compressed_image_path)

def read_image(file_path):
    """Reads the image file as binary data."""
    try:
        with open(file_path, "rb") as image_file:
            return image_file.read()
    except FileNotFoundError:
        exit(f"Error: File not found - {file_path}")
    except Exception as e:
        exit(f"Error: Unable to read the image file - {e}")

image_data = read_image(compressed_image_path)

chunks = [image_data[i:i + CHUNK_SIZE] for i in range(0, len(image_data), CHUNK_SIZE)]
total_packets = len(chunks)
print(f"Total packets: {total_packets}")

successful_transmission = True
for i, chunk in enumerate(chunks):
    try:
        if not isinstance(chunk, bytes):
            chunk = bytes(chunk)

        bspacket = bytes([i % 256, total_packets % 256]) + chunk

        # Send packet without delay for faster transmission
        arduino.write(bspacket)
    except Exception as e:
        print(f"Error in packet {i + 1}: {e}")
        successful_transmission = False
        break

if successful_transmission:
    print("Image transmission complete.")
else:
    print("Image transmission failed.")

arduino.close()
print("Connection to Arduino closed.")
