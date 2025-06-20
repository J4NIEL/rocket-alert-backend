import firebase_admin
from firebase_admin import credentials, messaging
import requests
import time
import os
import json

# Firebase Admin SDK'yı başlat
# Render, google-services.json dosyasını bu yola koyacak
cred = credentials.Certificate(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '/etc/secrets/google-services.json'))
firebase_admin.initialize_app(cred)

# Daha önce gönderilen uyarıların ID'lerini takip etmek için bir set
processed_alert_ids = set()
# Son kontrol edilen alert ID'sini takip et
last_checked_id = 5458  # Başlangıç ID'si

def send_fcm_notification(title, body):
    """Belirtilen konuya (topic) FCM bildirimi gönderir."""
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        topic='alerts',  # Tüm kullanıcıların abone olacağı konu
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

def check_alert_by_id(alert_id):
    """Belirli bir alert ID'sini kontrol eder."""
    try:
        url = f"https://www.tzevaadom.co.il/en/alerts/{alert_id}"
        print(f"Alert ID {alert_id} kontrol ediliyor: {url}")
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            # Sayfa içeriğini kontrol et
            content = response.text
            
            # Eğer sayfa "Alert -" içeriyorsa ve boş değilse, bu bir aktif alert'tir
            if "Alert -" in content and len(content.strip()) > 100:
                print(f"Aktif alert bulundu: ID {alert_id}")
                return True, content
            else:
                print(f"Alert ID {alert_id} aktif değil veya bulunamadı")
                return False, None
        else:
            print(f"Alert ID {alert_id} için HTTP hatası: {response.status_code}")
            return False, None
            
    except requests.exceptions.RequestException as e:
        print(f"Alert ID {alert_id} kontrol edilirken hata: {e}")
        return False, None
    except Exception as e:
        print(f"Beklenmeyen hata (Alert ID {alert_id}): {e}")
        return False, None

def extract_alert_info(content):
    """Alert sayfasından bilgileri çıkarır."""
    try:
        # Basit bir şekilde sayfa başlığından şehir adını çıkarmaya çalış
        if "Tzofar" in content:
            return "Tzofar"
        elif "Sderot" in content:
            return "Sderot"
        elif "Ashkelon" in content:
            return "Ashkelon"
        elif "Tel Aviv" in content:
            return "Tel Aviv"
        elif "Jerusalem" in content:
            return "Jerusalem"
        else:
            return "İsrail'de bir bölge"
    except:
        return "Bilinmeyen bölge"

def check_for_alerts():
    """Yeni alert'leri kontrol eder."""
    global processed_alert_ids, last_checked_id
    
    # Son 10 ID'yi kontrol et (yeni alert'ler için)
    for i in range(5):
        current_id = last_checked_id + i + 1
        
        # Eğer bu ID zaten işlendiyse atla
        if current_id in processed_alert_ids:
            continue
            
        is_active, content = check_alert_by_id(current_id)
        
        if is_active:
            city = extract_alert_info(content)
            title = "🚨 Roket Alarmı 🚨"
            body = f"Şu bölgede alarm verildi: {city} (ID: {current_id})"
            
            print(f"Yeni alarm tespit edildi: {body}")
            send_fcm_notification(title, body)
            
            # Bu alert'i işlendi olarak işaretle
            processed_alert_ids.add(current_id)
            
            # Son kontrol edilen ID'yi güncelle
            last_checked_id = current_id
        else:
            # Eğer bu ID aktif değilse, sonraki ID'leri kontrol etmeye devam et
            pass
    
    # Son kontrol edilen ID'yi güncelle
    last_checked_id += 1
    
    print(f"Son kontrol edilen ID: {last_checked_id}")
    print("Aktif alarm bulunamadı.")

if __name__ == "__main__":
    print("Roket Alarmı Takip Sistemi Başlatıldı...")
    print("tzevaadom.co.il sitesinden alert'ler kontrol ediliyor...")
    
    while True:
        check_for_alerts()
        # Her 60 saniyede bir kontrol et (site yükünü azaltmak için)
        time.sleep(60) 
