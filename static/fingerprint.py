import serial       # Importation du module serial pour la communication série
import requests     # Importation du module requests pour les requêtes HTTP

arduino_port = '/dev/ttyACM0'  # Port série de l'Arduino (à adapter selon votre configuration)
baud_rate = 9600               # Vitesse de communication série
url = 'http://localhost:8000/presence/receive/'  # URL de l'API Django pour recevoir les données d'empreintes digitales

ser = serial.Serial(arduino_port, baud_rate)  # Initialisation de la connexion série
print(f"Connected to Arduino on port {arduino_port}")  # Message de confirmation de la connexion

while True:
    line = ser.readline().decode('utf-8').strip()  # Lecture d'une ligne de données depuis le port série
    if "Fingerprint ID" in line:                   # Vérification si la ligne contient un ID d'empreinte digitale
        fingerprint_id = line.split(": ")[1]       # Extraction de l'ID d'empreinte digitale
        data = {'fingerprint_id': fingerprint_id}  # Préparation des données à envoyer
        response = requests.post(url, data=data)   # Envoi des données au serveur Django
        print(f"Sent fingerprint ID {fingerprint_id} to server. Response: {response.status_code}")  # Affichage du statut de la réponse
