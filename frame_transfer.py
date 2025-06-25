import serial
import time

# Serial port configuration
SERIAL_PORT = "COM4"  # Replace with your ESP32's port
BAUD_RATE = 115200    # Match the baud rate of your ESP32

# Frame dimensions
WIDTH, HEIGHT = 128, 64
BYTES_PER_FRAME = WIDTH * (HEIGHT // 8)  # Each frame is WIDTH * HEIGHT/8 bytes

def stream_video_to_esp32(bin_file_path):
    try:
        # Open the serial connection
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")

            # Open the binary file
            with open(bin_file_path, "rb") as bin_file:
                frame_count = 0
                while True:
                    # Read one frame (BYTES_PER_FRAME bytes)
                    frame_data = bin_file.read(BYTES_PER_FRAME)
                    if not frame_data:
                        break  # End of file

                    # Send the frame to ESP32
                    ser.write(frame_data)
                    print(f"Sent frame {frame_count} ({len(frame_data)} bytes).")

                    # Optional: Wait for ESP32 acknowledgment
                    time.sleep(1 / 15)  # Match the target FPS (15 FPS)

                    frame_count += 1

            print("Video streaming completed.")

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except FileNotFoundError:
        print(f"File not found: {bin_file_path}")

if __name__ == "__main__":
    stream_video_to_esp32("oled_frames_15fps.bin")