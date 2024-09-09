import mysql.connector
from datetime import datetime, timedelta

# MySQLLocal bağlantısını kullanarak veritabanına bağlan
db = mysql.connector.connect(
    host="localhost",  # Eğer farklı bir host kullanıyorsan burayı değiştir
    user="root",       # MySQL kullanıcı adını yaz
    password="Harunisik00.",  # MySQL şifreni yaz
    database="library_system"  # Veritabanı adın "library_system" olmalı
)

cursor = db.cursor()

# Proje kodları buradan devam edecek
# Kitap ekleme fonksiyonu
def kitap_ekle(isim, yazar, yil, kategori):
    sql = "INSERT INTO kitaplar (isim, yazar, yil, kategori) VALUES (%s, %s, %s, %s)"
    val = (isim, yazar, yil, kategori)
    cursor.execute(sql, val)
    db.commit()
    print(f"Kitap '{isim}' başarıyla eklendi.")

# Üye ekleme fonksiyonu
def uye_ekle(isim, email, telefon):
    sql = "INSERT INTO uyeler (isim, email, telefon) VALUES (%s, %s, %s)"
    val = (isim, email, telefon)
    cursor.execute(sql, val)
    db.commit()
    print(f"Üye '{isim}' başarıyla eklendi.")

# Kitap ödünç alma fonksiyonu
def kitap_odunc_al(uye_id, kitap_id):
    odunc_tarihi = datetime.now().date()
    iade_tarihi = odunc_tarihi + timedelta(days=14)  # 14 gün iade süresi
    sql = "INSERT INTO odunc_islemleri (uye_id, kitap_id, odunc_tarihi, iade_tarihi) VALUES (%s, %s, %s, %s)"
    val = (uye_id, kitap_id, odunc_tarihi, iade_tarihi)
    cursor.execute(sql, val)
    db.commit()
    print(f"Kitap ödünç alındı. İade tarihi: {iade_tarihi}")

# Gecikme kontrolü ve ceza uygulama fonksiyonu
def gecikme_kontrolu():
    sql = "SELECT odunc_id, uye_id, kitap_id, iade_tarihi FROM odunc_islemleri WHERE iade_tarihi < CURDATE() AND ceza = 0"
    cursor.execute(sql)
    gecikenler = cursor.fetchall()

    if len(gecikenler) == 0:
        print("Geciken kitap yok.")
    else:
        for odunc in gecikenler:
            odunc_id, uye_id, kitap_id, iade_tarihi = odunc
            gecikme_gun = (datetime.now().date() - iade_tarihi).days
            ceza = gecikme_gun * 25  # Gecikilen her gün için 25 TL ceza
            sql = "UPDATE odunc_islemleri SET ceza = %s WHERE odunc_id = %s"
            cursor.execute(sql, (ceza, odunc_id))
            db.commit()
            print(f"Üye {uye_id} için {gecikme_gun} gün gecikme tespit edildi. Uygulanan ceza: {ceza} TL.")

# Kullanıcı arayüzü
def main():
    while True:
        print("\n1. Kitap Ekle")
        print("2. Üye Ekle")
        print("3. Kitap Ödünç Al")
        print("4. Gecikmeleri Kontrol Et ve Ceza Uygula")
        print("5. Çıkış")
        secim = input("Seçim yapın: ")

        if secim == '1':
            isim = input("Kitap ismi: ")
            yazar = input("Yazar: ")
            yil = int(input("Yıl: "))
            kategori = input("Kategori: ")
            kitap_ekle(isim, yazar, yil, kategori)

        elif secim == '2':
            isim = input("Üye ismi: ")
            email = input("Email: ")
            telefon = input("Telefon: ")
            uye_ekle(isim, email, telefon)

        elif secim == '3':
            uye_id = int(input("Üye ID: "))
            kitap_id = int(input("Kitap ID: "))
            kitap_odunc_al(uye_id, kitap_id)

        elif secim == '4':
            gecikme_kontrolu()

        elif secim == '5':
            print("Çıkış yapılıyor...")
            break

        else:
            print("Geçersiz seçim!")

if __name__ == "__main__":
    main()
