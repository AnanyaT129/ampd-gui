from enum import Enum
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import requests
import firebase_admin
from firebase_admin import credentials, firestore, auth

from firebaseAuthURL import FIREBASE_AUTH_URL

class UploadStatus(Enum):
    WAITING_FOR_DATA = "Waiting for data"
    READY = "Ready to upload"
    AUTH_ERROR = "Error authententicating user"
    UPLOAD_ERROR = "Error uploading data"
    AUTHENTICATING = "Authenticating user"
    UPLOADING = "Uploading data to database"
    COMPLETE = "Upload complete"
    
class UploadThread(QThread):
    
    # Define signals to communicate with the main thread
    change_status_signal = pyqtSignal(UploadStatus)

    def __init__(self, username, password, data, title, action, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.username = username
        self.password = password
        self.data = data
        self.title = title
        self.action = action  # The action to be performed (e.g., 'start_data_collection')
    
    def run(self):
        try:
            if self.action == 'upload':
                if not firebase_admin._apps:
                    cred = credentials.Certificate("firebaseKey.json")
                    firebase_admin.initialize_app(cred)

                db = firestore.client()

                idToken = self.authenticate_user()

                if idToken:
                    try:
                        self.change_status_signal.emit(UploadStatus.UPLOADING)

                        # Decode the ID token to get the UID
                        decoded_token = auth.verify_id_token(idToken)
                        uid = decoded_token['uid']  # User's UID

                        doc_ref = db.collection(uid).document(self.title)

                        doc_ref.set(self.data)

                        self.change_status_signal.emit(UploadStatus.COMPLETE)
                    except Exception as e:
                        self.change_status_signal.emit(UploadStatus.UPLOAD_ERROR)
                else:
                    self.change_status_signal.emit(UploadStatus.AUTH_ERROR)
        except Exception as e:
            self.change_status_signal.emit(UploadStatus.AUTH_ERROR)
            print(e)
    
    def authenticate_user(self):
        self.change_status_signal.emit(UploadStatus.AUTHENTICATING)
        try:
            payload = {
                "email": self.username,
                "password": self.password,
                "returnSecureToken": True
            }

            # Send POST request to Firebase Authentication API
            response = requests.post(FIREBASE_AUTH_URL, data=payload)
            response_data = response.json()

            if "idToken" in response_data:
                # Return the ID token if authentication is successful
                return response_data["idToken"]
            else:
                # Return None if authentication fails
                print(f"Error: {response_data.get('error', {}).get('message')}")
                self.change_status_signal.emit(UploadStatus.AUTH_ERROR)
                return None

        except Exception as e:
            print(f"Error authenticating user: {e}")
            self.change_status_signal.emit(UploadStatus.AUTH_ERROR)
            return None