import firebase_admin
from firebase_admin import credentials, firestore

# Load Firebase credentials
cred = credentials.Certificate("attendence-system-2469d-firebase-adminsdk-fbsvc-d17efde6c5.json")
firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()

# Function to store attendance
def mark_attendance(student_id, location):
    attendance_ref = db.collection("attendance")
    attendance_ref.add({
        "student_id": student_id,
        "location": location,
        "status": "Present"
    })
    print("Attendance Marked!")
