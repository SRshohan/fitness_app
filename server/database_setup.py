from pyrebase import pyrebase


def database_authentication():
    firebaseConfig = {
  "apiKey": "AIzaSyDX2DH0jiErkd2bk1uiGDNS1muLHdq-8d8",
  "authDomain": "fitness-app-e3aa0.firebaseapp.com",
  "databaseURL": "https://fitness-app-e3aa0-default-rtdb.firebaseio.com",
 "projectId": "fitness-app-e3aa0",
  "storageBucket": "fitness-app-e3aa0.appspot.com",
  "messagingSenderId": "93872114626",
  "appId": "1:93872114626:web:bc89804869eb17440e645b",
  "measurementId": "G-3R15VLJNY2"
}


    # Initialize Firebase
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    db = firebase.database()
    storage = firebase.storage()

    access=[auth, db, storage]

    return access


if __name__ == '__main__':
    print("Working")