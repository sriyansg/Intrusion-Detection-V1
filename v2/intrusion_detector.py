import cv2
import time
import winsound
import threading
import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime

# Track the last time an alert was shown to avoid spamming
last_alert_time = 0
# State variable to know if an alert is currently on-screen
alert_active = False

def show_alert():
    global alert_active
    alert_active = True
    
    # 1. Beep using winsound (frequency: 1000Hz, duration: 1000ms)
    winsound.Beep(1000, 1000)
    
    # 2. Show a Windows Popup using tkinter
    root = tk.Tk()
    root.withdraw() # Hide the main tk window
    root.attributes("-topmost", True) # Force the popup to stay on top
    
    messagebox.showwarning("INTRUSION DETECTED", "Movement detected at the door!")
    
    root.destroy()
    alert_active = False

def main():
    global last_alert_time, alert_active
    last_snapshot_time = 0
    
    # --- Create a folder to store the intrusion screenshots ---
    save_folder = "Intrusions_Detected"
    os.makedirs(save_folder, exist_ok=True)
    
    print("=== Simple Intrusion Detection System ===")
    print("To use your iPhone's camera:")
    print("  1. Connect your iPhone and laptop to the same Wi-Fi.")
    print("  2. Install a free app like 'IP Camera Lite' or 'DroidCam' from the App Store.")
    print("  3. Start the server on the app, and it will display an IP address on your screen.")
    print("  4. Enter the URL below (e.g., http://192.168.1.15:8080/video or http://192.168.1.15:4747/video).")
    print("\nOr, press Enter without typing anything to test with your laptop's built-in webcam.")
    
    url = input("\nEnter camera URL (or press Enter for default webcam): ").strip()
    
    if url == "":
        print("\nOpening default laptop webcam...")
        cap = cv2.VideoCapture(0)
    else:
        # Automatically add http:// if the user forgets it
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
            
        print(f"\nAttempting to connect to video stream at: {url}...")
        cap = cv2.VideoCapture(url)
        
    if not cap.isOpened():
        print("\nError: Could not open video stream. Please check the URL or ensure the camera is not used by another app.")
        return

    # Read the first two frames to establish the baseline for motion detection
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    
    if not ret:
        print("\nError: Failed to grab frames from the camera.")
        return

    print("\nMonitoring started! Point the camera at your door.")
    print("=> Press 'q' in the video window to quit.")
    print(f"=> Intrusion photos will be saved inside the '{save_folder}' folder.")

    while cap.isOpened():
        # Calculate the absolute difference between the current frame and previous frame
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        movement_detected = False
        
        for contour in contours:
            if cv2.contourArea(contour) < 5000:
                continue
                
            movement_detected = True
            
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame1, "Status: MOVEMENT", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        if movement_detected:
            current_time = time.time()
            
            # 1. Take a screenshot at most once every 1 second (so we don't miss quick sequential passes)
            if current_time - last_snapshot_time > 1:
                exact_time_str = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
                file_safe_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                
                cv2.putText(frame1, f"Intrusion Time: {exact_time_str}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                
                image_path = os.path.join(save_folder, f"Intrusion_{file_safe_time}.jpg")
                cv2.imwrite(image_path, frame1)
                print(f"\n[ALERT] Snapshot saved: {image_path}")
                last_snapshot_time = current_time

            # 2. But only trigger the annoying Beep and Popup at most once every 5 seconds
            if current_time - last_alert_time > 5:
                if not alert_active:
                    threading.Thread(target=show_alert, daemon=True).start()
                else:
                    threading.Thread(target=winsound.Beep, args=(1000, 1000), daemon=True).start()
                    
                last_alert_time = current_time

        # Show the video feed
        cv2.imshow("Intrusion Detection Feed", frame1)
        
        frame1 = frame2
        ret, frame2 = cap.read()
        
        if not ret:
            print("\nStream ended unexpectedly.")
            break

        if cv2.waitKey(10) == ord('q'):
            print("\nExiting based on user request.")
            break
            
    cap.release()
    cv2.destroyAllWindows()
    print("Program terminated successfully.")

if __name__ == "__main__":
    main()
