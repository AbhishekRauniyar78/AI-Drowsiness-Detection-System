"""
Driver Drowsiness Detection System
Detects eye closure and triggers continuous alert sound
"""

import cv2
import numpy as np
from scipy.spatial import distance as dist
from imutils import face_utils
import os
import sys
import platform
import threading
import time

# Try to import sound libraries
try:
    from playsound import playsound
    HAS_PLAYSOUND = True
except ImportError:
    HAS_PLAYSOUND = False

# Try to import dlib, if not available use cascade classifiers
try:
    import dlib
    USE_DLIB = True
except ImportError:
    USE_DLIB = False
    print("dlib not available, using Haar Cascades instead")


class DrowsinessDetector:
    """Detects driver drowsiness based on eye closure"""
    
    def __init__(self):
        """Initialize the detector with face and eye cascade classifiers"""
        self.EYE_AR_THRESH = 0.2  # Eye Aspect Ratio threshold
        self.EYE_AR_CONSEC_FRAMES = 30  # Consecutive frames below threshold to trigger alert
        
        self.COUNTER = 0  # Counter for consecutive frames with closed eyes
        self.ALARM_ON = False  # Whether alarm is currently playing
        self.stop_alarm = False  # Flag to stop alarm thread
        self.alarm_thread = None  # Thread for continuous alarm
        
        # Initialize face detector
        if USE_DLIB:
            self.detector = dlib.get_frontal_face_detector()
            # Download shape predictor model if not available
            self.predictor_path = "shape_predictor_68_face_landmarks.dat"
            if not os.path.exists(self.predictor_path):
                print("Downloading dlib shape predictor...")
                self._download_predictor()
            self.predictor = dlib.shape_predictor(self.predictor_path)
        else:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            self.eye_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_eye.xml'
            )
        
        # Get alert sound path
        self.alert_sound = self._get_alert_sound()
    
    def _download_predictor(self):
        """Download the dlib shape predictor if not available"""
        try:
            import urllib.request
            import zipfile
            
            url = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
            print(f"Downloading from {url}...")
            # Note: This is a large file, you may want to download manually
            print("Please download manually from http://dlib.net/files/")
        except Exception as e:
            print(f"Error downloading predictor: {e}")
    
    def _get_alert_sound(self):
        """Get path to alert sound file"""
        # Try to find alert.wav in project directory
        if os.path.exists("alert.wav"):
            return "alert.wav"
        # Use system default beep or return None
        return None
    
    def eye_aspect_ratio(self, eye):
        """
        Calculate eye aspect ratio
        Lower values indicate closed eyes
        """
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        C = dist.euclidean(eye[0], eye[3])
        ear = (A + B) / (2.0 * C)
        return ear
    
    def play_alert(self):
        """Play alert sound continuously"""
        try:
            if HAS_PLAYSOUND and self.alert_sound and os.path.exists(self.alert_sound):
                # Play alert continuously until stop_alarm flag is set
                while not self.stop_alarm:
                    try:
                        playsound(self.alert_sound)
                    except:
                        break
            else:
                # System beep fallback - continuous beeping
                if platform.system() == "Windows":
                    import winsound
                    while not self.stop_alarm:
                        winsound.Beep(1000, 300)  # 1000 Hz for 300ms
                        time.sleep(0.2)
                else:
                    # Linux/Mac fallback
                    while not self.stop_alarm:
                        if platform.system() == "Darwin":
                            os.system('afplay /System/Library/Sounds/Alarm.aiff')
                        else:
                            os.system('beep')
                        time.sleep(0.5)
        except Exception as e:
            print(f"Alert error: {e}")
    
    def start_alarm(self):
        """Start continuous alarm in background thread"""
        if not self.ALARM_ON:
            self.ALARM_ON = True
            self.stop_alarm = False
            self.alarm_thread = threading.Thread(target=self.play_alert, daemon=True)
            self.alarm_thread.start()
    
    def stop_alert(self):
        """Stop continuous alarm"""
        if self.ALARM_ON:
            self.ALARM_ON = False
            self.stop_alarm = True
            if self.alarm_thread:
                self.alarm_thread.join(timeout=1)
    
    def detect_with_dlib(self, frame):
        """Detect drowsiness using dlib"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = self.detector(gray, 0)
        
        for rect in rects:
            shape = self.predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            
            # Extract left and right eyes (landmarks 36-41 and 42-47)
            leftEye = shape[36:42]
            rightEye = shape[42:48]
            
            # Calculate eye aspect ratio
            leftEAR = self.eye_aspect_ratio(leftEye)
            rightEAR = self.eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0
            
            # Draw eye contours
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            
            if ear < self.EYE_AR_THRESH:
                self.COUNTER += 1
                if self.COUNTER >= self.EYE_AR_CONSEC_FRAMES:
                    self.start_alarm()  # Start continuous alarm
                    
                    # Draw alert on frame
                    cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.drawContours(frame, [leftEyeHull, rightEyeHull], -1, (0, 0, 255), 2)
            else:
                self.COUNTER = 0
                self.stop_alert()  # Stop alarm when eyes open
                cv2.drawContours(frame, [leftEyeHull, rightEyeHull], -1, (0, 255, 0), 2)
            
            # Display eye aspect ratio
            cv2.putText(frame, f"EAR: {ear:.2f}", (300, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return frame
    
    def detect_with_cascades(self, frame):
        """Detect drowsiness using Haar Cascades"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            
            eyes = self.eye_cascade.detectMultiScale(roi_gray)
            
            eye_count = len(eyes)
            
            # Simple heuristic: if no eyes detected or very small eyes, likely drowsy
            if eye_count < 2:
                self.COUNTER += 1
                if self.COUNTER >= self.EYE_AR_CONSEC_FRAMES:
                    self.start_alarm()  # Start continuous alarm
                    cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                self.COUNTER = 0
                self.stop_alert()  # Stop alarm when eyes detected
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
            
            cv2.putText(frame, f"Eyes Detected: {eye_count}", (300, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return frame
    
    def run(self, camera_index=0):
        """Run the drowsiness detection system"""
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            print("Error: Could not open camera")
            return
        
        print("Drowsiness Detection System Started")
        print("Press 'q' to quit")
        print("-" * 40)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Resize for faster processing
            frame = cv2.resize(frame, (640, 480))
            
            # Detect drowsiness
            if USE_DLIB:
                frame = self.detect_with_dlib(frame)
            else:
                frame = self.detect_with_cascades(frame)
            
            # Display frame
            cv2.imshow("Driver Drowsiness Detection", frame)
            
            # Break on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        self.stop_alert()  # Ensure alarm stops on exit


def main():
    """Main entry point"""
    detector = DrowsinessDetector()
    detector.run()


if __name__ == "__main__":
    main()
