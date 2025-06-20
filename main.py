import firebase_admin
from firebase_admin import credentials, messaging
import requests
import time
import os

<<<<<<< HEAD
# Firebase Admin SDK'yı başlat
# Render, google-services.json dosyasını bu yola koyacak
cred = credentials.Certificate(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '/etc/secrets/google-services.json'))
firebase_admin.initialize_app(cred)

# Daha önce gönderilen uyarıların ID'lerini takip etmek için bir set
=======
cred = credentials.Certificate(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '/etc/secrets/google-services.json'))
firebase_admin.initialize_app(cred)

>>>>>>> 4e6cdf5ac75a67bbe5febf1130fff61aeb0ef728
processed_alert_ids = set()

def send_fcm_notification(title, body):
    """Belirtilen konuya (topic) FCM bildirimi gönderir."""
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
<<<<<<< HEAD
        topic='alerts',  # Tüm kullanıcıların abone olacağı konu
=======
        topic='alerts',  
>>>>>>> 4e6cdf5ac75a67bbe5febf1130fff61aeb0ef728
        android=messaging.AndroidConfig(
            priority='high',
            notification=messaging.AndroidNotification(
                sound='default'
            )
        )
    )
    try:
        response = messaging.send(message)
        print(f"Bildirim başarıyla gönderildi: {response}")
    except Exception as e:
        print(f"Bildirim gönderilirken hata oluştu: {e}")

def check_for_alerts():
    """tzevaadom.co.il API'sini kontrol eder ve yeni uyarılar için bildirim gönderir."""
    global processed_alert_ids
    try:
<<<<<<< HEAD
        # API'den güncel verileri al
        response = requests.get("https://www.tzevaadom.co.il/history/last-alerts.json")
        response.raise_for_status()  # HTTP hatalarını kontrol et
=======

        response = requests.get("https://www.tzevaadom.co.il/history/last-alerts.json")
        response.raise_for_status() 
>>>>>>> 4e6cdf5ac75a67bbe5febf1130fff61aeb0ef728
        alerts = response.json()

        if not alerts:
            print("Aktif alarm bulunamadı.")
            return

<<<<<<< HEAD
        # Sadece yeni ve daha önce işlenmemiş uyarıları işle
=======
>>>>>>> 4e6cdf5ac75a67bbe5febf1130fff61aeb0ef728
        new_alerts = [alert for alert in alerts if alert['id'] not in processed_alert_ids]

        if not new_alerts:
            print("Yeni alarm bulunamadı.")
            return

        for alert in new_alerts:
            alert_id = alert['id']
            city = alert['data']
            title = "🚨 Roket Alarmı 🚨"
            body = f"Şu şehirde alarm verildi: {city}"
            
            print(f"Yeni alarm tespit edildi: {body}")
            send_fcm_notification(title, body)
<<<<<<< HEAD
            
            # Bu uyarıyı işlendi olarak işaretle
=======

>>>>>>> 4e6cdf5ac75a67bbe5febf1130fff61aeb0ef728
            processed_alert_ids.add(alert_id)

    except requests.exceptions.RequestException as e:
        print(f"API'ye erişilirken bir hata oluştu: {e}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    print("Roket Alarmı Takip Sistemi Başlatıldı...")
    while True:
        check_for_alerts()
<<<<<<< HEAD
        # Her 3 saniyede bir kontrol et
        time.sleep(3) 
=======

        time.sleep(3)
>>>>>>> 4e6cdf5ac75a67bbe5febf1130fff61aeb0ef728
