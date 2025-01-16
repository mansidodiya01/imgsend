import serial
import time

# Configure serial connection to Arduino
SERIAL_PORT = '/dev/ttyUSB0'  # Update based on your setup
BAUD_RATE = 115200

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

while True:
    # Get text input
    text = input("Enter text to send: ")
    if text.lower() == "exit":
        print("Exiting program.")
        break

    # Send text to Arduino
    arduino.write((text + "\n").encode())
    print(f"Sent: {text}")

arduino.close()
print("Connection to Arduino closed.")
