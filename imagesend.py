### Raspberry Pi Code: Sending the Image
# Save this script as "send_image.py" on your Raspberry Pi

import serial
import time

# Configure serial connection to Arduino
arduino = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust port if necessary
time.sleep(2)  # Allow time for Arduino to reset

# Read image as binary
with open("image.jpg", "rb") as image_file:
    image_data = image_file.read()

# Split data into chunks
chunk_size = 200
chunks = [image_data[i:i + chunk_size] for i in range(0, len(image_data), chunk_size)]
total_packets = len(chunks)

# Send chunks with metadata
for i, chunk in enumerate(chunks):
    try:
        # Ensure chunk is bytes
        if not isinstance(chunk, bytes):
            chunk = bytes(chunk)

        # Validate chunk
        if not all(0 <= byte <= 255 for byte in chunk):
            raise ValueError(f"Chunk {i} contains invalid data.")

        # Create the packet
        bspacket = bytes([i, total_packets]) + chunk
        print(f"Sending packet {i + 1}/{total_packets}, Size: {len(bspacket)}")

        # Send packet
        arduino.write(bspacket)
        time.sleep(0.1)  # Small delay to avoid congestion
    except Exception as e:
        print(f"Error in packet {i + 1}: {e}")
        break

print("Image transmission complete.")
