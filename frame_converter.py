import cv2
import numpy as np
import time

WIDTH, HEIGHT = 128, 64
FPS = 15  # set to 15 FPS for UART limit

def frame_to_oled_buffer(frame):
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    buffer = bytearray()
    for page in range(HEIGHT // 8):
        for x in range(WIDTH):
            byte = 0
            for bit in range(8):
                y = page * 8 + bit
                if bw[y, x] == 0:  # pixel ON (black)
                    byte |= (1 << bit)
            buffer.append(byte)
    return buffer

def main():
    cap = cv2.VideoCapture("bad_apple_25.mp4")
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(original_fps / FPS)  # Skip frames to match 15 FPS

    with open("oled_frames_15fps.bin", "wb") as f:
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Skip frames not matching the interval
            if frame_count % frame_interval != 0:
                frame_count += 1
                continue

            oled_data = frame_to_oled_buffer(frame)
            f.write(oled_data)

            # Optional preview
            cv2.imshow("Preview", cv2.resize(frame, (256, 128)))
            if cv2.waitKey(1) == 27:  # ESC
                break

            frame_count += 1

    cap.release()
    cv2.destroyAllWindows()
    print("Conversion to 15 FPS completed.")

if __name__ == "__main__":
    main()