import serial
import time

# Open a serial connection to Arduino
arduino = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust the port if necessary

# Read image as binary data
with open("image.jpg", "rb") as image_file:
    image_data = image_file.read()

# Split image data into smaller packets
chunk_size = 200  # Adjust based on payload size
chunks = [image_data[i:i + chunk_size] for i in range(0, len(image_data), chunk_size)]

# Send chunks with metadata
total_packets = len(chunks)
for i, chunk in enumerate(chunks):
    packet = bytes([i, total_packets]) + chunk
    arduino.write(packet)  # Send packet to Arduino
    print(f"Sent packet {i+1}/{total_packets}")
    time.sleep(0.1)  # Short delay to avoid collisions
