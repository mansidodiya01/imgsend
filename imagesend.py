import serial
import time

# Configure serial connection to Arduino
arduino = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust if needed
time.sleep(2)  # Allow time for Arduino to reset

# Read image as binary
with open("image.jpg", "rb") as image_file:
    image_data = image_file.read()

# Split image data into 200-byte chunks
chunk_size = 200
chunks = [image_data[i:i + chunk_size] for i in range(0, len(image_data), chunk_size)]
total_packets = len(chunks)

# Send chunks
for i, chunk in enumerate(chunks):
    # Convert to bytes if necessary
    if not isinstance(chunk, bytes):
        chunk = bytes(chunk)
    
    # Validate the chunk
    if not all(0 <= byte <= 255 for byte in chunk):
        raise ValueError(f"Chunk contains invalid values: {chunk}")
    
    # Add metadata and send packet
    bspacket = bytes([i, total_packets]) + chunk
    print(f"Sending packet {i+1}/{total_packets}, size: {len(bspacket)}")
    arduino.write(bspacket)
    time.sleep(0.1)

print("Image transmission complete.")
