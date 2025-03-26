from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
import cv2
from plyer import gps
from firebase_config import mark_attendance
from geopy.distance import geodesic

# Define the allowed GPS location (school/campus)
ALLOWED_LOCATION = (18.452222, 73.848360)  # Pune - IRA Homes Luxury Boys Hostel

# Function to scan QR Code using OpenCV
def scan_qr_code():
    cap = cv2.VideoCapture(0)  # Open the camera
    detector = cv2.QRCodeDetector()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        data, _, _ = detector.detectAndDecode(frame)  # Scan QR code
        if data:
            cap.release()
            cv2.destroyAllWindows()
            return data  # Return QR data

KV = """
BoxLayout:
    orientation: 'vertical'
    
    Label:
        id: qr_result
        text: "Scan QR Code"
    
    Button:
        text: "Scan"
        on_press: app.scan_qr()
    
    Button:
        text: "Check Location"
        on_press: app.check_location()
"""

class AttendanceApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def scan_qr(self):
        qr_data = scan_qr_code()  # Use OpenCV function to scan
        if qr_data:
            self.root.ids.qr_result.text = f"Scanned: {qr_data}"
            self.student_id = qr_data
        else:
            self.root.ids.qr_result.text = "No QR Code Detected"

    def check_location(self):
        gps.configure(on_location=self.get_gps)
        gps.start()

    def get_gps(self, **kwargs):
        latitude = kwargs["lat"]
        longitude = kwargs["lon"]
        current_location = (latitude, longitude)

        # Verify if within allowed location
        distance = geodesic(current_location, ALLOWED_LOCATION).meters
        if distance <= 500:  # Within 500 meters
            mark_attendance(self.student_id, current_location)
            self.root.ids.qr_result.text = "Attendance Marked!"
        else:
            self.root.ids.qr_result.text = "Wrong Location!"

AttendanceApp().run()
