import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CREDENTIALS_PATH = (
    PROJECT_ROOT / "secrets" / "personal-life-admin-683ce-firebase-adminsdk-fbsvc-54f4d18074.json"
)


if not firebase_admin._apps:
    cred = credentials.Certificate(str(CREDENTIALS_PATH))
    firebase_admin.initialize_app(cred)


db = firestore.client()