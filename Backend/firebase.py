"""
Firebase Service Module
Handles all Firebase-related operations for the Personal Finance Manager
"""

import os
import firebase_admin
from firebase_admin import credentials, firestore, auth
from google.cloud.firestore import Client as FirestoreClient

# Define Firebase credentials path (Change this to match your actual JSON file location)
CREDENTIALS_PATH = "C:\\Users\\mkmad\\.cursor\\PFM\\Backend\\firebase.json"

# Define a custom exception for Firebase-related errors
class FirebaseError(Exception):
    """Custom exception for Firebase-related errors."""
    pass

# Firebase app and Firestore client (Singleton pattern)
_firebase_app = None
_db = None

def initialize_firebase() -> FirestoreClient:
    """
    Initialize Firebase Admin SDK using the service account JSON file.
    Returns the Firestore database client.
    
    Raises:
        FirebaseError: If initialization fails
    """
    global _firebase_app, _db

    if _firebase_app is None:
        try:
            # Check if credentials file exists
            if not os.path.exists(CREDENTIALS_PATH):
                raise FirebaseError(f"Firebase credentials file not found: {CREDENTIALS_PATH}")

            # Load credentials and initialize Firebase
            cred = credentials.Certificate(CREDENTIALS_PATH)
            _firebase_app = firebase_admin.initialize_app(cred)
            _db = firestore.client()

            print("🔥 Firebase initialized successfully!")

        except Exception as e:
            raise FirebaseError(f"Firebase initialization failed: {str(e)}")

    return _db


def get_firestore_client() -> FirestoreClient:
    """
    Get the Firestore client instance.
    Initializes Firebase if not already initialized.
    
    Returns:
        FirestoreClient: The Firestore database client
    
    Raises:
        FirebaseError: If Firebase is not initialized
    """
    if _db is None:
        return initialize_firebase()
    return _db


# Example debug print to check if script runs without errors
if __name__ == "__main__":
    try:
        db = initialize_firebase()
        print("✅ Firestore client is ready!")
    except FirebaseError as e:
        print(f"❌ Error initializing Firebase: {e}")